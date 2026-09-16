#!/usr/bin/env python3
"""Module 10: Low-Level TCP Socket Programming Demonstration.

This script demonstrates creating a TCP socket server and connecting
a client to exchange binary UTF-8 messages over localhost.
"""

from __future__ import annotations

import socket
import threading
import time


def run_echo_server(port: int) -> None:
    """Runs a single-client TCP echo server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", port))
        s.listen(1)

        conn, _addr = s.accept()
        with conn:
            data = conn.recv(1024)
            if data:
                response = b"ECHO: " + data
                conn.sendall(response)


def main() -> None:
    print("=" * 60)
    print("  Low-Level TCP Socket Client-Server Communication")
    print("=" * 60)

    port = 9876
    server_thread = threading.Thread(target=run_echo_server, args=(port,), daemon=True)
    server_thread.start()
    time.sleep(0.05)  # Allow server to bind

    # Client socket connects and sends data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(("127.0.0.1", port))
        message = "Hello Network Sockets!"
        print(f"Client sending: '{message}'")
        client.sendall(message.encode("utf-8"))

        received_bytes = client.recv(1024)
        print(f"Client received from server: '{received_bytes.decode('utf-8')}'")


if __name__ == "__main__":
    main()
