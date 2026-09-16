"""Unit tests for SOLID Principles & Clean Architecture Checkout Domain."""

from __future__ import annotations

from decimal import Decimal

import pytest
from clean_checkout import (
    CheckoutService,
    InMemoryOrderRepository,
    MockInventoryService,
    MockPaymentGateway,
    Money,
    Order,
    OrderPaidEvent,
    OrderPlacedEvent,
    OrderStatus,
)


def test_money_value_object_invariants() -> None:
    m1 = Money(Decimal("25.50"), "USD")
    m2 = Money(Decimal("14.50"), "USD")
    res = m1.add(m2)
    assert res.amount == Decimal("40.00")
    assert res.currency == "USD"

    # Invariant 1: Negative amount rejected
    with pytest.raises(ValueError, match="cannot be negative"):
        Money(Decimal("-5.00"), "USD")

    # Invariant 2: Currency mismatch rejected
    eur = Money(Decimal("10.00"), "EUR")
    with pytest.raises(ValueError, match="different currencies"):
        m1.add(eur)


def test_order_aggregate_mutation_and_calculation() -> None:
    order = Order(order_id="ord-100", customer_id="cust-1", currency="USD")
    order.add_item("prod-1", "Mechanical Keyboard", Money(Decimal("100.00"), "USD"), 2)
    order.add_item("prod-2", "USB-C Cable", Money(Decimal("15.00"), "USD"), 3)

    total = order.calculate_total()
    # (100 * 2) + (15 * 3) = 245.00
    assert total.amount == Decimal("245.00")
    assert total.currency == "USD"


def test_successful_checkout_orchestration_and_events() -> None:
    repo = InMemoryOrderRepository()
    inv = MockInventoryService(initial_stock={"prod-1": 10, "prod-2": 5})
    gateway = MockPaymentGateway()
    service = CheckoutService(repo, gateway, inv)

    order = Order(order_id="ord-200", customer_id="cust-42", currency="USD")
    order.add_item("prod-1", "Laptop Stand", Money(Decimal("45.00"), "USD"), 2)

    txn_id = service.execute_checkout(order)

    assert txn_id == "tx_stripe_ord-200"
    assert order.status == OrderStatus.PAID
    assert inv.get_available_stock("prod-1") == 8
    assert repo.find_by_id("ord-200") is not None

    # Check that domain events were generated
    events = order.domain_events
    assert len(events) == 2
    assert isinstance(events[0], OrderPlacedEvent)
    assert isinstance(events[1], OrderPaidEvent)
    assert events[0].total_amount == Decimal("90.00")


def test_checkout_rollback_when_inventory_insufficient() -> None:
    repo = InMemoryOrderRepository()
    inv = MockInventoryService(initial_stock={"prod-1": 1})  # only 1 in stock
    gateway = MockPaymentGateway()
    service = CheckoutService(repo, gateway, inv)

    order = Order(order_id="ord-300", customer_id="cust-1", currency="USD")
    order.add_item("prod-1", "4K Monitor", Money(Decimal("300.00"), "USD"), 2)  # asks for 2

    with pytest.raises(RuntimeError, match="Insufficient stock"):
        service.execute_checkout(order)

    assert order.status == OrderStatus.CANCELLED
    assert inv.get_available_stock("prod-1") == 1  # Unchanged
    assert len(gateway.processed_transactions) == 0  # No payment charged


def test_checkout_compensating_action_when_payment_fails() -> None:
    repo = InMemoryOrderRepository()
    inv = MockInventoryService(initial_stock={"prod-1": 10})
    gateway = MockPaymentGateway(should_fail=True)  # Payment declined
    service = CheckoutService(repo, gateway, inv)

    order = Order(order_id="ord-400", customer_id="cust-1", currency="USD")
    order.add_item("prod-1", "Headphones", Money(Decimal("80.00"), "USD"), 2)

    with pytest.raises(ConnectionError, match="Payment gateway card declined"):
        service.execute_checkout(order)

    # Invariant: Inventory was temporarily reserved, but MUST be released on payment failure!
    assert inv.get_available_stock("prod-1") == 10
    assert order.status == OrderStatus.CANCELLED
