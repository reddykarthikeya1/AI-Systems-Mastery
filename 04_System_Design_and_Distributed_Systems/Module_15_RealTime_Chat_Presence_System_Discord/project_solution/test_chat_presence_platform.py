"""Unit tests for Real-Time Distributed Chat & Presence Platform."""

from __future__ import annotations

import time

from chat_presence_platform import (
    DistributedChatPlatform,
    UserStatus,
    WebSocketGatewayNode,
)


def test_cross_gateway_message_routing() -> None:
    platform = DistributedChatPlatform()
    gw1 = WebSocketGatewayNode("gateway-us-east")
    gw2 = WebSocketGatewayNode("gateway-eu-west")

    platform.register_gateway(gw1)
    platform.register_gateway(gw2)

    # Alice connects to US gateway, Bob connects to EU gateway
    platform.user_connect("alice", "gateway-us-east")
    platform.user_connect("bob", "gateway-eu-west")

    # Alice sends message to Bob
    msg = platform.send_message(
        sender_id="alice",
        recipient_id="bob",
        conversation_id="conv-1",
        content="Hello from New York!",
    )

    # Message must be delivered to Bob's WebSocket inbox on gw2
    assert len(gw2.connected_users["bob"]) == 1
    assert gw2.connected_users["bob"][0].content == "Hello from New York!"
    assert gw2.connected_users["bob"][0].message_id == msg.message_id


def test_offline_mailbox_queuing_and_flush_on_connect() -> None:
    platform = DistributedChatPlatform()
    gw = WebSocketGatewayNode("gateway-1")
    platform.register_gateway(gw)

    # Alice sends message to Charlie who is currently OFFLINE
    platform.send_message(
        sender_id="alice",
        recipient_id="charlie",
        conversation_id="conv-2",
        content="Read this when you wake up!",
    )

    # Message is queued in Charlie's offline mailbox
    assert len(platform.offline_mailboxes["charlie"]) == 1

    # Charlie connects to gateway-1 -> Pending offline messages must flush to his inbox!
    platform.user_connect("charlie", "gateway-1")

    assert len(platform.offline_mailboxes["charlie"]) == 0
    assert len(gw.connected_users["charlie"]) == 1
    assert gw.connected_users["charlie"][0].content == "Read this when you wake up!"


def test_presence_heartbeat_and_timeout() -> None:
    # 0.4s timeout: >0.2s is AWAY, >0.4s is OFFLINE
    platform = DistributedChatPlatform(presence_timeout=0.4)
    gw = WebSocketGatewayNode("gw-main")
    platform.register_gateway(gw)

    platform.user_connect("david", "gw-main")
    assert platform.presence.get_status("david") == UserStatus.ONLINE

    # Wait 0.25s -> Transitions to AWAY
    time.sleep(0.25)
    assert platform.presence.get_status("david") == UserStatus.AWAY

    # Send heartbeat ping -> Restored to ONLINE
    platform.presence.heartbeat("david")
    assert platform.presence.get_status("david") == UserStatus.ONLINE

    # Wait 0.45s without heartbeat -> Transitions to OFFLINE
    time.sleep(0.45)
    assert platform.presence.get_status("david") == UserStatus.OFFLINE


def test_conversation_history_retention() -> None:
    platform = DistributedChatPlatform()
    gw = WebSocketGatewayNode("gw")
    platform.register_gateway(gw)

    platform.user_connect("user-a", "gw")
    platform.user_connect("user-b", "gw")

    platform.send_message("user-a", "user-b", "conv-room", "Message 1")
    platform.send_message("user-b", "user-a", "conv-room", "Message 2")

    history = platform.conversation_store["conv-room"]
    assert len(history) == 2
    assert history[0].content == "Message 1"
    assert history[1].content == "Message 2"
