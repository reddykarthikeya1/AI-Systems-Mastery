#!/usr/bin/env python3
"""Broken TCP Chat Server demonstrating socket framing, reuseaddr, and buffer traps."""

import socket
import time

def create_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 9999))
    server.listen(5)
    return server

def receive_chat_message(sock: socket.socket) -> str:
    # TCP is a streaming protocol; messages can be fragmented or coalesced.
    data = sock.recv(1024)
    return data.decode("utf-8")

def send_chat_message(sock: socket.socket, msg: str):
    sock.sendall(msg.encode("utf-8"))

if __name__ == "__main__":
    print("Socket framing demo initialized.")
    try:
        s1 = create_server_socket()
        print("Server socket bound to port 9999.")
        s1.close()
        # Immediate re-bind to demonstrate TIME_WAIT
        s2 = create_server_socket()
    except OSError as err:
        print(f"Socket bind failed: {err}")
