#ifndef EXECUTORMOUSE_H
#define EXECUTORMOUSE_H
#include <Arduino.h>

void initMouse();
void clickLeft();
void clickRight();
void moveMouse(int x, int y);

#endif