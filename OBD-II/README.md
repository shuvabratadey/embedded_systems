# 🚗 OBD2 Bluetooth ELM327 — Complete AT Command Guide
### Using Serial Debug Assistant on Windows

> **Device:** OBD2 Scanner Bluetooth ELM327 (Mini)

> **Interface:** Windows Serial Debug Assistant

> **Standard:** SAE J1979 / ISO 15765 / ISO 9141 / SAE J1850

---

## 📋 Table of Contents

1. [What is OBD2?](#what-is-obd2)
2. [The ELM327 Mini — Hardware Overview](#the-elm327-mini--hardware-overview)
3. [OBD2 Protocols Overview](#obd2-protocols-overview)
4. [Car vs Bike — Which Protocol?](#car-vs-bike--which-protocol)
5. [CAN Bus Protocol Explained](#can-bus-protocol-explained)
6. [All AT Commands Reference](#all-at-commands-reference)
7. [Setting Up Serial Debug Assistant](#setting-up-serial-debug-assistant)
8. [Step-by-Step Debugging Guide](#step-by-step-debugging-guide)
9. [OBD2 PID Commands](#obd2-pid-commands)
10. [Decoding Responses](#decoding-responses)
11. [Building a Single Debug Command](#building-a-single-debug-command)
12. [Troubleshooting](#troubleshooting)

---

## What is OBD2?

**OBD2** (On-Board Diagnostics, Version 2) is a standardized system built into all cars (1996+) and most motorcycles (2003+) that exposes the vehicle's internal sensors, ECU data, and diagnostic trouble codes (DTCs) through a standard 16-pin connector.

The **ELM327** chip acts as a **translator** between the vehicle's proprietary protocol (CAN, ISO, VPW, PWM) and a simple human-readable AT command interface over Bluetooth serial.

```
[Your Laptop] <--Bluetooth Serial--> [ELM327 Mini] <--OBD2 Wire--> [Vehicle ECU]
```

---

## The ELM327 Mini — Hardware Overview

```
┌──────────────────────────────────────────────┐
│          ELM327 Mini Bluetooth OBD2          │
│                                              │
│  ┌──────────┐   ┌──────────┐                 │
│  │ ELM327   │   │Bluetooth │                 │
│  │  Chip    │───│  Module  │                 │
│  │ (Parser) │   │ HC-05/06 │                 │
│  └──────────┘   └──────────┘                 │        ┌─────────────────┐
│       │                                      │          LED Indicators 
│  ┌────┴──────────────────────────────────┐   │          🔴 Power       
│  │        OBD2 16-Pin Connector          │   │          🟢 Connected   
│  │  Pin 4: Chassis Ground                │   │          🔵 Activity    
│  │  Pin 5: Signal Ground                 │   │        └─────────────────┘
│  │  Pin 6: CAN High (ISO 15765-4)        │   │
│  │  Pin 7: K-Line (ISO 9141-2)           │   │
│  │  Pin 14: CAN Low (ISO 15765-4)        │   │
│  │  Pin 15: L-Line (ISO 9141-2)          │   │
│  │  Pin 16: Battery (+12V)               │   │
│  └───────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
```

### Key Specifications

| Property         | Value                         |
|-----------------|------------------------------- |
| Chip            | ELM327 v1.5 / v2.1 (clone)     |
| Bluetooth       | SPP (Serial Port Profile)      |
| Baud Rate       | 38400 bps (default)            |
| Voltage Input   | 12V from OBD2 Pin 16           |
| Operating Temp  | -40°C to +85°C                 |
| Protocols       | All 5 OBD2 protocols           |
| Pairing PIN     | `1234` or `0000`               |

### Important Notes About Mini ELM327

> ⚠️ **Clone Warning:** Most "Mini" ELM327 adapters sold cheaply are **clones** of the original Elm Electronics chip. They work for basic OBD2 reading but may:
> - Report firmware version incorrectly (e.g., says v2.1 but behaves like v1.5)
> - Have limited AT command support
> - Fail on some advanced CAN protocols
> - Drop connections intermittently

---

## OBD2 Protocols Overview

OBD2 is a **standard interface** but supports **5 different underlying communication protocols** depending on the vehicle manufacturer and year.

| Protocol | Code | Description | Vehicles |
|---------|------|-------------|---------|
| **SAE J1850 PWM** | 1 | Pulse Width Modulation, 41.6 kbps | Ford (1996–2007) |
| **SAE J1850 VPW** | 2 | Variable Pulse Width, 10.4 kbps | GM, Chrysler |
| **ISO 9141-2** | 3 | K-Line serial, 10.4 kbps | European, Asian cars (Older) |
| **ISO 14230-4 (KWP2000)** | 4 & 5 | Keyword Protocol 2000 | European, Hyundai, Kia |
| **ISO 15765-4 (CAN)** | 6, 7, 8, 9 | CAN Bus — **Most modern vehicles** | All cars 2008+, Many 2003+ |

### Quick Selection Guide

```
Your car is:
├── Made after 2008?          → Almost certainly CAN (Protocol 6)
├── Ford (1996–2007)?         → J1850 PWM (Protocol 1)
├── GM/Chrysler (1996–2007)?  → J1850 VPW (Protocol 2)
├── European/Asian (pre-2008)?→ ISO 9141-2 or KWP2000 (Protocol 3/4/5)
└── Not sure?                 → Use ATSP0 (Auto-detect)
```

---

## Car vs Bike — Which Protocol?

### Cars (Automobiles)

**Standard:** SAE J1979 / ISO 15765-4 (CAN Bus)

All cars sold in the USA from **2008** (and many from 2003) are **required by law** to use CAN Bus (ISO 15765-4). Older vehicles use the protocol in the table above based on manufacturer.

### Motorcycles / Bikes

**Standard:** ISO 11898 (CAN Bus) or ISO 9141 (K-Line)

Motorcycles are **not required** by the same OBD2 mandate as cars. However:

| Manufacturer | Protocol Used |
|-------------|---------------|
| Yamaha (2006+) | ISO 9141 / CAN |
| Honda (2009+) | ISO 9141 / ISO 15765 |
| BMW Motorrad | CAN Bus (ISO 15765) |
| KTM (2014+) | CAN Bus |
| Kawasaki | ISO 9141 |
| Ducati | CAN Bus |
| Royal Enfield (2020+) | CAN Bus / Proprietary |
| Bajaj | Proprietary (limited OBD) |
| Hero / TVS | Limited OBD2 / Proprietary |

> 💡 **Indian Bikes Note:** BS6-compliant motorcycles (2020+) in India are **required to have OBD2** under BS6 Phase 2 norms. Older BS4 bikes may have a **diagnostic connector** but use proprietary protocols — not standard OBD2.

---

## CAN Bus Protocol Explained

CAN (Controller Area Network) is the most common modern vehicle protocol. Understanding it helps decode responses.

### CAN Frame Structure

```
┌────────┬──────────┬─────┬───────────────────────┬─────┐
│ SOF    │  CAN ID  │ DLC │        Data           │ CRC │
│ 1 bit  │ 11 bits  │4bit │   Up to 8 bytes       │     │
└────────┴──────────┴─────┴───────────────────────┴─────┘
```

### OBD2 CAN IDs (Standard 11-bit)

| ID       | Direction         | Description |
|---------|-------------------|-------------|
| `0x7DF` | Tester → ECU      | Functional broadcast (all ECUs listen) |
| `0x7E0` | Tester → ECU 1    | Physical address to Engine ECU |
| `0x7E8` | ECU 1 → Tester    | Response from Engine ECU |
| `0x7E1` | Tester → ECU 2    | Transmission ECU |
| `0x7E9` | ECU 2 → Tester    | Response from Transmission ECU |

### OBD2 CAN Message Format

When you send `010D` (vehicle speed), this is what happens at the CAN level:

```
REQUEST  (Tester → ECU via 0x7DF):
  Byte 0: 02       = 2 data bytes follow
  Byte 1: 01       = Mode 01 (current data)
  Byte 2: 0D       = PID 0x0D (vehicle speed)
  Bytes 3-7: 00 00 00 00 00  (padding)

RESPONSE (ECU → Tester via 0x7E8):
  Byte 0: 03       = 3 data bytes follow
  Byte 1: 41       = 0x40 + Mode (0x01) = positive response
  Byte 2: 0D       = PID echoed back
  Byte 3: XX       = Actual speed value
```

### ISO 15765-4 CAN Variants

| Sub-Protocol | Baud Rate | ID Length | Code |
|-------------|-----------|-----------|------|
| ISO 15765-4 11-bit 500K | 500 kbps | 11-bit | ATSP6 |
| ISO 15765-4 29-bit 500K | 500 kbps | 29-bit | ATSP7 |
| ISO 15765-4 11-bit 250K | 250 kbps | 11-bit | ATSP8 |
| ISO 15765-4 29-bit 250K | 250 kbps | 29-bit | ATSP9 |

> **Most modern cars use ATSP6** (11-bit CAN at 500K). When in doubt, use `ATSP0` (auto-detect).

---

## All AT Commands Reference

AT Commands are sent **directly to the ELM327 chip** (not to the vehicle). They configure the adapter's behavior.

### General / Reset Commands

| Command | Description | Example Response |
|--------|-------------|-----------------|
| `ATZ` | Reset all settings to default | `ELM327 v1.5` |
| `ATD` | Set all to defaults (keeps baud rate) | `OK` |
| `ATWS` | Warm start (like ATZ but faster) | `ELM327 v1.5` |
| `ATI` | Print version ID | `ELM327 v1.5` |
| `AT@1` | Display device description | `OBDII to RS232 Interpreter` |
| `AT@2` | Display device identifier | `<identifier string>` |

### Echo and Output Formatting

| Command | Description | Default |
|--------|-------------|---------|
| `ATE0` | Echo OFF (recommended) | Echo ON |
| `ATE1` | Echo ON | — |
| `ATL0` | Linefeeds OFF | — |
| `ATL1` | Linefeeds ON | — |
| `ATH0` | Headers OFF (hide CAN IDs) | Headers OFF |
| `ATH1` | Headers ON (show CAN IDs) | — |
| `ATS0` | Spaces OFF in response bytes | Spaces ON |
| `ATS1` | Spaces ON between response bytes | — |
| `ATSP` | Print spaces (between bytes) | — |

### Timing Commands

| Command | Description |
|--------|-------------|
| `ATAT0` | Adaptive timing OFF |
| `ATAT1` | Adaptive timing ON (recommended) |
| `ATAT2` | Aggressive adaptive timing |
| `ATST XX` | Set timeout to XX × 4ms (e.g., `ATST FF` = 1020ms) |
| `ATSTH XX` | Set timeout high byte |

### Protocol Commands

| Command | Description |
|--------|-------------|
| `ATSP0` | Auto-detect protocol |
| `ATSP1` | SAE J1850 PWM |
| `ATSP2` | SAE J1850 VPW |
| `ATSP3` | ISO 9141-2 |
| `ATSP4` | ISO 14230-4 KWP (5-baud init) |
| `ATSP5` | ISO 14230-4 KWP (fast init) |
| `ATSP6` | ISO 15765-4 CAN 11-bit 500K |
| `ATSP7` | ISO 15765-4 CAN 29-bit 500K |
| `ATSP8` | ISO 15765-4 CAN 11-bit 250K |
| `ATSP9` | ISO 15765-4 CAN 29-bit 250K |
| `ATSPA` | SAE J1939 CAN 29-bit 250K |
| `ATDP` | Describe current protocol |
| `ATDPN` | Describe protocol by number |
| `ATPC` | Protocol close |

### Advanced / Monitoring Commands

| Command | Description |
|--------|-------------|
| `ATMA` | Monitor all messages on bus |
| `ATMT XX` | Monitor for transmitter XX |
| `ATMR XX` | Monitor for receiver XX |
| `ATCRA` | Clear receive address filter |
| `ATCRA XXX` | Set receive address filter |
| `ATCSM0` | CAN silent monitoring OFF |
| `ATCSM1` | CAN silent monitoring ON |
| `ATBI` | Bypass init sequence |
| `ATIGN` | Read ignition voltage |
| `ATRV` | Read voltage (battery) |
| `ATPPS` | Print all programmable parameters |

---

## Setting Up Serial Debug Assistant

### Step 1 — Pair the ELM327 via Bluetooth

1. Plug the ELM327 Mini into the OBD2 port of your vehicle (ignition ON or engine running)
2. The red LED on the adapter should illuminate
3. On Windows: **Settings → Bluetooth & devices → Add device**
4. Look for `OBDII`, `ELM327`, or `V-LINK` in the list
5. Enter pairing PIN: **`1234`** (or try `0000`)
6. After pairing, a **virtual COM port** is created (e.g., COM4, COM5, COM6)

### Step 2 — Find the COM Port Number

1. Right-click **Start → Device Manager**
2. Expand **Ports (COM & LPT)**
3. Look for `Standard Serial over Bluetooth link (COMX)` — note the higher-numbered COM port (outgoing)

```
Example:
  Standard Serial over Bluetooth link (COM4)   ← Use this one (outgoing)
  Standard Serial over Bluetooth link (COM5)   ← Incoming (don't use)
```

### Step 3 — Configure Serial Debug Assistant

Open Serial Debug Assistant and configure:

| Setting         | Value                  |
|----------------|------------------------|
| **COM Port**   | Your COM port (e.g., COM4) |
| **Baud Rate**  | `38400`                |
| **Data Bits**  | `8`                    |
| **Parity**     | `None`                 |
| **Stop Bits**  | `1`                    |
| **Flow Control** | `None`              |
| **Send Format** | ASCII Text            |
| **Line Ending** | `\r` (Carriage Return) |

> ⚠️ **Critical:** ELM327 uses **Carriage Return (`\r`)** as command terminator, NOT newline (`\n`). Ensure your Serial Debug Assistant appends `\r` to each sent command.

---

## Step-by-Step Debugging Guide

Follow this exact sequence every time you start a debugging session.

---

### 🔌 Phase 1 — Connection & Reset

**Command 1: Reset the ELM327**
```
Send:    ATZ
Wait:    1–2 seconds
Receive: ELM327 v1.5
         >
```
The `>` prompt means the ELM327 is ready.

---

**Command 2: Turn Echo OFF**
```
Send:    ATE0
Receive: OK
         >
```
With echo off, the adapter won't repeat your commands back — cleaner output.

---

**Command 3: Turn Headers ON** (to see CAN IDs)
```
Send:    ATH1
Receive: OK
         >
```

---

**Command 4: Enable Adaptive Timing**
```
Send:    ATAT1
Receive: OK
         >
```

---

### 🔍 Phase 2 — Protocol Detection

**Command 5: Auto-detect Protocol**
```
Send:    ATSP0
Receive: OK
         >
```

**Command 6: Check What Protocol Was Detected**
```
Send:    ATDP
Receive: AUTO, ISO 15765-4 (CAN 11/500)
         >
```
This tells you the vehicle is using **CAN Bus at 11-bit 500K** — the most common modern standard.

---

**Command 7: Read Battery Voltage** (confirm connection is live)
```
Send:    ATRV
Receive: 12.4V
         >
```
> If you see `0.0V` or `NO DATA`, the adapter is not connected properly to the vehicle.

---

### 🚗 Phase 3 — Vehicle Communication Test

**Command 8: Request Supported PIDs (Mode 01, PID 00)**
```
Send:    0100
Receive: 7E8 06 41 00 BE 3F A8 13
         >
```

> This is the **most important test command**. If you get a response, the vehicle ECU is communicating. If you see `NO DATA` or `UNABLE TO CONNECT`, see the Troubleshooting section.

---

### 📊 Phase 4 — Read Live Data

**Command 9: Read Engine RPM**
```
Send:    010C
Receive: 7E8 04 41 0C 1A F8
         >
```

**Command 10: Read Vehicle Speed**
```
Send:    010D
Receive: 7E8 03 41 0D 3C
         >
```

**Command 11: Read Engine Coolant Temperature**
```
Send:    0105
Receive: 7E8 03 41 05 7B
         >
```

**Command 12: Read Throttle Position**
```
Send:    0111
Receive: 7E8 03 41 11 64
         >
```

---

### 🔴 Phase 5 — Read Diagnostic Trouble Codes (DTCs)

**Command 13: Check for DTCs (Mode 03)**
```
Send:    03
Receive: 7E8 06 43 01 P0300 00 00
         >
```
Or if no faults:
```
Receive: 7E8 02 43 00
```

**Command 14: Clear DTCs (Mode 04)** ⚠️ Use with caution!
```
Send:    04
Receive: 7E8 01 44
         >
```
> ⚠️ **Warning:** Clearing DTCs also resets all readiness monitors. The vehicle may fail an emissions test until all monitors complete their drive cycles.

---

## OBD2 PID Commands

### Mode 01 — Current Live Data

| Command | PID | Description | Formula | Unit |
|--------|-----|-------------|---------|------|
| `0100` | 00 | Supported PIDs 01–20 | Bitmask | — |
| `0101` | 01 | Monitor status since DTCs cleared | Bitmask | — |
| `0104` | 04 | Calculated engine load | A × 100/255 | % |
| `0105` | 05 | Engine coolant temperature | A − 40 | °C |
| `010A` | 0A | Fuel pressure | A × 3 | kPa |
| `010B` | 0B | Intake manifold pressure | A | kPa |
| `010C` | 0C | Engine RPM | (256A + B) / 4 | RPM |
| `010D` | 0D | Vehicle speed | A | km/h |
| `010E` | 0E | Timing advance | A/2 − 64 | ° |
| `010F` | 0F | Intake air temperature | A − 40 | °C |
| `0110` | 10 | MAF air flow rate | (256A + B) / 100 | g/s |
| `0111` | 11 | Throttle position | A × 100/255 | % |
| `011F` | 1F | Run time since engine start | 256A + B | seconds |
| `012F` | 2F | Fuel tank level input | A × 100/255 | % |
| `0133` | 33 | Barometric pressure | A | kPa |
| `015C` | 5C | Engine oil temperature | A − 40 | °C |

### Mode 03 — Diagnostic Trouble Codes

```
Send:    03
Purpose: Read stored DTCs
```

### Mode 04 — Clear DTCs

```
Send:    04
Purpose: Clear DTCs and reset readiness monitors
```

### Mode 09 — Vehicle Information

| Command | Description |
|--------|-------------|
| `0902` | VIN (Vehicle Identification Number) |
| `090A` | ECU name |

---

## Decoding Responses

### Response Format with Headers ON (ATH1)

```
7E8  03  41  0D  3C
 │    │   │   │   └── Data byte A (value = 0x3C = 60 decimal)
 │    │   │   └─────── PID echoed (0x0D = Vehicle Speed)
 │    │   └─────────── Response mode (0x41 = 0x40 + Mode 01)
 │    └─────────────── Number of data bytes that follow (3)
 └──────────────────── CAN ID of responding ECU (0x7E8 = Engine ECU)
```

### Decoding Engine RPM (PID 0x0C)

**Raw Response:**
```
7E8 04 41 0C 1A F8
```

**Parsing:**
- CAN ID: `7E8` → Engine ECU responding ✓
- Length: `04` → 4 bytes follow
- Mode: `41` → Mode 01 response ✓
- PID: `0C` → RPM confirmed ✓
- Data: `1A` = 26 decimal, `F8` = 248 decimal

**Formula:** `RPM = (256 × A + B) / 4`

```
RPM = (256 × 26 + 248) / 4
    = (6656 + 248) / 4
    = 6904 / 4
    = 1726 RPM
```

---

### Decoding Vehicle Speed (PID 0x0D)

**Raw Response:**
```
7E8 03 41 0D 3C
```

**Parsing:**
- Data byte A: `3C` = 60 decimal

**Formula:** `Speed = A`

```
Speed = 60 km/h
```

---

### Decoding Coolant Temperature (PID 0x05)

**Raw Response:**
```
7E8 03 41 05 7B
```

**Parsing:**
- Data byte A: `7B` = 123 decimal

**Formula:** `Temperature = A − 40`

```
Temperature = 123 − 40 = 83°C
```

---

### Decoding Throttle Position (PID 0x11)

**Raw Response:**
```
7E8 03 41 11 64
```

**Parsing:**
- Data byte A: `64` = 100 decimal

**Formula:** `Throttle = A × 100 / 255`

```
Throttle = 100 × 100 / 255 = 39.2%
```

---

### Decoding a DTC (Mode 03 Response)

**Raw Response:**
```
7E8 06 43 02 P0 30 0 P0 13 0
```

Simplified DTC format:

```
43           = Mode 03 response
02           = 2 DTCs stored
03 00        = DTC #1 → P0300
01 30        = DTC #2 → P0130
```

**DTC Character Mapping:**

```
Byte high nibble → First character:
  0x0X = P0 (Powertrain, generic)
  0x1X = P1 (Powertrain, manufacturer-specific)
  0x2X = P2 (Powertrain, generic)
  0x3X = P3 (Powertrain, manufacturer)
  0x4X = C0 (Chassis)
  0x8X = B0 (Body)
  0xCX = U0 (Network)
```

So `P0300` = Powertrain, Generic, Code 300 = **Random/Multiple Cylinder Misfire Detected**

---

## Building a Single Debug Command

To quickly diagnose a vehicle with one "master sequence," paste these commands in order into Serial Debug Assistant:

```
ATZ
ATE0
ATH1
ATAT1
ATSP0
ATRV
0100
010C
010D
0105
0111
012F
03
```

### What Each Line Does

```
ATZ     → Reset ELM327, confirm firmware version
ATE0    → Disable echo for clean output
ATH1    → Show CAN IDs so you can see which ECU responds
ATAT1   → Adaptive timing for reliable communication
ATSP0   → Auto-detect vehicle protocol
ATRV    → Confirm battery voltage (12V+ = ignition on)
0100    → Test ECU communication + get supported PIDs
010C    → Live engine RPM
010D    → Live vehicle speed
0105    → Engine coolant temperature
0111    → Throttle position percentage
012F    → Fuel level percentage
03      → Read all stored fault codes
```

### Expected Full Session Output

```
ATZ
ELM327 v1.5

ATE0
OK

ATH1
OK

ATAT1
OK

ATSP0
OK

ATRV
12.4V

0100
7E8 06 41 00 BE 3F A8 13

010C
7E8 04 41 0C 1A F8

010D
7E8 03 41 0D 00

0105
7E8 03 41 05 7B

0111
7E8 03 41 11 19

012F
7E8 03 41 2F A0

03
7E8 02 43 00

>
```

**Decoded Results:**
- Battery: **12.4V** ✅
- RPM: **(256×26 + 248) / 4 = 1726 RPM**
- Speed: **0 km/h** (vehicle stationary)
- Coolant: **123 − 40 = 83°C**
- Throttle: **(25 × 100) / 255 = 9.8%** (slight idle throttle)
- Fuel: **(160 × 100) / 255 = 62.7%**
- DTCs: **None stored** ✅

---

## Troubleshooting

| Problem | Cause | Fix |
|--------|-------|-----|
| `NO DATA` on OBD commands | Wrong protocol / ECU not responding | Try `ATSP0` to auto-detect; ensure ignition is ON |
| `UNABLE TO CONNECT` | Protocol mismatch or no response | Try `ATZ`, then manually set protocol with `ATSP1`–`ATSP9` |
| `BUS INIT: ERROR` | K-Line init failed | Vehicle may use CAN; try `ATSP6` |
| `?` response | Unknown AT command | Check command spelling — no spaces within command |
| No response at all | COM port wrong or baud rate mismatch | Check Device Manager; try baud 9600 or 115200 |
| `ELM327` not showing in Bluetooth | Adapter not powered | Ignition must be ON (or ACC position) when pairing |
| Voltage shows `0.0V` | Bad OBD port connection | Re-seat the adapter; check OBD port fuse (usually fuse box) |
| DTC clear doesn't work | Some ECUs require physical address | Try `ATSH 7E0` then send `04` |

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│              ELM327 Quick Reference                     │
├──────────────┬──────────────────────────────────────────┤
│ ATZ          │ Reset adapter                            │
│ ATE0         │ Echo off                                 │
│ ATH1         │ Show headers                             │
│ ATSP0        │ Auto protocol detect                     │
│ ATRV         │ Battery voltage                          │
│ ATDP         │ Show current protocol                    │
├──────────────┼──────────────────────────────────────────┤
│ 0100         │ Supported PIDs + ECU test                │
│ 010C         │ RPM → (256A+B)/4                         │
│ 010D         │ Speed → A (km/h)                         │
│ 0105         │ Coolant temp → A−40 (°C)                 │
│ 0111         │ Throttle → A×100/255 (%)                 │
│ 012F         │ Fuel level → A×100/255 (%)               │
│ 03           │ Read DTCs                                │
│ 04           │ Clear DTCs                               │
│ 0902         │ Read VIN                                 │
└──────────────┴──────────────────────────────────────────┘
COM Settings: 38400 baud, 8N1, No flow control, CR terminator
```

---

*Document prepared for ELM327 Mini Bluetooth OBD2 Scanner — Windows Serial Debug Assistant usage*
*Protocol References: SAE J1979, ISO 15765-4, ISO 9141-2, ISO 14230-4, SAE J1850*
