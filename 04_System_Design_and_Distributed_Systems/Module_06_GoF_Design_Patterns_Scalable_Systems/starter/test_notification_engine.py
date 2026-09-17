"""Unit tests for Gang of Four Design Patterns Notification Engine."""

from __future__ import annotations

import pytest
from notification_engine import (
    AuditLogDecorator,
    ChannelFactory,
    EmailChannel,
    MetricsCollector,
    NotificationHandler,
    NotificationMessage,
    PushNotificationChannel,
    RetryDecorator,
    SMSChannel,
)


def test_factory_pattern_creates_proper_strategies() -> None:
    email = ChannelFactory.create_channel("EMAIL")
    assert isinstance(email, EmailChannel)
    assert email.channel_name == "EMAIL"

    sms = ChannelFactory.create_channel("SMS")
    assert isinstance(sms, SMSChannel)
    assert sms.channel_name == "SMS"

    push = ChannelFactory.create_channel("PUSH", token_store={"token_123"})
    assert isinstance(push, PushNotificationChannel)
    assert push.channel_name == "PUSH"

    with pytest.raises(ValueError, match="Unknown notification channel"):
        ChannelFactory.create_channel("CARRIER_PIGEON")


def test_decorator_pattern_audit_logging() -> None:
    logs: list[str] = []
    base_channel = EmailChannel()
    audited = AuditLogDecorator(base_channel, audit_log=logs)

    msg = NotificationMessage(message_id="msg-1", recipient="dev@example.com", content="System Alert")
    res = audited.send(msg)

    assert res is True
    assert len(logs) == 1
    assert "EMAIL" in logs[0]
    assert "SUCCESS" in logs[0]
    assert "dev@example.com" in logs[0]


def test_decorator_pattern_retry_on_failure() -> None:
    calls = {"count": 0}

    class FlakyEmail(EmailChannel):
        def send(self, message: NotificationMessage) -> bool:
            calls["count"] += 1
            if calls["count"] < 2:
                raise ConnectionError("Temporary SMTP timeout")
            return True

    retried = RetryDecorator(FlakyEmail(), max_retries=3)
    msg = NotificationMessage(message_id="msg-2", recipient="user@test.org", content="Hello")
    assert retried.send(msg) is True
    assert calls["count"] == 2


def test_chain_of_responsibility_failover() -> None:
    # Set up chain: Push -> SMS -> Email
    push_channel = PushNotificationChannel(token_store={"known_device_token"})
    sms_channel = SMSChannel()
    email_channel = EmailChannel()

    chain = NotificationHandler(push_channel)
    sms_node = NotificationHandler(sms_channel)
    email_node = NotificationHandler(email_channel)
    chain.set_next(sms_node).set_next(email_node)

    metrics = MetricsCollector()

    # Case A: Recipient is a valid push token -> Handled at first node
    msg_push = NotificationMessage(message_id="m1", recipient="known_device_token", content="Alert 1")
    assert chain.handle(msg_push, [metrics]) is True
    assert metrics.counts["total"] == 1
    assert metrics.counts["success"] == 1

    # Case B: Recipient is an email -> Push fails, SMS fails, Email succeeds!
    msg_email = NotificationMessage(message_id="m2", recipient="admin@infra.net", content="Critical Down")
    assert chain.handle(msg_email, [metrics]) is True
    # Total attempts = 1 from Case A + 3 (Push fail, SMS fail, Email pass) = 4
    assert metrics.counts["total"] == 4
    assert metrics.counts["success"] == 2
    assert metrics.counts["failed"] == 2


def test_observer_pattern_telemetry_tracking() -> None:
    metrics = MetricsCollector()
    email = EmailChannel()
    handler = NotificationHandler(email)

    msg_ok = NotificationMessage("m10", "lead@company.com", "OK")
    handler.handle(msg_ok, [metrics])

    # Bad email should register as failure
    msg_bad = NotificationMessage("m11", "invalid-email-format", "FAIL")
    handler.handle(msg_bad, [metrics])

    assert metrics.counts["total"] == 2
    assert metrics.counts["success"] == 1
    assert metrics.counts["failed"] == 1
