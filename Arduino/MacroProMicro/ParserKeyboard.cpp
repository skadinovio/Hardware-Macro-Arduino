#include "ParserKeyboard.h"
#include "ExecutorKeyboard.h"
#include <Keyboard.h>

void parseKeyboard(String cmd) {
  cmd.trim();
  
  // Mengambil kata setelah "K:" (Contoh "K:F1" menjadi "F1")
  String keyStr = cmd.substring(2);
  uint8_t keyCode = 0;

  // Kamus Tombol Spesial
  if (keyStr == "F1") keyCode = KEY_F1;
  else if (keyStr == "F2") keyCode = KEY_F2;
  else if (keyStr == "F3") keyCode = KEY_F3;
  else if (keyStr == "F4") keyCode = KEY_F4;
  else if (keyStr == "F5") keyCode = KEY_F5;
  else if (keyStr == "F6") keyCode = KEY_F6;
  else if (keyStr == "F7") keyCode = KEY_F7;
  else if (keyStr == "F8") keyCode = KEY_F8;
  else if (keyStr == "F9") keyCode = KEY_F9;
  else if (keyStr == "F10") keyCode = KEY_F10;
  else if (keyStr == "F11") keyCode = KEY_F11;
  else if (keyStr == "F12") keyCode = KEY_F12;
  
  else if (keyStr == "ENTER") keyCode = KEY_RETURN;
  else if (keyStr == "ESC") keyCode = KEY_ESC;
  else if (keyStr == "TAB") keyCode = KEY_TAB;
  else if (keyStr == "SPACE") keyCode = ' '; 
  else if (keyStr == "BACKSPACE") keyCode = KEY_BACKSPACE;
  
  else if (keyStr == "UP") keyCode = KEY_UP_ARROW;
  else if (keyStr == "DOWN") keyCode = KEY_DOWN_ARROW;
  else if (keyStr == "LEFT") keyCode = KEY_LEFT_ARROW;
  else if (keyStr == "RIGHT") keyCode = KEY_RIGHT_ARROW;
  
  else if (keyStr == "CTRL") keyCode = KEY_LEFT_CTRL;
  else if (keyStr == "SHIFT") keyCode = KEY_LEFT_SHIFT;
  else if (keyStr == "ALT") keyCode = KEY_LEFT_ALT;
  
  // Jika teks hanya 1 huruf (A-Z atau 0-9)
  else if (keyStr.length() == 1) {
    char c = keyStr.charAt(0);
    if (c >= 'A' && c <= 'Z') {
      keyCode = c + 32; // Rumus ASCII mengubah A menjadi a
    } else {
      keyCode = c;
    }
  }
  
  // Jika tombol dikenali, eksekusi!
  if (keyCode != 0) {
    pressKey(keyCode);
  }
  
  Serial.println("OK"); // Kirim laporan selesai ke PC
}