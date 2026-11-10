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

2. Strict Multi-Phase Reservation State Machine:
   Enforces valid state transitions:
       `HELD -> PENDING_CONFIRMATION -> CONFIRMED` (successful payment & PG commit)
       `HELD -> RELEASED`                          (explicit user cancellation)
       `HELD -> EXPIRED`                           (TTL expiration via background reconciliation daemon)
       `PENDING_CONFIRMATION -> RELEASED`          (PG reconciliation failure, stock restored)
       `PENDING_CONFIRMATION -> PENDING_RECONCILIATION` (ambiguous PG timeout, unresolved)
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
   - The Dual-Write Problem & Architectural Reality:
     Redis Lua and PostgreSQL do NOT form a single atomic transaction merely because this
     Python simulator reconciles their states sequentially. They reside on distinct network
     endpoints with independent durability, failover, and crash profiles.
     Distributed two-phase commit (2PC) or XA transactions across heterogeneous Redis/PostgreSQL
     clusters are rarely viable at flash-sale scale due to locking overhead and coordinator vulnerability.
   - Crash / Ambiguous Timeout Failure Window & Intermediate State:
     When confirm() is called, the system atomically transitions `HELD -> PENDING_CONFIRMATION`
     and removes the reservation from the auto-expiry index BEFORE calling PostgreSQL.
     Only upon PostgreSQL success is it transitioned to `CONFIRMED`.
     If a crash or ambiguous timeout occurs before PostgreSQL finishes, the reservation is in
     `PENDING_CONFIRMATION` / `PENDING_RECONCILIATION`, NOT falsely marked `CONFIRMED`.
   - Rollback Invariant & The In-Flight Confirmation Race:
     Ordinary rollback (`rollback_confirmation` / `release_reservation`) MUST NOT release a reservation
     in `PENDING_CONFIRMATION` or `PENDING_RECONCILIATION`. If confirmation is in-flight, releasing
     inventory while PostgreSQL commits results in phantom double-allocated inventory (an active
     PostgreSQL order exists with inventory restored in Redis).
     Only authoritative reconciliation (`reconcile_pending_reservation` with `final_absence_confirmed=True`)
     or explicitly safe compensation may resolve these intermediate states.
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
from typing import Any, Dict, List, Optional, Set, Tuple

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
-- ARGV[3]: action ("STAGE" or "COMMIT", default "STAGE")

local reserves_key = KEYS[1]
local expirations_key = KEYS[2]
local res_id = ARGV[1]
local now = tonumber(ARGV[2])
local action = ARGV[3] or "STAGE"

local record_json = redis.call('HGET', reserves_key, res_id)
if not record_json then
    return cjson.encode({status = "NOT_FOUND"})
end

local record = cjson.decode(record_json)

if action == "STAGE" then
    if record.status ~= "HELD" then
        return cjson.encode({status = "INVALID_STATE", current_status = record.status})
    end

    -- Check if already expired by wall-clock timestamp
    if record.status == "HELD" and now and now >= record.expires_at then
        return cjson.encode({status = "INVALID_STATE", current_status = "EXPIRED"})
    end

    record.status = "PENDING_CONFIRMATION"
    if expirations_key then
        redis.call('ZREM', expirations_key, res_id)
    end
    local updated_json = cjson.encode(record)
    redis.call('HSET', reserves_key, res_id, updated_json)
    return updated_json
elseif action == "COMMIT" then
    if record.status ~= "PENDING_CONFIRMATION" and record.status ~= "HELD" then
        return cjson.encode({status = "INVALID_STATE", current_status = record.status})
    end
    record.status = "CONFIRMED"
    if expirations_key then
        redis.call('ZREM', expirations_key, res_id)
    end
    local updated_json = cjson.encode(record)
    redis.call('HSET', reserves_key, res_id, updated_json)
    return updated_json
else
    return cjson.encode({status = "ERROR", message = "Unknown action: " .. action})
end
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

if record.status == "PENDING_CONFIRMATION" then
    return cjson.encode({status = "PENDING_CONFIRMATION", message = "Cannot release reservation while confirmation is in-flight", current_status = record.status})
