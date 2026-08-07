import enum
import os
import signal
import socket
import time
from datetime import datetime
from typing import Dict, Optional, Tuple

from rustypot import Scs0009PyController


HOST = os.getenv("BRIDGE_HOST", "127.0.0.1")
PORT = int(os.getenv("BRIDGE_PORT", "54600"))
SERIAL_PORT = os.getenv("SERVO_COM_PORT", "COM6")
BAUDRATE = int(os.getenv("SERVO_BAUDRATE", "1000000"))
TIMEOUT = float(os.getenv("SERVO_TIMEOUT", "0.5"))
CONTROLLER_RETRY_DELAY = float(os.getenv("SERVO_RETRY_DELAY", "1.0"))
ACCEPT_TIMEOUT = float(os.getenv("BRIDGE_ACCEPT_TIMEOUT", "0.5"))
SOCKET_IO_TIMEOUT = float(os.getenv("BRIDGE_SOCKET_TIMEOUT", "0.5"))

MAX_LINE_BYTES = 2048
STOP_REQUESTED = False


def ts() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


class CommandId(enum.IntEnum):
    WRITE_TORQUE_ENABLE = 1
    WRITE_GOAL_SPEED = 2
    WRITE_GOAL_POSITION = 3
    READ_PRESENT_POSITION = 4
    SYNC_WRITE_RAW_GOAL_POSITION = 5


class ProtocolError(Exception):
    def __init__(self, code: int, message: str, cmd: str = "UNKNOWN", servo_id: str = "UNKNOWN"):
        super().__init__(message)
        self.code = code
        self.message = message
        self.cmd = cmd
        self.servo_id = servo_id


def parse_key_values(line: str) -> Dict[str, str]:
    parts = [p for p in line.split(";") if p]
    if not parts:
        raise ProtocolError(1002, "empty_request")

    fields: Dict[str, str] = {}
    for part in parts:
        if "=" not in part:
            raise ProtocolError(1002, "invalid_pair")
        key, value = part.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ProtocolError(1002, "empty_key")
        fields[key] = value
    return fields


