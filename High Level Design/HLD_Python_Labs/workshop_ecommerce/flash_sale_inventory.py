"""Educational Architecture Simulator & Reference Pattern: Flash Sale Inventory Reservation System.

Architectural Guarantees & Educational Context:
----------------------------------------------
Educational Simulator vs. Production Flash Sale Architecture:
- Logical Simulation (This Module):
  Demonstrates high-concurrency two-phase inventory reservation using Redis Cluster
  hash tags, Lua script atomic execution, Sorted Set expiration indexing, idempotency
  de-duplication, and relational ledger reconciliation in Python.
- Production Deployment Considerations & Boundaries:

1. Redis Cluster Hash Tags:
   Multi-key transactions in Redis Cluster fail with `CROSSSLOT Keys in request don't hash
   to the same slot` unless hash tags `{...}` are used.
   All keys for an item are partitioned identically using:
       `{item:<id>}:stock`
       `{item:<id>}:reserves`
       `{item:<id>}:idempotency`
       `{item:<id>}:expirations` (Sorted Set for TTL expiration indexing)

2. Strict Two-Phase Reservation State Machine:
   Enforces valid state transitions:
       `HELD -> CONFIRMED` (successful payment)
       `HELD -> RELEASED`  (explicit user cancellation)
       `HELD -> EXPIRED`   (TTL expiration via background reconciliation daemon)
   Any transition from a terminal or non-HELD state (e.g. duplicate confirm, duplicate release,
   or confirm after expire) is strictly rejected with `INVALID_STATE`.

3. Idempotency Key De-duplication & Parameter Validation:
   - Quantity must be strictly > 0 (rejects qty <= 0).
   - Re-submitting the exact same request with the same idempotency key returns the original
     reservation without deducting inventory twice.
   - Re-using an existing idempotency key with DIFFERENT parameters (e.g. changed item_id,
     user_id, or quantity) is rejected as an idempotency conflict.

4. Expiration Indexing via Redis Sorted Set (ZSET):
   Reservations are indexed in `{item:<id>}:expirations` with score = `expires_at` epoch timestamp.
   The background reconciliation worker scans expired reservations atomically via Lua script,
   restores uncommitted inventory, and transitions state to `EXPIRED`.
   A confirmation-vs-expiration race is handled atomically: once expired in reconciliation,
   any subsequent confirmation attempt is rejected.

5. Redis In-Memory Execution vs Replica Failover vs PostgreSQL Authoritative Ledger:
   - Redis In-Memory Atomicity: Single-threaded Lua script execution guarantees serialized,
     race-free stock reservation and state transitions within a Redis hash slot.
   - Replica Failover Data Loss: Redis asynchronous replication means that if the master node
     crashes before replicating writes to a replica, failover may result in lost reservations
     (phantom inventory availability). Redis serves as a high-throughput write-ahead reservation cache.
   - PostgreSQL Authoritative Ledger: PostgreSQL with ACID transactions, row-level locks,
     and durable WAL is the authoritative financial and inventory ledger. The confirmation
     path MUST inspect and respect the boolean return from PostgreSQL reconciliation. If PostgreSQL
     reconciliation returns False (e.g. authoritative ledger exhausted due to a prior failover discrepancy),
     the reservation confirmation is rejected and Redis state is rolled back.

6. The Cross-Database Dual-Write Consistency Gap & Production Mitigations:
   - The Dual-Write Problem:
     Redis Lua and PostgreSQL cannot achieve distributed two-phase commit (2PC) atomicity
     without an external distributed coordinator or transactional outbox. Redis and PostgreSQL
     are distinct distributed databases with separate storage engines, network connections,
     and transaction lifecycles.
   - Crash / Ambiguous Timeout Failure Window:
     If the application server successfully executes the Redis Lua confirmation script
     (transitioning the reservation to `CONFIRMED` and removing it from the TTL index),
     but crashes (e.g., process termination, host failure) or encounters an unhandled network
     timeout before committing the PostgreSQL transaction, Redis holds a `CONFIRMED`
     reservation while PostgreSQL lacks the corresponding order row. A client retry or
     subsequent query creates split-brain state between cache and durable ledger.
   - Production Mitigation Patterns:
     (A) Asynchronous Cross-System Reconciliation Daemon:
         A periodic background reconciliation job scans reservations marked `CONFIRMED` in Redis
         against PostgreSQL `orders` table. Any confirmed reservation lacking a corresponding
         committed order after a grace period is identified as an orphaned confirmation and is
         resolved by either inserting the missing order or rolling back the Redis reservation.
     (B) Database-Authoritative Reservation with Redis as Read-Only Rate Limiter:
         Redis is used solely as a high-throughput admission control filter / counter.
         The actual atomic stock deduction and reservation lock are executed inside PostgreSQL
         via `SELECT quantity FROM inventory WHERE item_id = $1 FOR UPDATE`. This eliminates
         distributed state synchronization because PostgreSQL is the single authoritative source of truth.
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
-- KEYS[4]: {item:<id>}:expirations
-- ARGV[1]: idempotency_key
-- ARGV[2]: reservation_id
-- ARGV[3]: user_id
-- ARGV[4]: quantity
-- ARGV[5]: ttl_seconds
-- ARGV[6]: current_time

local stock_key = KEYS[1]
local reserves_key = KEYS[2]
local idemp_key = KEYS[3]
local expirations_key = KEYS[4]

local idem_key_val = ARGV[1]
local res_id = ARGV[2]
local user_id = ARGV[3]
local qty = tonumber(ARGV[4])
local ttl = tonumber(ARGV[5])
local now = tonumber(ARGV[6])

-- 1. Validation
if not qty or qty <= 0 then
    return cjson.encode({status = "ERROR", message = "Quantity must be > 0"})
end

-- 2. Idempotency Check
local existing_res_id = redis.call('HGET', idemp_key, idem_key_val)
if existing_res_id then
    local existing_record_str = redis.call('HGET', reserves_key, existing_res_id)
    if existing_record_str then
        local existing_record = cjson.decode(existing_record_str)
        -- Validate parameter consistency
        if existing_record.quantity ~= qty or existing_record.user_id ~= user_id then
            return cjson.encode({status = "ERROR", message = "Idempotency key parameter mismatch"})
        end
        return existing_record_str -- Return idempotent response
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
if expirations_key then
    redis.call('ZADD', expirations_key, expires_at, res_id)
end

return record_json
"""

