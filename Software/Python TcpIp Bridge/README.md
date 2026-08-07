# IP_ST3215_Servo_Bridge (Python)

## Language / Sprache

- [Deutsch](#deutsch)
- [English](#english)

## Deutsch

Dieses Projekt enthaelt eine Python TCP-Command-Bridge fuer die Kommunikation mit STS/SCS-Servos ueber `rustypot`.


## Projektstruktur

- `PythonExample/TcpIp_Bridge_CmdServer.py`
	- Neuer TCP-Command-Server (CRLF, Cmd-Enum, `servo_id` immer in Antwort)
- `PythonExample/TcpIp_Bridge_CmdClient.py`
	- Test-Client fuer Demo und Einzelkommandos


## Voraussetzungen

1. Python-Umgebung aktivieren
2. `rustypot` muss in der aktiven venv installiert sein
3. Richtiger COM-Port muss verfuegbar sein (z. B. `COM6`)


## Installation

Empfohlene Einrichtung im Ordner `Python TcpIp Bridge`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` installiert das lokale Paket `rustypot-1.4.2` editierbar, damit die Python-Beispiele direkt damit arbeiten koennen.


## Was ins Git-Repo gehoert

Ins Repo gehoeren der Python-Code, `requirements.txt`, README-Dateien und bei Bedarf der angepasste `rustypot-1.4.2`-Quellcode.

Nicht ins Repo gehoeren lokale und generierte Dateien wie `.venv/`, `.venv312/`, `__pycache__/`, `.mypy_cache/` und `rustypot-1.4.2/target/`.


## Start: Command Server

Empfohlener lokaler Test (localhost):

```powershell
$env:SERVO_COM_PORT='COM6'
$env:BRIDGE_HOST='127.0.0.1'
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdServer.py"
```

Optionaler Netzwerkbetrieb:

```powershell
$env:SERVO_COM_PORT='COM6'
$env:BRIDGE_HOST='0.0.0.0'
$env:BRIDGE_PORT='54600'
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdServer.py"
```


## Start: Command Client

Hilfe anzeigen:

```powershell
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdClient.py" --help
```

Demo-Sequenz (Cmd 1..5):

```powershell
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdClient.py" --host 127.0.0.1 demo --servo-id 1 --position 0.2 --speed 6
```

Einzelkommando senden:

```powershell
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdClient.py" --host 127.0.0.1 send --cmd 4 --param servo_id=1
```


## Protokoll: Request/Response

Transport:

- TCP
- Eine Nachricht pro Zeile
- Zeilenende: `CRLF` (`\r\n`)

Request-Format:

```text
Cmd=<id>;param1=value1;param2=value2\r\n
```

Success-Response:

```text
Cmd=<id>;servo_id=<id_oder_csv>;result=OK;...\r\n
```

Error-Response:

```text
Cmd=<id>;servo_id=<id_oder_csv_oder_UNKNOWN>;result=ERR;error_code=<n>;message=<text>\r\n
```

Wichtig:

- `servo_id` ist immer in jeder Antwort enthalten (auch bei Fehlern)


## Cmd-Enum

Die aktuelle Command-Menge basiert auf dem lokalen Stub von `Scs0009PyController`:

1. `Cmd=1` -> `write_torque_enable(servo_id, mode)`
2. `Cmd=2` -> `write_goal_speed(servo_id, speed)`
3. `Cmd=3` -> `write_goal_position(servo_id, position)`
4. `Cmd=4` -> `read_present_position(servo_id)`
5. `Cmd=5` -> `sync_write_raw_goal_position(ids, positions)`


## Beispiel-Strings (direkt nutzbar)

### Cmd 1: Torque Enable

Request:

```text
Cmd=1;servo_id=1;mode=1\r\n
```

Response (OK):

```text
Cmd=1;servo_id=1;result=OK\r\n
```


### Cmd 2: Goal Speed

Request:

```text
Cmd=2;servo_id=1;speed=6\r\n
```

Response (OK):

```text
Cmd=2;servo_id=1;result=OK\r\n
```


### Cmd 3: Goal Position (radians)

Request:

```text
Cmd=3;servo_id=1;position=0.2\r\n
```

Response (OK):

```text
Cmd=3;servo_id=1;result=OK\r\n
```


### Cmd 4: Read Present Position

Request:

```text
Cmd=4;servo_id=1\r\n
```

Response (OK):

```text
Cmd=4;servo_id=1;result=OK;position=[0.07669903939428206]\r\n
```


### Cmd 5: Sync Write Raw Goal Position

Request:

```text
Cmd=5;ids=1,2;positions=512,600\r\n
```

Response (OK):

```text
Cmd=5;servo_id=1,2;result=OK;count=2\r\n
```


### Fehlerbeispiele

Unbekanntes Kommando:

```text
Cmd=99;servo_id=UNKNOWN;result=ERR;error_code=1001;message=unknown_command\r\n
```

Fehlender Parameter:

```text
Cmd=3;servo_id=UNKNOWN;result=ERR;error_code=1002;message=missing_servo_id\r\n
```

Ungueltiger Typ:

```text
Cmd=3;servo_id=UNKNOWN;result=ERR;error_code=1003;message=invalid_int_servo_id\r\n
```

Listenlaenge passt nicht:

```text
Cmd=5;servo_id=1,2;result=ERR;error_code=1004;message=ids_positions_length_mismatch\r\n
```


## Konfiguration per Environment Variables

- `SERVO_COM_PORT` (Default: `COM6`)
- `SERVO_BAUDRATE` (Default: `1000000`)
- `SERVO_TIMEOUT` (Default: `0.5`)
- `BRIDGE_HOST` (Default: `192.168.2.150`)
- `BRIDGE_PORT` (Default: `54600`)


## Troubleshooting

1. `WinError 10049` beim Start:
	 - `BRIDGE_HOST` ist auf dieser Maschine nicht gueltig.
	 - Fuer lokal testen: `127.0.0.1`
	 - Fuer Netzbetrieb: echte lokale Adapter-IP oder `0.0.0.0`

2. `ModuleNotFoundError: rustypot`:
	 - In der aktiven venv `rustypot` installieren

3. COM-Port Fehler (`Semaphore timeout`, `Datei nicht gefunden`):
	 - Richtigen COM-Port pruefen
	 - Port darf nicht von anderem Tool blockiert sein
	 - Kabel/USB-Adapter/Servo-Stromversorgung pruefen


## English

This project provides a Python TCP command bridge for STS/SCS servos using `rustypot`.


## Project structure

- `PythonExample/TcpIp_Bridge_CmdServer.py`
	- TCP command server (CRLF, command enum, `servo_id` always included in responses)
- `PythonExample/TcpIp_Bridge_CmdClient.py`
	- Test client for demo and single-command calls


## Requirements

1. Activate your Python environment
2. `rustypot` must be installed in the active venv
3. A valid COM port must be available (for example `COM6`)


## Installation

Recommended setup inside the `Python TcpIp Bridge` folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The `requirements.txt` installs the local `rustypot-1.4.2` package in editable mode so the Python examples can use it directly.


## What belongs in Git

Commit the Python source, `requirements.txt`, README files, and the `rustypot-1.4.2` source only if you actually want to vendor or modify it in this repository.

Do not commit local or generated files such as `.venv/`, `.venv312/`, `__pycache__/`, `.mypy_cache/`, or `rustypot-1.4.2/target/`.


## Start: Command Server

Recommended local test (localhost):

```powershell
$env:SERVO_COM_PORT='COM6'
$env:BRIDGE_HOST='127.0.0.1'
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdServer.py"
```

Optional network mode:

```powershell
$env:SERVO_COM_PORT='COM6'
$env:BRIDGE_HOST='0.0.0.0'
$env:BRIDGE_PORT='54600'
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdServer.py"
```


## Start: Command Client

Show help:

```powershell
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdClient.py" --help
```

Run demo sequence (Cmd 1..5):

```powershell
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdClient.py" --host 127.0.0.1 demo --servo-id 1 --position 0.2 --speed 6
```

Send a single command:

```powershell
& ".\.venv312\Scripts\python.exe" ".\PythonExample\TcpIp_Bridge_CmdClient.py" --host 127.0.0.1 send --cmd 4 --param servo_id=1
```


## Protocol: Request/Response

Transport:

- TCP
- One message per line
- Line ending: `CRLF` (`\r\n`)

Request format:

```text
Cmd=<id>;param1=value1;param2=value2\r\n
```

Success response:

```text
Cmd=<id>;servo_id=<id_or_csv>;result=OK;...\r\n
```

Error response:

```text
Cmd=<id>;servo_id=<id_or_csv_or_UNKNOWN>;result=ERR;error_code=<n>;message=<text>\r\n
```

Important:

- `servo_id` is always present in every response (including errors)


## Command enum

The current command set is based on the local `Scs0009PyController` stub:

1. `Cmd=1` -> `write_torque_enable(servo_id, mode)`
2. `Cmd=2` -> `write_goal_speed(servo_id, speed)`
3. `Cmd=3` -> `write_goal_position(servo_id, position)`
4. `Cmd=4` -> `read_present_position(servo_id)`
5. `Cmd=5` -> `sync_write_raw_goal_position(ids, positions)`


## Example strings

### Cmd 1: Torque Enable

Request:

```text
Cmd=1;servo_id=1;mode=1\r\n
```

Response (OK):

```text
Cmd=1;servo_id=1;result=OK\r\n
```


### Cmd 2: Goal Speed

Request:

```text
Cmd=2;servo_id=1;speed=6\r\n
```

Response (OK):

```text
Cmd=2;servo_id=1;result=OK\r\n
```


### Cmd 3: Goal Position (radians)

Request:

```text
Cmd=3;servo_id=1;position=0.2\r\n
```

Response (OK):

```text
Cmd=3;servo_id=1;result=OK\r\n
```


### Cmd 4: Read Present Position

Request:

```text
Cmd=4;servo_id=1\r\n
```

Response (OK):

```text
Cmd=4;servo_id=1;result=OK;position=[0.07669903939428206]\r\n
```


### Cmd 5: Sync Write Raw Goal Position

Request:

```text
Cmd=5;ids=1,2;positions=512,600\r\n
```

Response (OK):

```text
Cmd=5;servo_id=1,2;result=OK;count=2\r\n
```


### Error examples

Unknown command:

```text
Cmd=99;servo_id=UNKNOWN;result=ERR;error_code=1001;message=unknown_command\r\n
```

Missing parameter:

```text
Cmd=3;servo_id=UNKNOWN;result=ERR;error_code=1002;message=missing_servo_id\r\n
```

Invalid type:

```text
Cmd=3;servo_id=UNKNOWN;result=ERR;error_code=1003;message=invalid_int_servo_id\r\n
```

List length mismatch:

```text
Cmd=5;servo_id=1,2;result=ERR;error_code=1004;message=ids_positions_length_mismatch\r\n
```


## Configuration via environment variables

- `SERVO_COM_PORT` (default: `COM6`)
- `SERVO_BAUDRATE` (default: `1000000`)
- `SERVO_TIMEOUT` (default: `0.5`)
- `BRIDGE_HOST` (default: `192.168.2.150`)
- `BRIDGE_PORT` (default: `54600`)


## Troubleshooting

1. `WinError 10049` at startup:
	 - `BRIDGE_HOST` is invalid on this machine.
	 - For local tests use: `127.0.0.1`
	 - For network mode use: a real local adapter IP or `0.0.0.0`

2. `ModuleNotFoundError: rustypot`:
	 - Install `rustypot` in the active venv

3. COM port issues (`Semaphore timeout`, `File not found`):
	 - Verify correct COM port
	 - Ensure port is not locked by another tool
	 - Check cable/USB adapter/servo power

