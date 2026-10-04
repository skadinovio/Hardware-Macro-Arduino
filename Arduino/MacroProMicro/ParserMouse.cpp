#include "ParserMouse.h"
#include "ExecutorMouse.h"

void parseMouse(String cmd) {
  cmd.trim();
  
  // M:LCLICK
  if (cmd == "M:LCLICK") {
    clickLeft();
  } 
  // M:RCLICK
  else if (cmd == "M:RCLICK") {
    clickRight();
  } 
  // M:MOVE:10:-20
  else if (cmd.startsWith("M:MOVE:")) {
    String coords = cmd.substring(7); // Ambil teks setelah "M:MOVE:"
    int splitIdx = coords.indexOf(':'); // Cari posisi titik dua pemisah X dan Y
    
    if (splitIdx > 0) {
      int x = coords.substring(0, splitIdx).toInt();
      int y = coords.substring(splitIdx + 1).toInt();
      moveMouse(x, y);
    }
  }
  
  Serial.println("OK");
}