LUA_CONFIRM_RESERVATION = """
-- KEYS[1]: {item:<id>}:reserves
-- KEYS[2]: {item:<id>}:expirations
-- ARGV[1]: reservation_id
-- ARGV[2]: current_time (optional)

local reserves_key = KEYS[1]
local expirations_key = KEYS[2]
local res_id = ARGV[1]
local now = tonumber(ARGV[2])

local record_json = redis.call('HGET', reserves_key, res_id)
if not record_json then
    return cjson.encode({status = "NOT_FOUND"})
end

local record = cjson.decode(record_json)
if record.status ~= "HELD" then
    return cjson.encode({status = "INVALID_STATE", current_status = record.status})
end

-- Check if already expired by wall-clock timestamp
if now and now > record.expires_at then
    return cjson.encode({status = "INVALID_STATE", current_status = "EXPIRED"})
end

record.status = "CONFIRMED"
if expirations_key then
    redis.call('ZREM', expirations_key, res_id)
end
local updated_json = cjson.encode(record)
redis.call('HSET', reserves_key, res_id, updated_json)
return updated_json
"""

LUA_RELEASE_RESERVATION = """
-- KEYS[1]: {item:<id>}:stock
-- KEYS[2]: {item:<id>}:reserves
-- KEYS[3]: {item:<id>}:expirations
-- ARGV[1]: reservation_id

local stock_key = KEYS[1]
local reserves_key = KEYS[2]
local expirations_key = KEYS[3]
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
if expirations_key then
    redis.call('ZREM', expirations_key, res_id)
end
local updated_json = cjson.encode(record)
redis.call('HSET', reserves_key, res_id, updated_json)
return updated_json
"""

