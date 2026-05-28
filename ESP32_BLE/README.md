# ESP-IDF Bluetooth Low Energy (BLE) — Complete Developer Guide

> A comprehensive, step-by-step tutorial covering BLE fundamentals, GATT server/client implementation, services, characteristics, security, pairing, and bonding on the ESP32 using ESP-IDF.

---

## Table of Contents

- [ESP-IDF Bluetooth Low Energy (BLE) — Complete Developer Guide](#esp-idf-bluetooth-low-energy-ble--complete-developer-guide)
  - [Table of Contents](#table-of-contents)
  - [1. What is Bluetooth Low Energy (BLE)?](#1-what-is-bluetooth-low-energy-ble)
  - [2. Core BLE Concepts](#2-core-ble-concepts)
    - [2.1 GAP — Generic Access Profile](#21-gap--generic-access-profile)
    - [2.2 GATT — Generic Attribute Profile](#22-gatt--generic-attribute-profile)
    - [2.3 Services](#23-services)
    - [2.4 Characteristics](#24-characteristics)
    - [2.5 Descriptors](#25-descriptors)
    - [2.6 UUIDs](#26-uuids)
  - [3. Creating a BLE Project in ESP-IDF](#3-creating-a-ble-project-in-esp-idf)
    - [3.1 Project Structure](#31-project-structure)
    - [3.2 Menuconfig Settings](#32-menuconfig-settings)
      - [Step 1 — Enable Bluetooth](#step-1--enable-bluetooth)
      - [Step 2 — Choose BLE Host Stack](#step-2--choose-ble-host-stack)
      - [Step 3 — Enable Classic BT (if needed)](#step-3--enable-classic-bt-if-needed)
      - [Step 4 — Configure NVS for Bonding](#step-4--configure-nvs-for-bonding)
      - [Step 5 — Set BLE Feature Options](#step-5--set-ble-feature-options)
      - [Step 6 — Logging Level (optional)](#step-6--logging-level-optional)
    - [3.3 Required Dependencies](#33-required-dependencies)
  - [4. BLE Architecture in ESP-IDF](#4-ble-architecture-in-esp-idf)
    - [4.1 NimBLE vs Bluedroid](#41-nimble-vs-bluedroid)
    - [4.2 Stack Initialization Flow](#42-stack-initialization-flow)
  - [5. GATT Server — Complete Guide](#5-gatt-server--complete-guide)
    - [5.1 Key Structures](#51-key-structures)
      - [`esp_gatt_srvc_id_t` — Service ID](#esp_gatt_srvc_id_t--service-id)
      - [`esp_gatt_id_t` — Generic ID (used for services and characteristics)](#esp_gatt_id_t--generic-id-used-for-services-and-characteristics)
      - [`esp_bt_uuid_t` — UUID](#esp_bt_uuid_t--uuid)
      - [`gatts_profile_inst` — Application Profile (user-defined convenience struct)](#gatts_profile_inst--application-profile-user-defined-convenience-struct)
      - [`esp_ble_adv_data_t` — Advertisement Data](#esp_ble_adv_data_t--advertisement-data)
      - [`esp_ble_adv_params_t` — Advertising Parameters](#esp_ble_adv_params_t--advertising-parameters)
    - [5.2 Event Callbacks](#52-event-callbacks)
    - [5.3 GAP Events](#53-gap-events)
    - [5.4 GATTS Events](#54-gatts-events)
    - [5.5 Step-by-Step: Initializing the BLE Stack](#55-step-by-step-initializing-the-ble-stack)
    - [5.6 Step-by-Step: Registering an Application Profile](#56-step-by-step-registering-an-application-profile)
    - [5.7 Step-by-Step: Adding a Service](#57-step-by-step-adding-a-service)
    - [5.8 Step-by-Step: Adding a Characteristic](#58-step-by-step-adding-a-characteristic)
    - [5.9 Adding Read Support](#59-adding-read-support)
      - [Approach A — Auto-response (use `auto_rsp` in `add_char`)](#approach-a--auto-response-use-auto_rsp-in-add_char)
      - [Approach B — Manual response (recommended for dynamic data)](#approach-b--manual-response-recommended-for-dynamic-data)
    - [5.10 Adding Write Support](#510-adding-write-support)
      - [Long Write (\> MTU size)](#long-write--mtu-size)
    - [5.11 Adding Notify Support](#511-adding-notify-support)
      - [Prerequisites:](#prerequisites)
      - [Sending a Notification:](#sending-a-notification)
      - [Detecting when client enables/disables notifications:](#detecting-when-client-enablesdisables-notifications)
    - [5.12 Adding Indicate Support](#512-adding-indicate-support)
    - [5.13 Adding a CCCD Descriptor](#513-adding-a-cccd-descriptor)
    - [5.14 User Description Descriptor (0x2901)](#514-user-description-descriptor-0x2901)
    - [5.15 Full GATT Server Example Code](#515-full-gatt-server-example-code)
  - [6. GATT Client — Complete Guide](#6-gatt-client--complete-guide)
    - [6.1 GATTC Key Structures](#61-gattc-key-structures)
      - [`esp_gattc_service_elem_t` — Discovered Service](#esp_gattc_service_elem_t--discovered-service)
      - [`esp_gattc_char_elem_t` — Discovered Characteristic](#esp_gattc_char_elem_t--discovered-characteristic)
      - [`esp_gattc_descr_elem_t` — Discovered Descriptor](#esp_gattc_descr_elem_t--discovered-descriptor)
    - [6.2 GATTC Events](#62-gattc-events)
    - [6.3 Step-by-Step: Building a GATT Client](#63-step-by-step-building-a-gatt-client)
      - [Step 1 — Initialize Stack (same as server, §5.5)](#step-1--initialize-stack-same-as-server-55)
      - [Step 2 — Configure BLE Scan Parameters](#step-2--configure-ble-scan-parameters)
      - [Step 3 — Start Scanning in GAP Callback](#step-3--start-scanning-in-gap-callback)
      - [Step 4 — Handle Connection and Discover Services](#step-4--handle-connection-and-discover-services)
      - [Step 5 — Collect Discovered Services](#step-5--collect-discovered-services)
      - [Step 6 — Get Characteristics After Discovery](#step-6--get-characteristics-after-discovery)
      - [Step 7 — Enable Notifications (write CCCD)](#step-7--enable-notifications-write-cccd)
      - [Step 8 — Receive Notifications](#step-8--receive-notifications)
      - [Step 9 — Read/Write Characteristic](#step-9--readwrite-characteristic)
    - [6.4 Full GATT Client Example Code](#64-full-gatt-client-example-code)
  - [7. Security, Pairing \& Bonding](#7-security-pairing--bonding)
    - [7.1 Key Terms](#71-key-terms)
    - [7.2 IO Capabilities](#72-io-capabilities)
    - [7.3 Pairing Methods](#73-pairing-methods)
    - [7.4 Configuring Security in ESP-IDF](#74-configuring-security-in-esp-idf)
      - [Responding to Security Events:](#responding-to-security-events)
    - [7.5 Bonding — Storing Long-Term Keys](#75-bonding--storing-long-term-keys)
    - [7.6 Security Events](#76-security-events)
  - [8. Advertising \& Connection Parameters](#8-advertising--connection-parameters)
    - [Advertisement Data Fields](#advertisement-data-fields)
    - [Connection Parameter Update](#connection-parameter-update)
  - [9. Common Pitfalls \& Debugging Tips](#9-common-pitfalls--debugging-tips)
    - [❌ Forgetting NVS initialization](#-forgetting-nvs-initialization)
    - [❌ Wrong handle count](#-wrong-handle-count)
    - [❌ Not restarting advertising after disconnect](#-not-restarting-advertising-after-disconnect)
    - [❌ Sending notifications when not enabled](#-sending-notifications-when-not-enabled)
    - [❌ Sending response for Write Without Response](#-sending-response-for-write-without-response)
    - [❌ Calling BLE APIs before stack is fully enabled](#-calling-ble-apis-before-stack-is-fully-enabled)
    - [✅ Enable BLE logs for debugging](#-enable-ble-logs-for-debugging)
    - [✅ Use nRF Connect (mobile app) for testing](#-use-nrf-connect-mobile-app-for-testing)
    - [✅ MTU negotiation](#-mtu-negotiation)
  - [10. Quick Reference Cheat Sheet](#10-quick-reference-cheat-sheet)
    - [BLE Stack Init](#ble-stack-init)
    - [Properties vs Permissions](#properties-vs-permissions)
    - [Notification vs Indication vs Read](#notification-vs-indication-vs-read)
    - [IO Cap → Pairing Method](#io-cap--pairing-method)
    - [Key UUIDs](#key-uuids)
  - [References](#references)

---

## 1. What is Bluetooth Low Energy (BLE)?

Bluetooth Low Energy (BLE), also known as Bluetooth Smart, is a wireless communication protocol designed for short-range communication with an emphasis on **very low power consumption**. Unlike Classic Bluetooth, BLE is optimized for applications that transmit small amounts of data infrequently — such as sensors, wearables, beacons, and IoT devices.

| Feature | Classic Bluetooth | BLE |
|---|---|---|
| Power consumption | High | Very Low |
| Data throughput | Up to 3 Mbps | Up to 2 Mbps (BLE 5.0) |
| Range | ~10–100 m | ~10–400 m (BLE 5.0) |
| Latency | ~100 ms | ~6 ms |
| Use case | Audio, file transfer | Sensors, beacons, IoT |

The ESP32 supports **dual-mode Bluetooth** (Classic + BLE) and BLE 5.0 on newer variants.

---

## 2. Core BLE Concepts

### 2.1 GAP — Generic Access Profile

GAP controls how BLE devices **discover each other and establish connections**. It defines two roles:

- **Peripheral** — Advertises its presence, waits for connections (e.g., a temperature sensor).
- **Central** — Scans for peripherals and initiates connections (e.g., a smartphone).

A peripheral broadcasts **advertisement packets** containing:
- Device name
- Service UUIDs it offers
- Manufacturer-specific data
- TX power level

### 2.2 GATT — Generic Attribute Profile

GATT defines **how data is structured, exchanged, and stored** once a BLE connection is established. It uses a client-server model:

- **GATT Server** — Holds the data (attributes) and exposes them. Typically the peripheral.
- **GATT Client** — Reads/writes data from the server. Typically the central (e.g., phone).

All data in GATT is organized in a **hierarchical tree**:

```
GATT Server
└── Service (e.g., Heart Rate Service)
    ├── Characteristic (e.g., Heart Rate Measurement)
    │   ├── Value
    │   └── Descriptor (e.g., CCCD — Client Characteristic Configuration)
    └── Characteristic (e.g., Body Sensor Location)
        └── Value
```

### 2.3 Services

A **Service** is a logical grouping of related characteristics. Each service has:
- A **UUID** (16-bit standard or 128-bit custom)
- A **handle** — an integer used internally to identify it on the ATT layer
- A **type**: Primary or Secondary

**Standard Bluetooth SIG services** use 16-bit UUIDs (e.g., `0x180D` = Heart Rate Service).  
**Custom/vendor services** use 128-bit UUIDs (e.g., `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`).

### 2.4 Characteristics

A **Characteristic** is the actual data unit inside a service. Each characteristic has:

| Component | Description |
|---|---|
| UUID | Identifies the type of data |
| Value | The actual data bytes |
| Properties | What operations are allowed (read, write, notify, etc.) |
| Permissions | Access control (readable, writable, encrypted, etc.) |
| Descriptors | Metadata about the characteristic |

**Characteristic Properties** (bitmask):

| Property | Bit | Description |
|---|---|---|
| `ESP_GATT_CHAR_PROP_BIT_BROADCAST` | 0x01 | Value can be broadcast |
| `ESP_GATT_CHAR_PROP_BIT_READ` | 0x02 | Client can read the value |
| `ESP_GATT_CHAR_PROP_BIT_WRITE_NR` | 0x04 | Write without response |
| `ESP_GATT_CHAR_PROP_BIT_WRITE` | 0x08 | Write with response |
| `ESP_GATT_CHAR_PROP_BIT_NOTIFY` | 0x10 | Server can push updates (no ACK) |
| `ESP_GATT_CHAR_PROP_BIT_INDICATE` | 0x20 | Server can push updates (with ACK) |
| `ESP_GATT_CHAR_PROP_BIT_AUTH` | 0x40 | Signed write required |

**Characteristic Permissions** (access control):

| Permission | Value | Description |
|---|---|---|
| `ESP_GATT_PERM_READ` | 0x01 | Readable without encryption |
| `ESP_GATT_PERM_READ_ENCRYPTED` | 0x02 | Readable only when encrypted |
| `ESP_GATT_PERM_READ_ENC_MITM` | 0x04 | Readable only when encrypted + MITM |
| `ESP_GATT_PERM_WRITE` | 0x10 | Writable without encryption |
| `ESP_GATT_PERM_WRITE_ENCRYPTED` | 0x20 | Writable only when encrypted |
| `ESP_GATT_PERM_WRITE_ENC_MITM` | 0x40 | Writable only when encrypted + MITM |

### 2.5 Descriptors

**Descriptors** provide metadata about a characteristic. Common ones:

| Name | UUID | Description |
|---|---|---|
| Client Characteristic Configuration (CCCD) | `0x2902` | Used by client to enable Notify/Indicate |
| Characteristic User Description | `0x2901` | Human-readable name string |
| Characteristic Presentation Format | `0x2904` | Data format info (unit, exponent, etc.) |
| Server Characteristic Configuration | `0x2903` | Server-side broadcast config |

> **Important:** You MUST add a CCCD descriptor (UUID `0x2902`) to any characteristic that supports **Notify** or **Indicate**. The client writes `0x0001` to enable notifications, `0x0002` to enable indications.

### 2.6 UUIDs

UUIDs identify services and characteristics. There are two formats:

```c
// 16-bit UUID (Bluetooth SIG standard)
#define GATTS_SERVICE_UUID_EXAMPLE   0x00FF

// 128-bit UUID (custom vendor-defined)
// Use tools like https://www.uuidgenerator.net/ to generate
static uint8_t service_uuid128[16] = {
    0xfb, 0x34, 0x9b, 0x5f, 0x80, 0x00, 0x00, 0x80,
    0x00, 0x10, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00,
};
```

---

## 3. Creating a BLE Project in ESP-IDF

### 3.1 Project Structure

```
ESP_BLE/
├── CMakeLists.txt
├── sdkconfig
├── main/
│   ├── CMakeLists.txt
│   ├── main.c              ← Your BLE application code
│   └── gatts_demo.h        ← Optional: header with defines
└── partitions.csv          ← Optional: custom partition table for NVS
```

**main/CMakeLists.txt:**
```cmake
idf_component_register(SRCS "main.c"
                        INCLUDE_DIRS ".")
```

**Top-level CMakeLists.txt:**
```cmake
cmake_minimum_required(VERSION 3.16)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(my_ble_project)
```

### 3.2 Menuconfig Settings

Run `idf.py menuconfig` and configure these options:

#### Step 1 — Enable Bluetooth

```
Component config
  └── Bluetooth
        ├── [*] Bluetooth                          ← ENABLE THIS
        └── Bluetooth controller mode: BLE Only    ← or Dual mode
```

#### Step 2 — Choose BLE Host Stack

```
Component config
  └── Bluetooth
        └── Bluedroid - Disabled / NimBLE - Enabled
```

> Choose **Bluedroid** (the default, based on Android's stack, more examples available) or **NimBLE** (lightweight, recommended for constrained memory).  
> This guide uses **Bluedroid**.

#### Step 3 — Enable Classic BT (if needed)

```
Component config
  └── Bluetooth
        └── Bluetooth Host: Bluedroid
              └── Classic Bluetooth: [*]   ← Only if you need Classic BT too
```

#### Step 4 — Configure NVS for Bonding

Bonding keys must be stored in NVS flash:
```
Component config
  └── NVS
        └── [*] NVS encryption: disabled (or enable for production)
```

Make sure your partition table includes an NVS partition (it does by default).

#### Step 5 — Set BLE Feature Options

```
Component config
  └── Bluetooth
        └── Bluedroid Options
              ├── [*] Include GATT server (GATTS)
              ├── [*] Include GATT client (GATTC)
              ├── [*] Include SMP security
              └── BLE Max Connections: 3   ← adjust as needed
```

#### Step 6 — Logging Level (optional)

```
Component config
  └── Log output
        └── Default log verbosity: Debug   ← helps during development
```

### 3.3 Required Dependencies

In `main.c`, include these headers for Bluedroid BLE:

```c
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"     // For GATT Server
#include "esp_gattc_api.h"     // For GATT Client
#include "esp_bt_defs.h"
#include "esp_bt_main.h"
#include "esp_gatt_common_api.h"
#include "esp_log.h"
```

---

## 4. BLE Architecture in ESP-IDF

### 4.1 NimBLE vs Bluedroid

| Feature | Bluedroid | NimBLE |
|---|---|---|
| Based on | Android Bluedroid | Apache Mynewt NimBLE |
| RAM usage | Higher (~70 KB) | Lower (~25 KB) |
| Flash usage | Higher | Lower |
| API style | Event-driven callbacks | Event-driven callbacks |
| Maturity | More examples | Actively developed |
| Classic BT support | Yes | No |

> For most new projects with enough RAM, **Bluedroid** is easier to get started. For memory-constrained applications, use **NimBLE**.

### 4.2 Stack Initialization Flow

```
nvs_flash_init()
        ↓
esp_bt_controller_init()
        ↓
esp_bt_controller_enable(ESP_BT_MODE_BLE)
        ↓
esp_bluedroid_init()
        ↓
esp_bluedroid_enable()
        ↓
esp_ble_gatts_register_callback()   ← Register GATT Server event handler
esp_ble_gap_register_callback()     ← Register GAP event handler
        ↓
esp_ble_gatts_app_register(APP_ID)  ← Triggers ESP_GATTS_REG_EVT
        ↓
[In ESP_GATTS_REG_EVT]
esp_ble_gap_set_device_name()
esp_ble_gap_config_adv_data()       ← Set up advertisement
esp_ble_gatts_create_service()      ← Create GATT service
        ↓
[In ESP_GATTS_CREATE_EVT]
esp_ble_gatts_start_service()
esp_ble_gatts_add_char()            ← Add characteristics
        ↓
[In ESP_GATTS_ADD_CHAR_EVT]
esp_ble_gatts_add_char_descr()      ← Add descriptors (CCCD etc.)
        ↓
[In ESP_GAP_BLE_ADV_DATA_SET_COMPLETE_EVT]
esp_ble_gap_start_advertising()     ← Start advertising
```

---

## 5. GATT Server — Complete Guide

### 5.1 Key Structures

#### `esp_gatt_srvc_id_t` — Service ID
```c
typedef struct {
    esp_gatt_id_t   id;         // Contains UUID and instance ID
    bool            is_primary; // true = Primary service
} esp_gatt_srvc_id_t;
```

#### `esp_gatt_id_t` — Generic ID (used for services and characteristics)
```c
typedef struct {
    esp_bt_uuid_t   uuid;       // UUID of the service/characteristic
    uint8_t         inst_id;    // Instance ID (0 for single instance)
} esp_gatt_id_t;
```

#### `esp_bt_uuid_t` — UUID
```c
typedef struct {
    uint16_t len;               // ESP_UUID_LEN_16 or ESP_UUID_LEN_128
    union {
        uint16_t    uuid16;     // 16-bit UUID
        uint8_t     uuid128[ESP_UUID_LEN_128]; // 128-bit UUID
    } uuid;
} esp_bt_uuid_t;
```

#### `gatts_profile_inst` — Application Profile (user-defined convenience struct)
```c
struct gatts_profile_inst {
    esp_gatts_cb_t      gatts_cb;       // Callback for this profile
    uint16_t            gatts_if;       // GATT interface (assigned on register)
    uint16_t            app_id;         // Application ID
    uint16_t            conn_id;        // Connection ID (when connected)
    uint16_t            service_handle; // Handle of the created service
    esp_gatt_srvc_id_t  service_id;     // Service UUID & ID
    uint16_t            char_handle;    // Handle of the characteristic
    esp_bt_uuid_t       char_uuid;      // Characteristic UUID
    esp_gatt_perm_t     perm;           // Permissions
    esp_gatt_char_prop_t property;      // Properties
    uint16_t            descr_handle;   // Descriptor handle
    esp_bt_uuid_t       descr_uuid;     // Descriptor UUID
};
```

#### `esp_ble_adv_data_t` — Advertisement Data
```c
typedef struct {
    bool            set_scan_rsp;       // true = scan response, false = adv data
    bool            include_name;       // Include device name
    bool            include_txpower;    // Include TX power
    int             min_interval;       // Min connection interval hint
    int             max_interval;       // Max connection interval hint
    int             appearance;         // BLE appearance value
    uint16_t        manufacturer_len;   // Manufacturer data length
    uint8_t         *p_manufacturer_data;
    uint16_t        service_data_len;
    uint8_t         *p_service_data;
    uint16_t        service_uuid_len;
    uint8_t         *p_service_uuid;    // UUID bytes
    uint8_t         flag;               // AD flags
} esp_ble_adv_data_t;
```

#### `esp_ble_adv_params_t` — Advertising Parameters
```c
typedef struct {
    uint16_t        adv_int_min;        // Min advertising interval (units of 0.625ms)
    uint16_t        adv_int_max;        // Max advertising interval
    esp_ble_adv_type_t  adv_type;       // ADV_TYPE_IND, ADV_TYPE_DIRECT_IND_HIGH, etc.
    esp_ble_addr_type_t own_addr_type;  // BLE_ADDR_TYPE_PUBLIC or _RANDOM
    esp_bd_addr_t   peer_addr;          // For directed advertising
    esp_ble_addr_type_t peer_addr_type;
    esp_ble_adv_channel_t   channel_map; // ADV_CHNL_37, _38, _39, or _ALL
    esp_ble_adv_filter_t    adv_filter_policy; // Allow all, whitelist, etc.
} esp_ble_adv_params_t;
```

---

### 5.2 Event Callbacks

ESP-IDF BLE is **entirely event-driven**. You register two main callbacks:

```c
// Register GATT Server callback
esp_ble_gatts_register_callback(gatts_event_handler);

// Register GAP callback
esp_ble_gap_register_callback(gap_event_handler);
```

---

### 5.3 GAP Events

The GAP callback receives these important events:

| Event | Trigger | What to do |
|---|---|---|
| `ESP_GAP_BLE_ADV_DATA_SET_COMPLETE_EVT` | Advertisement data configured | Call `esp_ble_gap_start_advertising()` |
| `ESP_GAP_BLE_SCAN_RSP_DATA_SET_COMPLETE_EVT` | Scan response data configured | Start advertising (if adv data also set) |
| `ESP_GAP_BLE_ADV_START_COMPLETE_EVT` | Advertising started/failed | Check `param->adv_start_cmpl.status` |
| `ESP_GAP_BLE_ADV_STOP_COMPLETE_EVT` | Advertising stopped | — |
| `ESP_GAP_BLE_UPDATE_CONN_PARAMS_EVT` | Connection parameters updated | Log new parameters |
| `ESP_GAP_BLE_SEC_REQ_EVT` | Security request from client | Call `esp_ble_gap_security_rsp()` |
| `ESP_GAP_BLE_AUTH_CMPL_EVT` | Authentication/pairing complete | Check success/failure |
| `ESP_GAP_BLE_PASSKEY_REQ_EVT` | Passkey required (IO cap) | Call `esp_ble_passkey_reply()` |
| `ESP_GAP_BLE_PASSKEY_NOTIF_EVT` | Passkey to display to user | Show passkey to user |
| `ESP_GAP_BLE_NC_REQ_EVT` | Numeric comparison request | Call `esp_ble_confirm_reply()` |
| `ESP_GAP_BLE_KEY_EVT` | Key generated/distributed | Log key type |

---

### 5.4 GATTS Events

The GATT Server callback receives these events in order during setup:

| Event | When Triggered | Key Action |
|---|---|---|
| `ESP_GATTS_REG_EVT` | App profile registered | Create service, set device name, configure adv |
| `ESP_GATTS_CREATE_EVT` | Service created | Save `service_handle`, call `esp_ble_gatts_start_service()`, add characteristics |
| `ESP_GATTS_START_EVT` | Service started | — |
| `ESP_GATTS_ADD_CHAR_EVT` | Characteristic added | Save `attr_handle`, add descriptors |
| `ESP_GATTS_ADD_CHAR_DESCR_EVT` | Descriptor added | Save descriptor handle |
| `ESP_GATTS_CONNECT_EVT` | Client connected | Save `conn_id`, optionally update conn params |
| `ESP_GATTS_DISCONNECT_EVT` | Client disconnected | Restart advertising |
| `ESP_GATTS_READ_EVT` | Client is reading a characteristic | Respond with `esp_ble_gatts_send_response()` |
| `ESP_GATTS_WRITE_EVT` | Client wrote to a characteristic | Process data, send response if `need_rsp` |
| `ESP_GATTS_EXEC_WRITE_EVT` | Long write executed | Handle buffered writes |
| `ESP_GATTS_MTU_EVT` | MTU size negotiated | Save MTU value |
| `ESP_GATTS_CONF_EVT` | Indicate confirmed by client | — |
| `ESP_GATTS_UNREG_EVT` | Profile unregistered | Cleanup |
| `ESP_GATTS_DELETE_EVT` | Service deleted | — |
| `ESP_GATTS_STOP_EVT` | Service stopped | — |

---

### 5.5 Step-by-Step: Initializing the BLE Stack

```c
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_bt_main.h"
#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_log.h"

static const char *TAG = "BLE_SERVER";

void app_main(void)
{
    // Step 1: Initialize NVS (required for BLE bonding storage)
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Step 2: Release Classic BT memory if not needed (saves ~20KB heap)
    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));

    // Step 3: Initialize BT controller with default config
    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    ret = esp_bt_controller_init(&bt_cfg);
    ESP_ERROR_CHECK(ret);

    // Step 4: Enable BLE mode
    ret = esp_bt_controller_enable(ESP_BT_MODE_BLE);
    ESP_ERROR_CHECK(ret);

    // Step 5: Initialize Bluedroid host stack
    ret = esp_bluedroid_init();
    ESP_ERROR_CHECK(ret);

    // Step 6: Enable Bluedroid
    ret = esp_bluedroid_enable();
    ESP_ERROR_CHECK(ret);

    // Step 7: Register GATT Server and GAP callbacks
    ret = esp_ble_gatts_register_callback(gatts_event_handler);
    ESP_ERROR_CHECK(ret);

    ret = esp_ble_gap_register_callback(gap_event_handler);
    ESP_ERROR_CHECK(ret);

    // Step 8: Register an application profile (triggers ESP_GATTS_REG_EVT)
    ret = esp_ble_gatts_app_register(PROFILE_APP_ID);
    ESP_ERROR_CHECK(ret);

    // Step 9: Set maximum MTU size
    esp_ble_gatt_set_local_mtu(500);
}
```

---

### 5.6 Step-by-Step: Registering an Application Profile

An **Application Profile** is a logical container for a group of related services and characteristics. You can have multiple profiles (one per service group).

```c
#define PROFILE_APP_ID   0
#define GATTS_NUM_HANDLE 8    // Total handles: 1 service + (2 per char) + (1 per descr)

// Profile instance — stores all handles for your service
static struct gatts_profile_inst gl_profile = {
    .gatts_cb = gatts_profile_event_handler,
    .gatts_if = ESP_GATT_IF_NONE,   // Will be assigned on registration
};

// Main GATTS dispatcher — routes events to the right profile callback
static void gatts_event_handler(esp_gatts_cb_event_t event,
                                 esp_gatt_if_t gatts_if,
                                 esp_ble_gatts_cb_param_t *param)
{
    if (event == ESP_GATTS_REG_EVT) {
        if (param->reg.status == ESP_GATT_OK) {
            gl_profile.gatts_if = gatts_if; // Save the interface
        } else {
            ESP_LOGE(TAG, "App registration failed, status %d", param->reg.status);
            return;
        }
    }

    // Forward to the profile's own handler
    if (gatts_if == ESP_GATT_IF_NONE || gatts_if == gl_profile.gatts_if) {
        if (gl_profile.gatts_cb) {
            gl_profile.gatts_cb(event, gatts_if, param);
        }
    }
}
```

---

### 5.7 Step-by-Step: Adding a Service

Handle this inside `ESP_GATTS_REG_EVT`:

```c
// Define your Service UUID
#define GATTS_SERVICE_UUID   0x00FF
#define GATTS_NUM_HANDLE     8      // Must be >= 1 (service) + 2*num_chars + num_descr

static void gatts_profile_event_handler(esp_gatts_cb_event_t event,
                                         esp_gatt_if_t gatts_if,
                                         esp_ble_gatts_cb_param_t *param)
{
    switch (event) {
    case ESP_GATTS_REG_EVT:
        ESP_LOGI(TAG, "GATTS_REG_EVT, status %d, app_id %d",
                 param->reg.status, param->reg.app_id);

        // Set the device name visible during BLE scanning
        esp_ble_gap_set_device_name("MY_ESP32_BLE");

        // Configure and set advertisement data
        esp_ble_gap_config_adv_data(&adv_data);
        esp_ble_gap_config_adv_data(&scan_rsp_data);  // Optional scan response

        // Define and create the primary service
        gl_profile.service_id.is_primary = true;
        gl_profile.service_id.id.inst_id = 0;
        gl_profile.service_id.id.uuid.len = ESP_UUID_LEN_16;
        gl_profile.service_id.id.uuid.uuid.uuid16 = GATTS_SERVICE_UUID;

        // Create the service — triggers ESP_GATTS_CREATE_EVT
        esp_ble_gatts_create_service(gatts_if,
                                     &gl_profile.service_id,
                                     GATTS_NUM_HANDLE);
        break;

    case ESP_GATTS_CREATE_EVT:
        ESP_LOGI(TAG, "Service created, handle = %d", param->create.service_handle);

        // Save the service handle
        gl_profile.service_handle = param->create.service_handle;

        // Start the service
        esp_ble_gatts_start_service(gl_profile.service_handle);

        // Now add your first characteristic (see next section)
        add_characteristic(gatts_if);
        break;
    
    // ... more events below
    }
}
```

> **Handle Count Rule:**  
> Each service needs 1 handle.  
> Each characteristic needs 2 handles (declaration + value).  
> Each descriptor needs 1 handle.  
> So: `GATTS_NUM_HANDLE = 1 + (2 × num_chars) + num_descriptors`  
> **Always allocate a few extra handles as a safety margin.**

---

### 5.8 Step-by-Step: Adding a Characteristic

```c
#define GATTS_CHAR_UUID   0xFF01

static void add_characteristic(esp_gatt_if_t gatts_if)
{
    // Set the characteristic UUID
    gl_profile.char_uuid.len = ESP_UUID_LEN_16;
    gl_profile.char_uuid.uuid.uuid16 = GATTS_CHAR_UUID;

    // Initial value of the characteristic
    uint8_t char_value[4] = {0x11, 0x22, 0x33, 0x44};

    esp_attr_value_t gatts_char_val = {
        .attr_max_len = GATTS_CHAR_VAL_LEN_MAX,  // Maximum value length
        .attr_len     = sizeof(char_value),        // Current value length
        .attr_value   = char_value,                // Pointer to value
    };

    // Properties: what operations the client can do
    esp_gatt_char_prop_t property = ESP_GATT_CHAR_PROP_BIT_READ
                                  | ESP_GATT_CHAR_PROP_BIT_WRITE
                                  | ESP_GATT_CHAR_PROP_BIT_NOTIFY;

    // Permissions: access control
    esp_gatt_perm_t perm = ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE;

    // Add characteristic — triggers ESP_GATTS_ADD_CHAR_EVT
    esp_ble_gatts_add_char(gl_profile.service_handle,
                           &gl_profile.char_uuid,
                           perm,
                           property,
                           &gatts_char_val,
                           NULL);  // auto-response (NULL = handle manually)
}
```

Handle the result:

```c
case ESP_GATTS_ADD_CHAR_EVT:
    ESP_LOGI(TAG, "Characteristic added, attr_handle = %d, status = %d",
             param->add_char.attr_handle, param->add_char.status);

    // Save the characteristic handle
    gl_profile.char_handle = param->add_char.attr_handle;

    // Add a CCCD descriptor so clients can enable notifications
    add_cccd_descriptor(gatts_if);
    break;
```

---

### 5.9 Adding Read Support

The `ESP_GATTS_READ_EVT` fires when a client reads the characteristic. You have two approaches:

#### Approach A — Auto-response (use `auto_rsp` in `add_char`)

Set `auto_rsp` to auto-respond with the stored value automatically. Pass a non-NULL `esp_attr_control_t`:

```c
esp_attr_control_t control = {
    .auto_rsp = ESP_GATT_AUTO_RSP,  // Let stack respond automatically
};

esp_ble_gatts_add_char(gl_profile.service_handle,
                       &gl_profile.char_uuid,
                       perm, property,
                       &gatts_char_val,
                       &control);   // <-- pass control here
```

#### Approach B — Manual response (recommended for dynamic data)

```c
case ESP_GATTS_READ_EVT:
{
    ESP_LOGI(TAG, "Read request: conn_id=%d, handle=%d, offset=%d",
             param->read.conn_id, param->read.handle, param->read.offset);

    esp_gatt_rsp_t rsp;
    memset(&rsp, 0, sizeof(esp_gatt_rsp_t));

    rsp.attr_value.handle = param->read.handle;

    // Fill in your current data
    rsp.attr_value.len = 4;
    rsp.attr_value.value[0] = 0xDE;
    rsp.attr_value.value[1] = 0xAD;
    rsp.attr_value.value[2] = 0xBE;
    rsp.attr_value.value[3] = 0xEF;

    esp_ble_gatts_send_response(gatts_if,
                                param->read.conn_id,
                                param->read.trans_id,
                                ESP_GATT_OK,
                                &rsp);
    break;
}
```

> **User-Triggered Read:** The client always initiates reads. Your `READ_EVT` handler just provides the current data. To push data to the client without it polling, use **Notify** or **Indicate** instead.

---

### 5.10 Adding Write Support

```c
case ESP_GATTS_WRITE_EVT:
{
    ESP_LOGI(TAG, "Write request: conn_id=%d, handle=%d, len=%d",
             param->write.conn_id, param->write.handle, param->write.len);

    // Log the received data
    ESP_LOG_BUFFER_HEX(TAG, param->write.value, param->write.len);

    // Process the written data
    if (param->write.handle == gl_profile.char_handle) {
        // Example: copy value to a buffer
        memcpy(my_data_buffer, param->write.value,
               MIN(param->write.len, sizeof(my_data_buffer)));
    }

    // Send response only if the client requested one
    // (Write With Response vs Write Without Response)
    if (param->write.need_rsp) {
        esp_ble_gatts_send_response(gatts_if,
                                    param->write.conn_id,
                                    param->write.trans_id,
                                    ESP_GATT_OK,
                                    NULL);
    }
    break;
}
```

> **Write Without Response (`WRITE_NR`):** The client does not expect an acknowledgment. `param->write.need_rsp` will be `false`. Do NOT call `send_response()`.

#### Long Write (> MTU size)

For writes larger than MTU, the client uses **Prepared Write** (multi-packet). Handle `ESP_GATTS_EXEC_WRITE_EVT`:

```c
case ESP_GATTS_EXEC_WRITE_EVT:
    ESP_LOGI(TAG, "Execute write, flag = %d", param->exec_write.exec_write_flag);
    if (param->exec_write.exec_write_flag == ESP_GATT_PREP_WRITE_EXEC) {
        // Commit the buffered long write
        process_long_write(prepared_buf, prepare_len);
    } else {
        // Cancelled — discard buffer
    }
    esp_ble_gatts_send_response(gatts_if, param->exec_write.conn_id,
                                param->exec_write.trans_id, ESP_GATT_OK, NULL);
    break;
```

---

### 5.11 Adding Notify Support

**Notify** lets the server push data to the client **without the client polling**. No acknowledgment from the client.

#### Prerequisites:
1. The characteristic must have `ESP_GATT_CHAR_PROP_BIT_NOTIFY` in its properties.
2. A CCCD descriptor (`0x2902`) must be added (see §5.13).
3. The client must **write `0x0001`** to the CCCD to enable notifications.

#### Sending a Notification:

```c
// Call this whenever you want to push data to the connected client
void send_notify(esp_gatt_if_t gatts_if, uint16_t conn_id)
{
    uint8_t notify_data[] = {0xAA, 0xBB, 0xCC, 0xDD};

    esp_ble_gatts_send_indicate(
        gatts_if,
        conn_id,
        gl_profile.char_handle,
        sizeof(notify_data),
        notify_data,
        false   // false = Notify (no acknowledgment required)
    );
}
```

#### Detecting when client enables/disables notifications:

The client writes to the CCCD descriptor. Handle this in `ESP_GATTS_WRITE_EVT`:

```c
case ESP_GATTS_WRITE_EVT:
    if (param->write.handle == gl_profile.descr_handle
        && param->write.len == 2)
    {
        uint16_t cccd_value = (param->write.value[1] << 8) | param->write.value[0];

        if (cccd_value == 0x0001) {
            ESP_LOGI(TAG, "Notify enabled by client");
            notify_enabled = true;
        } else if (cccd_value == 0x0002) {
            ESP_LOGI(TAG, "Indicate enabled by client");
            indicate_enabled = true;
        } else if (cccd_value == 0x0000) {
            ESP_LOGI(TAG, "Notify/Indicate disabled by client");
            notify_enabled = false;
            indicate_enabled = false;
        }
    }
    break;
```

---

### 5.12 Adding Indicate Support

**Indicate** is like Notify but the client **sends an acknowledgment**. Use it for critical data that must be confirmed received.

```c
void send_indicate(esp_gatt_if_t gatts_if, uint16_t conn_id)
{
    uint8_t indicate_data[] = {0x11, 0x22, 0x33};

    esp_ble_gatts_send_indicate(
        gatts_if,
        conn_id,
        gl_profile.char_handle,
        sizeof(indicate_data),
        indicate_data,
        true    // true = Indicate (requires acknowledgment)
    );
    // After client ACKs, you get ESP_GATTS_CONF_EVT
}

// Confirmation received from client
case ESP_GATTS_CONF_EVT:
    ESP_LOGI(TAG, "Indicate confirmed, status=%d", param->conf.status);
    break;
```

| | Notify | Indicate |
|---|---|---|
| Client ACK required | No | Yes |
| Reliability | Best-effort | Guaranteed delivery |
| Throughput | Higher | Lower |
| Use case | Streaming data | Critical alerts |

---

### 5.13 Adding a CCCD Descriptor

The **Client Characteristic Configuration Descriptor (CCCD)** is required for Notify/Indicate:

```c
static void add_cccd_descriptor(esp_gatt_if_t gatts_if)
{
    gl_profile.descr_uuid.len = ESP_UUID_LEN_16;
    gl_profile.descr_uuid.uuid.uuid16 = ESP_GATT_UUID_CHAR_CLIENT_CONFIG; // 0x2902

    uint8_t cccd_value[2] = {0x00, 0x00};  // Default: notifications disabled

    esp_attr_value_t cccd_attr = {
        .attr_max_len = 2,
        .attr_len     = 2,
        .attr_value   = cccd_value,
    };

    // Add descriptor — triggers ESP_GATTS_ADD_CHAR_DESCR_EVT
    esp_ble_gatts_add_char_descr(
        gl_profile.service_handle,
        &gl_profile.descr_uuid,
        ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE,
        &cccd_attr,
        NULL
    );
}

case ESP_GATTS_ADD_CHAR_DESCR_EVT:
    ESP_LOGI(TAG, "Descriptor added, handle=%d", param->add_char_descr.attr_handle);
    gl_profile.descr_handle = param->add_char_descr.attr_handle;
    break;
```

---

### 5.14 User Description Descriptor (0x2901)

Adds a human-readable name to a characteristic (visible in some BLE tools):

```c
esp_bt_uuid_t user_desc_uuid = {
    .len = ESP_UUID_LEN_16,
    .uuid = { .uuid16 = ESP_GATT_UUID_CHAR_DESCRIPTION }, // 0x2901
};

char *desc_str = "Temperature (°C)";
esp_attr_value_t user_desc_val = {
    .attr_max_len = strlen(desc_str),
    .attr_len     = strlen(desc_str),
    .attr_value   = (uint8_t *)desc_str,
};

esp_ble_gatts_add_char_descr(
    gl_profile.service_handle,
    &user_desc_uuid,
    ESP_GATT_PERM_READ,
    &user_desc_val,
    NULL
);
```

---

### 5.15 Full GATT Server Example Code

```c
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_bt_main.h"
#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_gatt_common_api.h"
#include "esp_log.h"

#define TAG                  "GATTS_DEMO"
#define PROFILE_APP_ID       0
#define GATTS_SERVICE_UUID   0x00FF
#define GATTS_CHAR_UUID      0xFF01
#define GATTS_NUM_HANDLE     8
#define GATTS_CHAR_VAL_LEN   512
#define DEVICE_NAME          "ESP32_BLE_SERVER"

static bool adv_data_configured = false;
static bool scan_rsp_configured = false;
static bool notify_enabled = false;

struct gatts_profile_inst {
    esp_gatts_cb_t gatts_cb;
    uint16_t gatts_if;
    uint16_t app_id;
    uint16_t conn_id;
    uint16_t service_handle;
    esp_gatt_srvc_id_t service_id;
    uint16_t char_handle;
    esp_bt_uuid_t char_uuid;
    esp_gatt_perm_t perm;
    esp_gatt_char_prop_t property;
    uint16_t descr_handle;
    esp_bt_uuid_t descr_uuid;
};

static void gatts_profile_event_handler(esp_gatts_cb_event_t event,
                                         esp_gatt_if_t gatts_if,
                                         esp_ble_gatts_cb_param_t *param);

static struct gatts_profile_inst gl_profile = {
    .gatts_cb  = gatts_profile_event_handler,
    .gatts_if  = ESP_GATT_IF_NONE,
};

// Advertisement data
static uint8_t adv_service_uuid128[32] = {
    0xfb, 0x34, 0x9b, 0x5f, 0x80, 0x00, 0x00, 0x80,
    0x00, 0x10, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00,
};

static esp_ble_adv_data_t adv_data = {
    .set_scan_rsp        = false,
    .include_name        = true,
    .include_txpower     = false,
    .min_interval        = 0x0006,
    .max_interval        = 0x0010,
    .appearance          = 0x00,
    .manufacturer_len    = 0,
    .p_manufacturer_data = NULL,
    .service_data_len    = 0,
    .p_service_data      = NULL,
    .service_uuid_len    = sizeof(adv_service_uuid128),
    .p_service_uuid      = adv_service_uuid128,
    .flag                = ESP_BLE_ADV_FLAG_GEN_DISC | ESP_BLE_ADV_FLAG_BREDR_NOT_SPT,
};

static esp_ble_adv_params_t adv_params = {
    .adv_int_min        = 0x20,
    .adv_int_max        = 0x40,
    .adv_type           = ADV_TYPE_IND,
    .own_addr_type      = BLE_ADDR_TYPE_PUBLIC,
    .channel_map        = ADV_CHNL_ALL,
    .adv_filter_policy  = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY,
};

static void gap_event_handler(esp_gap_ble_cb_event_t event,
                               esp_ble_gap_cb_param_t *param)
{
    switch (event) {
    case ESP_GAP_BLE_ADV_DATA_SET_COMPLETE_EVT:
        adv_data_configured = true;
        if (adv_data_configured && scan_rsp_configured) {
            esp_ble_gap_start_advertising(&adv_params);
        }
        break;
    case ESP_GAP_BLE_SCAN_RSP_DATA_SET_COMPLETE_EVT:
        scan_rsp_configured = true;
        if (adv_data_configured && scan_rsp_configured) {
            esp_ble_gap_start_advertising(&adv_params);
        }
        break;
    case ESP_GAP_BLE_ADV_START_COMPLETE_EVT:
        if (param->adv_start_cmpl.status == ESP_BT_STATUS_SUCCESS) {
            ESP_LOGI(TAG, "Advertising started");
        } else {
            ESP_LOGE(TAG, "Advertising start failed: %d",
                     param->adv_start_cmpl.status);
        }
        break;
    case ESP_GAP_BLE_ADV_STOP_COMPLETE_EVT:
        ESP_LOGI(TAG, "Advertising stopped");
        break;
    case ESP_GAP_BLE_UPDATE_CONN_PARAMS_EVT:
        ESP_LOGI(TAG, "Connection params update: interval=%d, latency=%d, timeout=%d",
                 param->update_conn_params.interval,
                 param->update_conn_params.latency,
                 param->update_conn_params.timeout);
        break;
    default:
        break;
    }
}

static void gatts_profile_event_handler(esp_gatts_cb_event_t event,
                                         esp_gatt_if_t gatts_if,
                                         esp_ble_gatts_cb_param_t *param)
{
    switch (event) {
    case ESP_GATTS_REG_EVT:
        esp_ble_gap_set_device_name(DEVICE_NAME);
        esp_ble_gap_config_adv_data(&adv_data);

        gl_profile.service_id.is_primary = true;
        gl_profile.service_id.id.inst_id = 0;
        gl_profile.service_id.id.uuid.len = ESP_UUID_LEN_16;
        gl_profile.service_id.id.uuid.uuid.uuid16 = GATTS_SERVICE_UUID;

        esp_ble_gatts_create_service(gatts_if, &gl_profile.service_id, GATTS_NUM_HANDLE);
        break;

    case ESP_GATTS_CREATE_EVT:
        gl_profile.service_handle = param->create.service_handle;
        esp_ble_gatts_start_service(gl_profile.service_handle);

        gl_profile.char_uuid.len = ESP_UUID_LEN_16;
        gl_profile.char_uuid.uuid.uuid16 = GATTS_CHAR_UUID;

        uint8_t char_val[1] = {0x00};
        esp_attr_value_t gatts_char_val = {
            .attr_max_len = GATTS_CHAR_VAL_LEN,
            .attr_len     = sizeof(char_val),
            .attr_value   = char_val,
        };

        esp_ble_gatts_add_char(
            gl_profile.service_handle,
            &gl_profile.char_uuid,
            ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE,
            ESP_GATT_CHAR_PROP_BIT_READ | ESP_GATT_CHAR_PROP_BIT_WRITE |
            ESP_GATT_CHAR_PROP_BIT_NOTIFY,
            &gatts_char_val,
            NULL
        );
        break;

    case ESP_GATTS_ADD_CHAR_EVT:
        gl_profile.char_handle = param->add_char.attr_handle;

        gl_profile.descr_uuid.len = ESP_UUID_LEN_16;
        gl_profile.descr_uuid.uuid.uuid16 = ESP_GATT_UUID_CHAR_CLIENT_CONFIG;

        uint8_t cccd_val[2] = {0x00, 0x00};
        esp_attr_value_t cccd_attr = {
            .attr_max_len = 2, .attr_len = 2, .attr_value = cccd_val,
        };
        esp_ble_gatts_add_char_descr(
            gl_profile.service_handle,
            &gl_profile.descr_uuid,
            ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE,
            &cccd_attr,
            NULL
        );
        break;

    case ESP_GATTS_ADD_CHAR_DESCR_EVT:
        gl_profile.descr_handle = param->add_char_descr.attr_handle;
        ESP_LOGI(TAG, "Descriptor handle: %d", gl_profile.descr_handle);
        break;

    case ESP_GATTS_CONNECT_EVT:
        gl_profile.conn_id = param->connect.conn_id;
        ESP_LOGI(TAG, "Client connected, conn_id=%d", param->connect.conn_id);
        break;

    case ESP_GATTS_DISCONNECT_EVT:
        ESP_LOGI(TAG, "Client disconnected");
        notify_enabled = false;
        esp_ble_gap_start_advertising(&adv_params);
        break;

    case ESP_GATTS_READ_EVT: {
        ESP_LOGI(TAG, "Read request, handle=%d", param->read.handle);
        esp_gatt_rsp_t rsp;
        memset(&rsp, 0, sizeof(rsp));
        rsp.attr_value.handle = param->read.handle;
        rsp.attr_value.len = 4;
        rsp.attr_value.value[0] = 0xDE;
        rsp.attr_value.value[1] = 0xAD;
        rsp.attr_value.value[2] = 0xBE;
        rsp.attr_value.value[3] = 0xEF;
        esp_ble_gatts_send_response(gatts_if, param->read.conn_id,
                                    param->read.trans_id, ESP_GATT_OK, &rsp);
        break;
    }
    case ESP_GATTS_WRITE_EVT: {
        ESP_LOGI(TAG, "Write request, handle=%d, len=%d",
                 param->write.handle, param->write.len);
        ESP_LOG_BUFFER_HEX(TAG, param->write.value, param->write.len);

        if (param->write.handle == gl_profile.descr_handle && param->write.len == 2) {
            uint16_t cccd = (param->write.value[1] << 8) | param->write.value[0];
            notify_enabled = (cccd == 0x0001);
            ESP_LOGI(TAG, "Notifications %s", notify_enabled ? "enabled" : "disabled");
        }

        if (param->write.need_rsp) {
            esp_ble_gatts_send_response(gatts_if, param->write.conn_id,
                                        param->write.trans_id, ESP_GATT_OK, NULL);
        }
        break;
    }
    case ESP_GATTS_MTU_EVT:
        ESP_LOGI(TAG, "MTU negotiated: %d", param->mtu.mtu);
        break;

    default:
        break;
    }
}

static void gatts_event_handler(esp_gatts_cb_event_t event,
                                 esp_gatt_if_t gatts_if,
                                 esp_ble_gatts_cb_param_t *param)
{
    if (event == ESP_GATTS_REG_EVT) {
        if (param->reg.status == ESP_GATT_OK) {
            gl_profile.gatts_if = gatts_if;
        }
    }
    if (gatts_if == ESP_GATT_IF_NONE || gatts_if == gl_profile.gatts_if) {
        if (gl_profile.gatts_cb) {
            gl_profile.gatts_cb(event, gatts_if, param);
        }
    }
}

void app_main(void)
{
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));
    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_bt_controller_init(&bt_cfg));
    ESP_ERROR_CHECK(esp_bt_controller_enable(ESP_BT_MODE_BLE));
    ESP_ERROR_CHECK(esp_bluedroid_init());
    ESP_ERROR_CHECK(esp_bluedroid_enable());

    ESP_ERROR_CHECK(esp_ble_gatts_register_callback(gatts_event_handler));
    ESP_ERROR_CHECK(esp_ble_gap_register_callback(gap_event_handler));
    ESP_ERROR_CHECK(esp_ble_gatts_app_register(PROFILE_APP_ID));
    ESP_ERROR_CHECK(esp_ble_gatt_set_local_mtu(500));
}
```

---

## 6. GATT Client — Complete Guide

A **GATT Client** scans for BLE peripherals, connects, discovers services and characteristics, then reads, writes, or subscribes to notifications.

### 6.1 GATTC Key Structures

#### `esp_gattc_service_elem_t` — Discovered Service
```c
typedef struct {
    esp_gatt_srvc_id_t  srvc_id;    // Service UUID and ID
    uint16_t            start_handle;
    uint16_t            end_handle;
} esp_gattc_service_elem_t;
```

#### `esp_gattc_char_elem_t` — Discovered Characteristic
```c
typedef struct {
    uint16_t            char_handle;
    esp_bt_uuid_t       uuid;
    esp_gatt_char_prop_t properties;
} esp_gattc_char_elem_t;
```

#### `esp_gattc_descr_elem_t` — Discovered Descriptor
```c
typedef struct {
    uint16_t        handle;
    esp_bt_uuid_t   uuid;
} esp_gattc_descr_elem_t;
```

---

### 6.2 GATTC Events

| Event | Trigger | Action |
|---|---|---|
| `ESP_GATTC_REG_EVT` | App registered | Start scanning |
| `ESP_GATTC_CONNECT_EVT` | Physical connection established | — |
| `ESP_GATTC_OPEN_EVT` | GATT connection opened | Call `esp_ble_gattc_send_mtu_req()` |
| `ESP_GATTC_DIS_SRVC_CMPL_EVT` | Service discovery complete | Get services |
| `ESP_GATTC_SEARCH_RES_EVT` | One service found (per service) | Save service handles |
| `ESP_GATTC_SEARCH_CMPL_EVT` | All services discovered | Get characteristics |
| `ESP_GATTC_GET_CHAR_EVT` | Characteristic found *(deprecated)* | Use `esp_ble_gattc_get_all_char()` |
| `ESP_GATTC_READ_CHAR_EVT` | Read result received | Process value |
| `ESP_GATTC_WRITE_CHAR_EVT` | Write complete | Check status |
| `ESP_GATTC_WRITE_DESCR_EVT` | Descriptor write complete | Check status |
| `ESP_GATTC_NOTIFY_EVT` | Notification/Indication received | Process incoming data |
| `ESP_GATTC_DISCONNECT_EVT` | Disconnected | Reconnect or scan again |
| `ESP_GATTC_CFG_MTU_EVT` | MTU configured | Start service discovery |

---

### 6.3 Step-by-Step: Building a GATT Client

#### Step 1 — Initialize Stack (same as server, §5.5)

#### Step 2 — Configure BLE Scan Parameters

```c
static esp_ble_scan_params_t ble_scan_params = {
    .scan_type          = BLE_SCAN_TYPE_ACTIVE,   // Request scan responses
    .own_addr_type      = BLE_ADDR_TYPE_PUBLIC,
    .scan_filter_policy = BLE_SCAN_FILTER_ALLOW_ALL,
    .scan_interval      = 0x50,  // 50ms (units of 0.625ms)
    .scan_window        = 0x30,  // 30ms
    .scan_duplicate     = BLE_SCAN_DUPLICATE_DISABLE,
};
```

#### Step 3 — Start Scanning in GAP Callback

```c
case ESP_GAP_BLE_SCAN_PARAM_SET_COMPLETE_EVT:
    esp_ble_gap_start_scanning(30);  // Scan for 30 seconds
    break;

case ESP_GAP_BLE_SCAN_START_COMPLETE_EVT:
    ESP_LOGI(TAG, "Scan started");
    break;

case ESP_GAP_BLE_SCAN_RESULT_EVT: {
    esp_ble_gap_cb_param_t *scan_result = (esp_ble_gap_cb_param_t *)param;
    switch (scan_result->scan_rst.search_evt) {
    case ESP_GAP_SEARCH_INQ_RES_EVT:
        // Each discovered device lands here
        // Check device name or UUID to identify your target
        uint8_t *adv_name = NULL;
        uint8_t adv_name_len = 0;
        adv_name = esp_ble_resolve_adv_data(
            scan_result->scan_rst.ble_adv,
            ESP_BLE_AD_TYPE_NAME_CMPL,
            &adv_name_len
        );

        if (adv_name && strncmp((char *)adv_name,
                                TARGET_DEVICE_NAME,
                                adv_name_len) == 0) {
            ESP_LOGI(TAG, "Found target device: %s", TARGET_DEVICE_NAME);
            esp_ble_gap_stop_scanning();
            esp_ble_gattc_open(
                gl_profile_tab[PROFILE_A_APP_ID].gattc_if,
                scan_result->scan_rst.bda,
                scan_result->scan_rst.ble_addr_type,
                true   // true = direct connection
            );
        }
        break;

    case ESP_GAP_SEARCH_INQ_CMPL_EVT:
        ESP_LOGI(TAG, "Scan complete");
        break;
    }
    break;
}
```

#### Step 4 — Handle Connection and Discover Services

```c
case ESP_GATTC_OPEN_EVT:
    if (param->open.status != ESP_GATT_OK) {
        ESP_LOGE(TAG, "Open failed, status=%d", param->open.status);
        break;
    }
    gl_profile.conn_id = param->open.conn_id;
    memcpy(gl_profile.remote_bda, param->open.remote_bda, sizeof(esp_bd_addr_t));
    ESP_LOGI(TAG, "Connected to server");

    // Request larger MTU for better throughput
    esp_ble_gattc_send_mtu_req(gattc_if, param->open.conn_id);
    break;

case ESP_GATTC_CFG_MTU_EVT:
    ESP_LOGI(TAG, "MTU: %d", param->cfg_mtu.mtu);
    // Start service discovery
    esp_ble_gattc_search_service(gattc_if, param->cfg_mtu.conn_id, NULL);
    break;
```

#### Step 5 — Collect Discovered Services

```c
case ESP_GATTC_SEARCH_RES_EVT: {
    esp_gatt_srvc_id_t *srvc_id = &param->search_res.srvc_id;
    if (srvc_id->id.uuid.len == ESP_UUID_LEN_16
        && srvc_id->id.uuid.uuid.uuid16 == REMOTE_SERVICE_UUID)
    {
        ESP_LOGI(TAG, "Found target service");
        gl_profile.service_start_handle = param->search_res.start_handle;
        gl_profile.service_end_handle   = param->search_res.end_handle;
        get_server = true;
    }
    break;
}
```

#### Step 6 — Get Characteristics After Discovery

```c
case ESP_GATTC_SEARCH_CMPL_EVT:
    if (!get_server) { break; }

    uint16_t count = 0;
    esp_gatt_status_t status = esp_ble_gattc_get_attr_count(
        gattc_if, param->search_cmpl.conn_id,
        ESP_GATT_DB_CHARACTERISTIC,
        gl_profile.service_start_handle,
        gl_profile.service_end_handle,
        INVALID_HANDLE, &count
    );

    if (count > 0) {
        char_elem_result = malloc(sizeof(esp_gattc_char_elem_t) * count);
        esp_ble_gattc_get_all_char(
            gattc_if, param->search_cmpl.conn_id,
            gl_profile.service_start_handle,
            gl_profile.service_end_handle,
            char_elem_result, &count, 0
        );

        for (int i = 0; i < count; i++) {
            if (char_elem_result[i].uuid.uuid.uuid16 == REMOTE_CHAR_UUID) {
                gl_profile.char_handle = char_elem_result[i].char_handle;

                if (char_elem_result[i].properties & ESP_GATT_CHAR_PROP_BIT_NOTIFY) {
                    esp_ble_gattc_register_for_notify(gattc_if,
                        gl_profile.remote_bda, char_elem_result[i].char_handle);
                }
                if (char_elem_result[i].properties & ESP_GATT_CHAR_PROP_BIT_READ) {
                    esp_ble_gattc_read_char(gattc_if, gl_profile.conn_id,
                        char_elem_result[i].char_handle, ESP_GATT_AUTH_REQ_NONE);
                }
            }
        }
        free(char_elem_result);
    }
    break;
```

#### Step 7 — Enable Notifications (write CCCD)

```c
case ESP_GATTC_REG_FOR_NOTIFY_EVT: {
    // Find the CCCD descriptor for this characteristic
    uint16_t count = 0;
    uint16_t notify_en = 1;  // 0x0001 = enable notify

    esp_ble_gattc_get_attr_count(gattc_if, gl_profile.conn_id,
        ESP_GATT_DB_DESCRIPTOR,
        gl_profile.service_start_handle,
        gl_profile.service_end_handle,
        gl_profile.char_handle, &count);

    if (count > 0) {
        descr_elem_result = malloc(sizeof(esp_gattc_descr_elem_t) * count);
        esp_ble_gattc_get_all_descr(gattc_if, gl_profile.conn_id,
            gl_profile.char_handle,
            descr_elem_result, &count, 0);

        for (int i = 0; i < count; i++) {
            if (descr_elem_result[i].uuid.uuid.uuid16 ==
                ESP_GATT_UUID_CHAR_CLIENT_CONFIG)
            {
                esp_ble_gattc_write_char_descr(
                    gattc_if, gl_profile.conn_id,
                    descr_elem_result[i].handle,
                    sizeof(notify_en), (uint8_t *)&notify_en,
                    ESP_GATT_WRITE_TYPE_RSP,
                    ESP_GATT_AUTH_REQ_NONE
                );
                break;
            }
        }
        free(descr_elem_result);
    }
    break;
}
```

#### Step 8 — Receive Notifications

```c
case ESP_GATTC_NOTIFY_EVT:
    if (param->notify.is_notify) {
        ESP_LOGI(TAG, "Notification received, length=%d", param->notify.value_len);
    } else {
        ESP_LOGI(TAG, "Indication received, length=%d", param->notify.value_len);
    }
    ESP_LOG_BUFFER_HEX(TAG, param->notify.value, param->notify.value_len);
    break;
```

#### Step 9 — Read/Write Characteristic

```c
// Read
esp_ble_gattc_read_char(gattc_if, conn_id, char_handle, ESP_GATT_AUTH_REQ_NONE);

// Result
case ESP_GATTC_READ_CHAR_EVT:
    ESP_LOGI(TAG, "Read result, status=%d, len=%d",
             param->read.status, param->read.value_len);
    ESP_LOG_BUFFER_HEX(TAG, param->read.value, param->read.value_len);
    break;

// Write
uint8_t write_data[] = {0x01, 0x02};
esp_ble_gattc_write_char(gattc_if, conn_id, char_handle,
    sizeof(write_data), write_data,
    ESP_GATT_WRITE_TYPE_RSP,    // Write with response
    ESP_GATT_AUTH_REQ_NONE);

case ESP_GATTC_WRITE_CHAR_EVT:
    ESP_LOGI(TAG, "Write complete, status=%d", param->write.status);
    break;
```

---

### 6.4 Full GATT Client Example Code

For a full client implementation, refer to the official ESP-IDF example:  
`$IDF_PATH/examples/bluetooth/bluedroid/ble/gatt_client/`

The key flow in code form mirrors the steps above. The complete example is in the ESP-IDF repository and demonstrates all steps with clean structure.

---

## 7. Security, Pairing & Bonding

### 7.1 Key Terms

| Term | Definition |
|---|---|
| **Pairing** | The temporary authentication process where two devices verify each other and establish encryption keys for the current session |
| **Bonding** | Saving the encryption keys (Long-Term Keys) to persistent storage so future connections skip the full pairing ceremony |
| **LTK** | Long-Term Key — used to re-encrypt sessions after bonding |
| **IRK** | Identity Resolving Key — used to resolve random private addresses |
| **CSRK** | Connection Signature Resolving Key — for signed writes |
| **STK** | Short-Term Key — temporary key during initial pairing |
| **OOB** | Out-of-Band — sharing pairing data via a channel other than BLE (e.g., NFC) |
| **MITM** | Man-in-the-Middle attack protection — ensures both devices prove identity |
| **LE Secure Connections** | BLE 4.2+ pairing method using Elliptic Curve Diffie-Hellman (more secure than Legacy Pairing) |
| **Legacy Pairing** | Older BLE pairing, less secure, used on BLE 4.0/4.1 |

---

### 7.2 IO Capabilities

**IO Capabilities** describe what input/output your device has. They determine which pairing method is used:

| Capability | Constant | Meaning |
|---|---|---|
| Display Only | `ESP_IO_CAP_OUT` | Can display a number (passkey) but has no keyboard |
| Display Yes/No | `ESP_IO_CAP_IO` | Can display a number AND has Yes/No buttons |
| Keyboard Only | `ESP_IO_CAP_IN` | Has a keyboard/numpad; can enter a number |
| No Input No Output | `ESP_IO_CAP_NONE` | No display and no keyboard (e.g., a simple sensor) |
| Keyboard Display | `ESP_IO_CAP_KBDISP` | Has both a keyboard and a display |

---

### 7.3 Pairing Methods

The pairing method chosen depends on the **combined IO capabilities of both devices**:

| Initiator \ Responder | Display Only | Display Y/N | Keyboard Only | No I/O | Keyboard Display |
|---|---|---|---|---|---|
| **Display Only** | Just Works | Just Works | Passkey Entry | Just Works | Passkey Entry |
| **Display Y/N** | Just Works | Numeric Comparison | Passkey Entry | Just Works | Numeric Comparison |
| **Keyboard Only** | Passkey Entry | Passkey Entry | Passkey Entry | Just Works | Passkey Entry |
| **No I/O** | Just Works | Just Works | Just Works | Just Works | Just Works |
| **Keyboard Display** | Passkey Entry | Numeric Comparison | Passkey Entry | Just Works | Numeric Comparison |

**Pairing Method Descriptions:**

- **Just Works** — No user interaction. No MITM protection. Suitable for headphones, simple sensors, etc.
- **Passkey Entry** — One device displays a 6-digit passkey; the user enters it on the other device. Provides MITM protection.
- **Numeric Comparison** — Both devices display a 6-digit number; the user confirms they match on both devices. Requires `ESP_IO_CAP_IO`. Provides MITM protection. (BLE Secure Connections only)
- **OOB** — Pairing data exchanged via NFC, QR code, etc. Highest security but requires extra hardware.

---

### 7.4 Configuring Security in ESP-IDF

```c
// Set IO capabilities
esp_ble_io_cap_t iocap = ESP_IO_CAP_NONE;    // Change as needed
esp_ble_gap_set_security_param(ESP_BLE_SM_IOCAP_MODE, &iocap, sizeof(uint8_t));

// Set authentication requirements
// ESP_LE_AUTH_NO_BOND         — No bonding, no MITM
// ESP_LE_AUTH_BOND            — Bonding enabled, no MITM
// ESP_LE_AUTH_REQ_MITM        — MITM required, no bonding
// ESP_LE_AUTH_REQ_SC_ONLY     — LE Secure Connections only
// ESP_LE_AUTH_REQ_SC_BOND     — Secure Connections + Bonding
// ESP_LE_AUTH_REQ_SC_MITM     — Secure Connections + MITM
// ESP_LE_AUTH_REQ_SC_MITM_BOND — Secure Connections + MITM + Bonding (most secure)
esp_ble_auth_req_t auth_req = ESP_LE_AUTH_REQ_SC_MITM_BOND;
esp_ble_gap_set_security_param(ESP_BLE_SM_AUTHEN_REQ_MODE, &auth_req, sizeof(uint8_t));

// Set encryption key size (7–16 bytes; 16 = maximum security)
uint8_t key_size = 16;
esp_ble_gap_set_security_param(ESP_BLE_SM_MAX_KEY_SIZE, &key_size, sizeof(uint8_t));

// Set which keys to exchange
// ESP_BLE_ENC_KEY_MASK  — Encryption Key (LTK)
// ESP_BLE_ID_KEY_MASK   — Identity Key (IRK)
// ESP_BLE_CSR_KEY_MASK  — Connection Signature Key (CSRK)
// ESP_BLE_LINK_KEY_MASK — Link Key (for BT/BLE cross-transport)
uint8_t init_key = ESP_BLE_ENC_KEY_MASK | ESP_BLE_ID_KEY_MASK;
uint8_t rsp_key  = ESP_BLE_ENC_KEY_MASK | ESP_BLE_ID_KEY_MASK;
esp_ble_gap_set_security_param(ESP_BLE_SM_SET_INIT_KEY, &init_key, sizeof(uint8_t));
esp_ble_gap_set_security_param(ESP_BLE_SM_SET_RSP_KEY,  &rsp_key,  sizeof(uint8_t));
```

#### Responding to Security Events:

```c
case ESP_GAP_BLE_SEC_REQ_EVT:
    // Peer requests security; accept it
    esp_ble_gap_security_rsp(param->ble_security.ble_req.bd_addr, true);
    break;

case ESP_GAP_BLE_PASSKEY_REQ_EVT:
    // Our IO cap is Keyboard Only — we need to send the passkey the user types
    ESP_LOGI(TAG, "Enter passkey on peer device, then call passkey_reply");
    // In real code: read passkey from UART or keypad, then:
    esp_ble_passkey_reply(param->ble_security.ble_req.bd_addr, true, 123456);
    break;

case ESP_GAP_BLE_PASSKEY_NOTIF_EVT:
    // Our IO cap is Display Only — show this passkey to the user
    ESP_LOGI(TAG, "Passkey to display: %06d",
             param->ble_security.key_notif.passkey);
    break;

case ESP_GAP_BLE_NC_REQ_EVT:
    // Numeric Comparison — ask user: does the number match on both devices?
    ESP_LOGI(TAG, "Confirm passkey: %06d",
             param->ble_security.key_notif.passkey);
    esp_ble_confirm_reply(param->ble_security.ble_req.bd_addr, true); // true = yes, match
    break;

case ESP_GAP_BLE_AUTH_CMPL_EVT:
    if (param->ble_security.auth_cmpl.success) {
        ESP_LOGI(TAG, "Pairing SUCCESS. Auth mode: %d",
                 param->ble_security.auth_cmpl.auth_mode);
    } else {
        ESP_LOGE(TAG, "Pairing FAILED. Reason: %d",
                 param->ble_security.auth_cmpl.fail_reason);
    }
    break;

case ESP_GAP_BLE_KEY_EVT:
    ESP_LOGI(TAG, "Key exchange, key type: %d",
             param->ble_security.ble_key.key_type);
    break;
```

---

### 7.5 Bonding — Storing Long-Term Keys

When bonding is enabled (`ESP_LE_AUTH_BOND` flag), ESP-IDF **automatically stores and retrieves bond keys** from NVS flash. You don't need to manage the keys manually.

```c
// Remove all bonded devices
esp_ble_bond_dev_t *dev_list;
int dev_num = esp_ble_get_bond_device_num();
dev_list = malloc(sizeof(esp_ble_bond_dev_t) * dev_num);
esp_ble_get_bond_device_list(&dev_num, dev_list);
for (int i = 0; i < dev_num; i++) {
    esp_ble_remove_bond_device(dev_list[i].bd_addr);
}
free(dev_list);

// Remove a single bonded device (e.g., on user request)
esp_ble_remove_bond_device(peer_bd_addr);
```

**How re-connection works with bonding:**

1. ESP32 and phone pair and bond — keys are stored on both sides.
2. Phone disconnects.
3. Phone reconnects — both sides use the stored LTK to re-encrypt without user interaction.
4. No passkey entry or confirmation needed on subsequent connections.

---

### 7.6 Security Events

| Event | Description |
|---|---|
| `ESP_GAP_BLE_SEC_REQ_EVT` | Remote device requests a secured connection |
| `ESP_GAP_BLE_PASSKEY_NOTIF_EVT` | A passkey is generated to display to the user |
| `ESP_GAP_BLE_PASSKEY_REQ_EVT` | User must input a passkey (keyboard capability) |
| `ESP_GAP_BLE_NC_REQ_EVT` | Numeric comparison: user must confirm numbers match |
| `ESP_GAP_BLE_OOB_REQ_EVT` | OOB data required for pairing |
| `ESP_GAP_BLE_LOCAL_IR_EVT` | Local Identity Root key generated |
| `ESP_GAP_BLE_LOCAL_ER_EVT` | Local Encryption Root key generated |
| `ESP_GAP_BLE_KEY_EVT` | Keys exchanged between devices |
| `ESP_GAP_BLE_AUTH_CMPL_EVT` | Authentication/pairing attempt complete (success or fail) |
| `ESP_GAP_BLE_REMOVE_BOND_DEV_COMPLETE_EVT` | Bond removal confirmed |
| `ESP_GAP_BLE_GET_BOND_DEV_COMPLETE_EVT` | Bond device list retrieved |

---

## 8. Advertising & Connection Parameters

### Advertisement Data Fields

```c
static esp_ble_adv_data_t adv_data = {
    .set_scan_rsp    = false,          // false = primary adv, true = scan response
    .include_name    = true,           // Append device name
    .include_txpower = true,           // Append TX power level
    .min_interval    = 0x0006,         // Suggested min connection interval (×1.25ms = 7.5ms)
    .max_interval    = 0x0010,         // Suggested max connection interval (×1.25ms = 20ms)
    .appearance      = 0x0000,         // Generic Unknown; see Bluetooth SIG Appearance values
    .flag            = ESP_BLE_ADV_FLAG_GEN_DISC | ESP_BLE_ADV_FLAG_BREDR_NOT_SPT,
};
```

> **Advertising interval trade-off:**  
> - Shorter interval → faster discovery by clients → higher current draw  
> - Longer interval → slower discovery → lower power consumption  
> - Recommended for most IoT: 100–500 ms

### Connection Parameter Update

After connection, you can request updated parameters:

```c
esp_ble_conn_update_params_t conn_params = {
    .min_int  = 0x10,   // 20ms (×1.25ms)
    .max_int  = 0x20,   // 40ms
    .latency  = 0,      // Number of connection events to skip (slave latency)
    .timeout  = 400,    // Supervision timeout in 10ms units (4 seconds)
};
memcpy(conn_params.bda, remote_bda, sizeof(esp_bd_addr_t));
esp_ble_gap_update_conn_params(&conn_params);
```

---

## 9. Common Pitfalls & Debugging Tips

### ❌ Forgetting NVS initialization
```c
// Always call this FIRST before any BLE init
nvs_flash_init();
```

### ❌ Wrong handle count
If `GATTS_NUM_HANDLE` is too small, `ESP_GATTS_CREATE_EVT` won't provide enough handles for all your characteristics. Always compute:
```
handles = 1 (service) + 2 × num_chars + num_descriptors + safety_margin(2)
```

### ❌ Not restarting advertising after disconnect
```c
case ESP_GATTS_DISCONNECT_EVT:
    esp_ble_gap_start_advertising(&adv_params);  // ← Don't forget this
    break;
```

### ❌ Sending notifications when not enabled
Always check `notify_enabled` before calling `esp_ble_gatts_send_indicate()`.

### ❌ Sending response for Write Without Response
If `param->write.need_rsp == false`, do NOT call `esp_ble_gatts_send_response()`. It will cause an error.

### ❌ Calling BLE APIs before stack is fully enabled
All BLE calls must happen **after** `esp_bluedroid_enable()` returns `ESP_OK`, and ideally only after receiving `ESP_GATTS_REG_EVT`.

### ✅ Enable BLE logs for debugging

```c
esp_log_level_set("BT_BTM", ESP_LOG_DEBUG);
esp_log_level_set("BT_L2CAP", ESP_LOG_DEBUG);
esp_log_level_set("GATTS_DEMO", ESP_LOG_DEBUG);
```

### ✅ Use nRF Connect (mobile app) for testing

The **nRF Connect** app (iOS/Android) is the best tool for:
- Scanning and connecting to your ESP32
- Reading/writing characteristics
- Enabling notifications
- Viewing raw advertisement data

### ✅ MTU negotiation

Default ATT MTU is 23 bytes (20 bytes usable per packet). Always negotiate larger MTU for better throughput:

```c
// Server side
esp_ble_gatt_set_local_mtu(500);

// Client side
esp_ble_gattc_send_mtu_req(gattc_if, conn_id);
```

---

## 10. Quick Reference Cheat Sheet

### BLE Stack Init

```c
nvs_flash_init() → esp_bt_controller_init() → esp_bt_controller_enable()
→ esp_bluedroid_init() → esp_bluedroid_enable()
→ register callbacks → app_register()
```

### Properties vs Permissions

| | Properties | Permissions |
|---|---|---|
| **Purpose** | What the client CAN do | Who is ALLOWED to do it |
| **Location** | Characteristic declaration | Attribute Access Control |
| **Example** | READ, WRITE, NOTIFY | READ, WRITE, READ_ENCRYPTED |

### Notification vs Indication vs Read

| | Read | Notify | Indicate |
|---|---|---|---|
| Initiator | Client | Server | Server |
| ACK | Response | None | Client ACK |
| CCCD needed | No | Yes (0x0001) | Yes (0x0002) |
| Use case | On-demand data | Streaming | Critical alerts |

### IO Cap → Pairing Method

| Your Device | Phone | Method |
|---|---|---|
| `ESP_IO_CAP_NONE` | Any | Just Works |
| `ESP_IO_CAP_OUT` | Keyboard | Passkey Entry |
| `ESP_IO_CAP_IN` | Display | Passkey Entry |
| `ESP_IO_CAP_IO` | Display | Numeric Comparison |

### Key UUIDs

| Name | UUID |
|---|---|
| CCCD | `0x2902` |
| User Description | `0x2901` |
| Presentation Format | `0x2904` |
| Heart Rate Service | `0x180D` |
| Battery Service | `0x180F` |
| Device Information | `0x180A` |
| Generic Access | `0x1800` |
| Generic Attribute | `0x1801` |

---

## References

- [ESP-IDF Programming Guide — Bluetooth](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/bluetooth/index.html)
- [ESP-IDF BLE Examples](https://github.com/espressif/esp-idf/tree/master/examples/bluetooth/bluedroid/ble)
- [Bluetooth SIG Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/)
- [Bluetooth Core Specification](https://www.bluetooth.com/specifications/specs/core-specification/)
- [nRF Connect for Mobile](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-mobile)

---

*Made with ❤️ for the ESP32 developer community. Contributions welcome.*