end
if record.status == "PENDING_RECONCILIATION" then
    return cjson.encode({status = "PENDING_RECONCILIATION", message = "Cannot release reservation pending reconciliation without authoritative ledger resolution", current_status = record.status})
end

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

-- Rollback CANNOT proceed if the reservation is in PENDING_RECONCILIATION.
-- An ambiguous database timeout must be resolved by authoritative reconciliation, NOT ordinary rollback!
if record.status == "PENDING_RECONCILIATION" then
    return cjson.encode({
        status = "PENDING_RECONCILIATION",
        message = "Cannot rollback reservation pending reconciliation without authoritative ledger resolution",
        reservation_id = res_id,
        current_status = record.status
    })
end

-- Rollback CANNOT proceed if confirmation is currently in-flight (PENDING_CONFIRMATION).
-- An in-flight PostgreSQL transaction may commit after rollback, leading to double-allocation.
if record.status == "PENDING_CONFIRMATION" then
    return cjson.encode({
        status = "PENDING_CONFIRMATION",
        message = "Cannot rollback reservation while confirmation is in-flight",
        reservation_id = res_id,
        current_status = record.status
    })
end

-- Rollback can only succeed if the reservation is in a roll-backable state (CONFIRMED or HELD) and hasn't been rolled back already.
if record.status ~= "CONFIRMED" and record.status ~= "HELD" then
    return cjson.encode({
        status = "ALREADY_ROLLED_BACK",
        current_status = record.status,
        reservation_id = res_id,
        quantity = record.quantity
    })
end

record.status = "RELEASED"
redis.call('INCRBY', stock_key, record.quantity)
local updated_json = cjson.encode(record)
redis.call('HSET', reserves_key, res_id, updated_json)
return updated_json
"""

LUA_RECONCILE_PENDING = """
-- KEYS[1]: {item:<id>}:stock
-- KEYS[2]: {item:<id>}:reserves
-- ARGV[1]: reservation_id
-- ARGV[2]: resolution ("CONFIRM", "RELEASE", or "CHECK")

local stock_key = KEYS[1]
local reserves_key = KEYS[2]
local res_id = ARGV[1]
local resolution = ARGV[2]

local record_json = redis.call('HGET', reserves_key, res_id)
if not record_json then
    return cjson.encode({status = "NOT_FOUND"})
end

local record = cjson.decode(record_json)

-- Idempotent transitions
if record.status == "CONFIRMED" then
    return cjson.encode({status = "ALREADY_CONFIRMED", record = record})
end
if record.status == "RELEASED" then
    return cjson.encode({status = "ALREADY_RELEASED", record = record})
end

if record.status ~= "PENDING_RECONCILIATION" and record.status ~= "PENDING_CONFIRMATION" then
    return cjson.encode({status = "INVALID_STATE", current_status = record.status, record = record})
end

if resolution == "CONFIRM" then
    record.status = "CONFIRMED"
    redis.call('HSET', reserves_key, res_id, cjson.encode(record))
    return cjson.encode({status = "CONFIRMED", record = record})
elseif resolution == "RELEASE" then
    record.status = "RELEASED"
    redis.call('INCRBY', stock_key, record.quantity)
    redis.call('HSET', reserves_key, res_id, cjson.encode(record))
    return cjson.encode({status = "RELEASED", record = record})
else
    return cjson.encode({status = record.status, record = record})
