"""Transactional Outbox Pattern with Concurrent Poller, SKIP LOCKED Semantics, and Consumer Inbox.

Problem:
--------
In microservices and event-driven architectures, dual-write bugs occur when updating a
database and publishing an event to a message broker (e.g., Kafka, RabbitMQ):
1. DB write succeeds, but network partition fails the message bus publish -> Inconsistent state.
2. Publish succeeds, but DB commit fails -> Ghost message published for phantom transaction.

Solution:
---------
1. Transactional Outbox:
   Store business aggregate changes AND the outgoing events in the SAME database
   transaction using ACID guarantees.
2. Asynchronous Poller Worker:
   A background process claims pending events using PostgreSQL:
       `SELECT * FROM outbox WHERE status = 'PENDING' FOR UPDATE SKIP LOCKED LIMIT batch_size`
   guaranteeing multiple parallel workers process disjoint partitions without lock contention or deadlocks.
3. At-Least-Once Delivery & Idempotent Consumer Inbox:
   Because network retries can deliver duplicate messages, downstream consumers record
   processed event IDs in an `inbox` table within their own local transactions, achieving
   effectively exactly-once business processing.
"""

from __future__ import annotations
import copy
import enum
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set


class OutboxStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_FLIGHT = "IN_FLIGHT"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"


