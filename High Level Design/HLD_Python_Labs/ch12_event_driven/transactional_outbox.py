"""Transactional Outbox Pattern with Concurrent Poller and SKIP LOCKED Semantics.

Problem:
--------
In microservices and event-driven systems, dual-write bugs occur when updating a
database and publishing an event to Kafka/RabbitMQ:
1. DB write succeeds, but network partition fails the message bus publish -> Data inconsistent.
2. Publish succeeds, but DB commit fails -> Ghost message published.

Solution:
---------
1. Transactional Outbox:
   Store both business entity changes AND the outgoing events in the SAME database
   transaction using standard ACID guarantees.
2. Asynchronous Dispatcher:
   A background poller reads pending events using:
       `SELECT * FROM outbox WHERE status = 'PENDING' FOR UPDATE SKIP LOCKED LIMIT batch_size`
   guaranteeing multiple parallel workers process disjoint event partitions without deadlocks.
3. At-Least-Once Delivery & Idempotent Consumer:
   Ensures reliable propagation even across worker crashes or restarts.
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

    def __init__(self, rdbms: SimulatedRDBMS) -> None:
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


class SimulatedRDBMS:
    """Thread-safe transactional database simulating ACID writes and SKIP LOCKED."""

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
        """Simulates:

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

    def __init__(self, db: SimulatedRDBMS) -> None:
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
        db: SimulatedRDBMS,
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


class IdempotentConsumer:
    """Downstream consumer deduplicating events by event_id."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.processed_ids: Set[str] = set()
        self.consumed_events: List[OutboxRecord] = []

    def handle(self, record: OutboxRecord, handler_fn: Callable[[OutboxRecord], None]) -> bool:
        with self._lock:
            if record.event_id in self.processed_ids:
                return False  # Deduplicated
            self.processed_ids.add(record.event_id)
            handler_fn(record)
            self.consumed_events.append(record)
            return True
