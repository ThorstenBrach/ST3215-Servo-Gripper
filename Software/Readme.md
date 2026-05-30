# ST3215 Servo Gripper Software

<a id="language-selection"></a>

## Sprache / Language

- Deutsch: [Zur deutschen Version](#de-start)
- English: [Jump to English version](#en-start)

---

<a id="de-start"></a>

## Deutsch

[Zur Sprachauswahl](#language-selection)

### Status

> **In Entwicklung** — Dedizierte Software für diesen Greifer befindet sich aktuell in Planung.
> Geplante Implementierungen:
>
> - **Python** — Direkte Steuerung über den Waveshare Serial Bus Servo Driver
> - **IEC 61131-3 (Structured Text)** — Einbindung in SPS-Steuerungen (PLC)

---

### In der Zwischenzeit: Referenzprojekte

Der Greifer nutzt denselben Servo (Waveshare ST3215) und denselben Treiber (Waveshare Serial Bus Servo Driver) wie mehrere bekannte Open-Source-Robotikprojekte.
Die dort verwendete Software ist direkt übertragbar.

#### SO-ARM100 / SO-101 Roboterarm (HuggingFace / The Robot Studio)

Das SO-101-Projekt ist ein vollständiger 6-DOF-Roboterarm, der ebenfalls den ST3215-Servo und den Waveshare-Treiber verwendet.
Die zugehörige Python-Bibliothek `lerobot` von HuggingFace ermöglicht die direkte Servo-Steuerung.

| Thema | Details |
|---|---|
| Projekt | SO-ARM100 / SO-101 |
| Repository | [github.com/huggingface/lerobot](https://github.com/huggingface/lerobot) |
| Hardware-Guide | [github.com/TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) |
| Sprache | Python |
| Servo-Treiber | Waveshare Serial Bus Servo Driver (identisch) |

#### Schnellstart mit lerobot (Python)

```bash
# Repository klonen
git clone https://github.com/huggingface/lerobot.git
cd lerobot

# Abhängigkeiten installieren
pip install -e ".[feetech]"
```

```python
from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus

# Verbindung zum Waveshare Treiber herstellen
# Port anpassen: Windows z.B. "COM3", Linux z.B. "/dev/ttyUSB0"
bus = FeetechMotorsBus(
    port="COM3",
    motors={
        "gripper": (1, "sts3215"),  # Motor-ID und Modell anpassen
    },
)
bus.connect()

# Position lesen
pos = bus.read("Present_Position", "gripper")
print(f"Aktuelle Position: {pos}")

# Greifer schließen (Zielposition setzen)
bus.write("Goal_Position", 2048, "gripper")
```

> Hinweis: Die Motor-ID und der COM-Port müssen auf die eigene Konfiguration angepasst werden.
> Die ID lässt sich mit dem Waveshare-Tool oder über das lerobot-Konfigurationsscript setzen.

#### Amazing Hand (Rollen Robotics) — rustypot / Rust

Die Amazing Hand von Rollen Robotics ist eine anthropomorphe Roboterhand, die dasselbe Waveshare Serial Bus Servo Driver Board einsetzt.
Als Steuerungsbibliothek wird `rustypot` verwendet — eine in Rust geschriebene Low-Level-Bibliothek für das Feetech/Dynamixel-Protokoll.
`rustypot` kommuniziert direkt über die serielle Schnittstelle und ist damit besonders geeignet für eingebettete Systeme und Echtzeit-Anwendungen.

| Thema | Details |
|---|---|
| Projekt | Amazing Hand |
| Hersteller | [Rollen Robotics](https://github.com/rollen-robotics) |
| Bibliothek | [rustypot](https://github.com/pollen-robotics/rustypot) |
| Sprache | Rust |
| Servo-Treiber | Waveshare Serial Bus Servo Driver (identisch) |

#### Schnellstart mit rustypot (Rust)

```toml
# Cargo.toml
[dependencies]
rustypot = "0.11"
```

```rust
use rustypot::device::sts3215;
use rustypot::DynamixelSerialIO;
use std::time::Duration;

fn main() {
    // Serielle Verbindung öffnen
    // Port anpassen: Windows z.B. "COM3", Linux z.B. "/dev/ttyUSB0"
    let serial_port = serialport::new("COM3", 1_000_000)
        .timeout(Duration::from_millis(10))
        .open()
        .expect("Seriellen Port konnte nicht geoeffnet werden");

    let io = DynamixelSerialIO::v1();

    // Aktuelle Position lesen (Motor-ID 1)
    let pos = sts3215::sync_read_present_position(&io, &mut *serial_port.try_clone().unwrap(), &[1])
        .expect("Lesen fehlgeschlagen");
    println!("Aktuelle Position: {:?}", pos);

    // Greifer schliessen (Zielposition setzen)
    sts3215::sync_write_goal_position(&io, &mut *serial_port.try_clone().unwrap(), &[1], &[2048])
        .expect("Schreiben fehlgeschlagen");
}
```

> Hinweis: Baudrate (1 000 000) und Motor-ID müssen auf die eigene Konfiguration abgestimmt werden.

#### Weitere Referenzen mit ST3215 / Waveshare

- [Feetech SCS/STS Protokoll-Dokumentation](https://www.feetechrc.com/STS3215.html)
- [Waveshare Serial Servo Driver Wiki](https://www.waveshare.com/wiki/Serial_Bus_Servo_Driver_HAT)

---

### Geplante eigene Implementierungen

#### Python (geplant)

- Einfache Steuerungsklasse speziell für diesen Greifer
- Positions- und Kraftsteuerung
- Beispiel-Skripte für typische Greifaufgaben

#### IEC 61131-3 Structured Text (geplant)

- Funktionsbaustein (FB) für die serielle Servo-Kommunikation
- Kompatibel mit gängigen SPS-Systemen (Beckhoff TwinCAT, CODESYS)
- Beispielprogramm: Greifer öffnen / schließen / Kraftbegrenzung

### Lizenz

MIT — siehe [LICENSE](../LICENSE) | Änderungshistorie: [CHANGELOG.md](../CHANGELOG.md)

[Zur Sprachauswahl](#language-selection)

---

<a id="en-start"></a>

## English

[Back to language selection](#language-selection)

### Status

> **Work in progress** — Dedicated software for this gripper is currently in planning.
> Planned implementations:
>
> - **Python** — Direct control via the Waveshare Serial Bus Servo Driver
> - **IEC 61131-3 (Structured Text)** — Integration into PLC controllers

---

### In the meantime: Reference Projects

This gripper uses the same servo (Waveshare ST3215) and the same driver (Waveshare Serial Bus Servo Driver) as several well-known open-source robotics projects.
The software from those projects is directly applicable.

#### SO-ARM100 / SO-101 Robot Arm (HuggingFace / The Robot Studio)

The SO-101 project is a complete 6-DOF robot arm that also uses the ST3215 servo and the Waveshare driver.
The accompanying Python library `lerobot` by HuggingFace enables direct servo control.

| Topic | Details |
|---|---|
| Project | SO-ARM100 / SO-101 |
| Repository | [github.com/huggingface/lerobot](https://github.com/huggingface/lerobot) |
| Hardware Guide | [github.com/TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) |
| Language | Python |
| Servo driver | Waveshare Serial Bus Servo Driver (identical hardware) |

#### Quick Start with lerobot (Python)

```bash
# Clone repository
git clone https://github.com/huggingface/lerobot.git
cd lerobot

# Install dependencies
pip install -e ".[feetech]"
```

```python
from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus

# Connect to Waveshare driver
# Adjust port: Windows e.g. "COM3", Linux e.g. "/dev/ttyUSB0"
bus = FeetechMotorsBus(
    port="COM3",
    motors={
        "gripper": (1, "sts3215"),  # adjust motor ID and model
    },
)
bus.connect()

# Read current position
pos = bus.read("Present_Position", "gripper")
print(f"Current position: {pos}")

# Close gripper (set target position)
bus.write("Goal_Position", 2048, "gripper")
```

> Note: Motor ID and COM port must be adjusted to match your setup.
> The ID can be set using the Waveshare configuration tool or the lerobot setup script.

#### Amazing Hand (Rollen Robotics) — rustypot / Rust

The Amazing Hand by Rollen Robotics is an anthropomorphic robot hand that uses the exact same Waveshare Serial Bus Servo Driver board.
Control is handled via `rustypot` — a low-level Rust library for the Feetech/Dynamixel protocol.
`rustypot` communicates directly over serial and is therefore well suited for embedded systems and real-time applications.

| Topic | Details |
|---|---|
| Project | Amazing Hand |
| Manufacturer | [Rollen Robotics](https://github.com/rollen-robotics) |
| Library | [rustypot](https://github.com/pollen-robotics/rustypot) |
| Language | Rust |
| Servo driver | Waveshare Serial Bus Servo Driver (identical hardware) |

#### Quick Start with rustypot (Rust)

```toml
# Cargo.toml
[dependencies]
rustypot = "0.11"
```

```rust
use rustypot::device::sts3215;
use rustypot::DynamixelSerialIO;
use std::time::Duration;

fn main() {
    // Open serial connection
    // Adjust port: Windows e.g. "COM3", Linux e.g. "/dev/ttyUSB0"
    let serial_port = serialport::new("COM3", 1_000_000)
        .timeout(Duration::from_millis(10))
        .open()
        .expect("Failed to open serial port");

    let io = DynamixelSerialIO::v1();

    // Read current position (motor ID 1)
    let pos = sts3215::sync_read_present_position(&io, &mut *serial_port.try_clone().unwrap(), &[1])
        .expect("Read failed");
    println!("Current position: {:?}", pos);

    // Close gripper (set target position)
    sts3215::sync_write_goal_position(&io, &mut *serial_port.try_clone().unwrap(), &[1], &[2048])
        .expect("Write failed");
}
```

> Note: Baud rate (1 000 000) and motor ID must match your specific configuration.

#### More References for ST3215 / Waveshare

- [Feetech SCS/STS Protocol Documentation](https://www.feetechrc.com/STS3215.html)
- [Waveshare Serial Servo Driver Wiki](https://www.waveshare.com/wiki/Serial_Bus_Servo_Driver_HAT)

---

### Planned Implementations

#### Python (planned)

- Lightweight control class specifically for this gripper
- Position and force control
- Example scripts for common gripping tasks

#### IEC 61131-3 Structured Text (planned)

- Function block (FB) for serial servo communication
- Compatible with common PLC systems (Beckhoff TwinCAT, CODESYS)
- Example program: open / close gripper / force limiting

### License

MIT — see [LICENSE](../LICENSE) | Change history: [CHANGELOG.md](../CHANGELOG.md)

[Back to language selection](#language-selection)
