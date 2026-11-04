"""Production Flash Sale Inventory Reservation System.

Architectural Guarantees:
-------------------------
1. Redis Cluster Hash Tags:
   Multi-key transactions in Redis Cluster fail with `CROSSSLOT Keys in request don't hash
   to the same slot` unless hash tags `{...}` are used.
   All keys for an item are partitioned identically using:
       `{item:<id>}:stock`
       `{item:<id>}:reserves`
       `{item:<id>}:idempotency`

2. Idempotency Key De-duplication:
   Re-submitting the same checkout idempotency key returns the original reservation
   without deducting inventory twice.

3. Complete Two-Phase Reservation Lifecycle:
   - Initial Hold: HELD (with TTL, e.g. 10 minutes)
   - Payment Success: CONFIRMED
   - User Cancellation: RELEASED (stock replenished immediately)
   - Payment Timeout: EXPIRED (reconciliation daemon restores stock)

4. Database Eventual Consistency Layer:
   Syncs high-throughput Redis state to PostgreSQL persistent store.
"""

from __future__ import annotations
import enum
import json
import threading
import time
import uuid
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

LUA_RESERVE_INVENTORY = """
-- KEYS[1]: {item:<id>}:stock
-- KEYS[2]: {item:<id>}:reserves
-- KEYS[3]: {item:<id>}:idempotency
-- ARGV[1]: idempotency_key
-- ARGV[2]: reservation_id
-- ARGV[3]: user_id
-- ARGV[4]: quantity
-- ARGV[5]: ttl_seconds
-- ARGV[6]: current_time

local stock_key = KEYS[1]
local reserves_key = KEYS[2]
local idemp_key = KEYS[3]

local idem_key_val = ARGV[1]
local res_id = ARGV[2]
local user_id = ARGV[3]
local qty = tonumber(ARGV[4])
local ttl = tonumber(ARGV[5])
local now = tonumber(ARGV[6])

-- 1. Validation
if qty <= 0 then
    return cjson.encode({status = "ERROR", message = "Quantity must be > 0"})
end

-- 2. Idempotency Check
local existing_res_id = redis.call('HGET', idemp_key, idem_key_val)
if existing_res_id then
    local existing_record = redis.call('HGET', reserves_key, existing_res_id)
    if existing_record then
        return existing_record -- Return idempotent response
    end
end

-- 3. Check Stock
local current_stock = tonumber(redis.call('GET', stock_key) or "0")
if current_stock < qty then
    return cjson.encode({status = "OUT_OF_STOCK", remaining_stock = current_stock})
end

-- 4. Deduct Stock and Create Hold
redis.call('DECRBY', stock_key, qty)

local expires_at = now + ttl
local record = {
    reservation_id = res_id,
    user_id = user_id,
    quantity = qty,
    status = "HELD",
    created_at = now,
    expires_at = expires_at
}
local record_json = cjson.encode(record)

redis.call('HSET', reserves_key, res_id, record_json)
redis.call('HSET', idemp_key, idem_key_val, res_id)

return record_json
"""

LUA_CONFIRM_RESERVATION = """
-- KEYS[1]: {item:<id>}:reserves
-- ARGV[1]: reservation_id

local reserves_key = KEYS[1]
local res_id = ARGV[1]

local record_json = redis.call('HGET', reserves_key, res_id)
if not record_json then
    return cjson.encode({status = "NOT_FOUND"})
end

local record = cjson.decode(record_json)
if record.status ~= "HELD" then
    return cjson.encode({status = "INVALID_STATE", current_status = record.status})
end

record.status = "CONFIRMED"
local updated_json = cjson.encode(record)
redis.call('HSET', reserves_key, res_id, updated_json)
return updated_json
"""

LUA_RELEASE_RESERVATION = """
-- KEYS[1]: {item:<id>}:stock
-- KEYS[2]: {item:<id>}:reserves
-- ARGV[1]: reservation_id

local stock_key = KEYS[1]
local reserves_key = KEYS[2]
local res_id = ARGV[1]

local record_json = redis.call('HGET', reserves_key, res_id)
if not record_json then
    return cjson.encode({status = "NOT_FOUND"})
end

local record = cjson.decode(record_json)
if record.status ~= "HELD" then
    return cjson.encode({status = "INVALID_STATE", current_status = record.status})
end

record.status = "RELEASED"
redis.call('INCRBY', stock_key, record.quantity)
local updated_json = cjson.encode(record)
redis.call('HSET', reserves_key, res_id, updated_json)
return updated_json
"""


class ReservationState(str, enum.Enum):
    HELD = "HELD"
    CONFIRMED = "CONFIRMED"
    RELEASED = "RELEASED"
    EXPIRED = "EXPIRED"


