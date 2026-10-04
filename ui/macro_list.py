import tkinter as tk
from tkinter import ttk

class MacroList:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Action", "Key/Coord", "Delay (ms)")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", selectmode="extended")
        
        # Konfigurasi Perataan (Mentok Kiri)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W) # tk.W = West / Kiri
            
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Konfigurasi Warna Baris
        self.tree.tag_configure("Keyboard", background="#d4e6f1") # Biru Muda
        self.tree.tag_configure("Mouse", background="#d5f5e3")    # Hijau Muda
        self.tree.tag_configure("Mouse Move", background="#d5f5e3")
        self.tree.tag_configure("Delay", background="#e5e7e9")    # Abu-abu
        self.tree.tag_configure("DropTarget", background="black", foreground="white") # Penanda Drag & Drop

        # Variabel Drag & Drop
        self.on_drop_callback = None
        self._drag_data = {"active": False, "items": [], "indicator": None, "orig_tags": ""}
        
        # Binding Mouse
        self.tree.bind("<ButtonPress-1>", self._on_drag_start)
        self.tree.bind("<B1-Motion>", self._on_drag_motion)
        self.tree.bind("<ButtonRelease-1>", self._on_drag_release)

    def _get_icon_and_tag(self, action):
        if action == "Keyboard": return "⌨ Keyboard", "Keyboard"
        if action == "Mouse": return "🖱 Mouse Click", "Mouse"
        if action == "Mouse Move": return "🖲 Mouse Move", "Mouse Move"
        if action == "Delay": return "⏱ Delay", "Delay"
        return action, ""

    def add_step(self, action, key_coord, delay, index="end"):
        display_act, tag = self._get_icon_and_tag(action)
        # Teks asli disimpan tersembunyi, ikon ditampilkan di layar
        self.tree.insert("", index, text=action, values=(display_act, key_coord, delay), tags=(tag,))

    def update_step(self, item_id, action, key_coord, delay):
        display_act, tag = self._get_icon_and_tag(action)
        self.tree.item(item_id, text=action, values=(display_act, key_coord, delay), tags=(tag,))

    def delete_steps(self, item_ids):
        for item in item_ids:
            self.tree.delete(item)

    def clear_all(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def get_selected(self):
        return self.tree.selection()

    def get_step_data(self, item_id):
        action = self.tree.item(item_id, "text") # Ambil nama asli tanpa emoji
        values = self.tree.item(item_id, "values")
        return {"action": action, "key": values[1], "delay": values[2]}

    def get_index(self, item_id):
        return self.tree.index(item_id)

    def move_up(self, item_ids):
        item_ids = sorted(item_ids, key=self.get_index)
        for item in item_ids:
            idx = self.get_index(item)
            if idx > 0: self.tree.move(item, self.tree.parent(item), idx - 1)

    def move_down(self, item_ids):
        item_ids = sorted(item_ids, key=self.get_index, reverse=True)
        total = len(self.tree.get_children())
        for item in item_ids:
            idx = self.get_index(item)
            if idx < total - 1: self.tree.move(item, self.tree.parent(item), idx + 1)

    def get_all_steps(self):
        steps = []
        for item in self.tree.get_children():
            steps.append(self.get_step_data(item))
        return steps

    # --- LOGIKA DRAG & DROP & SWIPE SELECT ---
    def _on_drag_start(self, event):
        item = self.tree.identify_row(event.y)
        # Jika klik baris yang SUDAH TERELEKSI, aktifkan mode Drag & Drop
        if item and item in self.tree.selection():
            self._drag_data["active"] = True
            self._drag_data["items"] = self.tree.selection()
        # Jika klik baris kosong/belum terseleksi, biarkan Tkinter melakukan Swipe Select
        else:
            self._drag_data["active"] = False

    def _clear_indicator(self):
        indicator = self._drag_data["indicator"]
        if indicator and self.tree.exists(indicator):
            self.tree.item(indicator, tags=self._drag_data["orig_tags"])
        self._drag_data["indicator"] = None

    def _on_drag_motion(self, event):
        if self._drag_data["active"]:
            target = self.tree.identify_row(event.y)
            if target != self._drag_data["indicator"]:
                self._clear_indicator()
                if target and target not in self._drag_data["items"]:
                    self._drag_data["indicator"] = target
                    self._drag_data["orig_tags"] = self.tree.item(target, "tags")
                    self.tree.item(target, tags=("DropTarget",)) # Warna hitam
            return "break" # Blokir swipe-select bawaan saat Drag & Drop aktif

    def _on_drag_release(self, event):
        if self._drag_data["active"]:
            self._drag_data["active"] = False
            self._clear_indicator()
            target = self.tree.identify_row(event.y)
            if target and target not in self._drag_data["items"] and self.on_drop_callback:
                self.on_drop_callback(self._drag_data["items"], target)
            return "break"