class InboxStatus(str, enum.Enum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


@dataclass
class OutboxRecord:
    event_id: str
    aggregate_type: str
    aggregate_id: str
    event_type: str
    payload: Dict[str, Any]
    status: OutboxStatus = OutboxStatus.PENDING
    retry_count: int = 0
    created_at: float = field(default_factory=time.time)
    locked_by: Optional[str] = None
    locked_until: Optional[float] = None


class RDBMSTransaction:
    """Represents an active ACID database transaction."""

    def __init__(self, rdbms: InMemoryOutboxSimulator) -> None:
        self.rdbms = rdbms
        self.entities_buffer: Dict[str, Dict[str, Any]] = {}
        self.outbox_buffer: List[OutboxRecord] = []
        self.active = True

    def save_entity(self, table: str, entity_id: str, data: Dict[str, Any]) -> None:
        if not self.active:
            raise RuntimeError("Cannot write to closed transaction")
        key = f"{table}:{entity_id}"
        self.entities_buffer[key] = copy.deepcopy(data)

    def append_outbox(
        self,
        aggregate_type: str,
        aggregate_id: str,
        event_type: str,
        payload: Dict[str, Any],
    ) -> OutboxRecord:
        if not self.active:
            raise RuntimeError("Cannot write to closed transaction")
        rec = OutboxRecord(
            event_id=str(uuid.uuid4()),
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload=copy.deepcopy(payload),
        )
        self.outbox_buffer.append(rec)
        return rec

    def commit(self) -> None:
        if not self.active:
            raise RuntimeError("Transaction already closed")
        self.rdbms._commit_transaction(self)
        self.active = False

    def rollback(self) -> None:
        self.active = False
        self.entities_buffer.clear()
        self.outbox_buffer.clear()

    def __enter__(self) -> RDBMSTransaction:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()
        else:
            if self.active:
                self.commit()


class InMemoryOutboxSimulator:
    """Thread-safe transactional database simulating ACID writes and SKIP LOCKED concurrency.

    NOTE: This is an in-memory testing simulator. For production PostgreSQL,
    refer to `PostgresTransactionalOutbox`.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.outbox_table: Dict[str, OutboxRecord] = {}

    def begin(self) -> RDBMSTransaction:
        return RDBMSTransaction(self)

    def _commit_transaction(self, tx: RDBMSTransaction) -> None:
        with self._lock:
            # Atomic commit of both entity records and outbox records
            for key, val in tx.entities_buffer.items():
                self.entities[key] = val
            for rec in tx.outbox_buffer:
                self.outbox_table[rec.event_id] = rec

    def get_entity(self, table: str, entity_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            key = f"{table}:{entity_id}"
            return copy.deepcopy(self.entities.get(key))

    def fetch_pending_skip_locked(
        self, worker_id: str, batch_size: int = 10, lock_timeout_seconds: float = 30.0
    ) -> List[OutboxRecord]:
        """Simulates PostgreSQL:

        SELECT * FROM outbox
        WHERE status = 'PENDING' OR (status = 'IN_FLIGHT' AND locked_until < NOW())
        ORDER BY created_at ASC
        FOR UPDATE SKIP LOCKED
        LIMIT batch_size
        """
        now = time.time()
        claimed: List[OutboxRecord] = []

        with self._lock:
            for rec in self.outbox_table.values():
                if len(claimed) >= batch_size:
                    break

                is_available = (
                    rec.status == OutboxStatus.PENDING
                    or (
                        rec.status == OutboxStatus.IN_FLIGHT
                        and rec.locked_until is not None
                        and rec.locked_until < now
                    )
                )

                if is_available:
                    # Claim / lock the record atomically for this worker
                    rec.status = OutboxStatus.IN_FLIGHT
                    rec.locked_by = worker_id
                    rec.locked_until = now + lock_timeout_seconds
                    claimed.append(copy.deepcopy(rec))

        return claimed

    def mark_published(self, event_id: str) -> None:
        with self._lock:
            if event_id in self.outbox_table:
                rec = self.outbox_table[event_id]
                rec.status = OutboxStatus.PUBLISHED
                rec.locked_by = None
                rec.locked_until = None

    def mark_failed(self, event_id: str, max_retries: int = 3) -> None:
        with self._lock:
            if event_id in self.outbox_table:
                rec = self.outbox_table[event_id]
                rec.retry_count += 1
                rec.locked_by = None
                rec.locked_until = None
                if rec.retry_count >= max_retries:
                    rec.status = OutboxStatus.FAILED
                else:
                    rec.status = OutboxStatus.PENDING


# Backwards compatibility alias
SimulatedRDBMS = InMemoryOutboxSimulator


class PostgresTransactionalOutbox:
    """Production PostgreSQL Reference Implementation for Transactional Outbox.

    Demonstrates exact SQL schemas, transaction boundaries, and SKIP LOCKED mechanics.
    """

    SCHEMA_SQL = """
    CREATE TABLE IF NOT EXISTS outbox_events (
        event_id UUID PRIMARY KEY,
        aggregate_type VARCHAR(64) NOT NULL,
        aggregate_id VARCHAR(64) NOT NULL,
        event_type VARCHAR(64) NOT NULL,
        payload JSONB NOT NULL,
        status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
        retry_count INT NOT NULL DEFAULT 0,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        locked_by VARCHAR(64),
        locked_until TIMESTAMPTZ
    );

    CREATE INDEX IF NOT EXISTS idx_outbox_pending 
    ON outbox_events (created_at ASC) 
    WHERE status = 'PENDING';
    """

    CLAIM_SQL = """
    WITH claimable AS (
        SELECT event_id
        FROM outbox_events
        WHERE status = 'PENDING'
           OR (status = 'IN_FLIGHT' AND locked_until < NOW())
        ORDER BY created_at ASC
        FOR UPDATE SKIP LOCKED
        LIMIT %(batch_size)s
    )
    UPDATE outbox_events
    SET status = 'IN_FLIGHT',
        locked_by = %(worker_id)s,
        locked_until = NOW() + (%(lock_timeout)s || ' seconds')::INTERVAL
    FROM claimable
    WHERE outbox_events.event_id = claimable.event_id
    RETURNING outbox_events.*;
    """

    MARK_PUBLISHED_SQL = """
    UPDATE outbox_events
    SET status = 'PUBLISHED',
        locked_by = NULL,
        locked_until = NULL
    WHERE event_id = %(event_id)s;
    """

    MARK_FAILED_SQL = """
    UPDATE outbox_events
    SET retry_count = retry_count + 1,
        locked_by = NULL,
        locked_until = NULL,
        status = CASE 
            WHEN retry_count + 1 >= %(max_retries)s THEN 'FAILED'
            ELSE 'PENDING'
        END
    WHERE event_id = %(event_id)s;
    """

    @staticmethod
    def append_in_transaction(
        cursor: Any,
        aggregate_type: str,
        aggregate_id: str,
        event_type: str,
        payload_json: str,
        event_id: Optional[str] = None,
    ) -> str:
        """Appends an outbox record within the caller's active database transaction."""
        eid = event_id or str(uuid.uuid4())
        sql = """
        INSERT INTO outbox_events (event_id, aggregate_type, aggregate_id, event_type, payload)
        VALUES (%s, %s, %s, %s, %s::jsonb);
        """
        cursor.execute(sql, (eid, aggregate_type, aggregate_id, event_type, payload_json))
        return eid


class MessageBus:
    """Simulated resilient message broker (Kafka/RabbitMQ)."""

    def __init__(self, failure_rate: float = 0.0) -> None:
        self._lock = threading.Lock()
        self.published_events: List[OutboxRecord] = []
        self.dlq: List[OutboxRecord] = []
        self.failure_rate = failure_rate

    def publish(self, record: OutboxRecord) -> bool:
        with self._lock:
            if self.failure_rate > 0:
                import random
                if random.random() < self.failure_rate:
                    return False
            self.published_events.append(copy.deepcopy(record))
            return True

    def send_to_dlq(self, record: OutboxRecord) -> None:
        with self._lock:
            self.dlq.append(copy.deepcopy(record))


class TransactionalOutboxRepository:
    """Application service coordinating business logic with transactional outbox."""

    def __init__(self, db: InMemoryOutboxSimulator) -> None:
        self.db = db

    def create_order(self, order_id: str, customer_id: str, amount: float) -> str:
        with self.db.begin() as tx:
            # 1. Update business aggregate
            order_data = {
                "order_id": order_id,
                "customer_id": customer_id,
                "amount": amount,
                "status": "CREATED",
            }
            tx.save_entity("orders", order_id, order_data)

            # 2. Record outbox event in same transaction
            event = tx.append_outbox(
                aggregate_type="Order",
                aggregate_id=order_id,
                event_type="OrderCreated",
                payload={"order_id": order_id, "amount": amount},
            )
            return event.event_id


class OutboxPollerWorker:
    """Background worker continuously pulling events using SKIP LOCKED."""

    def __init__(
        self,
        worker_id: str,
        db: InMemoryOutboxSimulator,
        bus: MessageBus,
        batch_size: int = 5,
        max_retries: int = 3,
    ) -> None:
        self.worker_id = worker_id
        self.db = db
        self.bus = bus
        self.batch_size = batch_size
        self.max_retries = max_retries

    def poll_and_dispatch(self) -> int:
        """Poll one batch of events, publish to bus, and acknowledge."""
        records = self.db.fetch_pending_skip_locked(self.worker_id, self.batch_size)
        dispatched_count = 0
        for rec in records:
            success = self.bus.publish(rec)
            if success:
                self.db.mark_published(rec.event_id)
                dispatched_count += 1
            else:
                self.db.mark_failed(rec.event_id, self.max_retries)
                if rec.retry_count + 1 >= self.max_retries:
                    self.bus.send_to_dlq(rec)
        return dispatched_count


class IdempotentConsumerInbox:
    """Idempotent Consumer Inbox protecting downstream processing from duplicate events.

    In at-least-once messaging systems, network retries or worker crashes cause duplicate
    delivery of identical messages. The Inbox pattern ensures that each event_id is
    processed strictly once.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # event_id -> {"status": InboxStatus, "result": Any, "updated_at": float}
        self.inbox: Dict[str, Dict[str, Any]] = {}
        self.duplicate_count = 0

    def process(
        self,
        event_id: str,
        handler: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Tuple[bool, Any]:
        """Atomically deduplicate and execute handler.

        Returns:
            (executed: bool, result: Any)
            - executed=True: First-time processing succeeded; result contains return value.
            - executed=False: Duplicate detected and rejected; result contains previous result or None.
        """
        with self._lock:
            existing = self.inbox.get(event_id)
            if existing is not None:
                if existing["status"] == InboxStatus.PROCESSED:
                    self.duplicate_count += 1
                    return False, existing["result"]
                elif existing["status"] == InboxStatus.PROCESSING:
                    # Concurrent duplicate in-flight; reject duplicate execution
                    self.duplicate_count += 1
                    return False, None
                elif existing["status"] == InboxStatus.FAILED:
                    # Allow retry for previously failed events
                    pass

            # Mark as PROCESSING under lock
            self.inbox[event_id] = {
                "status": InboxStatus.PROCESSING,
                "result": None,
                "updated_at": time.time(),
            }

        try:
            result = handler(*args, **kwargs)
            with self._lock:
                self.inbox[event_id] = {
                    "status": InboxStatus.PROCESSED,
                    "result": copy.deepcopy(result),
                    "updated_at": time.time(),
                }
            return True, result
        except Exception:
            with self._lock:
                self.inbox[event_id] = {
                    "status": InboxStatus.FAILED,
                    "result": None,
                    "updated_at": time.time(),
                }
            raise


class IdempotentConsumer:
    """Downstream consumer deduplicating events by event_id."""

    def __init__(self) -> None:
        self.inbox = IdempotentConsumerInbox()
        self.consumed_events: List[OutboxRecord] = []
        self._lock = threading.Lock()

    @property
    def processed_ids(self) -> Set[str]:
        with self.inbox._lock:
            return {
                eid
                for eid, entry in self.inbox.inbox.items()
                if entry["status"] == InboxStatus.PROCESSED
            }

    def handle(self, record: OutboxRecord, handler_fn: Callable[[OutboxRecord], None]) -> bool:
        executed, _ = self.inbox.process(record.event_id, handler_fn, record)
        if executed:
            with self._lock:
                self.consumed_events.append(record)
        return executed
