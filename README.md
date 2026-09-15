# Wake&Brake: Multimodal Driver Alert Subsystem

An embedded driver counter-fatigue response system running an Arduino-based Finite State Machine (FSM). It communicates over a 9600-baud serial link with an upstream computer vision host (Raspberry Pi, Jetson, or PC) to deliver staged auditory, haptic, and olfactory stimuli.

---

## Required Hardware & Equipment

| Component | Function | Reference / Purchase Link |
| :--- | :--- | :--- |
| **Arduino Uno Rev3** | Subsystem microcontroller | [Arduino Uno Official Store](https://store.arduino.cc/products/arduino-uno-rev3) |
| **Seeed Grove Base Shield V2** | Modular header expansion board | [Seeed Studio Grove Base Shield](https://www.seeedstudio.com/Base-Shield-V2.html) |
| **Grove - Active Buzzer** | Auditory alarm unit | [Seeed Studio Grove Buzzer](https://www.seeedstudio.com/Grove-Buzzer.html) |
| **Grove - Vibration Motor** | Haptic physical alert | [Seeed Studio Grove Vibration Motor](https://www.seeedstudio.com/Grove-Vibration-Motor.html) |
| **Grove - 1-Channel Relay (or MOSFET Module)** | Switched 5V/12V driver for scent atomizer | [Seeed Studio Grove Relay](https://www.seeedstudio.com/Grove-Relay.html) |
| **Ultrasonic Scent Diffuser (5V Atomizer)** | Olfactory dispersal unit | [Adafruit DIY Ultrasonic Atomizer](https://www.adafruit.com/product/5725) |
| **Grove Universal 4-Pin Cables** | Interconnect wiring harness | [Seeed Studio 4-Pin Buckled Cables](https://www.seeedstudio.com/Grove-Universal-4-Pin-Buckled-20cm-Cable-5-PCs-Pack.html) |
| **USB Type-A to Type-B Cable** | Host-to-Arduino bridge & power line | [Standard USB 2.0 A-B Cable](https://www.adafruit.com/product/62) |

---

## Grove Base Shield Pinout

| Peripheral | Shield Port | Microcontroller Pin | Signal Type |
| :--- | :--- | :--- | :--- |
| **Vibration Motor** | **D2** | Digital Pin 2 | Digital Output |
| **Active Buzzer** | **D7** | Digital Pin 7 | Digital Output |
| **Diffuser Relay / Driver** | **D8** | Digital Pin 8 | Digital Output |

> **IMPORTANT:** Slide the small voltage toggle switch on the Grove Base Shield surface to the **5V** position before applying power.

---

## Assembly Steps

1. **Mount Shield:** Press the Grove Base Shield pins firmly into the female headers of the Arduino Uno until seated flush.
2. **Set Logic Voltage:** Verify that the onboard 3V3 / 5V selector switch is set to **5V**.
3. **Connect Actuators:**
   - Plug the Vibration Motor cable into Grove port **D2**.
   - Plug the Active Buzzer cable into Grove port **D7**.
   - Plug the Scent Diffuser Relay cable into Grove port **D8**.
4. **Attach Host:** Connect the Arduino Uno to your host system using the USB-A to USB-B cable.

---

## Serial Protocol Specification

- **Baud Rate:** `9600`
- **Line Terminator:** `\n` (Newline)

### Alert Commands

| Payload | Mode Name | Behavior |
| :--- | :--- | :--- |
| `H\n` | `ALERT_HAPTIC` | Vibration Motor ON, Buzzer OFF. |
| `B\n` | `ALERT_BUZZER` | Vibration Motor ON, Buzzer ON. |
| `S\n` | `ALERT_SEVERE` | Vibration ON, Buzzer ON, Triggers 30s Scent Spray (if IDLE). |
| `N\n` or `0\n` | `ALERT_NONE` | Deactivates active alerts; returns to monitoring state. |

### Configuration Commands

Runtime feature toggles accept a single parameterized line:

```text
CFG SOUND:x VIB:y SCENT:z\n
```

- `x`, `y`, `z` accept binary flags: `1` (Enable) or `0` (Disable).
- **Example:** `CFG SOUND:1 VIB:1 SCENT:0\n` enables sound and vibration while shutting off the scent channel.

---

## Olfactory Cycle Timing (FSM)

To mitigate olfactory fatigue (anosmia) and prevent driver habituation, scent dispersal runs on an independent state machine:

- **Active Dispersal:** 30 seconds (`digitalWrite(diffuserPin, HIGH)`)
- **Cooldown Lockout:** 90 seconds (`digitalWrite(diffuserPin, LOW)`)
- Re-triggering severe alerts during the 90-second cooldown will **not** trigger premature sprays.

---

## Host Integration Example (Python)

```python
import time
from serial import Serial

# Adjust port based on OS: '/dev/ttyACM0' (Linux/Pi) or 'COM3' (Windows)
ser = Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino DTR auto-reset

# Send Severe Alert
ser.write(b"S\n")
time.sleep(3)

# Clear Alerts
ser.write(b"N\n")
ser.close()
```
