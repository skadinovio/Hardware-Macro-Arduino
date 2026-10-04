# 🚀 Hardware Macro Arduino & Tkinter (Versi 1)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![PySerial](https://img.shields.io/badge/Serial-PySerial-green.svg)](https://pyserial.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Aplikasi desktop berbasis **Python & Tkinter** yang dirancang khusus untuk mengontrol perangkat **Hardware Macro berbasis Arduino / USB HID** secara visual. Dilengkapi dengan manajemen port serial *real-time*, editor daftar perintah interaktif, serta sistem eksekusi macro yang stabil tanpa membuat antarmuka membeku (freeze).

---

## 🖼️ Tampilan Antarmuka & Fitur Utama

* 🔌 **Koneksi Hardware Otomatis:** Panel deteksi port COM otomatis & pengaturan *baudrate* (mendukung mode *Mock* untuk pengujian tanpa perangkat fisik).
* 📝 **Editor Perintah (Treeview):** Manajemen baris perintah macro terstruktur (seperti Delay, Mouse Click, Press Key, Move Mouse).
* ⚡ **Eksekusi Aman (Multi-threaded):** Berjalan di latar belakang (background thread) sehingga GUI tetap responsif saat macro sedang aktif berjalan.
* 💾 **Project Save/Load:** Simpan susunan perintah macro Anda ke dalam format `.json` dan muat kembali kapan saja tanpa harus mengulang dari awal.

---

## 📥 Cara Mengunduh & Menggunakan Kode (ZIP)

1. Klik tombol hijau **`< > Code`** di bagian atas halaman repository ini.
2. Pilih **Download ZIP**.
3. Ekstrak file zip tersebut di komputer Anda.

---

## 🛠️ Panduan Instalasi & Menjalankan Program (Bagi Developer)

Bagi Anda yang ingin menjalankan atau memodifikasi kode sumber menggunakan Python, ikuti langkah-langkah di terminal/CMD berikut:

### 1. Buka Terminal di Folder Proyek
Arahkan direktori terminal / Command Prompt Anda ke folder tempat file proyek ini diekstrak.

### 2. Buat dan Aktifkan Virtual Environment (venv)
Sangat disarankan untuk menggunakan *virtual environment* agar instalasi library terisolasi dengan rapi:
```bash
# Membuat venv
python -m venv venv

# Mengaktifkan venv (Untuk Command Prompt Windows):
venv\Scripts\activate.bat

# Atau (Untuk PowerShell Windows):
venv\Scripts\Activate.ps1
```

### 3. Install Library yang Dibutuhkan
Setelah venv aktif (biasanya ditandai dengan teks `(venv)` di awal baris terminal), install *pyserial*:
```bash
pip install pyserial
```

### 4. Jalankan Aplikasi
```bash
python main.py
```

---

## 🗺️ Roadmap & Versi Berikutnya (Versi 2)
Proyek ini akan terus dikembangkan. Beberapa fitur lanjutan yang sedang disiapkan untuk rilis berikutnya:
* [ ] **Advanced Keyboard Shortcuts:** Dukungan `Del` (hapus), `Shift+Arrow` (multiple select), `Ctrl+Arrow` (memindahkan baris), dan `Ctrl+C/V/X` pada editor.
* [ ] **Logic Commands (IF Find Pixel):** Mengeksekusi perintah berdasarkan kecocokan warna pixel pada koordinat tertentu.
* [ ] **Logic Commands (IF Find Picture):** Deteksi gambar/snippet layar dengan fitur *region capture* langsung dari GUI.
* [ ] **Visual Hierarchy / Indentasi:** Tampilan menjorok ke dalam pada GUI untuk perintah-perintah yang berada di dalam blok logika `IF` agar mudah dibaca.
* [ ] **Non-Blocking Execution:** Engine eksekusi yang memungkinkan macro mengabaikan pencarian gambar/pixel yang gagal dan langsung melanjutkan tugas lain tanpa berhenti.

---
*Dibuat dengan penuh semangat untuk otomatisasi hardware yang lebih cerdas dan mudah digunakan!*