LUA_RECONCILE_EXPIRED = """
-- KEYS[1]: {item:<id>}:stock
-- KEYS[2]: {item:<id>}:reserves
-- KEYS[3]: {item:<id>}:expirations
-- ARGV[1]: current_time
-- ARGV[2]: batch_size

local stock_key = KEYS[1]
local reserves_key = KEYS[2]
local expirations_key = KEYS[3]
local now = tonumber(ARGV[1])
local batch_size = tonumber(ARGV[2]) or 100

local expired_ids = redis.call('ZRANGEBYSCORE', expirations_key, '-inf', now, 'LIMIT', 0, batch_size)
local restored_qty = 0

for _, res_id in ipairs(expired_ids) do
    redis.call('ZREM', expirations_key, res_id)
    local rec_json = redis.call('HGET', reserves_key, res_id)
    if rec_json then
        local rec = cjson.decode(rec_json)
        if rec.status == "HELD" then
            rec.status = "EXPIRED"
            redis.call('HSET', reserves_key, res_id, cjson.encode(rec))
            redis.call('INCRBY', stock_key, rec.quantity)
            restored_qty = restored_qty + rec.quantity
        end
    end
end

return restored_qty
"""

LUA_ROLLBACK_CONFIRMATION = """
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
    """Educational In-Memory Simulation for Local Testing and Demonstration.

    Simulates a PostgreSQL durable relational database with row-level locking (SELECT FOR UPDATE)
    and transactional order persistence. In a production deployment, this would be an actual ACID-compliant
    RDBMS connection pool (e.g. asyncpg or psycopg) writing durably to Write-Ahead Logs (WAL).
    """

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


# Alias for educational and workshop clarity
SimulatedPostgresLedger = PostgresInventoryStore


class FlashSaleInventoryService:
    """Educational Architecture Simulator & Reference Pattern: Flash Sale Inventory Service.

    Coordinates high-concurrency inventory reservation using Redis Cluster hash tags,
    Lua script atomic execution, and PostgreSQL authoritative reconciliation.
    """

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
        self._expirations_store: Dict[str, Dict[str, float]] = {}
        self._res_to_item: Dict[str, str] = {}
        self.inconsistencies: List[Dict[str, Any]] = []

    def _keys(self, item_id: str) -> Tuple[str, str, str, str]:
        """Cluster hash tags guarantee all keys reside on the same cluster slot."""
        return (
            f"{{item:{item_id}}}:stock",
            f"{{item:{item_id}}}:reserves",
            f"{{item:{item_id}}}:idempotency",
            f"{{item:{item_id}}}:expirations",
        )

    def initialize_stock(self, item_id: str, stock: int) -> None:
        """Seed stock in both Redis and PostgreSQL."""
        self.postgres_db.set_initial_inventory(item_id, stock)
        stock_key, _, _, _ = self._keys(item_id)
        if self.redis is not None:
            self.redis.set(stock_key, stock)
        else:
            with self._lock:
                self._stock_store[stock_key] = stock
                self._reserves_store[item_id] = {}
                self._idemp_store[item_id] = {}
                self._expirations_store[item_id] = {}

    def get_stock(self, item_id: str) -> int:
        stock_key, _, _, _ = self._keys(item_id)
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
        """Reserve inventory under hold with idempotency and parameter validation."""
        if quantity <= 0:
            return ReservationResult(
                success=False,
                status="ERROR",
                message="Quantity must be > 0",
            )

        if now is None:
            now = time.time()

        res_id = str(uuid.uuid4())
        stock_k, reserves_k, idemp_k, exp_k = self._keys(item_id)

        if self.redis is not None:
            raw = self.redis.eval(
                LUA_RESERVE_INVENTORY,
                4,
                stock_k,
                reserves_k,
                idemp_k,
                exp_k,
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
            self._res_to_item[rec.reservation_id] = item_id
            return ReservationResult(success=True, status=rec.status.value, record=rec)

        # In-memory execution
        with self._lock:
            idemp_map = self._idemp_store.setdefault(item_id, {})
            reserves_map = self._reserves_store.setdefault(item_id, {})
            exp_map = self._expirations_store.setdefault(item_id, {})

            # Check idempotency
            if idempotency_key in idemp_map:
                existing_id = idemp_map[idempotency_key]
                existing_rec = reserves_map.get(existing_id)
                if existing_rec:
                    # Parameter mismatch check: same key with different quantity or user_id is rejected
                    if existing_rec.quantity != quantity or existing_rec.user_id != user_id:
                        return ReservationResult(
                            success=False,
                            status="ERROR",
                            message="Idempotency key parameter mismatch",
                        )
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
            expires_at = now + ttl_seconds
            rec = ReservationRecord(
                reservation_id=res_id,
                user_id=user_id,
                quantity=quantity,
                status=ReservationState.HELD,
                created_at=now,
                expires_at=expires_at,
            )
            reserves_map[res_id] = rec
            idemp_map[idempotency_key] = res_id
            exp_map[res_id] = expires_at
            self._res_to_item[res_id] = item_id
            return ReservationResult(success=True, status="HELD", record=rec)

    def confirm(
        self,
        item_id: str,
        reservation_id: Optional[str] = None,
        now: Optional[float] = None,
    ) -> ReservationResult:
        """Transitions reservation from HELD to CONFIRMED and reconciles with PostgreSQL ledger."""
        # Normalize arguments to allow confirm(item_id, reservation_id, now=None) or confirm(reservation_id, now=None)
        if reservation_id is None or isinstance(reservation_id, (int, float)):
            if isinstance(reservation_id, (int, float)):
                now = float(reservation_id)
            res_id = item_id
            target_item_id = self._res_to_item.get(res_id)
            if target_item_id is None:
                for it_id, rmap in self._reserves_store.items():
                    if res_id in rmap:
                        target_item_id = it_id
                        break
            if target_item_id is None:
                target_item_id = res_id
            item_id = target_item_id
            reservation_id = res_id

        if now is None:
            now = time.time()

        stock_k, reserves_k, _, exp_k = self._keys(item_id)
        if self.redis is not None:
            raw = self.redis.eval(
                LUA_CONFIRM_RESERVATION,
                2,
                reserves_k,
                exp_k,
                reservation_id,
                now,
            )
            data = json.loads(raw)
            if "status" in data and data["status"] in ("NOT_FOUND", "INVALID_STATE"):
                return ReservationResult(
                    success=False,
                    status=data["status"],
                    message=f"Status is {data.get('current_status')}",
                )
            rec = ReservationRecord(
                reservation_id=data["reservation_id"],
                user_id=data["user_id"],
                quantity=data["quantity"],
                status=ReservationState(data["status"]),
                created_at=data["created_at"],
                expires_at=data["expires_at"],
            )
            # Reconcile against PostgreSQL authoritative ledger
            try:
                pg_success = self.postgres_db.reconcile_confirmed_order(item_id, rec)
            except Exception as exc:
                # Dual-write crash / ambiguous timeout window: attempt rollback and record inconsistency
                self.redis.eval(LUA_ROLLBACK_CONFIRMATION, 2, stock_k, reserves_k, reservation_id)
                rec.status = ReservationState.RELEASED
                self.inconsistencies.append({
                    "reservation_id": reservation_id,
                    "item_id": item_id,
                    "error": str(exc),
                    "timestamp": now,
                })
                return ReservationResult(
                    success=False,
                    status="RECONCILIATION_FAILED",
                    message=f"PostgreSQL reconciliation error: {exc}",
                    record=rec,
                )

            if not pg_success:
                # Rollback Redis confirmation to maintain ledger consistency
                self.redis.eval(LUA_ROLLBACK_CONFIRMATION, 2, stock_k, reserves_k, reservation_id)
                rec.status = ReservationState.RELEASED
                return ReservationResult(
                    success=False,
                    status="RECONCILIATION_FAILED",
                    message="PostgreSQL authoritative ledger reconciliation failed",
                    record=rec,
                )
            return ReservationResult(success=True, status="CONFIRMED", record=rec)

        with self._lock:
            reserves_map = self._reserves_store.get(item_id, {})
            rec = reserves_map.get(reservation_id)
            if not rec:
                return ReservationResult(success=False, status="NOT_FOUND")

            # Enforce state machine: only HELD reservations can be confirmed
            if rec.status != ReservationState.HELD:
                return ReservationResult(
                    success=False,
                    status="INVALID_STATE",
                    message=f"Status is {rec.status.value}",
                    record=rec,
                )

            # Check if reservation has expired by timestamp
            if now > rec.expires_at:
                return ReservationResult(
                    success=False,
                    status="INVALID_STATE",
                    message="Status is EXPIRED",
                    record=rec,
                )

            # Optimistically update to CONFIRMED (simulating Redis Lua confirmation)
            rec.status = ReservationState.CONFIRMED

            # Attempt PostgreSQL authoritative ledger reconciliation
            try:
                pg_success = self.postgres_db.reconcile_confirmed_order(item_id, rec)
            except Exception as exc:
                # Crash / unhandled network timeout simulation: rollback in-memory state and log inconsistency
                rec.status = ReservationState.RELEASED
                self._stock_store[stock_k] = self._stock_store.get(stock_k, 0) + rec.quantity
                self._expirations_store.get(item_id, {}).pop(reservation_id, None)
                self.inconsistencies.append({
                    "reservation_id": reservation_id,
                    "item_id": item_id,
                    "error": str(exc),
                    "timestamp": now,
                })
                return ReservationResult(
                    success=False,
                    status="RECONCILIATION_FAILED",
                    message=f"PostgreSQL reconciliation error: {exc}",
                    record=rec,
                )

            if not pg_success:
                # Reconcile failure: authoritative ledger exhausted; release Redis stock hold
                rec.status = ReservationState.RELEASED
                self._stock_store[stock_k] = self._stock_store.get(stock_k, 0) + rec.quantity
                self._expirations_store.get(item_id, {}).pop(reservation_id, None)
                return ReservationResult(
                    success=False,
                    status="RECONCILIATION_FAILED",
                    message="PostgreSQL authoritative ledger reconciliation failed",
                    record=rec,
                )

            rec.status = ReservationState.CONFIRMED
            self._expirations_store.get(item_id, {}).pop(reservation_id, None)
            return ReservationResult(success=True, status="CONFIRMED", record=rec)

    def release(self, item_id: str, reservation_id: str) -> ReservationResult:
        """Manually releases HELD inventory and restores stock."""
        stock_k, reserves_k, _, exp_k = self._keys(item_id)
        if self.redis is not None:
            raw = self.redis.eval(
                LUA_RELEASE_RESERVATION, 3, stock_k, reserves_k, exp_k, reservation_id
            )
            data = json.loads(raw)
            if "status" in data and data["status"] in ("NOT_FOUND", "INVALID_STATE"):
                return ReservationResult(
                    success=False,
                    status=data["status"],
                    message=f"Status is {data.get('current_status')}",
                )
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

            # Enforce state machine: only HELD reservations can be released
            if rec.status != ReservationState.HELD:
                return ReservationResult(
                    success=False,
                    status="INVALID_STATE",
                    message=f"Status is {rec.status.value}",
                    record=rec,
                )

            rec.status = ReservationState.RELEASED
            self._stock_store[stock_k] = self._stock_store.get(stock_k, 0) + rec.quantity
            self._expirations_store.get(item_id, {}).pop(reservation_id, None)
            return ReservationResult(success=True, status="RELEASED", record=rec)

    def reconcile_expired_reservations(
        self,
        item_id: str,
        now: Optional[float] = None,
        batch_size: int = 100,
    ) -> int:
        """Daemon worker: scans expired reservations from sorted set, restores inventory atomically, marks EXPIRED."""
        if now is None:
            now = time.time()

        stock_k, reserves_k, _, exp_k = self._keys(item_id)

        if self.redis is not None:
            restored = self.redis.eval(
                LUA_RECONCILE_EXPIRED,
                3,
                stock_k,
                reserves_k,
                exp_k,
                now,
                batch_size,
            )
            return int(restored) if restored else 0

        restored_count = 0
        with self._lock:
            reserves_map = self._reserves_store.get(item_id, {})
            exp_map = self._expirations_store.get(item_id, {})
            expired_ids = [
                res_id for res_id, exp_time in exp_map.items()
                if now >= exp_time
            ]

            for res_id in expired_ids:
                exp_map.pop(res_id, None)
                rec = reserves_map.get(res_id)
                if rec and rec.status == ReservationState.HELD:
                    rec.status = ReservationState.EXPIRED
                    self._stock_store[stock_k] = (
                        self._stock_store.get(stock_k, 0) + rec.quantity
                    )
                    restored_count += rec.quantity

        return restored_count


# Educational and architectural aliases
FlashSaleInventory = FlashSaleInventoryService


