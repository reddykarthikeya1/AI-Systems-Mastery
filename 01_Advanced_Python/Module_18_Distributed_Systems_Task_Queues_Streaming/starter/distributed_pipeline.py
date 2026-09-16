"""STARTER - Module 18: Distributed Systems Task Queues Streaming

Module 18 - A genuinely distributed task queue on Redis Streams.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_distributed_pipeline.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/distributed_pipeline.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
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
        # [Tier 1] Algorithm: Implement Job.to_wire adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_job_wire_roundtrip_preserves_nested_payload
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement Job.to_wire()")


    @classmethod
    def from_wire(cls, fields: dict[str, str], stream_id: str | None = None) -> Job:
        # [Tier 1] Algorithm: Normalize raw input data structure into typed
        #   domain representation.
        # HINTS:
        #  - Handle missing optional keys with sensible defaults (.get()
        #   pattern).
        #  - Coerce primitive data types safely and strip surrounding
        #   whitespace.
        # GRADES: test_job_wire_roundtrip_preserves_nested_payload
        # WARNING: Watch for unexpected null or None values in optional fields.
        raise NotImplementedError("Module 18: implement Job.from_wire()")



def derive_idempotency_key(task_type: str, payload: dict[str, Any]) -> str:
    """Stable key for a (task_type, payload) pair.

    ``sort_keys=True`` is essential: without it ``{"a":1,"b":2}`` and
    ``{"b":2,"a":1}`` hash differently and the same logical job is enqueued
    twice. The old implementation used ``str(payload)``, which had exactly that
    bug plus a dependence on dict insertion order.

    """
    # [Tier 2] Algorithm: Implement derive_idempotency_key adhering to the
    #   contract defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_idempotency_key_is_stable
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 18: implement derive_idempotency_key()")


class Broker(Protocol):
    """The transport. Swapping Redis for SQS/Kafka should only change this."""
    name: str

    def submit(self, job: Job) -> Job:
        ...


    def reserve(self, consumer: str, count: int, block_ms: int) -> list[Job]:
        ...


    def ack(self, job: Job) -> None:
        ...


    def retry(self, job: Job) -> None:
        ...


    def dead_letter(self, job: Job, error: str) -> None:
        ...


    def pending_count(self) -> int:
        ...


    def dead_letter_jobs(self) -> list[Job]:
        ...


    def reclaim_stalled(self, consumer: str, min_idle_ms: int) -> list[Job]:
        ...


    def purge(self) -> None:
        ...



class RedisStreamBroker:
    """At-least-once delivery over Redis Streams with a consumer group + DLQ."""
    name = "redis-streams"

    def __init__(
        self,
        url: str = "redis://localhost:6379/0",
        namespace: str = "m18",
        group: str = "workers",
    ) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_idempotency_key_is_stable
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.__init__()")


    def ping(self) -> bool:
        # [Tier 2] Algorithm: Implement RedisStreamBroker.ping adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_redis_group_creation_is_idempotent
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.ping()")


    def _ensure_group(self) -> None:
        """Create the consumer group, tolerating the 'already exists' race.

        ``mkstream=True`` creates the stream if it does not exist yet, which
        avoids a chicken-and-egg failure on a cold deployment.

        """
        # [Tier 2] Algorithm: Implement RedisStreamBroker._ensure_group adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_redis_group_creation_is_idempotent
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker._ensure_group()")


    def submit(self, job: Job) -> Job:
        """Enqueue a job, deduplicating on its idempotency key.

        ``SET NX`` is atomic, so two producers racing on the same key cannot
        both win. Doing this with GET-then-SET would be a textbook race.

        """
        # [Tier 2] Algorithm: Implement RedisStreamBroker.submit adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_submit_enqueues_a_pending_job
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.submit()")


    def reserve(self, consumer: str, count: int = 1, block_ms: int = 10) -> list[Job]:
        """Claim up to `count` messages for this consumer.

        ``">"`` means "messages never delivered to this group". Each message
        goes to exactly one consumer, and stays pending until XACK.

        """
        # [Tier 2] Algorithm: Implement RedisStreamBroker.reserve adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_job_wire_roundtrip_preserves_nested_payload
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.reserve()")


    def ack(self, job: Job) -> None:
        # [Tier 2] Algorithm: Implement RedisStreamBroker.ack adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_backoff_doubles
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.ack()")


    def retry(self, job: Job) -> None:
        """Ack the old delivery and re-enqueue with an incremented attempt count.

        Re-adding rather than leaving it pending gives us explicit control over
        backoff and keeps the pending list meaning "in flight right now".

        """
        # [Tier 2] Algorithm: Implement RedisStreamBroker.retry adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_idempotency_key_is_stable
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.retry()")


    def dead_letter(self, job: Job, error: str) -> None:
        """Move a permanently-failed job to the DLQ.

        A DLQ is not a bin; it is a queue of things a human must look at. Losing
        a poison message silently is how data disappears.

        """
        # [Tier 2] Algorithm: Implement RedisStreamBroker.dead_letter adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_worker_dead_letters_unknown_task_type
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.dead_letter()")


    def reclaim_stalled(self, consumer: str, min_idle_ms: int = 5_000) -> list[Job]:
        """Take over messages a dead worker never acknowledged.

        This is the crash-recovery path that makes delivery at-least-once. Set
        ``min_idle_ms`` above your longest legitimate processing time, or you
        will reclaim work that is still running and execute it twice.

        """
        # [Tier 2] Algorithm: Implement RedisStreamBroker.reclaim_stalled
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_unacked_job_can_be_reclaimed
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.reclaim_stalled()")


    def pending_count(self) -> int:
        # [Tier 2] Algorithm: Implement RedisStreamBroker.pending_count adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_reserved_job_is_pending_until_acked
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.pending_count()")


    def queue_depth(self) -> int:
        # [Tier 2] Algorithm: Implement RedisStreamBroker.queue_depth adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_redis_namespaces_are_isolated
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.queue_depth()")


    def dead_letter_jobs(self) -> list[Job]:
        # [Tier 2] Algorithm: Implement RedisStreamBroker.dead_letter_jobs
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_worker_dead_letters_unknown_task_type
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.dead_letter_jobs()")


    def purge(self) -> None:
        # [Tier 2] Algorithm: Implement RedisStreamBroker.purge adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_redis_reclaimed_job_can_be_completed
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement RedisStreamBroker.purge()")



class InMemoryBroker:
    """A single-process stand-in. **Explicitly NOT distributed.**

    It mimics the Streams semantics (pending set, ack, DLQ) closely enough to
    test worker logic, but it has no process boundary, no durability, and no
    crash recovery. Named honestly so nobody mistakes it for the real thing.

    """
    name = "memory-TESTDOUBLE"

    def __init__(self) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_idempotency_key_is_stable
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 18: implement InMemoryBroker.__init__()")


    def ping(self) -> bool:
        # [Tier 2] Algorithm: Implement InMemoryBroker.ping adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_redis_group_creation_is_idempotent
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.ping()")


    def submit(self, job: Job) -> Job:
        # [Tier 2] Algorithm: Implement InMemoryBroker.submit adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_submit_enqueues_a_pending_job
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.submit()")


    def reserve(self, consumer: str, count: int = 1, block_ms: int = 0) -> list[Job]:
        # [Tier 2] Algorithm: Implement InMemoryBroker.reserve adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_job_wire_roundtrip_preserves_nested_payload
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.reserve()")


    def ack(self, job: Job) -> None:
        # [Tier 2] Algorithm: Implement InMemoryBroker.ack adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_backoff_doubles
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.ack()")


    def retry(self, job: Job) -> None:
        # [Tier 2] Algorithm: Implement InMemoryBroker.retry adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_idempotency_key_is_stable
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.retry()")


    def dead_letter(self, job: Job, error: str) -> None:
        # [Tier 2] Algorithm: Implement InMemoryBroker.dead_letter adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_worker_dead_letters_unknown_task_type
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.dead_letter()")


    def reclaim_stalled(self, consumer: str, min_idle_ms: int = 5_000) -> list[Job]:
        # [Tier 2] Algorithm: Implement InMemoryBroker.reclaim_stalled adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_unacked_job_can_be_reclaimed
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.reclaim_stalled()")


    def pending_count(self) -> int:
        # [Tier 2] Algorithm: Implement InMemoryBroker.pending_count adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_reserved_job_is_pending_until_acked
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.pending_count()")


    def queue_depth(self) -> int:
        # [Tier 2] Algorithm: Implement InMemoryBroker.queue_depth adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_redis_namespaces_are_isolated
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.queue_depth()")


    def dead_letter_jobs(self) -> list[Job]:
        # [Tier 2] Algorithm: Implement InMemoryBroker.dead_letter_jobs adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_worker_dead_letters_unknown_task_type
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.dead_letter_jobs()")


    def purge(self) -> None:
        # [Tier 2] Algorithm: Implement InMemoryBroker.purge adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_redis_reclaimed_job_can_be_completed
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement InMemoryBroker.purge()")



def load_broker(url: str | None = None, namespace: str = "m18") -> Broker:
    """Return a Redis Streams broker when reachable, else the test double."""
    # [Tier 1] Algorithm: Normalize raw input data structure into typed domain
    #   representation.
    # HINTS:
    #  - Handle missing optional keys with sensible defaults (.get() pattern).
    #  - Coerce primitive data types safely and strip surrounding whitespace.
    # GRADES: test_redis_broker_is_selected_when_available
    # WARNING: Watch for unexpected null or None values in optional fields.
    raise NotImplementedError("Module 18: implement load_broker()")


class Producer:
    """Enqueues work. Knows nothing about how it is processed."""

    def __init__(self, broker: Broker) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_idempotency_key_is_stable
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 18: implement Producer.__init__()")


    def submit(
        self,
        task_type: str,
        payload: dict[str, Any],
        *,
        idempotency_key: str | None = None,
        max_attempts: int = 3,
    ) -> Job:
        # [Tier 2] Algorithm: Implement Producer.submit adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_submit_enqueues_a_pending_job
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement Producer.submit()")



def exponential_backoff(attempt: int, base: float = 0.05, cap: float = 5.0) -> float:
    """Delay before retry N. Doubling, capped.

    Production systems add **jitter** (a random factor) so that a thousand
    workers retrying a recovered dependency do not all hit it on the same tick -
    a thundering herd that re-breaks what just came back.

    """
    # [Tier 2] Algorithm: Implement exponential_backoff adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_backoff_doubles
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 18: implement exponential_backoff()")


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
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_idempotency_key_is_stable
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 18: implement Worker.__init__()")


    def register(self, task_type: str, handler: Callable[[dict[str, Any]], Any]) -> None:
        # [Tier 2] Algorithm: Implement Worker.register adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_worker_processes_a_job
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement Worker.register()")


    def run_once(self, count: int = 10, block_ms: int = 10) -> int:
        """Process one batch. Returns how many jobs were handled."""
        # [Tier 2] Algorithm: Coordinate execution pipeline, processing inputs
        #   and aggregating results.
        # HINTS:
        #  - Process items sequentially or in batches, applying transformations.
        #  - Track successes and errors separately for a clean summary.
        # GRADES: test_multiple_workers_share_the_queue
        # WARNING: Ensure exceptions from individual items do not crash the
        #   entire batch.
        raise NotImplementedError("Module 18: implement Worker.run_once()")


    def _process(self, job: Job) -> None:
        # [Tier 2] Algorithm: Coordinate execution pipeline, processing inputs
        #   and aggregating results.
        # HINTS:
        #  - Process items sequentially or in batches, applying transformations.
        #  - Track successes and errors separately for a clean summary.
        # GRADES: test_worker_processes_a_job
        # WARNING: Ensure exceptions from individual items do not crash the
        #   entire batch.
        raise NotImplementedError("Module 18: implement Worker._process()")


    def drain(self, max_batches: int = 50) -> None:
        """Run until the queue is empty or the batch budget is spent.

        The bound matters: a retrying job re-enters the queue, so an unbounded
        drain on a permanently-failing job would never return.

        """
        # [Tier 2] Algorithm: Implement Worker.drain adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_worker_drain_is_bounded
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 18: implement Worker.drain()")



def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_idempotency_key_is_stable
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 18: implement main()")


if __name__ == "__main__":
    main()
