#!/usr/bin/env python3
"""Multi-Client Asynchronous TCP Chat Server.

Module 10 (Networking & Sockets) Turnkey Project Implementation.
Demonstrates asyncio streams (asyncio.start_server, StreamReader, StreamWriter).
"""

from __future__ import annotations

import asyncio


class AsyncChatServer:
    """Multi-client broadcast TCP chat server."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8888) -> None:
        self.host = host
        self.port = port
        self.clients: dict[str, asyncio.StreamWriter] = {}
        self.server: asyncio.Server | None = None

    async def broadcast(self, message: str, sender_id: str | None = None) -> None:
        """Sends a message to all connected clients except optionally the sender."""
        payload = (message + "\n").encode("utf-8")
        for client_id, writer in list(self.clients.items()):
            if client_id != sender_id:
                try:
                    writer.write(payload)
                    await writer.drain()
                except (ConnectionError, BrokenPipeError, ConnectionResetError):
                    self.clients.pop(client_id, None)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handles lifecycle and message loop for a single connected client."""
        addr = writer.get_extra_info("peername")
        client_id = f"User-{addr[1]}" if addr else "Anonymous"
        self.clients[client_id] = writer

        welcome_msg = f"[SYSTEM] Welcome {client_id}! There are {len(self.clients)} active users."
        try:
            writer.write((welcome_msg + "\n").encode("utf-8"))
            await writer.drain()
            await self.broadcast(f"[SYSTEM] {client_id} has joined the chat room.", sender_id=client_id)

            while True:
                line_bytes = await reader.readline()
                if not line_bytes:  # Client disconnected
                    break

                text = line_bytes.decode("utf-8").strip()
                if text.lower() == "/quit":
                    break

                if text:
                    await self.broadcast(f"[{client_id}] {text}", sender_id=client_id)
        except (ConnectionResetError, asyncio.CancelledError):
            pass
        finally:
            self.clients.pop(client_id, None)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            await self.broadcast(f"[SYSTEM] {client_id} has left the chat room.")

    async def start(self) -> None:
        """Starts listening for incoming connections."""
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Chat server running on {self.host}:{self.port}...")

    async def stop(self) -> None:
        """Closes all client connections and shuts down the server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        for writer in list(self.clients.values()):
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        self.clients.clear()


async def main() -> None:
    server = AsyncChatServer()
    await server.start()
    if server.server:
        async with server.server:
            await server.server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
