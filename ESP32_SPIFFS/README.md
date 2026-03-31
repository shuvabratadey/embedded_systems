# ESP32 Filesystem Image Guide (SPIFFS & LittleFS)

## Overview
This guide explains how to:
- Create a filesystem image (`spiffs.bin` or `littlefs.bin`)
- Determine correct partition size from the partition table
- Flash the image to ESP32
- Mount and use it in code

---
## Loction

### Location of mkspiffs: 
`C:\Users\<user_name>\AppData\Local\Arduino15\packages\esp32\tools\mkspiffs\0.2.3\mkspiffs.exe`

### Location of mklittlefs: 
`C:\Users\<user_name>\AppData\Local\Arduino15\packages\esp32\tools\mklittlefs\3.0.0-gnu12-dc7f933\mklittlefs.exe`

---

## Project Structure

```
your_project/
 ├── main.ino
 └── data/
     ├── index.html
     ├── config.json
```

---

## Step 1: Get Partition Size & Address

Open:
`Arduino15/packages/esp32/hardware/esp32/<version>/tools/partitions/`

Example:
`spiffs, data, spiffs, 0x290000, 0x170000`

- Offset: 0x290000
- Size:   0x170000

---

## Step 2: Create Filesystem Image

### SPIFFS
`mkspiffs -c data -p 256 -b 4096 -s 0x170000 spiffs.bin`

### LittleFS
`mklittlefs -c data -p 256 -b 4096 -s 0x170000 littlefs.bin`

---

## Step 3: Flash to ESP32

`esptool write_flash 0x290000 spiffs.bin`

---

## Example Code (SPIFFS)

```cpp
#include <SPIFFS.h>

void setup() {
  Serial.begin(115200);

  if (!SPIFFS.begin(true)) {
    Serial.println("SPIFFS Mount Failed");
    return;
  }

  File file = SPIFFS.open("/config.json", "r");
  if (file) {
    Serial.println(file.readString());
    file.close();
  }
}

void loop() {}
```

---

## Example Code (LittleFS)

```cpp
#include <LittleFS.h>

void setup() {
  Serial.begin(115200);

  if (!LittleFS.begin(true)) {
    Serial.println("LittleFS Mount Failed");
    return;
  }

  File file = LittleFS.open("/config.json", "r");
  if (file) {
    Serial.println(file.readString());
    file.close();
  }
}

void loop() {}
```

---

## Notes
- Size must match partition table
- Wrong size = mount failure
- Use LittleFS for new projects