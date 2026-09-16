"""Module 05: Production Clean Architecture & Domain-Driven Design Checkout System.

Demonstrates SOLID Principles (SRP, OCP, LSP, ISP, DIP), Value Objects,
Entities, Aggregate Roots, Domain Events, and Repository Inversion.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Protocol

@dataclass(frozen=True, slots=True)
class Money:
    """Immutable Value Object enforcing currency equality and non-negative amounts."""
    amount: Decimal
    currency: str = 'USD'

    def __post_init__(self) -> None:
        if self.amount < Decimal('0.00'):
            raise ValueError(f'Money amount cannot be negative: {self.amount}')
        if len(self.currency) != 3 or not self.currency.isupper():
            raise ValueError(f'Invalid ISO currency code: {self.currency}')

    def add(self, other: Money) -> Money:
        raise NotImplementedError('05: implement add()')

    def multiply(self, factor: int) -> Money:
        raise NotImplementedError('05: implement multiply()')

class OrderStatus(str, Enum):
    DRAFT = 'DRAFT'
    PENDING_PAYMENT = 'PENDING_PAYMENT'
    PAID = 'PAID'
    CANCELLED = 'CANCELLED'

@dataclass(slots=True)
class OrderItem:
    """Entity with unique product_id within the order."""
    product_id: str
    product_name: str
    unit_price: Money
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(f'Quantity must be strictly positive: {self.quantity}')

    @property
    def subtotal(self) -> Money:
        raise NotImplementedError('05: implement subtotal()')

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

    def __init__(self, order_id: str, customer_id: str, currency: str='USD') -> None:
        self.order_id = order_id
        self.customer_id = customer_id
        self.currency = currency
        self.status = OrderStatus.DRAFT
        self._items: list[OrderItem] = []
        self._events: list[DomainEvent] = []

    @property
    def items(self) -> list[OrderItem]:
        raise NotImplementedError('05: implement items()')

    @property
    def domain_events(self) -> list[DomainEvent]:
        raise NotImplementedError('05: implement domain_events()')

    def clear_events(self) -> None:
        raise NotImplementedError('05: implement clear_events()')

    def add_item(self, product_id: str, product_name: str, unit_price: Money, quantity: int) -> None:
        raise NotImplementedError('05: implement add_item()')

    def calculate_total(self) -> Money:
        raise NotImplementedError('05: implement calculate_total()')

    def place_order(self) -> None:
        raise NotImplementedError('05: implement place_order()')

    def mark_as_paid(self, transaction_id: str) -> None:
        raise NotImplementedError('05: implement mark_as_paid()')

class PaymentGateway(Protocol):
    """ISP: Focused payment processor interface."""

    def process_payment(self, order_id: str, amount: Money) -> str:
        """Processes payment and returns transaction ID or raises PaymentError."""
        raise NotImplementedError('05: implement process_payment()')

class InventoryService(Protocol):
    """ISP: Focused stock reservation interface."""

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        raise NotImplementedError('05: implement reserve_stock()')

    def release_stock(self, product_id: str, quantity: int) -> None:
        raise NotImplementedError('05: implement release_stock()')

class OrderRepository(Protocol):
    """Port for persistence."""

    def save(self, order: Order) -> None:
        raise NotImplementedError('05: implement save()')

    def find_by_id(self, order_id: str) -> Order | None:
        raise NotImplementedError('05: implement find_by_id()')

class CheckoutService:
    """Orchestrates checkout business flow without coupling to concrete infrastructure."""

    def __init__(self, repository: OrderRepository, payment_gateway: PaymentGateway, inventory_service: InventoryService) -> None:
        self.repository = repository
        self.payment_gateway = payment_gateway
        self.inventory_service = inventory_service

    def execute_checkout(self, order: Order) -> str:
        raise NotImplementedError('05: implement execute_checkout()')

class InMemoryOrderRepository:

    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        raise NotImplementedError('05: implement save()')

    def find_by_id(self, order_id: str) -> Order | None:
        raise NotImplementedError('05: implement find_by_id()')

class MockPaymentGateway:

    def __init__(self, should_fail: bool=False) -> None:
        self.should_fail = should_fail
        self.processed_transactions: dict[str, Money] = {}

    def process_payment(self, order_id: str, amount: Money) -> str:
        raise NotImplementedError('05: implement process_payment()')

class MockInventoryService:

    def __init__(self, initial_stock: dict[str, int] | None=None) -> None:
        self._stock: dict[str, int] = initial_stock or {}

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        raise NotImplementedError('05: implement reserve_stock()')

    def release_stock(self, product_id: str, quantity: int) -> None:
        raise NotImplementedError('05: implement release_stock()')

    def get_available_stock(self, product_id: str) -> int:
        raise NotImplementedError('05: implement get_available_stock()')