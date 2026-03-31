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

## 🚀 ESP-IDF (Recommended Way – Automatic Build & Flash)
### Instead of manually using mkspiffs, ESP-IDF can generate and flash the image automatically.
### Add to `CMakeLists.txt`

`spiffs_create_partition_image(spiffs data FLASH_IN_PROJECT)`

### Build & Flash

`idf.py build`
`idf.py flash`

#### ✔ This will:
* Create SPIFFS image from data/
* Automatically use correct partition size
* Flash it to the correct offset


---

## 🧠 Example Code (ESP-IDF SPIFFS)

```c
#include <stdio.h>
#include "esp_log.h"
#include "esp_spiffs.h"

static const char *TAG = "SPIFFS";

void app_main(void)
{
    esp_vfs_spiffs_conf_t conf = {
        .base_path = "/spiffs",
        .partition_label = NULL,
        .max_files = 5,
        .format_if_mount_failed = true
    };

    esp_err_t ret = esp_vfs_spiffs_register(&conf);

    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Mount failed");
        return;
    }

    FILE *f = fopen("/spiffs/config.json", "r");
    if (f == NULL) {
        ESP_LOGE(TAG, "File open failed");
        return;
    }

    char line[128];
    while (fgets(line, sizeof(line), f)) {
        printf("%s", line);
    }

    fclose(f);
}
```
## 🔧 ESP-IDF Requirements
### Enable SPIFFS

Run:

`idf.py menuconfig`

Go to:

`Component config → SPIFFS`

Enable:

* SPIFFS support

---
## Add Dependency

### In `CMakeLists.txt`:

`REQUIRES spiffs`

---

## Notes
- Size must match partition table
- Wrong size = mount failure
- Use LittleFS for new projects
- Use SPIFFS (ESP-IDF built-in) for native ESP-IDF projects
- In ESP-IDF, file path must include mount point:

```
/config.json → Arduino
/spiffs/config.json → ESP-IDF
```
