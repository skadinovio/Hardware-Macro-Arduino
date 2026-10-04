import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ui.macro_list import MacroList
from core.file_manager import FileManager

class GUIManager:
    def __init__(self, root, runner):
        self.root = root
        self.root.title("Hardware Macro Recorder")
        self.root.geometry("850x500")
        
        self.runner = runner
        self.file_manager = FileManager()
        self.runner.sync_callback = self._trigger_play_from_hotkey
        
        self.clipboard = []
        self.undo_stack = []
        self.redo_stack = []
        
        self._build_menu()
        self._build_top_panel()
        
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.left_panel = ttk.Frame(self.main_paned, width=150)
        self.right_panel = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_panel, weight=0)
        self.main_paned.add(self.right_panel, weight=1)
        
        self._build_left_toolbar()
        self._build_table()
        self._build_control_panel()
        self._update_recent_menu()

        # Keyboard Shortcuts Undo & Redo
        self.root.bind("<Control-z>", self._undo)
        self.root.bind("<Control-y>", self._redo)

    def _center_window(self, window, width, height):
        self.root.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    # --- UNDO / REDO SYSTEM ---
    def _save_history(self):
        """Menyimpan state sebelum tabel diubah"""
        self.undo_stack.append(self.macro_list.get_all_steps())
        self.redo_stack.clear()
        if len(self.undo_stack) > 50: self.undo_stack.pop(0)

    def _undo(self, event=None):
        # Abaikan undo jika user sedang mengetik di dalam textbox (Entry)
        if isinstance(self.root.focus_get(), ttk.Entry): return
        
        if self.undo_stack:
            self.redo_stack.append(self.macro_list.get_all_steps())
            self._restore_state(self.undo_stack.pop())

    def _redo(self, event=None):
        if isinstance(self.root.focus_get(), ttk.Entry): return
        
        if self.redo_stack:
            self.undo_stack.append(self.macro_list.get_all_steps())
            self._restore_state(self.redo_stack.pop())

    def _restore_state(self, steps):
        self.macro_list.clear_all()
        for step in steps:
            self.macro_list.add_step(step['action'], step['key'], step['delay'])

    # --- MENU BAR & FILE ---
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self._file_new)
        file_menu.add_command(label="Open...", command=self._file_open)
        file_menu.add_command(label="Save As...", command=self._file_save)
        
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Open Recent", menu=self.recent_menu)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=self._undo)
        edit_menu.add_command(label="Redo (Ctrl+Y)", command=self._redo)
        
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        self.root.config(menu=menubar)

    def _update_recent_menu(self):
        self.recent_menu.delete(0, tk.END)
        for filepath in self.file_manager.recent_files:
            self.recent_menu.add_command(label=filepath, command=lambda p=filepath: self._load_file_data(p))

    def _file_new(self):
        if messagebox.askyesno("New", "Clear all steps?"):
            self._save_history()
            self.macro_list.clear_all()

    def _file_open(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filepath: self._load_file_data(filepath)

    def _load_file_data(self, filepath):
        self._save_history()
        steps = self.file_manager.load_macro(filepath)
        self.macro_list.clear_all()
        for step in steps:
            if isinstance(step, dict):
                self.macro_list.add_step(step.get("action", ""), step.get("key", ""), step.get("delay", 0))
            elif isinstance(step, str):
                parts = step.split(":", 1)
                self.macro_list.add_step(parts[0] if len(parts) > 0 else step, parts[1] if len(parts) > 1 else "", 0.1)
        self._update_recent_menu()

    def _file_save(self):
        steps = self.macro_list.get_all_steps()
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filepath:
            self.file_manager.save_macro(filepath, steps)
            self._update_recent_menu()

    # --- PANEL ATAS & TABEL ---
    def _build_top_panel(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="COM Port:").pack(side=tk.LEFT)
        self.port_cb = ttk.Combobox(frame, values=self.runner.serial.get_available_ports(), width=10)
        self.port_cb.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Connect", command=lambda: self.runner.serial.connect(self.port_cb.get())).pack(side=tk.LEFT)

    def _build_table(self):
        self.macro_list = MacroList(self.right_panel)
        self.macro_list.tree.bind("<Button-3>", self._show_context_menu)
        self.macro_list.tree.bind("<Double-1>", self._edit_selected)
        
        # Integrasi Drop Logic dengan Undo
        self.macro_list.on_drop_callback = self._handle_drag_drop
        self._build_context_menu()

    def _handle_drag_drop(self, items, target):
        self._save_history()
        target_idx = self.macro_list.get_index(target)
        for item in reversed(items):
            self.macro_list.tree.move(item, "", target_idx)

    # --- KONTEKS MENU & CLIPBOARD ---
    def _build_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self._menu_copy)
        self.context_menu.add_command(label="Cut", command=self._menu_cut)
        self.context_menu.add_command(label="Paste", command=self._menu_paste)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Edit", command=self._edit_selected)
        self.context_menu.add_command(label="Delete", command=self._menu_delete)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Move Up", command=self._menu_move_up)
        self.context_menu.add_command(label="Move Down", command=self._menu_move_down)

    def _show_context_menu(self, event):
        item = self.macro_list.tree.identify_row(event.y)
        if item:
            if item not in self.macro_list.tree.selection():
                self.macro_list.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def _menu_copy(self):
        selected = self.macro_list.get_selected()
        self.clipboard = [self.macro_list.get_step_data(i) for i in selected]

    def _menu_cut(self):
        self._menu_copy()
        self._menu_delete()

    def _menu_paste(self):
        if not self.clipboard: return
        self._save_history()
        selected = self.macro_list.get_selected()
        insert_idx = self.macro_list.get_index(selected[-1]) + 1 if selected else "end"
        for step in self.clipboard:
            self.macro_list.add_step(step['action'], step['key'], step['delay'], index=insert_idx)
            if isinstance(insert_idx, int): insert_idx += 1

    def _menu_delete(self):
        self._save_history()
        self.macro_list.delete_steps(self.macro_list.get_selected())

    def _menu_move_up(self):
        self._save_history()
        self.macro_list.move_up(self.macro_list.get_selected())

    def _menu_move_down(self):
        self._save_history()
        self.macro_list.move_down(self.macro_list.get_selected())

    def _edit_selected(self, event=None):
        selected = self.macro_list.get_selected()
        if not selected: return
        item = selected[0]
        data = self.macro_list.get_step_data(item)
        if data['action'] == "Keyboard": self._add_keyboard(edit_item=item)
        elif data['action'] == "Mouse": self._add_mouse(edit_item=item)
        elif data['action'] == "Mouse Move": self._add_mouse_move(edit_item=item)
        elif data['action'] == "Delay": self._add_delay(edit_item=item)

    # --- PANEL KIRI ---
    def _build_left_toolbar(self):
        ttk.Label(self.left_panel, text="Commands", font=("Arial", 10, "bold")).pack(pady=5)
        ttk.Button(self.left_panel, text="⌨ Keyboard", command=self._add_keyboard).pack(fill=tk.X, pady=2, padx=5)
        ttk.Button(self.left_panel, text="🖱 Mouse Click", command=self._add_mouse).pack(fill=tk.X, pady=2, padx=5)
        ttk.Button(self.left_panel, text="🖲 Mouse Move", command=self._add_mouse_move).pack(fill=tk.X, pady=2, padx=5)
        ttk.Button(self.left_panel, text="⏱ Delay", command=self._add_delay).pack(fill=tk.X, pady=2, padx=5)

    def _get_target_index(self, loc):
        if loc == "end": return "end"
        selected = self.macro_list.get_selected()
        if not selected: return "end"
        return self.macro_list.get_index(selected[0]) if loc == "above" else self.macro_list.get_index(selected[-1]) + 1

    # --- DIALOG POPUP (MENDUKUNG UNDO) ---
    def _add_keyboard(self, loc="end", edit_item=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Keyboard" if edit_item else "Add Keyboard")
        self._center_window(dialog, 250, 130)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Enter Key (e.g., A, Enter):").pack(pady=10)
        key_var = tk.StringVar()
        if edit_item: key_var.set(self.macro_list.get_step_data(edit_item)['key'])
        entry = ttk.Entry(dialog, textvariable=key_var, justify="center")
        entry.pack(pady=5)
        entry.focus()

        def on_ok(event=None):
            val = key_var.get().strip().upper()
            if val:
                self._save_history()
                if edit_item:
                    delay = self.macro_list.get_step_data(edit_item)['delay']
                    self.macro_list.update_step(edit_item, "Keyboard", val, delay)
                else:
                    self.macro_list.add_step("Keyboard", val, 0.1, index=self._get_target_index(loc))
            dialog.destroy()

        ttk.Button(dialog, text="OK", command=on_ok).pack(pady=10)
        dialog.bind('<Return>', on_ok)

    def _add_mouse(self, loc="end", edit_item=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Mouse Click" if edit_item else "Add Mouse Click")
        self._center_window(dialog, 250, 130)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Pilih Tombol Mouse:").pack(pady=10)
        btn_var = tk.StringVar(value="Left")
        if edit_item:
            old_key = self.macro_list.get_step_data(edit_item)['key']
            if "Right" in old_key: btn_var.set("Right")
            elif "Middle" in old_key: btn_var.set("Middle")

        cb = ttk.Combobox(dialog, textvariable=btn_var, values=["Left", "Right", "Middle"], state="readonly", justify="center")
        cb.pack(pady=5)

        def on_ok(event=None):
            self._save_history()
            val = f"Click {btn_var.get()}"
            if edit_item:
                delay = self.macro_list.get_step_data(edit_item)['delay']
                self.macro_list.update_step(edit_item, "Mouse", val, delay)
            else:
                self.macro_list.add_step("Mouse", val, 0.1, index=self._get_target_index(loc))
            dialog.destroy()

        ttk.Button(dialog, text="OK", command=on_ok).pack(pady=10)
        dialog.bind('<Return>', on_ok)

    def _add_mouse_move(self, loc="end", edit_item=None):
        from pynput import keyboard
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Mouse Move" if edit_item else "Add Mouse Move")
        self._center_window(dialog, 250, 180)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="X Coordinate:").pack(pady=(10, 0))
        x_var = tk.StringVar(value="0")
        ttk.Entry(dialog, textvariable=x_var, justify="center").pack(pady=2)

        ttk.Label(dialog, text="Y Coordinate:").pack(pady=(5, 0))
        y_var = tk.StringVar(value="0")
        ttk.Entry(dialog, textvariable=y_var, justify="center").pack(pady=2)
        
        if edit_item:
            try:
                x, y = self.macro_list.get_step_data(edit_item)['key'].split(',')
                x_var.set(x.strip())
                y_var.set(y.strip())
            except: pass

        ttk.Label(dialog, text="(Tekan F12 untuk rekam kursor)", foreground="blue", font=("Arial", 8)).pack(pady=5)

        def on_ok(event=None):
            self._save_history()
            val = f"{x_var.get()},{y_var.get()}"
            if edit_item:
                delay = self.macro_list.get_step_data(edit_item)['delay']
                self.macro_list.update_step(edit_item, "Mouse Move", val, delay)
            else:
                self.macro_list.add_step("Mouse Move", val, 0.1, index=self._get_target_index(loc))
            on_close()

        ttk.Button(dialog, text="OK", command=on_ok).pack(pady=5)

        def update_ui(x, y):
            x_var.set(str(x))
            y_var.set(str(y))

        def on_press(key):
            if key == keyboard.Key.f12: dialog.after(0, update_ui, dialog.winfo_pointerx(), dialog.winfo_pointery())

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        def on_close():
            listener.stop()
            dialog.destroy()
            
        dialog.protocol("WM_DELETE_WINDOW", on_close)

    def _add_delay(self, loc="end", edit_item=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Delay" if edit_item else "Add Delay")
        self._center_window(dialog, 250, 130)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Delay dalam milidetik\n(Contoh: 1000 = 1 detik)", justify="center").pack(pady=10)
        delay_var = tk.StringVar(value="1000")
        if edit_item: delay_var.set(str(self.macro_list.get_step_data(edit_item)['delay']))
        entry = ttk.Entry(dialog, textvariable=delay_var, justify="center")
        entry.pack(pady=5)
        entry.focus()

        def on_ok(event=None):
            try:
                val = float(delay_var.get())
                self._save_history()
                if edit_item: self.macro_list.update_step(edit_item, "Delay", "None", val)
                else: self.macro_list.add_step("Delay", "None", val, index=self._get_target_index(loc))
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Harap masukkan angka yang valid!", parent=dialog)

        ttk.Button(dialog, text="OK", command=on_ok).pack(pady=10)
        dialog.bind('<Return>', on_ok)

    # --- PANEL BAWAH (CONTROLS) ---
    def _build_control_panel(self):
        frame = ttk.LabelFrame(self.root, text="Playback Controls (F8: Play, F9: Pause, F10: Stop)")
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(btn_frame, text="▶ Play", command=self._sync_and_play).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="⏸ Pause", command=self.runner.pause).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="⏹ Stop", command=self.runner.stop).pack(side=tk.LEFT, padx=2)
        
        loop_frame = ttk.Frame(frame)
        loop_frame.pack(side=tk.RIGHT, padx=5, pady=5)
        self.loop_var = tk.IntVar(value=1)
        self.infinite_var = tk.BooleanVar(value=False)
        ttk.Label(loop_frame, text="Loop:").pack(side=tk.LEFT)
        self.spinbox = ttk.Spinbox(loop_frame, from_=1, to=9999, textvariable=self.loop_var, width=5)
        self.spinbox.pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(loop_frame, text="Infinite", variable=self.infinite_var, command=self._toggle_spinbox).pack(side=tk.LEFT)

    def _toggle_spinbox(self):
        self.spinbox.config(state=tk.DISABLED if self.infinite_var.get() else tk.NORMAL)

    def _sync_and_play(self):
        self.runner.load_settings(self.macro_list.get_all_steps(), self.loop_var.get(), self.infinite_var.get())
        self.runner.play()

    def _trigger_play_from_hotkey(self):
        self.root.after(0, self._sync_and_play)