#!/usr/bin/env python3
"""Broken WebSocket Server demonstrating dead socket broadcast crashes."""

import asyncio

class BrokenChatRoom:
    def __init__(self):
        self.active_sockets = []

    def connect(self, ws):
        self.active_sockets.append(ws)

    def disconnect(self, ws):
        if ws in self.active_sockets:
            self.active_sockets.remove(ws)

    async def broadcast(self, message: str):
        # If one client disconnected, exception halts broadcast to all other healthy clients!
        for ws in self.active_sockets:
            await ws.send_text(message)

class MockWS:
    def __init__(self, name: str, is_alive: bool = True):
        self.name = name
        self.is_alive = is_alive

    async def send_text(self, text: str):
        if not self.is_alive:
            raise ConnectionResetError(f"Client {self.name} dropped")
        print(f"[{self.name}] received: {text}")

async def main():
    room = BrokenChatRoom()
    client1 = MockWS("Alice", is_alive=False)  # Dead socket
    client2 = MockWS("Bob", is_alive=True)

    room.connect(client1)
    room.connect(client2)

    try:
        await room.broadcast("Hello to room")
    except ConnectionResetError as err:
        print(f"Broadcast crashed: {err} -> Bob never received the message!")

if __name__ == "__main__":
    asyncio.run(main())