def parse_int(value: str, field: str, cmd: str, servo_id: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ProtocolError(1003, f"invalid_int_{field}", cmd=cmd, servo_id=servo_id) from exc


def parse_float(value: str, field: str, cmd: str, servo_id: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ProtocolError(1003, f"invalid_float_{field}", cmd=cmd, servo_id=servo_id) from exc


def parse_csv_ints(value: str, field: str, cmd: str, servo_id: str) -> list[int]:
    if value == "":
        raise ProtocolError(1003, f"invalid_csv_{field}", cmd=cmd, servo_id=servo_id)

    items = [item.strip() for item in value.split(",") if item.strip()]
    if not items:
        raise ProtocolError(1003, f"invalid_csv_{field}", cmd=cmd, servo_id=servo_id)

    out: list[int] = []
    for item in items:
        out.append(parse_int(item, field, cmd, servo_id))
    return out


def get_servo_id_for_error(fields: Dict[str, str]) -> str:
    if "servo_id" in fields:
        try:
            int(fields["servo_id"])
            return fields["servo_id"]
        except ValueError:
            return "UNKNOWN"
    if "ids" in fields:
        raw = fields["ids"].strip()
        return raw if raw else "UNKNOWN"
    return "UNKNOWN"


def parse_request(line: str) -> Tuple[CommandId, Dict[str, str], str, str]:
    fields = parse_key_values(line)
    cmd_raw = fields.get("Cmd", "UNKNOWN")
    servo_id_for_error = get_servo_id_for_error(fields)

    if "Cmd" not in fields:
        raise ProtocolError(1002, "missing_Cmd", cmd=cmd_raw, servo_id=servo_id_for_error)

    cmd_value = parse_int(fields["Cmd"], "Cmd", cmd_raw, servo_id_for_error)
    try:
        cmd = CommandId(cmd_value)
    except ValueError as exc:
        raise ProtocolError(1001, "unknown_command", cmd=str(cmd_value), servo_id=servo_id_for_error) from exc

    return cmd, fields, str(cmd_value), servo_id_for_error


def ensure_fields(fields: Dict[str, str], required: list[str], cmd: str, servo_id: str) -> None:
    for key in required:
        if key not in fields:
            raise ProtocolError(1002, f"missing_{key}", cmd=cmd, servo_id=servo_id)


def sanitize_value(value: str) -> str:
    # Keep protocol line-safe: no separators and no embedded line breaks.
    return value.replace(";", ",").replace("\r", " ").replace("\n", " ")


def format_response(parts: Dict[str, str]) -> bytes:
    order = ["Cmd", "servo_id", "result", "error_code", "message", "position", "count"]
    out: list[str] = []

    for key in order:
        if key in parts:
            out.append(f"{key}={sanitize_value(parts[key])}")

    for key, value in parts.items():
        if key not in order:
            out.append(f"{key}={sanitize_value(value)}")

    return (";".join(out) + "\r\n").encode("ascii", errors="replace")


def recv_lines(conn: socket.socket):
    buffer = bytearray()
    while True:
        if STOP_REQUESTED:
            return

        try:
            chunk = conn.recv(1024)
        except socket.timeout:
            continue

        if not chunk:
            return
        buffer.extend(chunk)

        if len(buffer) > MAX_LINE_BYTES and b"\n" not in buffer:
            raise ProtocolError(1005, "line_too_long")

        while True:
            idx = buffer.find(b"\n")
            if idx < 0:
                break

            line = bytes(buffer[:idx + 1])
            del buffer[:idx + 1]

            if not line.endswith(b"\r\n"):
                raise ProtocolError(1002, "missing_crlf")

            payload = line[:-2].decode("ascii", errors="strict")
            if payload:
                yield payload


def handle_command(c: Scs0009PyController, cmd: CommandId, fields: Dict[str, str], cmd_text: str) -> Dict[str, str]:
    servo_id_for_error = get_servo_id_for_error(fields)

    match cmd:
        case CommandId.WRITE_TORQUE_ENABLE:
            ensure_fields(fields, ["servo_id", "mode"], cmd_text, servo_id_for_error)
            servo_id = parse_int(fields["servo_id"], "servo_id", cmd_text, servo_id_for_error)
            mode = parse_int(fields["mode"], "mode", cmd_text, str(servo_id))
            c.write_torque_enable(servo_id, mode)
            return {"Cmd": cmd_text, "servo_id": str(servo_id), "result": "OK"}

        case CommandId.WRITE_GOAL_SPEED:
            ensure_fields(fields, ["servo_id", "speed"], cmd_text, servo_id_for_error)
            servo_id = parse_int(fields["servo_id"], "servo_id", cmd_text, servo_id_for_error)
            speed = parse_int(fields["speed"], "speed", cmd_text, str(servo_id))
            c.write_goal_speed(servo_id, speed)
            return {"Cmd": cmd_text, "servo_id": str(servo_id), "result": "OK"}

        case CommandId.WRITE_GOAL_POSITION:
            ensure_fields(fields, ["servo_id", "position"], cmd_text, servo_id_for_error)
            servo_id = parse_int(fields["servo_id"], "servo_id", cmd_text, servo_id_for_error)
            position = parse_float(fields["position"], "position", cmd_text, str(servo_id))
            c.write_goal_position(servo_id, position)
            return {"Cmd": cmd_text, "servo_id": str(servo_id), "result": "OK"}

        case CommandId.READ_PRESENT_POSITION:
            ensure_fields(fields, ["servo_id"], cmd_text, servo_id_for_error)
            servo_id = parse_int(fields["servo_id"], "servo_id", cmd_text, servo_id_for_error)
            position = c.read_present_position(servo_id)
            return {
                "Cmd": cmd_text,
                "servo_id": str(servo_id),
                "position": str(position),
                "result": "OK",
            }

        case CommandId.SYNC_WRITE_RAW_GOAL_POSITION:
            ensure_fields(fields, ["ids", "positions"], cmd_text, servo_id_for_error)
            ids = parse_csv_ints(fields["ids"], "ids", cmd_text, servo_id_for_error)
            positions = parse_csv_ints(fields["positions"], "positions", cmd_text, ",".join(str(i) for i in ids))
            if len(ids) != len(positions):
                raise ProtocolError(1004, "ids_positions_length_mismatch", cmd=cmd_text, servo_id=",".join(str(i) for i in ids))

            c.sync_write_raw_goal_position(ids, positions)
            return {
                "Cmd": cmd_text,
                "servo_id": ",".join(str(i) for i in ids),
                "count": str(len(ids)),
                "result": "OK",
            }

    raise ProtocolError(1001, "unknown_command", cmd=cmd_text, servo_id=servo_id_for_error)


def create_controller() -> Scs0009PyController:
    return Scs0009PyController(
        serial_port=SERIAL_PORT,
        baudrate=BAUDRATE,
        timeout=TIMEOUT,
    )


def _handle_shutdown_signal(signum, _frame) -> None:
    global STOP_REQUESTED
    STOP_REQUESTED = True
    print(f"Shutdown signal received ({signum}). Stopping server...")


def main() -> None:
    global STOP_REQUESTED
    controller: Optional[Scs0009PyController] = None
    next_controller_retry_ts = 0.0

    signal.signal(signal.SIGINT, _handle_shutdown_signal)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _handle_shutdown_signal)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        server.settimeout(ACCEPT_TIMEOUT)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[{ts()}] Command server listening on {HOST}:{PORT}")

        while not STOP_REQUESTED:
            try:
                try:
                    conn, addr = server.accept()
                except socket.timeout:
                    continue
                print(f"[{ts()}] Client connected: {addr}")

                with conn:
                    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    conn.settimeout(SOCKET_IO_TIMEOUT)
                    try:
                        for line in recv_lines(conn):
                            print(f"[{ts()}] RX: {line}")
                            cmd_text = "UNKNOWN"
                            servo_id = "UNKNOWN"
                            try:
                                cmd, fields, cmd_text, servo_id = parse_request(line)

                                # Lazily connect to the servo controller. If COM is locked,
                                # keep server alive and return a protocol error instead of crashing.
                                now = time.time()
                                if controller is None and now >= next_controller_retry_ts:
                                    try:
                                        controller = create_controller()
                                        print(f"[{ts()}] Servo controller connected on {SERIAL_PORT}")
                                    except Exception as exc:
                                        next_controller_retry_ts = now + CONTROLLER_RETRY_DELAY
                                        raise ProtocolError(
                                            2002,
                                            f"controller_unavailable:{exc}",
                                            cmd=cmd_text,
                                            servo_id=servo_id,
                                        ) from exc

                                if controller is None:
                                    raise ProtocolError(
                                        2002,
                                        "controller_unavailable:retry_later",
                                        cmd=cmd_text,
                                        servo_id=servo_id,
                                    )

                                try:
                                    response = handle_command(controller, cmd, fields, cmd_text)
                                except Exception as exc:
                                    controller = None
                                    next_controller_retry_ts = time.time() + CONTROLLER_RETRY_DELAY
                                    raise ProtocolError(
                                        2001,
                                        f"controller_runtime_error:{exc}",
                                        cmd=cmd_text,
                                        servo_id=servo_id,
                                    ) from exc

                            except ProtocolError as exc:
                                response = {
                                    "Cmd": exc.cmd if exc.cmd else cmd_text,
                                    "servo_id": exc.servo_id if exc.servo_id else servo_id,
                                    "result": "ERR",
                                    "error_code": str(exc.code),
                                    "message": exc.message,
                                }
                            except Exception as exc:  # parser/runtime fallback
                                response = {
                                    "Cmd": cmd_text,
                                    "servo_id": servo_id,
                                    "result": "ERR",
                                    "error_code": "2001",
                                    "message": str(exc),
                                }

                            try:
                                raw_response = format_response(response)
                                print(f"[{ts()}] TX: {raw_response.decode('ascii', errors='replace').rstrip()}")
                                conn.sendall(raw_response)
                            except OSError as exc:
                                print(f"Response send failed: {exc}")
                                break
                    except Exception as exc:
                        print(f"Client session ended with exception: {exc}")
                    finally:
                        print(f"[{ts()}] Client disconnected. Waiting for next connection...")

            except KeyboardInterrupt:
                STOP_REQUESTED = True
            except Exception as exc:
                print(f"Accept loop recovered from exception: {exc}")
                time.sleep(0.2)

    print("Server shutdown complete.")


if __name__ == "__main__":
    main()
