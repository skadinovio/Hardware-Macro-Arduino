#include "ParserKeyboard.h"
#include "ExecutorKeyboard.h"
#include "ParserMouse.h"
#include "ExecutorMouse.h"

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  initKeyboard();
  initMouse(); // Aktifkan fungsi Mouse
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("K:")) {
      parseKeyboard(cmd);
    } 
    else if (cmd.startsWith("M:")) {
      parseMouse(cmd);
    }
    else if (cmd.startsWith("D:")) {
      int delayTime = cmd.substring(2).toInt();
      delay(delayTime);
      Serial.println("OK");
    }
  }
}