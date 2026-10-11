"""AeroTrade Core - Domain Models

Demonstrates concepts from Chapters 01-05:
- Immutable value objects with __slots__ for minimal memory footprint (Ch 05).
- Custom descriptor validation for positive prices and quantities (Ch 04).
- Modern Python 3.11+ Enum and typing conventions (Ch 01, 07).
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from enum import Enum, auto


class Side(Enum):
    BUY = auto()
    SELL = auto()


class OrderType(Enum):
    LIMIT = auto()
    MARKET = auto()


class OrderStatus(Enum):
    PENDING = auto()
    PARTIALLY_FILLED = auto()
    FILLED = auto()
    CANCELLED = auto()


class PositiveNumericDescriptor:
    """Descriptor ensuring assigned attribute is a strictly positive number (Ch 04)."""

    def __init__(self, name: str):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value: float | int):
        if value <= 0:
            raise ValueError(f"{self.name} must be strictly positive, got {value}")
        setattr(instance, self.private_name, value)


@dataclass(slots=True)
class Order:
    """Represents a limit or market order. Uses __slots__ to save ~60% RAM per instance."""

    order_id: str
    trader_id: str
    symbol: str
    side: Side
    price: float
    quantity: int
    remaining_quantity: int = field(init=False)
    order_type: OrderType = OrderType.LIMIT
    status: OrderStatus = OrderStatus.PENDING
    timestamp_ns: int = field(default_factory=time.time_ns)

    # Descriptors enforce domain rules
    price = PositiveNumericDescriptor("price")
    quantity = PositiveNumericDescriptor("quantity")

    def __post_init__(self):
        self.remaining_quantity = self.quantity

    @property
    def is_filled(self) -> bool:
        return self.remaining_quantity == 0

    def fill(self, qty: int) -> None:
        if qty > self.remaining_quantity:
            raise ValueError(f"Cannot fill {qty} units; only {self.remaining_quantity} remaining")
        self.remaining_quantity -= qty
        self.status = OrderStatus.FILLED if self.remaining_quantity == 0 else OrderStatus.PARTIALLY_FILLED


@dataclass(slots=True, frozen=True)
class Trade:
    """Immutable record of an executed trade match."""

    trade_id: str
    symbol: str
    price: float
    quantity: int
    buyer_order_id: str
    seller_order_id: str
    buyer_id: str
    seller_id: str
    timestamp_ns: int = field(default_factory=time.time_ns)
