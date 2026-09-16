"""Tests for Module 18 - the distributed task queue.

Every test runs twice: once against the in-memory test double, and once against
real Redis Streams when a server is reachable. That parametrisation is the point
- a broker abstraction you have only tested against a dict is an abstraction you
have not tested.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

import pytest
from distributed_pipeline import (
    InMemoryBroker,
    Job,
    JobStatus,
    Producer,
    RedisStreamBroker,
    Worker,
    derive_idempotency_key,
    exponential_backoff,
    load_broker,
)


def _redis_up() -> bool:
    try:
        return RedisStreamBroker(namespace="m18test").ping()
    except Exception:
        return False


REDIS_UP = _redis_up()
requires_redis = pytest.mark.skipif(
    not REDIS_UP,
    reason="no Redis on localhost:6379 - start one with: docker run -d -p 6379:6379 redis",
)

# Run the whole behavioural suite against both broker implementations.
BROKER_IDS = ["memory"] + (["redis"] if REDIS_UP else [])


@pytest.fixture(params=BROKER_IDS)
def broker(request: pytest.FixtureRequest) -> Iterator[Any]:
    if request.param == "redis":
        instance: Any = RedisStreamBroker(namespace=f"m18test_{time.monotonic_ns()}")
    else:
        instance = InMemoryBroker()
    instance.purge()
    yield instance
    instance.purge()


@pytest.fixture
def producer(broker: Any) -> Producer:
    return Producer(broker)


@pytest.fixture
def worker(broker: Any) -> Worker:
    return Worker(broker, name="test-worker")


# ===========================================================================
# 1. Idempotency key derivation
# ===========================================================================


def test_idempotency_key_is_stable() -> None:
    a = derive_idempotency_key("EMAIL", {"to": "a@b.c", "subject": "hi"})
    b = derive_idempotency_key("EMAIL", {"to": "a@b.c", "subject": "hi"})
    assert a == b


def test_idempotency_key_ignores_dict_ordering() -> None:
    """The bug in the old version: ``str(payload)`` depended on insertion order.

    Two producers building the same logical payload in a different order would
    enqueue the same job twice.
    """
    a = derive_idempotency_key("EMAIL", {"to": "a@b.c", "subject": "hi"})
    b = derive_idempotency_key("EMAIL", {"subject": "hi", "to": "a@b.c"})
    assert a == b


def test_idempotency_key_distinguishes_payloads() -> None:
    assert derive_idempotency_key("T", {"x": 1}) != derive_idempotency_key("T", {"x": 2})
    assert derive_idempotency_key("A", {"x": 1}) != derive_idempotency_key("B", {"x": 1})


def test_idempotency_key_handles_nesting() -> None:
    a = derive_idempotency_key("T", {"outer": {"inner": [1, 2, 3]}})
    b = derive_idempotency_key("T", {"outer": {"inner": [1, 2, 3]}})
    c = derive_idempotency_key("T", {"outer": {"inner": [3, 2, 1]}})
    assert a == b != c


# ===========================================================================
# 2. Job serialisation
# ===========================================================================


def test_job_wire_roundtrip_preserves_nested_payload() -> None:
    """Redis stream fields are flat strings, so nesting must survive JSON."""
    original = Job(
        job_id="j1",
        task_type="REPORT",
        payload={"name": "Q3", "pages": 15, "tags": ["a", "b"], "meta": {"x": 1}},
        idempotency_key="key1",
        attempts=2,
        max_attempts=5,
    )
    revived = Job.from_wire(original.to_wire(), stream_id="1-0")
    assert revived.payload == original.payload
    assert revived.attempts == 2
    assert revived.max_attempts == 5
    assert revived.stream_id == "1-0"


def test_job_wire_fields_are_all_strings() -> None:
    """A non-string value here is an XADD error at runtime, not import time."""
    wire = Job("j", "T", {"n": 1}, "k").to_wire()
    assert all(isinstance(v, str) for v in wire.values())


# ===========================================================================
# 3. Backoff
# ===========================================================================


def test_backoff_doubles() -> None:
    assert exponential_backoff(0, base=0.1) == pytest.approx(0.1)
    assert exponential_backoff(1, base=0.1) == pytest.approx(0.2)
    assert exponential_backoff(2, base=0.1) == pytest.approx(0.4)
    assert exponential_backoff(3, base=0.1) == pytest.approx(0.8)


def test_backoff_is_capped() -> None:
    """Unbounded doubling reaches hours by attempt 20. Always cap."""
    assert exponential_backoff(50, base=0.1, cap=5.0) == 5.0


def test_backoff_is_monotonic_until_the_cap() -> None:
    delays = [exponential_backoff(i, base=0.01, cap=1.0) for i in range(10)]
    assert delays == sorted(delays)


# ===========================================================================
# 4. Submit / reserve / ack
# ===========================================================================


def test_submit_enqueues_a_pending_job(producer: Producer) -> None:
    job = producer.submit("PDF", {"name": "report", "pages": 3})
    assert job.status is JobStatus.PENDING
    assert job.stream_id is not None
    assert job.idempotency_key


def test_reserve_returns_the_submitted_job(producer: Producer, broker: Any) -> None:
    producer.submit("PDF", {"name": "report"})
    reserved = broker.reserve("c1", count=5, block_ms=50)
    assert len(reserved) == 1
    assert reserved[0].task_type == "PDF"
    assert reserved[0].payload == {"name": "report"}


def test_reserved_job_is_pending_until_acked(producer: Producer, broker: Any) -> None:
    """The heart of at-least-once: unacked work is still owed."""
    producer.submit("PDF", {"name": "report"})
    reserved = broker.reserve("c1", count=1, block_ms=50)
    assert broker.pending_count() == 1
    broker.ack(reserved[0])
    assert broker.pending_count() == 0


def test_a_message_goes_to_exactly_one_consumer(producer: Producer, broker: Any) -> None:
    """Consumer-group semantics: two workers must not both get the same job."""
    producer.submit("PDF", {"n": 1})
    first = broker.reserve("consumer-a", count=10, block_ms=50)
    second = broker.reserve("consumer-b", count=10, block_ms=50)
    assert len(first) == 1
    assert len(second) == 0


def test_reserve_on_empty_queue_returns_nothing(broker: Any) -> None:
    assert broker.reserve("c1", count=5, block_ms=10) == []


def test_duplicate_submission_is_rejected(producer: Producer) -> None:
    first = producer.submit("PDF", {"name": "same"})
    second = producer.submit("PDF", {"name": "same"})
    assert first.status is JobStatus.PENDING
    assert second.status is JobStatus.DUPLICATE


def test_duplicate_detection_survives_key_reordering(producer: Producer) -> None:
    producer.submit("PDF", {"a": 1, "b": 2})
    dup = producer.submit("PDF", {"b": 2, "a": 1})
    assert dup.status is JobStatus.DUPLICATE


def test_explicit_idempotency_key_overrides_derivation(producer: Producer) -> None:
    a = producer.submit("PDF", {"n": 1}, idempotency_key="manual-key")
    b = producer.submit("PDF", {"n": 999}, idempotency_key="manual-key")
    assert a.status is JobStatus.PENDING
    assert b.status is JobStatus.DUPLICATE, "the caller's key must win"


# ===========================================================================
# 5. Worker processing
# ===========================================================================


def test_worker_processes_a_job(producer: Producer, worker: Worker) -> None:
    seen: list[dict[str, Any]] = []
    worker.register("PDF", lambda payload: seen.append(payload) or "done")
    producer.submit("PDF", {"name": "report"})
    worker.drain()
    assert seen == [{"name": "report"}]
    assert worker.stats.succeeded == 1


def test_worker_acks_successful_jobs(producer: Producer, worker: Worker, broker: Any) -> None:
    worker.register("PDF", lambda payload: "ok")
    producer.submit("PDF", {"n": 1})
    worker.drain()
    assert broker.pending_count() == 0, "a completed job must not stay pending"


def test_worker_dead_letters_unknown_task_type(
    producer: Producer, worker: Worker, broker: Any
) -> None:
    producer.submit("NO_HANDLER", {"n": 1})
    worker.drain()
    dlq = broker.dead_letter_jobs()
    assert len(dlq) == 1
    assert "no handler registered" in (dlq[0].error or "")
    assert worker.stats.dead_lettered == 1


def test_worker_retries_a_transient_failure(producer: Producer, worker: Worker) -> None:
    calls = {"n": 0}

    def flaky(payload: dict[str, Any]) -> str:
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("transient")
        return "ok"

    worker.register("FLAKY", flaky)
    producer.submit("FLAKY", {"n": 1}, max_attempts=5)
    worker.drain()
    assert calls["n"] == 3
    assert worker.stats.retried == 2
    assert worker.stats.succeeded == 1


def test_worker_dead_letters_after_max_attempts(
    producer: Producer, worker: Worker, broker: Any
) -> None:
    calls = {"n": 0}

    def always_fails(payload: dict[str, Any]) -> str:
        calls["n"] += 1
        raise ValueError("permanent")

    worker.register("POISON", always_fails)
    producer.submit("POISON", {"n": 1}, max_attempts=3)
    worker.drain()

    assert calls["n"] == 3, f"should try exactly max_attempts times, tried {calls['n']}"
    dlq = broker.dead_letter_jobs()
    assert len(dlq) == 1
    assert "ValueError" in (dlq[0].error or "")


def test_dead_lettered_job_is_not_left_pending(
    producer: Producer, worker: Worker, broker: Any
) -> None:
    """A DLQ'd job must be acked, or it will be reclaimed and retried forever."""
    worker.register("POISON", lambda p: (_ for _ in ()).throw(ValueError("bad")))
    producer.submit("POISON", {"n": 1}, max_attempts=1)
    worker.drain()
    assert broker.pending_count() == 0


