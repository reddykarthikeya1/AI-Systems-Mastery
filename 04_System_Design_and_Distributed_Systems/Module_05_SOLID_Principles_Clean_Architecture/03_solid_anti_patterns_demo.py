#!/usr/bin/env python3
"""Module 05 Demo: SOLID Anti-Patterns vs Clean Hexagonal Architecture."""

import sys
from decimal import Decimal
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from clean_checkout import (
    CheckoutService,
    InMemoryOrderRepository,
    MockInventoryService,
    MockPaymentGateway,
    Money,
    Order,
)


def main() -> None:
    print("=" * 72)
    print("  MODULE 05: SOLID PRINCIPLES & CLEAN ARCHITECTURE IN PRACTICE")
    print("=" * 72)

    print("\n--- 1. Testing Domain Value Objects (Money Invariant Protection) ---")
    usd = Money(Decimal("99.99"), "USD")
    tax = Money(Decimal("8.50"), "USD")
    total = usd.add(tax)
    print(f"Price: {usd.amount} {usd.currency} + Tax: {tax.amount} {tax.currency} = {total.amount} {total.currency}")

    try:
        eur = Money(Decimal("10.00"), "EUR")
        usd.add(eur)
    except ValueError as e:
        print(f"Domain Invariant Caught: {e}")

    print("\n--- 2. Clean Checkout Orchestration (DIP in Action) ---")
    repo = InMemoryOrderRepository()
    inv = MockInventoryService(initial_stock={"sku-laptop": 5, "sku-mouse": 20})
    stripe_gateway = MockPaymentGateway()

    checkout_service = CheckoutService(
        repository=repo,
        payment_gateway=stripe_gateway,
        inventory_service=inv,
    )

    order = Order(order_id="ORD-9912", customer_id="user-alex")
    order.add_item("sku-laptop", "MacBook Pro M3", Money(Decimal("1999.00"), "USD"), 1)
    order.add_item("sku-mouse", "Magic Mouse", Money(Decimal("79.00"), "USD"), 1)

    print(f"Order created with total: ${order.calculate_total().amount}")
    print(f"Available laptop stock BEFORE checkout: {inv.get_available_stock('sku-laptop')}")

    txn_id = checkout_service.execute_checkout(order)
    print(f"Checkout SUCCESS! Transaction ID: {txn_id}")
    print(f"Order Status: {order.status.value}")
    print(f"Available laptop stock AFTER checkout: {inv.get_available_stock('sku-laptop')}")

    print("\n--- 3. Domain Events Emitted by Aggregate Root ---")
    for event in order.domain_events:
        print(f"  [Event] {type(event).__name__} (ID: {event.event_id}, Time: {event.occurred_at})")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
