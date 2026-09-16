"""
Module 11: In-Process Echo Socket Demo
Run: python try_it_yourself.py
"""

import socket
import threading
import time


def echo_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", port))
    server.listen(1)
    conn, _ = server.accept()
    data = conn.recv(1024)
    conn.sendall(b"ECHO: " + data)
    conn.close()
    server.close()


def main():
    print("=" * 60)
    print("  MODULE 11: SOCKET NETWORKING PLAYGROUND [*]")
    print("=" * 60)
    port = 54321

    t = threading.Thread(target=echo_server, args=(port,), daemon=True)
    t.start()
    time.sleep(0.2)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))
    msg = "Hello Socket Server!"
    print(f"  [Client] Sending: '{msg}'")
    client.sendall(msg.encode("utf-8"))

    reply = client.recv(1024).decode("utf-8")
    print(f"  [Client] Received: '{reply}'")
    client.close()
    print("\n[OK] TCP client-server round-trip successful!")


if __name__ == "__main__":
    main()