end
"""


class ReservationState(str, enum.Enum):
    HELD = "HELD"
    PENDING_CONFIRMATION = "PENDING_CONFIRMATION"
    CONFIRMED = "CONFIRMED"
    RELEASED = "RELEASED"
    EXPIRED = "EXPIRED"
    PENDING_RECONCILIATION = "PENDING_RECONCILIATION"


# Architectural Alias
ReservationState.CONFIRMING = ReservationState.PENDING_CONFIRMATION


def _is_ambiguous_timeout(exc: Exception) -> bool:
    """Identifies ambiguous timeout and network partition errors during database reconciliation."""
    if isinstance(exc, TimeoutError):
        return True
    exc_type_name = type(exc).__name__.lower()
    if "timeout" in exc_type_name:
        return True
    return False


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

    Simulates a PostgreSQL durable relational database with row-level locking (SELECT FOR UPDATE),
    transactional order persistence, and idempotent reconciliation tracking.
    NOTE: This is an educational in-memory simulation component. In a production deployment,
    this would be an actual ACID-compliant RDBMS connection pool (e.g. asyncpg or psycopg)
    writing durably to Write-Ahead Logs (WAL) on disk.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.inventory: Dict[str, int] = {}
        self.orders: Dict[str, Dict[str, Any]] = {}
        self._reconciled_reservations: Dict[str, Any] = {}

    def set_initial_inventory(self, item_id: str, quantity: int) -> None:
        with self._lock:
            self.inventory[item_id] = quantity

    def reconcile_confirmed_order(self, item_id: str, reservation: ReservationRecord) -> bool:
        with self._lock:
            if reservation.reservation_id in self._reconciled_reservations:
                return True
            current = self.inventory.get(item_id, 0)
            if current < reservation.quantity:
                return False
            self.inventory[item_id] -= reservation.quantity
            order_data = asdict(reservation)
            order_data["item_id"] = item_id
            self.orders[reservation.reservation_id] = order_data
            self._reconciled_reservations[reservation.reservation_id] = order_data
            return True

    def get_order(self, reservation_id: str) -> Optional[Dict[str, Any]]:
        """Authoritative lookup of an order by reservation ID."""
        with self._lock:
            return self.orders.get(reservation_id)

    def has_order(self, reservation_id: str) -> bool:
        """Checks if the order was committed to the authoritative ledger."""
        with self._lock:
            return reservation_id in self.orders

    def cancel_order(self, reservation_id: str) -> bool:
        """Cancels an active confirmed order in the authoritative ledger and restores stock."""
        with self._lock:
            order = self.orders.pop(reservation_id, None)
            if order is None:
                return False
            item_id = order.get("item_id")
            quantity = order.get("quantity", 0)
            if item_id is not None and item_id in self.inventory:
                self.inventory[item_id] += quantity
            self._reconciled_reservations.pop(reservation_id, None)
            return True


# Alias for educational and workshop clarity
SimulatedPostgresLedger = PostgresInventoryStore


class FlashSaleInventoryService:
    """Educational Architecture Simulator & Reference Pattern: Flash Sale Inventory Service.

    Coordinates high-concurrency inventory reservation using Redis Cluster hash tags,
    Lua script atomic execution, and PostgreSQL authoritative reconciliation.

    Architectural Reality & Distributed Dual-Write Limitation:
    ----------------------------------------------------------
    Redis and PostgreSQL do not form one atomic transaction merely because the simulator
    reconciles their states sequentially. They reside on distinct network endpoints with
    independent durability, failover, and crash profiles. A failure or crash between
    committing in PostgreSQL and acknowledging in Redis creates intermediate states
    (PENDING_CONFIRMATION, PENDING_RECONCILIATION) that require strict state machine guards
    and authoritative reconciliation to prevent phantom stock restoration.

    NOTE: When redis_client is None, this service uses internal dictionaries
    (_stock_store, _reserves_store, _idemp_store, _expirations_store) as an educational in-memory
    Redis simulation for local testing and demonstration without requiring a running Redis cluster.
    """

    def __init__(
        self,
        postgres_db: PostgresInventoryStore,
        redis_client: Any = None,
    ) -> None:
        self.postgres_db = postgres_db
        self.redis = redis_client
        self._lock = threading.RLock()

        # In-memory cluster hash simulation
        self._stock_store: Dict[str, int] = {}
        self._reserves_store: Dict[str, Dict[str, ReservationRecord]] = {}
        self._idemp_store: Dict[str, Dict[str, str]] = {}
        self._expirations_store: Dict[str, Dict[str, float]] = {}
        self._res_to_item: Dict[str, str] = {}
        self.inconsistencies: List[Dict[str, Any]] = []
        self._rolled_back_reservations: Set[str] = set()

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

    def rollback_confirmation(
        self,
        item_id: str,
        reservation_id: Optional[str] = None,
    ) -> ReservationResult:
        """Rolls back a confirmation idempotently, restoring inventory at most once,
        enforcing the Rollback Invariant against the PostgreSQL authoritative ledger."""
        if reservation_id is None:
            res_id = item_id
            target_item_id = self._res_to_item.get(res_id)
            if target_item_id is None:
                for it_id, rmap in self._reserves_store.items():
                    if res_id in rmap:
                        target_item_id = it_id
                        break
            item_id = target_item_id or res_id
            reservation_id = res_id

        # Fast idempotent path: already rolled back
        if reservation_id in self._rolled_back_reservations:
            reserves_map = self._reserves_store.get(item_id, {})
            rec = reserves_map.get(reservation_id)
            return ReservationResult(
                success=True,
                status="RELEASED",
                record=rec,
                message="Reservation already rolled back",
            )

        # Ordinary rollback CANNOT release PENDING_CONFIRMATION or PENDING_RECONCILIATION!
        if self.redis is None:
            with self._lock:
                reserves_map = self._reserves_store.get(item_id, {})
                rec = reserves_map.get(reservation_id)
                if not rec:
                    return ReservationResult(success=False, status="NOT_FOUND")
                if rec.status == ReservationState.PENDING_CONFIRMATION:
                    return ReservationResult(
                        success=False,
                        status="PENDING_CONFIRMATION",
                        message="Cannot rollback reservation while confirmation is in-flight",
                        record=rec,
                    )
                if rec.status == ReservationState.PENDING_RECONCILIATION:
                    return ReservationResult(
                        success=False,
                        status="PENDING_RECONCILIATION",
                        message="Cannot rollback reservation pending reconciliation without authoritative ledger resolution",
                        record=rec,
                    )
        else:
            stock_k, reserves_k, _, _ = self._keys(item_id)
            rec_raw = self.redis.hget(reserves_k, reservation_id)
            if not rec_raw:
                return ReservationResult(success=False, status="NOT_FOUND")
            try:
                rec_json = json.loads(rec_raw)
                st = rec_json.get("status")
                if st == "PENDING_CONFIRMATION":
                    return ReservationResult(
                        success=False,
                        status="PENDING_CONFIRMATION",
                        message="Cannot rollback reservation while confirmation is in-flight",
                    )
                if st == "PENDING_RECONCILIATION":
                    return ReservationResult(
                        success=False,
                        status="PENDING_RECONCILIATION",
                        message="Cannot rollback reservation pending reconciliation without authoritative ledger resolution",
                    )
            except Exception:
                pass

        # Enforce Rollback Invariant: Check PostgreSQL!
        # A rollback CANNOT restore stock while leaving an active confirmed order in PostgreSQL.
        has_active_order = False
        try:
            if hasattr(self.postgres_db, "has_order"):
                has_active_order = self.postgres_db.has_order(reservation_id)
            elif hasattr(self.postgres_db, "get_order"):
                has_active_order = self.postgres_db.get_order(reservation_id) is not None
            elif hasattr(self.postgres_db, "orders"):
                has_active_order = reservation_id in self.postgres_db.orders
        except Exception as exc:
            if _is_ambiguous_timeout(exc):
                return ReservationResult(
                    success=False,
                    status="PENDING_RECONCILIATION",
                    message=f"Cannot rollback while PostgreSQL status is ambiguous (timeout): {exc}",
                )
            raise

        if has_active_order:
            cancelled = False
            if hasattr(self.postgres_db, "cancel_order"):
                try:
                    cancelled = self.postgres_db.cancel_order(reservation_id)
                except Exception:
                    cancelled = False
            if not cancelled:
                return ReservationResult(
                    success=False,
                    status="ACTIVE_ORDER_EXISTS",
                    message="Cannot rollback confirmation: active confirmed order exists in PostgreSQL and could not be cancelled",
                )

        stock_k, reserves_k, _, _ = self._keys(item_id)

        if self.redis is not None:
            raw = self.redis.eval(
                LUA_ROLLBACK_CONFIRMATION, 2, stock_k, reserves_k, reservation_id
            )
            data = json.loads(raw)
            if data.get("status") in ("NOT_FOUND", "ALREADY_ROLLED_BACK", "INVALID_STATE", "PENDING_RECONCILIATION", "PENDING_CONFIRMATION"):
                if data.get("status") == "ALREADY_ROLLED_BACK":
                    self._rolled_back_reservations.add(reservation_id)
                    return ReservationResult(
                        success=True,
                        status="RELEASED",
                        message="Reservation already rolled back",
                    )
                if data.get("status") == "PENDING_RECONCILIATION":
                    return ReservationResult(
                        success=False,
                        status="PENDING_RECONCILIATION",
                        message=data.get("message", "Cannot rollback reservation pending reconciliation without authoritative ledger resolution"),
                    )
                if data.get("status") == "PENDING_CONFIRMATION":
                    return ReservationResult(
                        success=False,
                        status="PENDING_CONFIRMATION",
                        message=data.get("message", "Cannot rollback reservation while confirmation is in-flight"),
                    )
                return ReservationResult(
                    success=False,
                    status=data["status"],
                    message=data.get("message", "Rollback failed"),
                )
            self._rolled_back_reservations.add(reservation_id)
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

            if rec.status == ReservationState.PENDING_RECONCILIATION:
                return ReservationResult(
                    success=False,
                    status="PENDING_RECONCILIATION",
                    message="Cannot rollback reservation pending reconciliation without authoritative ledger resolution",
                    record=rec,
                )

            if rec.status == ReservationState.PENDING_CONFIRMATION:
                return ReservationResult(
                    success=False,
                    status="PENDING_CONFIRMATION",
                    message="Cannot rollback reservation while confirmation is in-flight",
                    record=rec,
                )

            if rec.status not in (
                ReservationState.CONFIRMED,
                ReservationState.HELD,
            ):
                return ReservationResult(
                    success=False,
                    status="INVALID_STATE",
                    message=f"Cannot rollback reservation with status {rec.status.value}",
                    record=rec,
                )

            rec.status = ReservationState.RELEASED
            self._stock_store[stock_k] = self._stock_store.get(stock_k, 0) + rec.quantity
            self._expirations_store.get(item_id, {}).pop(reservation_id, None)
            self._rolled_back_reservations.add(reservation_id)
            return ReservationResult(success=True, status="RELEASED", record=rec)

    rollback = rollback_confirmation

    def reconcile_pending_reservation(
        self,
        item_id: str,
        reservation_id: Optional[str] = None,
        *,
        final_absence_confirmed: bool = False,
    ) -> ReservationResult:
        """Authoritative reconciliation flow for reservations in PENDING_RECONCILIATION.

        Educational Concurrency & Fault-Tolerance Contract:
        ---------------------------------------------------
        1. While database outcome is unknown (e.g. database still times out), keep reservation
           in PENDING_RECONCILIATION. Never release stock on a timeout.
        2. Query authoritative ledger by reservation_id.
        3. If order exists: mark reservation CONFIRMED without deducting stock again.
        4. If order is definitively absent and failure is known to be final: release hold exactly once
           and restore stock.
        5. If database query fails or outcome remains unknown: leave pending.
        6. Idempotent: repeated reconciliation attempts return consistent state without double-restoring stock.
        7. Ordinary rollback is prohibited from releasing pending reservations without authoritative resolution.
        """
        if reservation_id is None:
            res_id = item_id
            target_item_id = self._res_to_item.get(res_id)
            if target_item_id is None:
                for it_id, rmap in self._reserves_store.items():
                    if res_id in rmap:
                        target_item_id = it_id
                        break
            item_id = target_item_id or res_id
            reservation_id = res_id

        stock_k, reserves_k, _, _ = self._keys(item_id)

        # 1. Authoritative ledger lookup
        is_committed = False
        try:
            if hasattr(self.postgres_db, "has_order"):
                is_committed = self.postgres_db.has_order(reservation_id)
            elif hasattr(self.postgres_db, "get_order"):
                is_committed = self.postgres_db.get_order(reservation_id) is not None
            else:
                is_committed = reservation_id in getattr(self.postgres_db, "orders", {})
        except Exception as exc:
            if _is_ambiguous_timeout(exc):
                # Authoritative DB still timing out: outcome remains unknown!
                return ReservationResult(
                    success=False,
                    status="PENDING_RECONCILIATION",
                    message=f"PostgreSQL still unreachable: {exc}",
                )
            raise

        # 2. Redis execution
        if self.redis is not None:
            resolution = "CHECK"
            if is_committed:
                resolution = "CONFIRM"
            elif final_absence_confirmed:
                resolution = "RELEASE"

            raw = self.redis.eval(
                LUA_RECONCILE_PENDING,
                2,
                stock_k,
                reserves_k,
                reservation_id,
                resolution,
            )
            data = json.loads(raw)
            status = data.get("status")
            rec_data = data.get("record")
            rec = None
            if rec_data:
                rec = ReservationRecord(
                    reservation_id=rec_data["reservation_id"],
                    user_id=rec_data["user_id"],
                    quantity=rec_data["quantity"],
                    status=ReservationState(rec_data["status"]),
                    created_at=rec_data["created_at"],
                    expires_at=rec_data["expires_at"],
                )

            if status in ("CONFIRMED", "ALREADY_CONFIRMED"):
                return ReservationResult(
                    success=True,
                    status="CONFIRMED",
                    record=rec,
                    message="Reconciled: order confirmed in authoritative ledger",
                )
            elif status in ("RELEASED", "ALREADY_RELEASED"):
                self._rolled_back_reservations.add(reservation_id)
                return ReservationResult(
                    success=True,
                    status="RELEASED",
                    record=rec,
                    message="Reconciled: order absent, hold released and stock restored exactly once",
                )
            elif status == "PENDING_RECONCILIATION":
                return ReservationResult(
                    success=False,
                    status="PENDING_RECONCILIATION",
                    record=rec,
                    message="Reservation remains in PENDING_RECONCILIATION awaiting final resolution",
                )
            else:
                return ReservationResult(
                    success=False,
                    status=status,
                    record=rec,
                    message=data.get("message", "Reconciliation error"),
                )

        # 3. In-memory execution
        with self._lock:
            reserves_map = self._reserves_store.get(item_id, {})
            rec = reserves_map.get(reservation_id)
            if not rec:
                return ReservationResult(success=False, status="NOT_FOUND")

            # Idempotency checks
            if rec.status == ReservationState.CONFIRMED:
                return ReservationResult(
                    success=True,
                    status="CONFIRMED",
                    record=rec,
                    message="Reservation already confirmed",
                )
            if rec.status == ReservationState.RELEASED:
                return ReservationResult(
                    success=True,
                    status="RELEASED",
                    record=rec,
                    message="Reservation already released",
                )

            if rec.status not in (
                ReservationState.PENDING_RECONCILIATION,
                ReservationState.PENDING_CONFIRMATION,
            ):
                return ReservationResult(
                    success=False,
                    status="INVALID_STATE",
                    record=rec,
                    message=f"Cannot reconcile reservation in state {rec.status.value}",
                )

            if is_committed:
                rec.status = ReservationState.CONFIRMED
                return ReservationResult(
                    success=True,
                    status="CONFIRMED",
                    record=rec,
                    message="Reconciled: order confirmed in authoritative ledger",
                )
            elif final_absence_confirmed:
                rec.status = ReservationState.RELEASED
                self._stock_store[stock_k] = self._stock_store.get(stock_k, 0) + rec.quantity
                self._rolled_back_reservations.add(reservation_id)
                return ReservationResult(
                    success=True,
                    status="RELEASED",
                    record=rec,
                    message="Reconciled: order absent, hold released and stock restored exactly once",
                )
            else:
                return ReservationResult(
                    success=False,
                    status=rec.status.value,
                    record=rec,
                    message="Reservation remains pending awaiting final resolution",
                )

    def confirm(
        self,
        item_id: str,
        reservation_id: Optional[str] = None,
        now: Optional[float] = None,
    ) -> ReservationResult:
        """Transitions reservation from HELD to PENDING_CONFIRMATION, reconciles with PostgreSQL ledger,
        and transitions to CONFIRMED only upon PostgreSQL success."""
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
            # Phase 1: Atomically transition HELD -> PENDING_CONFIRMATION (removing from normal auto-expiry)
            raw = self.redis.eval(
                LUA_CONFIRM_RESERVATION,
                2,
                reserves_k,
                exp_k,
                reservation_id,
                now,
                "STAGE",
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
            # Phase 2: Reconcile against PostgreSQL authoritative ledger
            try:
                pg_success = self.postgres_db.reconcile_confirmed_order(item_id, rec)
            except Exception as exc:
                if _is_ambiguous_timeout(exc):
                    # Ambiguous timeout: do NOT blindly restore stock!
                    rec.status = ReservationState.PENDING_RECONCILIATION
                    rec_dict = asdict(rec)
                    rec_dict["status"] = "PENDING_RECONCILIATION"
                    self.redis.hset(reserves_k, reservation_id, json.dumps(rec_dict))
                    self.inconsistencies.append({
                        "reservation_id": reservation_id,
                        "item_id": item_id,
                        "error": str(exc),
                        "timestamp": now,
                        "status": "PENDING_RECONCILIATION",
                    })
                    return ReservationResult(
                        success=False,
                        status="PENDING_RECONCILIATION",
                        message=f"PostgreSQL reconciliation timeout: {exc}",
                        record=rec,
                    )
                # PostgreSQL fails (e.g. non-timeout error): transition to RELEASED and restore stock
                # Use authoritative reconciliation to compensate rather than rollback_confirmation
                rb_res = self.reconcile_pending_reservation(item_id, reservation_id, final_absence_confirmed=True)
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
                    record=rb_res.record or rec,
                )

            if not pg_success:
                # PostgreSQL fails (e.g. inventory exhausted in authoritative ledger):
                # use authoritative reconciliation to transition to RELEASED and restore stock
                rb_res = self.reconcile_pending_reservation(item_id, reservation_id, final_absence_confirmed=True)
                rec.status = ReservationState.RELEASED
                return ReservationResult(
                    success=False,
                    status="RECONCILIATION_FAILED",
                    message="PostgreSQL authoritative ledger reconciliation failed",
                    record=rb_res.record or rec,
                )

            # Phase 3: Only upon PostgreSQL success, transition PENDING_CONFIRMATION -> CONFIRMED
            self.redis.eval(
                LUA_CONFIRM_RESERVATION,
                2,
                reserves_k,
                exp_k,
                reservation_id,
                now,
                "COMMIT",
            )
            rec.status = ReservationState.CONFIRMED
            return ReservationResult(success=True, status="CONFIRMED", record=rec)

        # In-memory execution: Decouple Phase 1 (Stage) and Phase 2 (PostgreSQL call)
        # to allow concurrent operations to observe PENDING_CONFIRMATION without lock contention!
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

            # Check if reservation has expired by timestamp (strictly expired at now >= expires_at)
            if rec.status == ReservationState.HELD and now >= rec.expires_at:
                return ReservationResult(
                    success=False,
                    status="INVALID_STATE",
                    message="Status is EXPIRED",
                    record=rec,
                )

            # Phase 1: Atomically transition HELD -> PENDING_CONFIRMATION (removing from normal auto-expiry)
            rec.status = ReservationState.PENDING_CONFIRMATION
            self._expirations_store.get(item_id, {}).pop(reservation_id, None)

        # Phase 2: Attempt PostgreSQL authoritative ledger reconciliation (OUTSIDE LOCK)
        pg_success = False
        pg_exc = None
        try:
            pg_success = self.postgres_db.reconcile_confirmed_order(item_id, rec)
        except Exception as exc:
            pg_exc = exc

        # Phase 3: Transition state under lock based on PostgreSQL outcome
        with self._lock:
            if rec.status == ReservationState.CONFIRMED:
                return ReservationResult(success=True, status="CONFIRMED", record=rec)
            if rec.status == ReservationState.RELEASED:
                return ReservationResult(
                    success=False,
                    status="RECONCILIATION_FAILED",
                    message="Reservation already rolled back or released",
                    record=rec,
                )

            if pg_exc is not None:
                if _is_ambiguous_timeout(pg_exc):
                    # Ambiguous timeout: do NOT blindly restore stock!
                    rec.status = ReservationState.PENDING_RECONCILIATION
                    self.inconsistencies.append({
                        "reservation_id": reservation_id,
                        "item_id": item_id,
                        "error": str(pg_exc),
                        "timestamp": now,
                        "status": "PENDING_RECONCILIATION",
                    })
                    return ReservationResult(
                        success=False,
                        status="PENDING_RECONCILIATION",
                        message=f"PostgreSQL reconciliation timeout: {pg_exc}",
                        record=rec,
                    )
                # Crash / unhandled network error: transition to RELEASED and restore stock
                rec.status = ReservationState.RELEASED
                self._stock_store[stock_k] = self._stock_store.get(stock_k, 0) + rec.quantity
                self._rolled_back_reservations.add(reservation_id)
                self.inconsistencies.append({
                    "reservation_id": reservation_id,
                    "item_id": item_id,
                    "error": str(pg_exc),
                    "timestamp": now,
                })
                return ReservationResult(
                    success=False,
                    status="RECONCILIATION_FAILED",
                    message=f"PostgreSQL reconciliation error: {pg_exc}",
                    record=rec,
                )

            if not pg_success:
                # Reconcile failure: authoritative ledger exhausted; transition to RELEASED and restore stock
                rec.status = ReservationState.RELEASED
                self._stock_store[stock_k] = self._stock_store.get(stock_k, 0) + rec.quantity
                self._rolled_back_reservations.add(reservation_id)
                return ReservationResult(
                    success=False,
                    status="RECONCILIATION_FAILED",
                    message="PostgreSQL authoritative ledger reconciliation failed",
                    record=rec,
                )

            # Phase 3: Only upon PostgreSQL success, transition PENDING_CONFIRMATION -> CONFIRMED
            rec.status = ReservationState.CONFIRMED
            return ReservationResult(success=True, status="CONFIRMED", record=rec)

    def release(self, item_id: str, reservation_id: str) -> ReservationResult:
        """Manually releases HELD inventory and restores stock."""
        stock_k, reserves_k, _, exp_k = self._keys(item_id)
        if self.redis is not None:
            raw = self.redis.eval(
                LUA_RELEASE_RESERVATION, 3, stock_k, reserves_k, exp_k, reservation_id
            )
            data = json.loads(raw)
            if "status" in data and data["status"] in ("NOT_FOUND", "INVALID_STATE", "PENDING_CONFIRMATION", "PENDING_RECONCILIATION"):
                return ReservationResult(
                    success=False,
                    status=data["status"],
                    message=data.get("message", f"Status is {data.get('current_status')}"),
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

            if rec.status == ReservationState.PENDING_CONFIRMATION:
                return ReservationResult(
                    success=False,
                    status="PENDING_CONFIRMATION",
                    message="Cannot release reservation while confirmation is in-flight",
                    record=rec,
                )
            if rec.status == ReservationState.PENDING_RECONCILIATION:
                return ReservationResult(
                    success=False,
                    status="PENDING_RECONCILIATION",
                    message="Cannot release reservation pending reconciliation without authoritative ledger resolution",
                    record=rec,
                )

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

    release_reservation = release

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

    def reconcile_expired(
        self,
        item_id: Optional[str] = None,
        now: Optional[float] = None,
        batch_size: int = 100,
    ) -> int:
        """Alias / convenience method to reconcile expired reservations for a single item or across all tracked items."""
        if isinstance(item_id, (int, float)):
            now = float(item_id)
            item_id = None
        if item_id is not None:
            return self.reconcile_expired_reservations(item_id, now=now, batch_size=batch_size)
        if now is None:
            now = time.time()
        total_restored = 0
        with self._lock:
            all_items = set(list(self._expirations_store.keys()) + list(self._reserves_store.keys()))
        for it_id in all_items:
            total_restored += self.reconcile_expired_reservations(it_id, now=now, batch_size=batch_size)
        return total_restored


# Educational and architectural aliases
FlashSaleInventory = FlashSaleInventoryService


