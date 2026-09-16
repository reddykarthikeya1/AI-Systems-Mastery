#!/usr/bin/env python3
"""Module 06: Production Multi-Channel Enterprise Notification Engine.

Demonstrates core Gang of Four (GoF) design patterns:
- Strategy (Pluggable channel algorithms: Email, SMS, Push)
- Factory (Dynamic channel instantiation)
- Decorator (Cross-cutting audit logging, rate limiting, and retries)
- Chain of Responsibility (Priority failover: Push -> SMS -> Email)
- Observer (Decoupled analytics and telemetry events)

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class NotificationMessage:
    message_id: str
    recipient: str
    content: str
    priority: str = "NORMAL"  # HIGH, NORMAL, LOW
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# 1. Strategy Pattern: Pluggable Delivery Channels
# ============================================================================


class ChannelStrategy(ABC):
    """Abstract Strategy interface for delivery channels."""

    @property
    @abstractmethod
    def channel_name(self) -> str: ...

    @abstractmethod
    def send(self, message: NotificationMessage) -> bool:
        """Sends notification; returns True if successful, False/raises on error."""


class EmailChannel(ChannelStrategy):
    @property
    def channel_name(self) -> str:
        return "EMAIL"

    def send(self, message: NotificationMessage) -> bool:
        if "@" not in message.recipient:
            raise ValueError(f"Invalid email address: {message.recipient}")
        return True


class SMSChannel(ChannelStrategy):
    @property
    def channel_name(self) -> str:
        return "SMS"

    def send(self, message: NotificationMessage) -> bool:
        clean = message.recipient.replace("-", "").replace("+", "")
        if not clean.isdigit():
            raise ValueError(f"Invalid phone number: {message.recipient}")
        return True


class PushNotificationChannel(ChannelStrategy):
    def __init__(self, token_store: set[str] | None = None) -> None:
        self.valid_tokens: set[str] = token_store or set()

    @property
    def channel_name(self) -> str:
        return "PUSH"

    def send(self, message: NotificationMessage) -> bool:
        # Unregistered device token -> delivery fails.
        return not (self.valid_tokens and message.recipient not in self.valid_tokens)


# ============================================================================
# 2. Factory Pattern: Creation of Channel Strategies
# ============================================================================


class ChannelFactory:
    """Factory creating ChannelStrategy instances dynamically."""

    @staticmethod
    def create_channel(channel_type: str, **kwargs: Any) -> ChannelStrategy:
        ctype = channel_type.upper()
        if ctype == "EMAIL":
            return EmailChannel()
        elif ctype == "SMS":
            return SMSChannel()
        elif ctype == "PUSH":
            return PushNotificationChannel(kwargs.get("token_store"))
        else:
            raise ValueError(f"Unknown notification channel type: {channel_type}")


# ============================================================================
# 3. Decorator Pattern: Cross-Cutting Auditing & Retries
# ============================================================================


class ChannelDecorator(ChannelStrategy):
    """Base structural Decorator wrapping another ChannelStrategy."""

    def __init__(self, wrapped: ChannelStrategy) -> None:
        self._wrapped = wrapped

    @property
    def channel_name(self) -> str:
        return self._wrapped.channel_name

    def send(self, message: NotificationMessage) -> bool:
        return self._wrapped.send(message)


class AuditLogDecorator(ChannelDecorator):
    """Decorates delivery with tamper-evident in-memory audit logs."""

    def __init__(self, wrapped: ChannelStrategy, audit_log: list[str]) -> None:
        super().__init__(wrapped)
        self.audit_log = audit_log

    def send(self, message: NotificationMessage) -> bool:
        timestamp = datetime.now(UTC).isoformat()
        try:
            success = self._wrapped.send(message)
            status_str = "SUCCESS" if success else "FAILED"
            self.audit_log.append(
                f"[{timestamp}] [{self.channel_name}] [{status_str}] To: {message.recipient} | Msg: {message.message_id}"
            )
            return success
        except Exception as exc:
            self.audit_log.append(
                f"[{timestamp}] [{self.channel_name}] [ERROR] To: {message.recipient} | Exc: {exc}"
            )
            raise


class RetryDecorator(ChannelDecorator):
    """Decorates delivery with automatic retries before failing."""

    def __init__(self, wrapped: ChannelStrategy, max_retries: int = 2) -> None:
        super().__init__(wrapped)
        self.max_retries = max_retries

    def send(self, message: NotificationMessage) -> bool:
        last_error: Exception | None = None
        for _attempt in range(self.max_retries + 1):
            try:
                if self._wrapped.send(message):
                    return True
            except Exception as exc:
                last_error = exc
        if last_error:
            raise last_error
        return False


# ============================================================================
# 4. Observer Pattern: Metrics & Event Notification
# ============================================================================


class NotificationObserver(ABC):
    @abstractmethod
    def on_sent(self, channel: str, message: NotificationMessage, success: bool) -> None: ...


class MetricsCollector(NotificationObserver):
    def __init__(self) -> None:
        self.counts: dict[str, int] = {"total": 0, "success": 0, "failed": 0}

    def on_sent(self, channel: str, message: NotificationMessage, success: bool) -> None:
        self.counts["total"] += 1
        if success:
            self.counts["success"] += 1
        else:
            self.counts["failed"] += 1


# ============================================================================
# 5. Chain of Responsibility Pattern: Priority Fallback Dispatch
# ============================================================================


class NotificationHandler:
    """Handler node in a Chain of Responsibility.

    Deliberately **not** an ABC. ``handle`` below is a fully-implemented
    *template method*: it fixes the algorithm (try this channel, notify
    observers, fall through to the next handler) while the behaviour that varies
    arrives by constructor injection as a ``ChannelStrategy``.

    Inheriting from ``ABC`` with no abstract member buys nothing — the class is
    still instantiable and nothing is enforced — while implying to a reader that
    subclasses must override something. Here they must not: overriding
    ``handle`` would discard the fallback chaining that is the whole pattern.

    Contrast ``ChannelStrategy`` above, which *is* an ABC, because
    ``send`` genuinely differs per channel and must be supplied.
    """

    def __init__(self, channel: ChannelStrategy) -> None:
        self.channel = channel
        self._next_handler: NotificationHandler | None = None

    def set_next(self, next_handler: NotificationHandler) -> NotificationHandler:
        self._next_handler = next_handler
        return next_handler

    def handle(
        self,
        message: NotificationMessage,
        observers: list[NotificationObserver] | None = None,
    ) -> bool:
        success = False
        try:
            success = self.channel.send(message)
        except Exception:
            success = False

        if observers:
            for obs in observers:
                obs.on_sent(self.channel.channel_name, message, success)

        if success:
            return True

        # Fall back to next channel in the chain
        if self._next_handler is not None:
            return self._next_handler.handle(message, observers)

        return False
