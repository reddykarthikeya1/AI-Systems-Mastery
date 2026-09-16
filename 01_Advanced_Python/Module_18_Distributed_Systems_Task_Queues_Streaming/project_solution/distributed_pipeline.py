#!/usr/bin/env python3
"""Module 18 - A genuinely distributed task queue on Redis Streams.

The previous version of this file called its ``dict`` a
"DistributedPipelineBroker". A dict in one process is not distributed: it has no
process boundary, no persistence, no at-least-once delivery, and no way for a
second worker to participate. Nothing it demonstrated would survive contact
with a real deployment.

This version uses **Redis Streams**, which give you the four primitives that
actually make a queue a queue:

===========================  ==================================================
``XADD``                     append a message to the log (durable)
``XREADGROUP``               read as part of a *consumer group* - each message
                             goes to exactly one member
``XACK``                     acknowledge; until then the message is "pending"
``XAUTOCLAIM`` / ``XPENDING``  reclaim messages from a worker that died
===========================  ==================================================

Because unacknowledged messages stay pending, a crashed worker loses nothing:
another worker reclaims the message after a visibility timeout. That is
**at-least-once delivery**, and it is why your handlers must be idempotent.

Falls back to ``InMemoryBroker`` (clearly labelled as a test double) when no
Redis is reachable, so the tests still run on a bare checkout.

Run:  python distributed_pipeline.py
Redis: docker run -d -p 6379:6379 redis
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Protocol

# ===========================================================================
# Domain model
# ===========================================================================


class JobStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DEAD_LETTERED = "DEAD_LETTERED"
    DUPLICATE = "DUPLICATE"


@dataclass(slots=True)
class Job:
    """One unit of work travelling through the pipeline."""

    job_id: str
    task_type: str
    payload: dict[str, Any]
    idempotency_key: str
    status: JobStatus = JobStatus.PENDING
    attempts: int = 0
    max_attempts: int = 3
    result: Any = None
    error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    stream_id: str | None = None  # Redis message id, for XACK

    def to_wire(self) -> dict[str, str]:
        """Redis stream fields must be flat strings/bytes - so JSON the nesting."""
        return {
            "job_id": self.job_id,
            "task_type": self.task_type,
            "payload": json.dumps(self.payload),
            "idempotency_key": self.idempotency_key,
            "attempts": str(self.attempts),
            "max_attempts": str(self.max_attempts),
            "created_at": self.created_at,
        }

    @classmethod
    def from_wire(cls, fields: dict[str, str], stream_id: str | None = None) -> Job:
        return cls(
            job_id=fields["job_id"],
            task_type=fields["task_type"],
            payload=json.loads(fields["payload"]),
            idempotency_key=fields["idempotency_key"],
            attempts=int(fields.get("attempts", 0)),
            max_attempts=int(fields.get("max_attempts", 3)),
            created_at=fields.get("created_at", ""),
            stream_id=stream_id,
        )


def derive_idempotency_key(task_type: str, payload: dict[str, Any]) -> str:
    """Stable key for a (task_type, payload) pair.

    ``sort_keys=True`` is essential: without it ``{"a":1,"b":2}`` and
    ``{"b":2,"a":1}`` hash differently and the same logical job is enqueued
    twice. The old implementation used ``str(payload)``, which had exactly that
    bug plus a dependence on dict insertion order.
    """
    canonical = json.dumps({"t": task_type, "p": payload}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()[:32]


# ===========================================================================
# Broker interface
# ===========================================================================


class Broker(Protocol):
    """The transport. Swapping Redis for SQS/Kafka should only change this."""

    name: str

    def submit(self, job: Job) -> Job: ...
    def reserve(self, consumer: str, count: int, block_ms: int) -> list[Job]: ...
    def ack(self, job: Job) -> None: ...
    def retry(self, job: Job) -> None: ...
    def dead_letter(self, job: Job, error: str) -> None: ...
    def pending_count(self) -> int: ...
    def dead_letter_jobs(self) -> list[Job]: ...
    def reclaim_stalled(self, consumer: str, min_idle_ms: int) -> list[Job]: ...
    def purge(self) -> None: ...


# ===========================================================================
# Redis Streams broker
# ===========================================================================


class RedisStreamBroker:
    """At-least-once delivery over Redis Streams with a consumer group + DLQ."""

    name = "redis-streams"

    def __init__(
        self,
        url: str = "redis://localhost:6379/0",
        namespace: str = "m18",
        group: str = "workers",
    ) -> None:
        import redis

        self.stream = f"{namespace}:jobs"
        self.dlq_stream = f"{namespace}:dlq"
        self.seen_key = f"{namespace}:idempotency"
        self.group = group
        self._client = redis.Redis.from_url(
            url, decode_responses=True, socket_timeout=2.0, socket_connect_timeout=2.0
        )
        self._ensure_group()

    def ping(self) -> bool:
        try:
            return bool(self._client.ping())
        except Exception:
            return False

    def _ensure_group(self) -> None:
        """Create the consumer group, tolerating the 'already exists' race.

        ``mkstream=True`` creates the stream if it does not exist yet, which
        avoids a chicken-and-egg failure on a cold deployment.
        """
        try:
            self._client.xgroup_create(self.stream, self.group, id="0", mkstream=True)
        except Exception as exc:
            if "BUSYGROUP" not in str(exc):
                raise

    # -- producer ----------------------------------------------------------

    def submit(self, job: Job) -> Job:
        """Enqueue a job, deduplicating on its idempotency key.

        ``SET NX`` is atomic, so two producers racing on the same key cannot
        both win. Doing this with GET-then-SET would be a textbook race.
        """
        claimed = self._client.set(
            f"{self.seen_key}:{job.idempotency_key}", job.job_id, nx=True, ex=86_400
        )
        if not claimed:
            job.status = JobStatus.DUPLICATE
            return job
        job.stream_id = self._client.xadd(self.stream, job.to_wire())
        job.status = JobStatus.PENDING
        return job

    # -- consumer ----------------------------------------------------------

    def reserve(self, consumer: str, count: int = 1, block_ms: int = 10) -> list[Job]:
        """Claim up to `count` messages for this consumer.

        ``">"`` means "messages never delivered to this group". Each message
        goes to exactly one consumer, and stays pending until XACK.
        """
        response = self._client.xreadgroup(
            self.group, consumer, {self.stream: ">"}, count=count, block=block_ms
        )
        jobs: list[Job] = []
        for _stream, entries in response or []:
            for stream_id, fields in entries:
                jobs.append(Job.from_wire(fields, stream_id=stream_id))
        return jobs

    def ack(self, job: Job) -> None:
        if job.stream_id:
            self._client.xack(self.stream, self.group, job.stream_id)

    def retry(self, job: Job) -> None:
        """Ack the old delivery and re-enqueue with an incremented attempt count.

        Re-adding rather than leaving it pending gives us explicit control over
        backoff and keeps the pending list meaning "in flight right now".
        """
        self.ack(job)
        job.attempts += 1
        self._client.xadd(self.stream, job.to_wire())

    def dead_letter(self, job: Job, error: str) -> None:
        """Move a permanently-failed job to the DLQ.

        A DLQ is not a bin; it is a queue of things a human must look at. Losing
        a poison message silently is how data disappears.
        """
        self.ack(job)
        payload = job.to_wire()
        payload["error"] = error[:500]
        payload["failed_at"] = datetime.now(UTC).isoformat()
        self._client.xadd(self.dlq_stream, payload)

    def reclaim_stalled(self, consumer: str, min_idle_ms: int = 5_000) -> list[Job]:
        """Take over messages a dead worker never acknowledged.

        This is the crash-recovery path that makes delivery at-least-once. Set
        ``min_idle_ms`` above your longest legitimate processing time, or you
        will reclaim work that is still running and execute it twice.
        """
        try:
            _cursor, entries, _deleted = self._client.xautoclaim(
                self.stream, self.group, consumer, min_idle_time=min_idle_ms, count=50
            )
        except Exception:
            return []
        return [Job.from_wire(fields, stream_id=sid) for sid, fields in entries or []]

    def pending_count(self) -> int:
        try:
            return int(self._client.xpending(self.stream, self.group)["pending"])
        except Exception:
            return 0

    def queue_depth(self) -> int:
        try:
            return int(self._client.xlen(self.stream))
        except Exception:
            return 0

    def dead_letter_jobs(self) -> list[Job]:
        entries = self._client.xrange(self.dlq_stream)
        out: list[Job] = []
        for sid, fields in entries:
            job = Job.from_wire(fields, stream_id=sid)
            job.status = JobStatus.DEAD_LETTERED
            job.error = fields.get("error")
            out.append(job)
        return out

    def purge(self) -> None:
        for key in (self.stream, self.dlq_stream):
            self._client.delete(key)
        for key in self._client.scan_iter(match=f"{self.seen_key}:*", count=500):
            self._client.delete(key)
        self._ensure_group()


# ===========================================================================
# In-memory test double
# ===========================================================================


class InMemoryBroker:
    """A single-process stand-in. **Explicitly NOT distributed.**

    It mimics the Streams semantics (pending set, ack, DLQ) closely enough to
    test worker logic, but it has no process boundary, no durability, and no
    crash recovery. Named honestly so nobody mistakes it for the real thing.
    """

    name = "memory-TESTDOUBLE"

    def __init__(self) -> None:
        self._queue: list[Job] = []
        self._pending: dict[str, tuple[Job, float]] = {}
        self._dlq: list[Job] = []
        self._seen: dict[str, str] = {}
        self._counter = 0

    def ping(self) -> bool:
        return True

    def submit(self, job: Job) -> Job:
        if job.idempotency_key in self._seen:
            job.status = JobStatus.DUPLICATE
            return job
        self._seen[job.idempotency_key] = job.job_id
        self._counter += 1
        job.stream_id = f"{self._counter}-0"
        self._queue.append(job)
        job.status = JobStatus.PENDING
        return job

    def reserve(self, consumer: str, count: int = 1, block_ms: int = 0) -> list[Job]:
        taken: list[Job] = []
        while self._queue and len(taken) < count:
            job = self._queue.pop(0)
            assert job.stream_id
            self._pending[job.stream_id] = (job, time.monotonic())
            taken.append(job)
        return taken

    def ack(self, job: Job) -> None:
        if job.stream_id:
            self._pending.pop(job.stream_id, None)

    def retry(self, job: Job) -> None:
        self.ack(job)
        job.attempts += 1
        self._counter += 1
        job.stream_id = f"{self._counter}-0"
        self._queue.append(job)

    def dead_letter(self, job: Job, error: str) -> None:
        self.ack(job)
        job.status = JobStatus.DEAD_LETTERED
        job.error = error
        self._dlq.append(job)

    def reclaim_stalled(self, consumer: str, min_idle_ms: int = 5_000) -> list[Job]:
        cutoff = time.monotonic() - (min_idle_ms / 1000.0)
        stalled = [job for job, taken_at in self._pending.values() if taken_at <= cutoff]
        return stalled

    def pending_count(self) -> int:
        return len(self._pending)

    def queue_depth(self) -> int:
        return len(self._queue)

    def dead_letter_jobs(self) -> list[Job]:
        return list(self._dlq)

    def purge(self) -> None:
        self._queue.clear()
        self._pending.clear()
        self._dlq.clear()
        self._seen.clear()


def load_broker(url: str | None = None, namespace: str = "m18") -> Broker:
    """Return a Redis Streams broker when reachable, else the test double."""
    url = url or os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    try:
        broker = RedisStreamBroker(url=url, namespace=namespace)
        if broker.ping():
            return broker
    except Exception:
        pass
    return InMemoryBroker()


# ===========================================================================
# Producer / worker
# ===========================================================================


class Producer:
    """Enqueues work. Knows nothing about how it is processed."""

    def __init__(self, broker: Broker) -> None:
        self.broker = broker

    def submit(
        self,
        task_type: str,
        payload: dict[str, Any],
        *,
        idempotency_key: str | None = None,
        max_attempts: int = 3,
    ) -> Job:
        key = idempotency_key or derive_idempotency_key(task_type, payload)
        job = Job(
            job_id=f"job-{uuid.uuid4().hex[:10]}",
            task_type=task_type,
            payload=payload,
            idempotency_key=key,
            max_attempts=max_attempts,
        )
        return self.broker.submit(job)


def exponential_backoff(attempt: int, base: float = 0.05, cap: float = 5.0) -> float:
    """Delay before retry N. Doubling, capped.

    Production systems add **jitter** (a random factor) so that a thousand
    workers retrying a recovered dependency do not all hit it on the same tick -
    a thundering herd that re-breaks what just came back.
    """
    return min(cap, base * (2**attempt))


@dataclass
class WorkerStats:
    processed: int = 0
    succeeded: int = 0
    retried: int = 0
    dead_lettered: int = 0
    duplicates_skipped: int = 0


class Worker:
    """Pulls jobs, runs handlers, and enforces the retry/DLQ policy.

    Handlers must be **idempotent**. At-least-once delivery means any job can be
    delivered twice - a reclaim after a slow-but-alive worker, a network blip
    between processing and XACK. "Exactly once" is not available; idempotent
    handlers plus at-least-once is how real systems get the same result.
    """

    def __init__(self, broker: Broker, name: str = "worker-1") -> None:
        self.broker = broker
        self.name = name
        self.handlers: dict[str, Callable[[dict[str, Any]], Any]] = {}
        self.stats = WorkerStats()
        self._processed_keys: set[str] = set()

    def register(self, task_type: str, handler: Callable[[dict[str, Any]], Any]) -> None:
        self.handlers[task_type] = handler

    def run_once(self, count: int = 10, block_ms: int = 10) -> int:
        """Process one batch. Returns how many jobs were handled."""
        jobs = self.broker.reserve(self.name, count=count, block_ms=block_ms)
        for job in jobs:
            self._process(job)
        return len(jobs)

    def _process(self, job: Job) -> None:
        self.stats.processed += 1

        # Consumer-side idempotency: cheap insurance against double delivery.
        if job.idempotency_key in self._processed_keys:
            self.stats.duplicates_skipped += 1
            self.broker.ack(job)
            return

        handler = self.handlers.get(job.task_type)
        if handler is None:
            self.broker.dead_letter(job, f"no handler registered for {job.task_type!r}")
            self.stats.dead_lettered += 1
            return

        try:
            job.result = handler(job.payload)
        except Exception as exc:
            if job.attempts + 1 >= job.max_attempts:
                self.broker.dead_letter(job, f"{type(exc).__name__}: {exc}")
                self.stats.dead_lettered += 1
            else:
                time.sleep(exponential_backoff(job.attempts))
                self.broker.retry(job)
                self.stats.retried += 1
            return

        job.status = JobStatus.COMPLETED
        self._processed_keys.add(job.idempotency_key)
        self.broker.ack(job)
        self.stats.succeeded += 1

    def drain(self, max_batches: int = 50) -> None:
        """Run until the queue is empty or the batch budget is spent.

        The bound matters: a retrying job re-enters the queue, so an unbounded
        drain on a permanently-failing job would never return.
        """
        for _ in range(max_batches):
            if self.run_once() == 0:
                return


# ===========================================================================
# Demo
# ===========================================================================


def main() -> None:
    print("=" * 74)
    print("   MODULE 18 - DISTRIBUTED TASK QUEUE (Redis Streams)")
    print("=" * 74)

    broker = load_broker(namespace="m18demo")
    print(f"\n  broker: {broker.name}")
    if broker.name.startswith("memory"):
        print("  (no Redis reachable — start one:  docker run -d -p 6379:6379 redis)")
    broker.purge()

    producer = Producer(broker)
    worker = Worker(broker, name="worker-A")

    # ---- handlers --------------------------------------------------------
    def render_pdf(payload: dict[str, Any]) -> str:
        return f"rendered {payload['pages']}pp of {payload['name']!r}"

    flaky_calls = {"n": 0}

    def flaky_upload(payload: dict[str, Any]) -> str:
        flaky_calls["n"] += 1
        if flaky_calls["n"] < 3:  # fails twice, succeeds on the 3rd attempt
            raise ConnectionError("S3 timed out")
        return f"uploaded {payload['file']}"

    def always_broken(payload: dict[str, Any]) -> str:
        raise ValueError("corrupt payload - this will never succeed")

    worker.register("PDF_REPORT", render_pdf)
    worker.register("UPLOAD", flaky_upload)
    worker.register("POISON", always_broken)

    # ---- 1. happy path ---------------------------------------------------
    print("\n" + "-" * 74)
    print(" 1. SUBMIT AND PROCESS")
    print("-" * 74)
    producer.submit("PDF_REPORT", {"name": "Q3 Financials", "pages": 15})
    producer.submit("PDF_REPORT", {"name": "Annual Review", "pages": 42})
    print(f"\n  queue depth after 2 submits : {broker.queue_depth()}")  # type: ignore[attr-defined]
    worker.drain()
    print(f"  succeeded                   : {worker.stats.succeeded}")
    print(f"  pending (unacknowledged)    : {broker.pending_count()}")

    # ---- 2. idempotency --------------------------------------------------
    print("\n" + "-" * 74)
    print(" 2. IDEMPOTENT SUBMISSION (same payload twice)")
    print("-" * 74)
    first = producer.submit("PDF_REPORT", {"name": "Duplicate Me", "pages": 1})
    second = producer.submit("PDF_REPORT", {"name": "Duplicate Me", "pages": 1})
    reordered = producer.submit("PDF_REPORT", {"pages": 1, "name": "Duplicate Me"})
    print(f"\n  1st submit : {first.status.value}")
    print(f"  2nd submit : {second.status.value}")
    print(f"  reordered  : {reordered.status.value}   <- key sorting makes this a dup too")
    worker.drain()

    # ---- 3. retry with backoff -------------------------------------------
    print("\n" + "-" * 74)
    print(" 3. RETRY WITH EXPONENTIAL BACKOFF (fails twice, then succeeds)")
    print("-" * 74)
    producer.submit("UPLOAD", {"file": "video.mp4"}, max_attempts=5)
    worker.drain()
    print(f"\n  handler invocations : {flaky_calls['n']}")
    print(f"  retries             : {worker.stats.retried}")
    print(f"  succeeded           : {worker.stats.succeeded}")
    print(f"  backoff schedule    : {[round(exponential_backoff(i), 3) for i in range(5)]}")

    # ---- 4. dead-letter queue --------------------------------------------
    print("\n" + "-" * 74)
    print(" 4. DEAD-LETTER QUEUE (permanent failure)")
    print("-" * 74)
    producer.submit("POISON", {"data": "bad"}, max_attempts=2)
    producer.submit("UNKNOWN_TASK", {"x": 1})
    worker.drain()
    dlq = broker.dead_letter_jobs()
    print(f"\n  dead-lettered : {len(dlq)}")
    for job in dlq:
        print(f"    {job.task_type:<14} {job.error}")

    # ---- 5. crash recovery ------------------------------------------------
    print("\n" + "-" * 74)
    print(" 5. CRASH RECOVERY (at-least-once delivery)")
    print("-" * 74)
    broker.purge()
    producer.submit("PDF_REPORT", {"name": "Orphaned Job", "pages": 3})
    dead_worker = Worker(broker, name="worker-B-doomed")
    dead_worker.register("PDF_REPORT", render_pdf)
    reserved = broker.reserve("worker-B-doomed", count=1, block_ms=10)
    print(f"\n  worker-B reserved {len(reserved)} job then 'crashed' without acking")
    print(f"  pending (in flight)  : {broker.pending_count()}")
    reclaimed = broker.reclaim_stalled("worker-A", min_idle_ms=0)
    print(f"  worker-A reclaimed   : {len(reclaimed)} job(s)")
    print("  -> nothing was lost. This is why handlers must be idempotent.")

    print("\n" + "=" * 74)
    print(f"  final worker stats: {asdict(worker.stats)}")
    print("=" * 74)


if __name__ == "__main__":
    main()
