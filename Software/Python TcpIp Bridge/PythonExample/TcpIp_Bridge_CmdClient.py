import argparse
import socket
from typing import Dict


DEFAULT_HOST = "192.168.2.150"
DEFAULT_PORT = 54600


def build_request(fields: Dict[str, str]) -> bytes:
    payload = ";".join(f"{k}={v}" for k, v in fields.items()) + "\r\n"
    return payload.encode("ascii", errors="strict")


def recv_line(sock: socket.socket) -> str:
    buf = bytearray()
    while True:
        chunk = sock.recv(1)
        if not chunk:
            raise ConnectionError("socket closed while waiting for response")
        buf.extend(chunk)
        if len(buf) >= 2 and buf[-2:] == b"\r\n":
            return buf[:-2].decode("ascii", errors="replace")


def send_cmd(sock: socket.socket, fields: Dict[str, str]) -> str:
    req = build_request(fields)
    sock.sendall(req)
    return recv_line(sock)


def run_demo(host: str, port: int, servo_id: int, position: float, speed: int) -> None:
    with socket.create_connection((host, port), timeout=5.0) as sock:
        sock.settimeout(5.0)

        requests = [
            {"Cmd": "1", "servo_id": str(servo_id), "mode": "1"},
            {"Cmd": "2", "servo_id": str(servo_id), "speed": str(speed)},
            {"Cmd": "3", "servo_id": str(servo_id), "position": str(position)},
            {"Cmd": "4", "servo_id": str(servo_id)},
            {"Cmd": "5", "ids": f"{servo_id}", "positions": "512"},
        ]

        for req in requests:
            resp = send_cmd(sock, req)
            print(f"REQ: {req}")
            print(f"RSP: {resp}")
            print("-")


def run_single(host: str, port: int, cmd: int, params: Dict[str, str]) -> None:
    with socket.create_connection((host, port), timeout=5.0) as sock:
        sock.settimeout(5.0)
        req = {"Cmd": str(cmd)}
        req.update(params)
        resp = send_cmd(sock, req)
        print(f"REQ: {req}")
        print(f"RSP: {resp}")


def parse_kv_list(values: list[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"invalid param '{item}', expected key=value")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError("empty key is not allowed")
        out[key] = value
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP test client for TcpIp_Bridge_CmdServer")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Bridge host")
    parser.add_argument("--port", default=DEFAULT_PORT, type=int, help="Bridge port")

    subparsers = parser.add_subparsers(dest="mode", required=True)

    demo = subparsers.add_parser("demo", help="Run a demo sequence for Cmd 1..5")
    demo.add_argument("--servo-id", type=int, default=1)
    demo.add_argument("--position", type=float, default=0.0)
    demo.add_argument("--speed", type=int, default=6)

    single = subparsers.add_parser("send", help="Send one command")
    single.add_argument("--cmd", required=True, type=int, help="Command id")
    single.add_argument("--param", action="append", default=[], help="Command parameter key=value")

    args = parser.parse_args()

    if args.mode == "demo":
        run_demo(args.host, args.port, args.servo_id, args.position, args.speed)
        return

    if args.mode == "send":
        params = parse_kv_list(args.param)
        run_single(args.host, args.port, args.cmd, params)
        return


if __name__ == "__main__":
    main()
