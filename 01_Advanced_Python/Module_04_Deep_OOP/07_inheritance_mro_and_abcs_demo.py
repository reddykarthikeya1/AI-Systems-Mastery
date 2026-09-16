#!/usr/bin/env python3
"""Module 04: Inheritance, MRO & Abstract Base Classes Demonstration.

This script demonstrates super(), multiple inheritance, C3 linearization,
and interface enforcement with abc.ABC and @abstractmethod.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Abstract Base Class enforcing a strict payment interface."""

    def __init__(self, merchant_id: str) -> None:
        self.merchant_id = merchant_id

    @abstractmethod
    def charge(self, amount: float) -> bool:
        """Process a credit/debit charge."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> bool:
        """Process a customer refund."""
        pass


class StripeProcessor(PaymentProcessor):
    """Concrete implementation of PaymentProcessor using Stripe API simulation."""

    def charge(self, amount: float) -> bool:
        print(f"[STRIPE] Successfully charged ${amount:.2f} (Merchant: {self.merchant_id})")
        return True

    def refund(self, transaction_id: str, amount: float) -> bool:
        print(f"[STRIPE] Refunded ${amount:.2f} for Tx: {transaction_id}")
        return True


class LoggerMixin:
    """Mixin class providing telemetry logging."""
    def log_event(self, event: str) -> None:
        print(f"[AUDIT LOG] {event}")


class AuditedStripeProcessor(StripeProcessor, LoggerMixin):
    """Demonstrates multiple inheritance combining concrete processor and mixin."""
    def charge(self, amount: float) -> bool:
        self.log_event(f"Pre-charge validation for ${amount:.2f}")
        result = super().charge(amount)
        self.log_event(f"Post-charge completed: status={result}")
        return result


def main() -> None:
    print("=" * 60)
    print("  1. Abstract Base Class Contract Enforcement")
    print("=" * 60)

    processor = StripeProcessor("merchant_apex_99")
    processor.charge(149.99)
    processor.refund("TX-88192", 49.99)

    print("\n" + "=" * 60)
    print("  2. Multiple Inheritance & MRO Inspection")
    print("=" * 60)

    audited = AuditedStripeProcessor("merchant_secure_01")
    audited.charge(500.00)

    print("\nMethod Resolution Order (MRO) for AuditedStripeProcessor:")
    for idx, cls in enumerate(AuditedStripeProcessor.__mro__):
        print(f"  [{idx}] {cls.__name__}")


if __name__ == "__main__":
    main()
