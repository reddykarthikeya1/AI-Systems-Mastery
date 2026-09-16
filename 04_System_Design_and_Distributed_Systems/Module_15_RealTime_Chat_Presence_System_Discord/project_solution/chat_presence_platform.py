#!/usr/bin/env python3
"""Module 15: In-Process Architectural Simulation Model: Real-Time Distributed Chat & Presence Platform.

Implements:
- Distributed WebSocket Gateway Session Routing
- Heartbeat-driven User Presence Engine (Online / Away / Offline)
- Cross-Server Message Bus with Offline Mailbox Queuing
- Conversation Append-Only History Store
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum


class UserStatus(StrEnum):
    ONLINE = "ONLINE"
    AWAY = "AWAY"
    OFFLINE = "OFFLINE"


@dataclass(frozen=True)
class ChatMessage:
    message_id: str
    conversation_id: str
    sender_id: str
    recipient_id: str
    content: str
    timestamp: float = field(default_factory=time.time)


class PresenceTracker:
    """Manages real-time user online/offline status via heartbeats with TTL timeout."""

    def __init__(self, timeout_seconds: float = 5.0) -> None:
        self.timeout_seconds = timeout_seconds
        # user_id -> last_heartbeat_timestamp
        self._heartbeats: dict[str, float] = {}
        self._lock = threading.Lock()

    def heartbeat(self, user_id: str) -> None:
        with self._lock:
            self._heartbeats[user_id] = time.monotonic()

    def disconnect(self, user_id: str) -> None:
        with self._lock:
            self._heartbeats.pop(user_id, None)

    def get_status(self, user_id: str) -> UserStatus:
        with self._lock:
            last = self._heartbeats.get(user_id)
            if last is None:
                return UserStatus.OFFLINE
            elapsed = time.monotonic() - last
            if elapsed > self.timeout_seconds:
                return UserStatus.OFFLINE
            elif elapsed > (self.timeout_seconds / 2.0):
                return UserStatus.AWAY
            return UserStatus.ONLINE


class WebSocketGatewayNode:
    """Represents an active edge gateway server maintaining open TCP/WebSocket connections."""

    def __init__(self, gateway_id: str) -> None:
        self.gateway_id = gateway_id
        # user_id -> inbox of delivered messages
        self.connected_users: dict[str, list[ChatMessage]] = {}
        self._lock = threading.Lock()

    def connect(self, user_id: str) -> None:
        with self._lock:
            if user_id not in self.connected_users:
                self.connected_users[user_id] = []

    def disconnect(self, user_id: str) -> None:
        with self._lock:
            self.connected_users.pop(user_id, None)

    def deliver_message(self, message: ChatMessage) -> bool:
        """Pushes message down the user's active WebSocket connection."""
        with self._lock:
            if message.recipient_id in self.connected_users:
                self.connected_users[message.recipient_id].append(message)
                return True
            return False


class DistributedChatPlatform:
    """Coordinates cross-gateway routing, presence, and offline message storage."""

    def __init__(self, presence_timeout: float = 5.0) -> None:
        self.presence = PresenceTracker(timeout_seconds=presence_timeout)
        self.gateways: dict[str, WebSocketGatewayNode] = {}
        # Distributed Session Store: user_id -> gateway_id
        self.session_registry: dict[str, str] = {}
        # Offline Mailbox: user_id -> list of unread messages
        self.offline_mailboxes: dict[str, list[ChatMessage]] = defaultdict(list)
        # Append-only conversation history: conversation_id -> list of messages
        self.conversation_store: dict[str, list[ChatMessage]] = defaultdict(list)
        self._lock = threading.RLock()

    def register_gateway(self, gateway: WebSocketGatewayNode) -> None:
        with self._lock:
            self.gateways[gateway.gateway_id] = gateway

    def user_connect(self, user_id: str, gateway_id: str) -> None:
        with self._lock:
            if gateway_id not in self.gateways:
                raise ValueError(f"Gateway {gateway_id} does not exist")

            self.session_registry[user_id] = gateway_id
            self.gateways[gateway_id].connect(user_id)
            self.presence.heartbeat(user_id)

            # Flush any pending offline mailbox messages
            pending = self.offline_mailboxes.pop(user_id, [])
            for msg in pending:
                self.gateways[gateway_id].deliver_message(msg)

    def user_disconnect(self, user_id: str) -> None:
        with self._lock:
            gw_id = self.session_registry.pop(user_id, None)
            if gw_id and gw_id in self.gateways:
                self.gateways[gw_id].disconnect(user_id)
            self.presence.disconnect(user_id)

    def send_message(
        self,
        sender_id: str,
        recipient_id: str,
        conversation_id: str,
        content: str,
    ) -> ChatMessage:
        """Routes message to recipient's connected gateway, or stages in offline mailbox."""
        msg = ChatMessage(
            message_id=f"msg-{time.time_ns()}",
            conversation_id=conversation_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content,
        )

        with self._lock:
            # 1. Append to conversation history
            self.conversation_store[conversation_id].append(msg)

            # 2. Check if recipient is online on an active gateway
            target_gw_id = self.session_registry.get(recipient_id)
            recipient_status = self.presence.get_status(recipient_id)

            if target_gw_id and recipient_status != UserStatus.OFFLINE:
                target_gw = self.gateways.get(target_gw_id)
                if target_gw and target_gw.deliver_message(msg):
                    return msg

            # Recipient is offline or gateway dropped connection -> stage in offline mailbox
            self.offline_mailboxes[recipient_id].append(msg)
            return msg
