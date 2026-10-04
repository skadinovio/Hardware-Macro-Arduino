import tkinter as tk
from core.serial_com import SerialManager
from core.macro_runner import MacroRunner
from ui.gui_manager import GUIManager

def main():
    root = tk.Tk()
    root.geometry("600x500")
    
    # 1. Inisialisasi Core (Logika)
    serial_manager = SerialManager()
    macro_runner = MacroRunner(serial_manager)
    
    # 2. Inisialisasi UI (Antarmuka)
    app = GUIManager(root, macro_runner)
    
    # 3. Jalankan Listener Keyboard Global & GUI
    macro_runner.start_hotkeys()
    
    # Pastikan hotkeys berhenti saat aplikasi ditutup
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, macro_runner))
    root.mainloop()

def on_closing(root, macro_runner):
    macro_runner.stop()
    macro_runner.stop_hotkeys()
    root.destroy()

if __name__ == "__main__":
    main()