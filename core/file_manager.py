import json
import os
import sys

class FileManager:
    def __init__(self):
        # Path aman untuk .EXE
        self.recent_file_path = os.path.join(self.get_base_path(), "recent_config.json")
        self.recent_files = self._load_recent()

    def get_base_path(self):
        if hasattr(sys, '_MEIPASS'):
            return os.path.dirname(sys.executable)
        return os.path.abspath(".")

    def _load_recent(self):
        if os.path.exists(self.recent_file_path):
            try:
                with open(self.recent_file_path, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_recent(self):
        with open(self.recent_file_path, 'w') as f:
            json.dump(self.recent_files, f)

    def add_recent(self, filepath):
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        
        # Batasi maksimal 5 file recent
        if len(self.recent_files) > 5:
            self.recent_files = self.recent_files[:5]
        self._save_recent()

    def save_macro(self, filepath, steps):
        with open(filepath, 'w') as f:
            json.dump(steps, f, indent=4)
        self.add_recent(filepath)

    def load_macro(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                steps = json.load(f)
            self.add_recent(filepath)
            return steps
        return []