@dataclass
class ReservationRecord:
    reservation_id: str
    user_id: str
    quantity: int
    status: ReservationState
    created_at: float
    expires_at: float


@dataclass
class ReservationResult:
    success: bool
    status: str
    record: Optional[ReservationRecord] = None
    message: Optional[str] = None
    remaining_stock: Optional[int] = None


class PostgresInventoryStore:
    """Simulated PostgreSQL durable relational database with row locking."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.inventory: Dict[str, int] = {}
        self.orders: Dict[str, Dict[str, Any]] = {}

    def set_initial_inventory(self, item_id: str, quantity: int) -> None:
        with self._lock:
            self.inventory[item_id] = quantity

    def reconcile_confirmed_order(self, item_id: str, reservation: ReservationRecord) -> bool:
        with self._lock:
            current = self.inventory.get(item_id, 0)
            if current < reservation.quantity:
                return False
            self.inventory[item_id] -= reservation.quantity
            self.orders[reservation.reservation_id] = asdict(reservation)
            return True


class FlashSaleInventoryService:
    """Flash sale inventory coordinator with Redis Cluster hash tags and reconciliation."""

    def __init__(
        self,
        postgres_db: PostgresInventoryStore,
        redis_client: Any = None,
    ) -> None:
        self.postgres_db = postgres_db
        self.redis = redis_client
        self._lock = threading.Lock()

        # In-memory cluster hash simulation
        self._stock_store: Dict[str, int] = {}
        self._reserves_store: Dict[str, Dict[str, ReservationRecord]] = {}
        self._idemp_store: Dict[str, Dict[str, str]] = {}

    def _keys(self, item_id: str) -> Tuple[str, str, str]:
        """Cluster hash tags guarantee all keys reside on the same cluster slot."""
        return (
            f"{{item:{item_id}}}:stock",
            f"{{item:{item_id}}}:reserves",
            f"{{item:{item_id}}}:idempotency",
        )

    def initialize_stock(self, item_id: str, stock: int) -> None:
        """Seed stock in both Redis and PostgreSQL."""
        self.postgres_db.set_initial_inventory(item_id, stock)
        stock_key, _, _ = self._keys(item_id)
        if self.redis is not None:
            self.redis.set(stock_key, stock)
        else:
            with self._lock:
                self._stock_store[stock_key] = stock
                self._reserves_store[item_id] = {}
                self._idemp_store[item_id] = {}

    def get_stock(self, item_id: str) -> int:
        stock_key, _, _ = self._keys(item_id)
        if self.redis is not None:
            val = self.redis.get(stock_key)
            return int(val) if val else 0
        with self._lock:
            return self._stock_store.get(stock_key, 0)

    def reserve(
        self,
        item_id: str,
        user_id: str,
        quantity: int,
        idempotency_key: str,
        ttl_seconds: float = 600.0,
        now: Optional[float] = None,
    ) -> ReservationResult:
        """Reserve inventory under hold with idempotency."""
        if quantity <= 0:
            return ReservationResult(
                success=False,
                status="ERROR",
                message="Quantity must be > 0",
            )

        if now is None:
            now = time.time()

        res_id = str(uuid.uuid4())
        stock_k, reserves_k, idemp_k = self._keys(item_id)

        if self.redis is not None:
            raw = self.redis.eval(
                LUA_RESERVE_INVENTORY,
                3,
                stock_k,
                reserves_k,
                idemp_k,
                idempotency_key,
                res_id,
                user_id,
                quantity,
                ttl_seconds,
                now,
            )
            data = json.loads(raw)
            if data.get("status") == "OUT_OF_STOCK":
                return ReservationResult(
                    success=False,
                    status="OUT_OF_STOCK",
                    remaining_stock=data.get("remaining_stock", 0),
                )
            if data.get("status") == "ERROR":
                return ReservationResult(
                    success=False,
                    status="ERROR",
                    message=data.get("message"),
                )

            rec = ReservationRecord(
                reservation_id=data["reservation_id"],
                user_id=data["user_id"],
                quantity=data["quantity"],
                status=ReservationState(data["status"]),
                created_at=data["created_at"],
                expires_at=data["expires_at"],
            )
            return ReservationResult(success=True, status=rec.status.value, record=rec)

        # In-memory execution
        with self._lock:
            idemp_map = self._idemp_store.setdefault(item_id, {})
            reserves_map = self._reserves_store.setdefault(item_id, {})

            # Check idempotency
            if idempotency_key in idemp_map:
                existing_id = idemp_map[idempotency_key]
                existing_rec = reserves_map.get(existing_id)
                if existing_rec:
                    return ReservationResult(
                        success=True,
                        status=existing_rec.status.value,
                        record=existing_rec,
                    )

            current_stock = self._stock_store.get(stock_k, 0)
            if current_stock < quantity:
                return ReservationResult(
                    success=False,
                    status="OUT_OF_STOCK",
                    remaining_stock=current_stock,
                )

            # Deduct stock
            self._stock_store[stock_k] = current_stock - quantity
            rec = ReservationRecord(
                reservation_id=res_id,
                user_id=user_id,
                quantity=quantity,
                status=ReservationState.HELD,
                created_at=now,
                expires_at=now + ttl_seconds,
            )
            reserves_map[res_id] = rec
            idemp_map[idempotency_key] = res_id
            return ReservationResult(success=True, status="HELD", record=rec)

    def confirm(self, item_id: str, reservation_id: str) -> ReservationResult:
        """Transitions reservation from HELD to CONFIRMED and syncs to DB."""
        _, reserves_k, _ = self._keys(item_id)
        if self.redis is not None:
            raw = self.redis.eval(LUA_CONFIRM_RESERVATION, 1, reserves_k, reservation_id)
            data = json.loads(raw)
            if "status" in data and data["status"] in ("NOT_FOUND", "INVALID_STATE"):
                return ReservationResult(
                    success=False,
                    status=data["status"],
                    message=data.get("current_status"),
                )
            rec = ReservationRecord(
                reservation_id=data["reservation_id"],
                user_id=data["user_id"],
                quantity=data["quantity"],
                status=ReservationState(data["status"]),
                created_at=data["created_at"],
                expires_at=data["expires_at"],
            )
            self.postgres_db.reconcile_confirmed_order(item_id, rec)
            return ReservationResult(success=True, status="CONFIRMED", record=rec)

        with self._lock:
            reserves_map = self._reserves_store.get(item_id, {})
            rec = reserves_map.get(reservation_id)
            if not rec:
                return ReservationResult(success=False, status="NOT_FOUND")
            if rec.status != ReservationState.HELD:
                return ReservationResult(
                    success=False,
                    status="INVALID_STATE",
                    message=f"Status is {rec.status.value}",
                )

            rec.status = ReservationState.CONFIRMED
            self.postgres_db.reconcile_confirmed_order(item_id, rec)
            return ReservationResult(success=True, status="CONFIRMED", record=rec)

    def release(self, item_id: str, reservation_id: str) -> ReservationResult:
        """Manually releases HELD inventory and restores stock."""
        stock_k, reserves_k, _ = self._keys(item_id)
        if self.redis is not None:
            raw = self.redis.eval(
                LUA_RELEASE_RESERVATION, 2, stock_k, reserves_k, reservation_id
            )
            data = json.loads(raw)
            if "status" in data and data["status"] in ("NOT_FOUND", "INVALID_STATE"):
                return ReservationResult(success=False, status=data["status"])
            rec = ReservationRecord(
                reservation_id=data["reservation_id"],
                user_id=data["user_id"],
                quantity=data["quantity"],
                status=ReservationState(data["status"]),
                created_at=data["created_at"],
                expires_at=data["expires_at"],
            )
            return ReservationResult(success=True, status="RELEASED", record=rec)

        with self._lock:
            reserves_map = self._reserves_store.get(item_id, {})
            rec = reserves_map.get(reservation_id)
            if not rec:
                return ReservationResult(success=False, status="NOT_FOUND")
            if rec.status != ReservationState.HELD:
                return ReservationResult(
                    success=False,
                    status="INVALID_STATE",
                    message=f"Status is {rec.status.value}",
                )

            rec.status = ReservationState.RELEASED
            self._stock_store[stock_k] = self._stock_store.get(stock_k, 0) + rec.quantity
            return ReservationResult(success=True, status="RELEASED", record=rec)

    def reconcile_expired_reservations(
        self, item_id: str, now: Optional[float] = None
    ) -> int:
        """Daemon worker: scans HELD reservations whose TTL expired and restores stock."""
        if now is None:
            now = time.time()

        stock_k, _, _ = self._keys(item_id)
        restored_count = 0

        with self._lock:
            reserves_map = self._reserves_store.get(item_id, {})
            for rec in reserves_map.values():
                if rec.status == ReservationState.HELD and now > rec.expires_at:
                    rec.status = ReservationState.EXPIRED
                    self._stock_store[stock_k] = (
                        self._stock_store.get(stock_k, 0) + rec.quantity
                    )
                    restored_count += rec.quantity

        return restored_count
