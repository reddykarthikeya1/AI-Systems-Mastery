"""Unit tests for the Async TCP Chat Server."""

from __future__ import annotations

import asyncio

import pytest
from chat_server import AsyncChatServer


@pytest.mark.asyncio
async def test_chat_server_connection_and_broadcast() -> None:
    """Test two clients connecting, exchanging messages, and receiving broadcasts."""
    server = AsyncChatServer(port=8901)
    await server.start()

    # Connect Client 1 (Alice)
    reader1, writer1 = await asyncio.open_connection("127.0.0.1", 8901)
    welcome1 = await reader1.readline()
    assert b"Welcome" in welcome1

    # Connect Client 2 (Bob)
    reader2, writer2 = await asyncio.open_connection("127.0.0.1", 8901)
    welcome2 = await reader2.readline()
    assert b"Welcome" in welcome2

    # Client 1 should receive notification that Client 2 joined
    join_notification = await reader1.readline()
    assert b"joined the chat room" in join_notification

    # Client 1 sends a chat message
    writer1.write(b"Hello everyone!\n")
    await writer1.drain()

    # Client 2 should receive the broadcasted message
    broadcast_msg = await reader2.readline()
    assert b"Hello everyone!" in broadcast_msg

    # Cleanup clients and server
    writer1.close()
    await writer1.wait_closed()
    writer2.close()
    await writer2.wait_closed()
    await server.stop()


@pytest.mark.asyncio
async def test_client_quit_command() -> None:
    """Test sending /quit disconnects the client."""
    server = AsyncChatServer(port=8902)
    await server.start()

    reader, writer = await asyncio.open_connection("127.0.0.1", 8902)
    await reader.readline()  # welcome

    writer.write(b"/quit\n")
    await writer.drain()

    # Server should close connection
    data = await reader.read()
    assert data == b""

    writer.close()
    await writer.wait_closed()
    await server.stop()


@pytest.mark.asyncio
async def test_server_custom_host_and_port() -> None:
    """Test configuring custom host and port."""
    server = AsyncChatServer(host="127.0.0.1", port=8903)
    assert server.host == "127.0.0.1"
    assert server.port == 8903


@pytest.mark.asyncio
async def test_server_stop_when_not_started() -> None:
    """Test calling stop on unstarted server is safe and does not raise."""
    server = AsyncChatServer(port=8904)
    await server.stop()


@pytest.mark.asyncio
async def test_broadcast_without_clients() -> None:
    """Test broadcast with zero active clients does not raise error."""
    server = AsyncChatServer(port=8905)
    await server.broadcast("Hello to nobody")


@pytest.mark.asyncio
async def test_client_count_in_welcome_message() -> None:
    """Test welcome message reflects correct active user count."""
    server = AsyncChatServer(port=8906)
    await server.start()

    reader1, writer1 = await asyncio.open_connection("127.0.0.1", 8906)
    welcome1 = await reader1.readline()
    assert b"1 active users" in welcome1

    reader2, writer2 = await asyncio.open_connection("127.0.0.1", 8906)
    welcome2 = await reader2.readline()
    assert b"2 active users" in welcome2

    writer1.close()
    await writer1.wait_closed()
    writer2.close()
    await writer2.wait_closed()
    await server.stop()


@pytest.mark.asyncio
async def test_client_disconnect_leaves_room_notification() -> None:
    """Test client disconnect broadcasts departure message to remaining clients."""
    server = AsyncChatServer(port=8907)
    await server.start()

    reader1, writer1 = await asyncio.open_connection("127.0.0.1", 8907)
    await reader1.readline()  # welcome1

    reader2, writer2 = await asyncio.open_connection("127.0.0.1", 8907)
    await reader2.readline()  # welcome2
    await reader1.readline()  # client 2 joined

    # Disconnect client 2
    writer2.close()
    await writer2.wait_closed()

    # Client 1 should receive left notification
    left_msg = await reader1.readline()
    assert b"left the chat room" in left_msg

    writer1.close()
    await writer1.wait_closed()
    await server.stop()


@pytest.mark.asyncio
async def test_empty_message_ignored() -> None:
    """Test sending empty whitespace lines is ignored and not broadcasted."""
    server = AsyncChatServer(port=8908)
    await server.start()

    reader1, writer1 = await asyncio.open_connection("127.0.0.1", 8908)
    await reader1.readline()  # welcome

    reader2, writer2 = await asyncio.open_connection("127.0.0.1", 8908)
    await reader2.readline()  # welcome
    await reader1.readline()  # joined

    writer1.write(b"   \n")
    await writer1.drain()

    # Send a real message to verify stream is clear
    writer1.write(b"Real message\n")
    await writer1.drain()

    msg = await reader2.readline()
    assert b"Real message" in msg

    writer1.close()
    await writer1.wait_closed()
    writer2.close()
    await writer2.wait_closed()
    await server.stop()


@pytest.mark.asyncio
async def test_multiple_messages_roundtrip() -> None:
    """Test sequential messages between connected clients."""
    server = AsyncChatServer(port=8909)
    await server.start()

    reader1, writer1 = await asyncio.open_connection("127.0.0.1", 8909)
    await reader1.readline()
    reader2, writer2 = await asyncio.open_connection("127.0.0.1", 8909)
    await reader2.readline()
    await reader1.readline()

    for i in range(3):
        writer1.write(f"Msg {i}\n".encode())
        await writer1.drain()
        rec = await reader2.readline()
        assert f"Msg {i}".encode() in rec

    writer1.close()
    await writer1.wait_closed()
    writer2.close()
    await writer2.wait_closed()
    await server.stop()


@pytest.mark.asyncio
async def test_server_clients_registry_cleared() -> None:
    """Test server clients dictionary empties as clients disconnect."""
    server = AsyncChatServer(port=8910)
    await server.start()

    reader, writer = await asyncio.open_connection("127.0.0.1", 8910)
    await reader.readline()
    assert len(server.clients) == 1

    writer.close()
    await writer.wait_closed()
    # Give event loop a cycle to process cleanup
    await asyncio.sleep(0.05)
    assert len(server.clients) == 0

    await server.stop()
