# ESP32 TcpIp_Server

<a id="language-selection"></a>

## Sprache / Language

- Deutsch: [Zur deutschen Version](#de-start)
- English: [Jump to English version](#en-start)

---

<a id="de-start"></a>

## Deutsch

[Zur Sprachauswahl](#language-selection)

### Überblick

Der Ordner `TcpIp_Server` enthält die ESP32-Firmware für den Servo-Treiber. Die Firmware bietet:

- WLAN im AP- oder STA-Modus
- Weboberfläche auf Port 80
- TCP-Textserver auf Port 5000
- Servo-Kommunikation über `Serial1` mit 1 000 000 Baud
- OLED-Statusanzeige und RGB-Status-LEDs

### Benötigte Versionen

Diese Kombination ist in diesem Projekt funktionierend getestet und sollte exakt so installiert werden:

| Paket | Version |
|---|---|
| `esp32` von Espressif Systems | `3.3.10` |
| `Adafruit BusIO` | `1.17.4` |
| `Adafruit GFX Library` | `1.12.6` |
| `Adafruit NeoPixel` | `1.15.5` |
| `Adafruit SSD1306` | `2.5.17` |
| `SCServo` | `1.0.2` |

Hinweise:

- `WiFi`, `WebServer`, `esp_now`, `Wire` und `Preferences` sind Teil des ESP32-Core-Pakets.
- Das Paket `Arduino ESP32 Boards` von Arduino ist für dieses Projekt nicht erforderlich, da die Firmware auf dem ESP32-Core von Espressif Systems basiert.
- Bitte keine neueren oder abweichenden Versionen der genannten Pakete verwenden, wenn die stabile Kombination aus diesem Projekt reproduziert werden soll.

### Arduino-Einstellungen

- Board: ein ESP32-Board mit WLAN-Unterstützung, für WaveShare ESP32 muss das `ESP32 Dev Module` ausgewählt sein.
- Upload über den COM-Port des angeschlossenen ESP32-Boards ( COM Port kann im Windows Gerätemanager ermittelt werden )

### Netzwerk-Ports

- HTTP/Weboberfläche: Port `80`
- TCP-Textserver: Port `5000`

Im AP-Modus ist der Standard-Access-Point:

- SSID: `ESP32_DEV`
- Passwort: `12345678`

Im STA-Modus verbindet sich der ESP32 mit dem in `PreferencesConfig.h` eingetragenen WLAN.

### TCP/IP-Server: Befehle

Der TCP-Server erwartet zeilenbasierte Texteingaben. Jede Zeile muss mit einem Zeilenumbruch abgeschlossen werden.

| Befehl | Wirkung | Beispiel |
|---|---|---|
| `PING` | Verbindungstest | `PING` |
| `GET STS` | Status des aktuell aktiven Servos | `GET STS` |
| `SEARCH` | Servos scannen | `SEARCH` |
| `CMD <nummer>` | interne Steuerfunktion ausführen | `CMD 1` |
| `SET POS <id> <pos> <speed>` | Servo direkt anfahren | `SET POS 1 511 300` |

Rückmeldungen:

- `PONG`
- `OK SEARCH`
- `OK CMD`
- `OK SET POS`
- `ERR unknown command`
- `ERR timeout`

### CMD-Befehle

`CMD` verwendet dieselben internen Aktionen wie die Weboberfläche. Die wichtigsten Zuordnungen sind:

| CMD | Aktion |
|---|---|
| `1` | Aktiven Servo auf Mittelstellung fahren |
| `2` | Stop / Hold |
| `3` | Torque aus |
| `4` | Torque an |
| `5` | Position + / öffnen |
| `6` | Position - / schließen |
| `7` | Geschwindigkeit erhöhen |
| `8` | Geschwindigkeit verringern |
| `9` | Ziel-ID erhöhen |
| `10` | Ziel-ID verringern |
| `11` | Mittelstellung kalibrieren |
| `12` | Servo-Modus setzen |
| `13` | Motor-Modus setzen |
| `14` | Serial Forwarding starten |
| `15` | Serial Forwarding stoppen |
| `16` | Neue ID schreiben |
| `17` | Normaler Modus |
| `18` | Leader-Modus |
| `19` | Follower-Modus |
| `20` | Rainbow ein |
| `21` | Rainbow aus |

### Beispiel: TCP-Server mit Python testen

```python
import socket

HOST = "192.168.4.1"  # im AP-Modus der Default-Wert
PORT = 5000

with socket.create_connection((HOST, PORT), timeout=5) as sock:
    def send(cmd: str) -> None:
        sock.sendall((cmd + "\n").encode("utf-8"))
        print(sock.recv(1024).decode("utf-8", errors="replace").strip())

    send("PING")
    send("GET STS")
    send("SEARCH")
    send("CMD 1")
    send("SET POS 1 511 300")
```

### Beispiel: Nutzung über die Weboberfläche

1. ESP32 einschalten und über Serial Monitor oder OLED die IP-Adresse ablesen.
2. Im Browser `http://<IP-Adresse>/` öffnen.
3. Über die Buttons Servos suchen, auswählen und bewegen.
4. Für direkte Statusabfragen werden die Endpunkte `readID` und `readSTS` verwendet.

### Praktische Hinweise

- Der TCP-Server arbeitet mit einer einzelnen Verbindung und trennt sie nach 30 Sekunden Inaktivität.
- Die Firmware gibt die aktuelle IP-Adresse im Serial Monitor und auf dem OLED aus.
- Die Weboberfläche und der TCP-Server laufen parallel.

---

<a id="en-start"></a>

## English

[Back to language selection](#language-selection)

### Overview

The `TcpIp_Server` folder contains the ESP32 firmware for the servo driver. It provides:

- Wi-Fi in AP or STA mode
- Web UI on port 80
- TCP text server on port 5000
- Servo communication over `Serial1` at 1,000,000 baud
- OLED status output and RGB status LEDs

### Required Versions

This project was tested and works with the exact package combination below:

| Package | Version |
|---|---|
| `esp32` by Espressif Systems | `3.3.10` |
| `Adafruit BusIO` | `1.17.4` |
| `Adafruit GFX Library` | `1.12.6` |
| `Adafruit NeoPixel` | `1.15.5` |
| `Adafruit SSD1306` | `2.5.17` |
| `SCServo` | `1.0.2` |

Notes:

- `WiFi`, `WebServer`, `esp_now`, `Wire`, and `Preferences` are part of the ESP32 core package.
- The `Arduino ESP32 Boards` package by Arduino is not required for this project because the firmware targets the Espressif Systems ESP32 core.
- Do not mix in newer or different versions of these packages if you want to reproduce the working setup from this project.

### Arduino settings

- Board: an ESP32 board with Wi-Fi support, for WaveShare ESP32 the `ESP32 Dev Module` must be selected
- Upload via the COM port of the connected ESP32 board 
  (COM Port can be detected via the Windows device manager)

### Network ports

- HTTP web UI: port `80`
- TCP text server: port `5000`

In AP mode, the default access point is:

- SSID: `ESP32_DEV`
- Password: `12345678`

### TCP/IP server commands

The TCP server uses line-based text commands. End each command with a newline.

| Command | Effect | Example |
|---|---|---|
| `PING` | connection test | `PING` |
| `GET STS` | status of the active servo | `GET STS` |
| `SEARCH` | scan for servos | `SEARCH` |
| `CMD <number>` | run an internal control action | `CMD 1` |
| `SET POS <id> <pos> <speed>` | move a servo directly | `SET POS 1 511 300` |

Typical replies:

- `PONG`
- `OK SEARCH`
- `OK CMD`
- `OK SET POS`
- `ERR unknown command`
- `ERR timeout`

### CMD mapping

`CMD` uses the same internal actions as the web UI.

| CMD | Action |
|---|---|
| `1` | Move active servo to center |
| `2` | Stop / hold |
| `3` | Torque off |
| `4` | Torque on |
| `5` | Position + / open |
| `6` | Position - / close |
| `7` | Increase speed |
| `8` | Decrease speed |
| `9` | Increase target ID |
| `10` | Decrease target ID |
| `11` | Calibrate center |
| `12` | Set servo mode |
| `13` | Set motor mode |
| `14` | Start serial forwarding |
| `15` | Stop serial forwarding |
| `16` | Write new ID |
| `17` | Normal mode |
| `18` | Leader mode |
| `19` | Follower mode |
| `20` | Rainbow on |
| `21` | Rainbow off |

### Python example

```python
import socket

HOST = "192.168.4.1"  # default in AP mode
PORT = 5000

with socket.create_connection((HOST, PORT), timeout=5) as sock:
    def send(cmd: str) -> None:
        sock.sendall((cmd + "\n").encode("utf-8"))
        print(sock.recv(1024).decode("utf-8", errors="replace").strip())

    send("PING")
    send("GET STS")
    send("SEARCH")
    send("CMD 1")
    send("SET POS 1 511 300")
```

### Web UI usage

1. Power on the ESP32 and read the IP address from the Serial Monitor or OLED.
2. Open `http://<IP address>/` in a browser.
3. Use the buttons to search, select, and move servos.
4. The `readID` and `readSTS` endpoints provide live information.

### Practical notes

- The TCP server uses a single client connection and disconnects after 30 seconds of inactivity.
- The firmware prints the current IP address to the Serial Monitor and OLED.
- The web UI and TCP server run in parallel.