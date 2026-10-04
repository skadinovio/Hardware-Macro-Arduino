#include "ExecutorMouse.h"
#include <AbsMouse.h>

void initMouse() {
  // Sesuaikan 1920, 1080 dengan resolusi monitor Anda
  AbsMouse.init(1920, 1080); 
}

void clickLeft() {
  AbsMouse.press(MOUSE_LEFT);
  delay(50);
  AbsMouse.release(MOUSE_LEFT);
}

void clickRight() {
  AbsMouse.press(MOUSE_RIGHT);
  delay(50);
  AbsMouse.release(MOUSE_RIGHT);
}

void moveMouse(int x, int y) {
  AbsMouse.move(x, y);
  delay(20);
}