def test_worker_skips_a_duplicate_delivery(producer: Producer, worker: Worker) -> None:
    """Consumer-side idempotency: the same key must not run the handler twice."""
    calls = {"n": 0}
    worker.register("TASK", lambda p: calls.__setitem__("n", calls["n"] + 1))

    job = producer.submit("TASK", {"n": 1})
    worker.drain()
    assert calls["n"] == 1

    # Simulate a redelivery of the identical job (a reclaim after a slow ack).
    replay = Job(
        job_id=job.job_id,
        task_type="TASK",
        payload={"n": 1},
        idempotency_key=job.idempotency_key,
    )
    worker._process(replay)
    assert calls["n"] == 1, "handler must not run twice for one idempotency key"
    assert worker.stats.duplicates_skipped == 1


def test_worker_drain_is_bounded(producer: Producer, worker: Worker) -> None:
    """A permanently-retrying job must not spin forever."""
    worker.register("FOREVER", lambda p: (_ for _ in ()).throw(ConnectionError("nope")))
    producer.submit("FOREVER", {"n": 1}, max_attempts=1000)
    worker.drain(max_batches=3)  # must return, not hang
    assert worker.stats.processed <= 4


def test_multiple_workers_share_the_queue(producer: Producer, broker: Any) -> None:
    """Horizontal scaling: N workers must partition the work, not duplicate it."""
    for i in range(6):
        producer.submit("TASK", {"i": i})

    handled: list[int] = []
    workers = [Worker(broker, name=f"w{n}") for n in range(3)]
    for w in workers:
        w.register("TASK", lambda p: handled.append(p["i"]))
    for _ in range(6):
        for w in workers:
            w.run_once(count=1)

    assert sorted(handled) == list(range(6)), "each job exactly once across workers"


