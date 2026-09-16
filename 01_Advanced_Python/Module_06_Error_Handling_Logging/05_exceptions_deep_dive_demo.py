#!/usr/bin/env python3
"""Module 06: Exceptions Deep Dive Demonstration.

This script demonstrates custom exception hierarchies, exception chaining (raise from),
try/except/else/finally control flow, and Python 3.11+ ExceptionGroup.
"""

from __future__ import annotations


# Custom Domain Exception Hierarchy
class CommerceError(Exception):
    """Base exception for all e-commerce operations."""
    pass


class InventoryError(CommerceError):
    """Raised when stock is unavailable."""
    pass


class PaymentGatewayError(CommerceError):
    """Raised when payment processor encounters an error."""
    pass


def simulate_checkout(item_id: str, quantity: int, card_valid: bool) -> bool:
    """Simulates multi-stage checkout with custom error handling."""
    print(f"\n[CHECKOUT] Processing Item: '{item_id}', Qty: {quantity}")

    # Stage 1: Inventory Check
    if quantity > 5:
        raise InventoryError(f"Requested quantity {quantity} exceeds in-stock limit of 5 units.")

    # Stage 2: Payment Processing with Exception Chaining
    if not card_valid:
        try:
            # Low-level provider socket timeout simulation
            raise TimeoutError("Stripe API socket connection timed out after 3000ms")
        except TimeoutError as root_err:
            raise PaymentGatewayError("Payment authorization failed due to provider timeout.") from root_err

    return True


def demo_exception_chaining() -> None:
    print("=" * 60)
    print("  1. Custom Exception Hierarchy & Chaining (raise from)")
    print("=" * 60)

    try:
        simulate_checkout(item_id="PROD-99", quantity=2, card_valid=False)
    except CommerceError as err:
        print(f"[CAUGHT DOMAIN ERROR]: {type(err).__name__} -> {err}")
        if err.__cause__:
            print(f"  Root Cause (__cause__): {type(err.__cause__).__name__} -> {err.__cause__}")


def demo_exception_group() -> None:
    print("\n" + "=" * 60)
    print("  2. Python 3.11+ ExceptionGroup & except* Pattern")
    print("=" * 60)

    tasks_failures = [
        InventoryError("Item #101 out of stock"),
        PaymentGatewayError("Card declined for User #45"),
        InventoryError("Item #105 warehouse damaged"),
    ]
    group = ExceptionGroup("Multi-Service Batch Execution Errors", tasks_failures)

    try:
        raise group
    except* InventoryError as e:
        print(f"Handled {len(e.exceptions)} Inventory Errors:")
        for sub in e.exceptions:
            print(f"  - {sub}")
    except* PaymentGatewayError as e:
        print(f"Handled {len(e.exceptions)} Payment Gateway Errors:")
        for sub in e.exceptions:
            print(f"  - {sub}")


def main() -> None:
    demo_exception_chaining()
    demo_exception_group()


if __name__ == "__main__":
    main()
