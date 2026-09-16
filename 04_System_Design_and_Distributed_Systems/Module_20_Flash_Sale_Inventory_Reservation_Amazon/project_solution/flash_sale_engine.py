"""Module 20: E-Commerce Flash Sale & Inventory Reservation System.

Reference implementation of atomic inventory reservations, TTL auto-expiry,
zero-overselling guarantees, and distributed lock simulation.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from dataclasses import dataclass


class ReservationStatus(enum.StrEnum):
    RESERVED = "RESERVED"
    PURCHASED = "PURCHASED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


@dataclass
class ReservationToken:
    """Represents a temporary hold on inventory during checkout."""
    reservation_id: str
    sku: str
    user_id: str
    quantity: int
    created_at: float
    expires_at: float
    status: ReservationStatus = ReservationStatus.RESERVED


# ============================================================================
# 1. Naive Inventory (Demonstrates Concurrency Bug / Overselling)
# ============================================================================

class NaiveInventoryStore:
    """Vulnerable inventory store exhibiting race conditions under concurrent load."""

    def __init__(self, initial_stock: int) -> None:
        self.stock = initial_stock
        self.oversold_count = 0
        self.successful_orders = 0

    def attempt_buy(self, quantity: int = 1) -> bool:
        """Simulates non-atomic read-then-write race condition."""
        if self.stock >= quantity:
            # Yield to OS thread scheduler to amplify concurrency interleaved execution
            time.sleep(0.0001)
            self.stock -= quantity
            self.successful_orders += quantity
            if self.stock < 0:
                self.oversold_count += abs(self.stock)
            return True
        return False


# ============================================================================
# 2. Reference Atomic Inventory Reservation Manager
# ============================================================================

class AtomicInventoryReservationManager:
    """Simulates Redis atomic Lua-scripted reservation manager with zero overselling."""

    def __init__(self) -> None:
        self._lock = threading.RLock()

        # sku -> { "available": int, "reserved": int, "purchased": int, "total": int }
        self._inventory: dict[str, dict[str, int]] = {}

        # reservation_id -> ReservationToken
        self._reservations: dict[str, ReservationToken] = {}

    def register_sku(self, sku: str, total_stock: int) -> None:
        """Initializes a product SKU with initial stock."""
        with self._lock:
            if total_stock < 0:
                raise ValueError("Total stock cannot be negative")
            self._inventory[sku] = {
                "available": total_stock,
                "reserved": 0,
                "purchased": 0,
                "total": total_stock,
            }

    def reserve(
        self,
        sku: str,
        user_id: str,
        quantity: int,
        ttl_sec: float = 600.0,
        current_time: float | None = None
    ) -> tuple[bool, ReservationToken | None]:
        """Atomically checks stock and places a temporary hold on requested quantity."""
        if current_time is None:
            current_time = time.time()

        if quantity <= 0:
            return False, None

        with self._lock:
            inv = self._inventory.get(sku)
            if not inv:
                return False, None

            if inv["available"] < quantity:
                return False, None  # Insufficient stock, reject immediately (HTTP 429/409)

            # Atomic decrement available, increment reserved
            inv["available"] -= quantity
            inv["reserved"] += quantity

            token = ReservationToken(
                reservation_id=f"res_{uuid.uuid4().hex[:12]}",
                sku=sku,
                user_id=user_id,
                quantity=quantity,
                created_at=current_time,
                expires_at=current_time + ttl_sec,
                status=ReservationStatus.RESERVED,
            )
            self._reservations[token.reservation_id] = token
            return True, token

    def confirm_purchase(
        self,
        reservation_id: str,
        current_time: float | None = None
    ) -> bool:
        """Confirms payment; transitions reservation from RESERVED to PURCHASED."""
        if current_time is None:
            current_time = time.time()

        with self._lock:
            token = self._reservations.get(reservation_id)
            if not token:
                return False

            if token.status != ReservationStatus.RESERVED:
                return False

            if current_time > token.expires_at:
                # Token expired before payment confirmation
                self._expire_token(token)
                return False

            # Successful checkout
            token.status = ReservationStatus.PURCHASED
            inv = self._inventory[token.sku]
            inv["reserved"] -= token.quantity
            inv["purchased"] += token.quantity
            return True

    def cancel_reservation(self, reservation_id: str) -> bool:
        """User explicitly cancels cart; returns stock back to available pool immediately."""
        with self._lock:
            token = self._reservations.get(reservation_id)
            if not token or token.status != ReservationStatus.RESERVED:
                return False

            token.status = ReservationStatus.CANCELLED
            inv = self._inventory[token.sku]
            inv["reserved"] -= token.quantity
            inv["available"] += token.quantity
            return True

    def reap_expired_reservations(self, current_time: float | None = None) -> list[ReservationToken]:
        """Background sweeper (reaper) identifying timed-out reservations and restoring stock."""
        if current_time is None:
            current_time = time.time()

        expired_tokens: list[ReservationToken] = []

        with self._lock:
            for token in self._reservations.values():
                if token.status == ReservationStatus.RESERVED and current_time > token.expires_at:
                    self._expire_token(token)
                    expired_tokens.append(token)

        return expired_tokens

    def _expire_token(self, token: ReservationToken) -> None:
        """Helper to expire a single token and return inventory to available pool."""
        token.status = ReservationStatus.EXPIRED
        inv = self._inventory[token.sku]
        inv["reserved"] -= token.quantity
        inv["available"] += token.quantity

    def get_stock_snapshot(self, sku: str) -> dict[str, int] | None:
        """Returns deep copy of current inventory counters for auditing."""
        with self._lock:
            inv = self._inventory.get(sku)
            return dict(inv) if inv else None

    def verify_conservation_invariant(self, sku: str) -> bool:
        """Verifies universal stock conservation invariant: Available + Reserved + Purchased == Total."""
        with self._lock:
            inv = self._inventory.get(sku)
            if not inv:
                return False
            sum_counters = inv["available"] + inv["reserved"] + inv["purchased"]
            return sum_counters == inv["total"] and inv["available"] >= 0