# ===========================================================================
# 6. Crash recovery
# ===========================================================================


def test_unacked_job_can_be_reclaimed(producer: Producer, broker: Any) -> None:
    """The crash-recovery path that makes delivery at-least-once."""
    producer.submit("PDF", {"name": "orphan"})
    reserved = broker.reserve("doomed-worker", count=1, block_ms=50)
    assert len(reserved) == 1
    assert broker.pending_count() == 1

    # 'doomed-worker' dies here without acking.
    reclaimed = broker.reclaim_stalled("rescue-worker", min_idle_ms=0)
    assert len(reclaimed) == 1
    assert reclaimed[0].payload == {"name": "orphan"}


def test_reclaim_ignores_recently_delivered_jobs(producer: Producer, broker: Any) -> None:
    """A visibility timeout below your processing time causes double execution."""
    producer.submit("PDF", {"name": "in-progress"})
    broker.reserve("busy-worker", count=1, block_ms=50)
    reclaimed = broker.reclaim_stalled("thief", min_idle_ms=60_000)
    assert reclaimed == [], "must not steal work that is still legitimately running"


@requires_redis
def test_redis_reclaimed_job_can_be_completed() -> None:
    """End-to-end recovery on real Redis: reclaim, process, ack."""
    broker = RedisStreamBroker(namespace=f"m18test_recover_{time.monotonic_ns()}")
    broker.purge()
    try:
        Producer(broker).submit("PDF", {"name": "orphan"})
        broker.reserve("doomed", count=1, block_ms=50)

        rescue = Worker(broker, name="rescue")
        rescue.register("PDF", lambda p: f"recovered {p['name']}")
        for job in broker.reclaim_stalled("rescue", min_idle_ms=0):
            rescue._process(job)

        assert rescue.stats.succeeded == 1
        assert broker.pending_count() == 0
    finally:
        broker.purge()


