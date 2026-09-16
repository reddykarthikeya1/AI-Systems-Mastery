#!/usr/bin/env python3
"""Module 05: Production Clean Architecture & Domain-Driven Design Checkout System.

Demonstrates SOLID Principles (SRP, OCP, LSP, ISP, DIP), Value Objects,
Entities, Aggregate Roots, Domain Events, and Repository Inversion.

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

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Protocol

# ============================================================================
# Domain Layer: Value Objects (Immutable, Identity by Value)
# ============================================================================


@dataclass(frozen=True, slots=True)
class Money:
    """Immutable Value Object enforcing currency equality and non-negative amounts."""

    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < Decimal("0.00"):
            raise ValueError(f"Money amount cannot be negative: {self.amount}")
        if len(self.currency) != 3 or not self.currency.isupper():
            raise ValueError(f"Invalid ISO currency code: {self.currency}")

    def add(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError(f"Cannot add different currencies: {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: int) -> Money:
        if factor < 0:
            raise ValueError("Multiplier cannot be negative")
        return Money(self.amount * Decimal(factor), self.currency)


# ============================================================================
# Domain Layer: Entities & Aggregate Root
# ============================================================================


class OrderStatus(StrEnum):
    DRAFT = "DRAFT"
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


@dataclass(slots=True)
class OrderItem:
    """Entity with unique product_id within the order."""

    product_id: str
    product_name: str
    unit_price: Money
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be strictly positive: {self.quantity}")

    @property
    def subtotal(self) -> Money:
        return self.unit_price.multiply(self.quantity)


@dataclass(frozen=True)
class DomainEvent:
    event_id: str
    occurred_at: str


@dataclass(frozen=True)
class OrderPlacedEvent(DomainEvent):
    order_id: str
    customer_id: str
    total_amount: Decimal
    currency: str


@dataclass(frozen=True)
class OrderPaidEvent(DomainEvent):
    order_id: str
    transaction_id: str


class Order:
    """Aggregate Root: Enforces all business invariants for an Order."""

    def __init__(self, order_id: str, customer_id: str, currency: str = "USD") -> None:
        self.order_id = order_id
        self.customer_id = customer_id
        self.currency = currency
        self.status = OrderStatus.DRAFT
        self._items: list[OrderItem] = []
        self._events: list[DomainEvent] = []

    @property
    def items(self) -> list[OrderItem]:
        return list(self._items)

    @property
    def domain_events(self) -> list[DomainEvent]:
        return list(self._events)

    def clear_events(self) -> None:
        self._events.clear()

    def add_item(self, product_id: str, product_name: str, unit_price: Money, quantity: int) -> None:
        if self.status != OrderStatus.DRAFT:
            raise ValueError(f"Cannot mutate order in status '{self.status}'")
        if unit_price.currency != self.currency:
            raise ValueError(f"Item currency {unit_price.currency} does not match order currency {self.currency}")

        # If product already exists in draft, merge quantity
        for existing in self._items:
            if existing.product_id == product_id:
                existing.quantity += quantity
                return

        self._items.append(OrderItem(product_id, product_name, unit_price, quantity))

    def calculate_total(self) -> Money:
        total = Money(Decimal("0.00"), self.currency)
        for item in self._items:
            total = total.add(item.subtotal)
        return total

    def place_order(self) -> None:
        if self.status != OrderStatus.DRAFT:
            raise ValueError(f"Cannot place order in status '{self.status}'")
        if not self._items:
            raise ValueError("Cannot place an empty order")

        self.status = OrderStatus.PENDING_PAYMENT
        total = self.calculate_total()
        self._events.append(
            OrderPlacedEvent(
                event_id=f"evt-{self.order_id}-placed",
                occurred_at=datetime.now(UTC).isoformat(),
                order_id=self.order_id,
                customer_id=self.customer_id,
                total_amount=total.amount,
                currency=total.currency,
            )
        )

    def mark_as_paid(self, transaction_id: str) -> None:
        if self.status != OrderStatus.PENDING_PAYMENT:
            raise ValueError(f"Cannot pay order in status '{self.status}'")

        self.status = OrderStatus.PAID
        self._events.append(
            OrderPaidEvent(
                event_id=f"evt-{self.order_id}-paid",
                occurred_at=datetime.now(UTC).isoformat(),
                order_id=self.order_id,
                transaction_id=transaction_id,
            )
        )


# ============================================================================
# Ports & Protocols (Dependency Inversion Principle - DIP & ISP)
# ============================================================================


class PaymentGateway(Protocol):
    """ISP: Focused payment processor interface."""

    def process_payment(self, order_id: str, amount: Money) -> str:
        """Processes payment and returns transaction ID or raises PaymentError."""
        ...


class InventoryService(Protocol):
    """ISP: Focused stock reservation interface."""

    def reserve_stock(self, product_id: str, quantity: int) -> bool: ...
    def release_stock(self, product_id: str, quantity: int) -> None: ...


class OrderRepository(Protocol):
    """Port for persistence."""

    def save(self, order: Order) -> None: ...
    def find_by_id(self, order_id: str) -> Order | None: ...


# ============================================================================
# Application Service Layer (Single Responsibility Principle - SRP)
# ============================================================================


class CheckoutService:
    """Orchestrates checkout business flow without coupling to concrete infrastructure."""

    def __init__(
        self,
        repository: OrderRepository,
        payment_gateway: PaymentGateway,
        inventory_service: InventoryService,
    ) -> None:
        self.repository = repository
        self.payment_gateway = payment_gateway
        self.inventory_service = inventory_service

    def execute_checkout(self, order: Order) -> str:
        # 1. Place the order
        order.place_order()

        # 2. Reserve inventory for all items
        reserved_items: list[tuple[str, int]] = []
        try:
            for item in order.items:
                success = self.inventory_service.reserve_stock(item.product_id, item.quantity)
                if not success:
                    raise RuntimeError(f"Insufficient stock for product '{item.product_name}'")
                reserved_items.append((item.product_id, item.quantity))

            # 3. Process payment through payment gateway
            total = order.calculate_total()
            txn_id = self.payment_gateway.process_payment(order.order_id, total)

            # 4. Mark order as paid and persist
            order.mark_as_paid(txn_id)
            self.repository.save(order)
            return txn_id

        except Exception:
            # Compensate: release reserved inventory on failure
            for prod_id, qty in reserved_items:
                self.inventory_service.release_stock(prod_id, qty)
            order.status = OrderStatus.CANCELLED
            self.repository.save(order)
            raise


# ============================================================================
# Concrete Infrastructure Adapters (Liskov Substitution & Clean Arch)
# ============================================================================


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def find_by_id(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)


class MockPaymentGateway:
    def __init__(self, should_fail: bool = False) -> None:
        self.should_fail = should_fail
        self.processed_transactions: dict[str, Money] = {}

    def process_payment(self, order_id: str, amount: Money) -> str:
        if self.should_fail:
            raise ConnectionError("Payment gateway card declined / network failure")
        txn_id = f"tx_stripe_{order_id}"
        self.processed_transactions[txn_id] = amount
        return txn_id


class MockInventoryService:
    def __init__(self, initial_stock: dict[str, int] | None = None) -> None:
        self._stock: dict[str, int] = initial_stock or {}

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        current = self._stock.get(product_id, 0)
        if current >= quantity:
            self._stock[product_id] = current - quantity
            return True
        return False

    def release_stock(self, product_id: str, quantity: int) -> None:
        self._stock[product_id] = self._stock.get(product_id, 0) + quantity

    def get_available_stock(self, product_id: str) -> int:
        return self._stock.get(product_id, 0)
