#include "ExecutorKeyboard.h"
#include <Keyboard.h>

void initKeyboard() {
  Keyboard.begin();
}

void pressKey(uint8_t key) {
  Keyboard.press(key);
  delay(150); // Waktu tekan yang ideal (150ms)
  Keyboard.release(key);
  delay(10);
  Keyboard.releaseAll(); // SAFETY NET: Cegah tombol nyangkut yang bikin Arduino hang
}