# ===========================================================================
# 7. Redis-specific guarantees
# ===========================================================================


@requires_redis
def test_redis_broker_is_selected_when_available() -> None:
    assert load_broker(namespace=f"m18test_sel_{time.monotonic_ns()}").name == "redis-streams"


def test_unreachable_redis_falls_back_to_the_test_double() -> None:
    broker = load_broker(url="redis://127.0.0.1:6391/0")
    assert broker.name.startswith("memory")


@requires_redis
def test_redis_namespaces_are_isolated() -> None:
    a = RedisStreamBroker(namespace=f"m18test_a_{time.monotonic_ns()}")
    b = RedisStreamBroker(namespace=f"m18test_b_{time.monotonic_ns()}")
    a.purge()
    b.purge()
    try:
        Producer(a).submit("TASK", {"n": 1})
        assert a.queue_depth() == 1
        assert b.queue_depth() == 0, "one namespace must not see another's jobs"
    finally:
        a.purge()
        b.purge()


@requires_redis
def test_redis_group_creation_is_idempotent() -> None:
    """Two workers starting simultaneously both call XGROUP CREATE - BUSYGROUP."""
    namespace = f"m18test_group_{time.monotonic_ns()}"
    first = RedisStreamBroker(namespace=namespace)
    second = RedisStreamBroker(namespace=namespace)  # must not raise
    assert first.ping() and second.ping()
    first.purge()


@requires_redis
def test_redis_job_survives_a_new_broker_instance() -> None:
    """Durability: the queue lives in Redis, not in the Python process."""
    namespace = f"m18test_durable_{time.monotonic_ns()}"
    writer = RedisStreamBroker(namespace=namespace)
    writer.purge()
    try:
        Producer(writer).submit("PDF", {"name": "persisted"})
        del writer

        reader = RedisStreamBroker(namespace=namespace)
        reserved = reader.reserve("fresh-process", count=1, block_ms=100)
        assert len(reserved) == 1
        assert reserved[0].payload == {"name": "persisted"}
        reader.purge()
    except Exception:
        RedisStreamBroker(namespace=namespace).purge()
        raise
