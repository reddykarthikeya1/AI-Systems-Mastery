#!/usr/bin/env python3
"""Module 06 Demo: Gang of Four Design Patterns in Scalable Backends."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from notification_engine import (
    AuditLogDecorator,
    ChannelFactory,
    MetricsCollector,
    NotificationHandler,
    NotificationMessage,
    RetryDecorator,
)


def main() -> None:
    print("=" * 72)
    print("  MODULE 06: GANG OF FOUR (GoF) DESIGN PATTERNS IN ACTION")
    print("=" * 72)

    # 1. Factory + Strategy
    print("\n--- 1. Factory & Strategy: Dynamic Channel Instantiation ---")
    email_channel = ChannelFactory.create_channel("EMAIL")
    sms_channel = ChannelFactory.create_channel("SMS")
    push_channel = ChannelFactory.create_channel("PUSH", token_store={"alice_iphone_apns"})
    print(f"Created channels: {email_channel.channel_name}, {sms_channel.channel_name}, {push_channel.channel_name}")

    # 2. Decorator Pattern
    print("\n--- 2. Structural Decorator: Audit Logging & Retries ---")
    audit_trail: list[str] = []
    decorated_email = AuditLogDecorator(
        RetryDecorator(email_channel, max_retries=1),
        audit_log=audit_trail,
    )

    sample_msg = NotificationMessage(
        message_id="ALERT-501",
        recipient="ops-oncall@fintech.io",
        content="Database latency > 200ms",
        priority="HIGH",
    )
    decorated_email.send(sample_msg)
    print("Audit log entry emitted by Decorator:")
    for entry in audit_trail:
        print(f"  {entry}")

    # 3. Chain of Responsibility + Observer
    print("\n--- 3. Chain of Responsibility: Fallback Dispatch (Push -> SMS -> Email) ---")
    metrics = MetricsCollector()

    root_handler = NotificationHandler(push_channel)
    sms_handler = NotificationHandler(sms_channel)
    email_handler = NotificationHandler(email_channel)

    root_handler.set_next(sms_handler).set_next(email_handler)

    # Dispatch to an email recipient (Push will reject, SMS will reject, Email will succeed)
    dispatch_msg = NotificationMessage(
        message_id="PAYMENT-RECEIPT-99",
        recipient="customer@domain.com",
        content="Payment of $150.00 confirmed.",
    )
    print(f"Routing notification to recipient: {dispatch_msg.recipient}")
    delivered = root_handler.handle(dispatch_msg, observers=[metrics])
    print(f"Chain execution result: {'DELIVERED' if delivered else 'UNDELIVERED'}")
    print(f"Metrics collected by Observer: {metrics.counts}")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
