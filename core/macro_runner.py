import threading
import time
import os
import sys
from pynput import keyboard

class MacroRunner:
    def __init__(self, serial_manager):
        self.serial = serial_manager
        self.steps = []
        
        # State Control
        self.is_running = False
        self.is_paused = False
        self.loop_count = 1
        self.is_infinite = False
        
        # Thread & Hotkeys
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.listener = None

        # Tambahkan ini: Callback untuk mengambil data dari UI
        self.sync_callback = None

    def get_base_path(self):
        """Path aman agar file JSON tidak hilang saat diconvert ke .EXE"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.dirname(sys.executable)
        return os.path.abspath(".")

    def load_settings(self, steps, loop_count, is_infinite):
        self.steps = steps
        self.loop_count = loop_count
        self.is_infinite = is_infinite

    def play(self):
        if len(self.steps) == 0:
            print("Tabel kosong, tidak ada yang dijalankan.")
            return

        if self.is_paused:
            self.is_paused = False
            self.pause_event.set()
            print("Macro Dilanjutkan (Resumed)")
        elif not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.pause_event.set()
            threading.Thread(target=self._execution_loop, daemon=True).start()
            print("Macro Dimulai (Started)")

    def pause(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_event.clear()
            print("Macro Dijeda (Paused)")

    def stop(self):
        self.is_running = False
        self.is_paused = False
        self.pause_event.set()
        print("Macro Dihentikan (Stopped)")

    def _execution_loop(self):
        current_loop = 0
        
        while self.is_infinite or current_loop < self.loop_count:
            if not self.is_running:
                break
                
            print(f"\n--- Memulai Loop ke-{current_loop + 1} ---")
            
            for step in self.steps:
                if not self.is_running:
                    break
                
                self.pause_event.wait()
                
                action = step.get('action', '')
                key = str(step.get('key', ''))
                delay_val = float(step.get('delay', 0))

                arduino_command = ""
                python_sleep = delay_val

                # --- PENERJEMAH KE BAHASA ARDUINO ---
                if action == "Keyboard":
                    arduino_command = f"K:{key}"
                elif action == "Mouse":
                    if "Left" in key: arduino_command = "M:LCLICK"
                    elif "Right" in key: arduino_command = "M:RCLICK"
                    elif "Middle" in key: arduino_command = "M:MCLICK"
                elif action == "Mouse Move":
                    # Mengubah "692,304" menjadi "M:MOVE:692:304"
                    parts = key.replace(" ", "").split(",")
                    if len(parts) == 2:
                        arduino_command = f"M:MOVE:{parts[0]}:{parts[1]}"
                elif action == "Delay":
                    # Mengubah input 1000 menjadi D:1000
                    ms_val = int(delay_val)
                    arduino_command = f"D:{ms_val}"
                    # Karena Python menggunakan detik, bagi 1000
                    python_sleep = ms_val / 1000.0  
                
                # --- JIKA MEMBACA FORMAT FILE LAMA (.json lama) ---
                elif action in ["K", "M", "D"]:
                    arduino_command = f"{action}:{key}"
                    if action == "D":
                        python_sleep = float(key) / 1000.0

                # 1. Kirim perintah ke Arduino
                if arduino_command:
                    self.serial.send_command(arduino_command)
                
                # 2. Jeda Python agar seirama dengan delay Arduino
                time.sleep(python_sleep)
                
            current_loop += 1
            
        self.is_running = False
        print("Macro Selesai.")

    # --- KONFIGURASI GLOBAL HOTKEY ---
    def on_press(self, key):
        if key == keyboard.Key.f8:
            # Jika ada fungsi sync dari GUI, jalankan itu dulu. Jika tidak, langsung play.
            if self.sync_callback:
                self.sync_callback()
            else:
                self.play()
        elif key == keyboard.Key.f9:
            self.pause()
        elif key == keyboard.Key.f10:
            self.stop()

    def start_hotkeys(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_hotkeys(self):
        if self.listener:
            self.listener.stop()