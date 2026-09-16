"""Module 18 starter - build the dimensional model yourself.

How to work here
----------------
The shipped tests in ``project_solution/`` are your specification. Run them from
*this* directory and they will import your code instead of the solution::

    cd starter
    python -m pytest ../project_solution/test_dimensional_engine.py -q

Every test should fail with ``NotImplementedError`` before you start. If any test
passes on an untouched starter, stop - the grading loop is broken and you are
being told your work is correct when it has not been done.

Order of attack
---------------
1. ``SurrogateKeyAllocator``  - two lines, gets you moving
2. ``DimensionVersion.covers`` - the inclusive-range predicate everything rests on
3. ``DimensionTable.upsert``   - the SCD2 core; expect this to take the longest
4. ``DimensionTable.lookup_as_of`` - the as-of join
5. ``FactTable.insert``        - grain enforcement
6. ``StarSchema.aggregate``    - the star join
7. ``MaterializedView``        - full refresh first, incremental second
8. ``PipelineDAG``             - Kahn's algorithm, then idempotency, then retries
9. ``WatermarkStore`` / ``Backfill`` - small, and a good place to finish

The trap in step 4
------------------
``lookup_as_of`` must return the version that was in effect on the given date,
which is *not* the same as the current version. If you implement it by returning
``current()``, most tests still pass and ``test_scd2_preserves_history`` fails.
That test is the whole module.
"""

from __future__ import annotations

import itertools
from collections import defaultdict
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from datetime import date
from typing import Any

END_OF_TIME = date(9999, 12, 31)


class DimensionalModelError(Exception):
    """Raised when a modelling invariant would be violated."""


class SurrogateKeyAllocator:
    """Monotonic integer keys, one independent sequence per dimension table."""

    def __init__(self) -> None:
        self._counters: dict[str, itertools.count] = {}

    def next_key(self, table: str) -> int:
        """Return the next key for ``table``, starting at 1."""
        raise NotImplementedError("TODO: allocate a monotonic key per table name")


@dataclass
class DimensionVersion:
    surrogate_key: int
    natural_key: str
    attributes: dict[str, Any]
    valid_from: date
    valid_to: date = END_OF_TIME
    is_current: bool = True

    def covers(self, when: date) -> bool:
        """True when ``when`` falls inside this version's validity range.

        Both bounds are inclusive. Getting this off by one day is the reason
        ``test_scd2_intervals_tile_the_timeline`` exists.
        """
        raise NotImplementedError("TODO: inclusive range check")


class DimensionTable:
    """A dimension with a declared SCD strategy (1 = overwrite, 2 = versioned)."""

    def __init__(
        self,
        name: str,
        scd_type: int = 2,
        tracked_attributes: set[str] | None = None,
        allocator: SurrogateKeyAllocator | None = None,
    ) -> None:
        # Reject an unsupported type here rather than at first write - a
        # constructor is the cheapest place to fail.
        raise NotImplementedError("TODO: validate scd_type and set up version storage")

    @property
    def rows(self) -> list[DimensionVersion]:
        """Every version, ordered by natural key then validity start."""
        raise NotImplementedError("TODO: flatten the per-key version lists")

    def current(self, natural_key: str) -> DimensionVersion | None:
        """The open version for this key, or None if the key is unknown."""
        raise NotImplementedError("TODO: find the version with is_current set")

    def lookup_as_of(self, natural_key: str, when: date) -> int | None:
        """The surrogate key in effect on ``when``. NOT the current key."""
        raise NotImplementedError("TODO: find the version whose range covers `when`")

    def version_count(self, natural_key: str) -> int:
        raise NotImplementedError("TODO: how many versions exist for this key")

    def upsert(self, natural_key: str, attributes: dict[str, Any], effective: date) -> int:
        """Apply one source row; return the surrogate key a fact should use.

        Cases to handle, in this order:
          * key unseen            -> insert the first version
          * no tracked change     -> update untracked attributes in place, no new version
          * scd_type == 1         -> overwrite in place, no new version
          * effective <= open row -> raise; late-arriving rows need a real correction path
          * otherwise             -> close the open row (valid_to = effective - 1 day,
                                     is_current = False) and open a new version
        """
        raise NotImplementedError("TODO: the SCD2 core - see the case list above")


@dataclass
class FactTable:
    name: str
    grain: tuple[str, ...]
    measures: tuple[str, ...]
    rows: list[dict[str, Any]] = field(default_factory=list)

    def insert(self, keys: dict[str, int], measures: dict[str, float], event_date: date) -> None:
        """Append one row, rejecting anything that violates the declared grain.

        Reject three things separately, with distinguishable messages: missing
        grain keys, keys outside the grain, and unknown measures.
        """
        raise NotImplementedError("TODO: validate against grain and measures, then append")


class StarSchema:
    def __init__(self, fact: FactTable) -> None:
        self.fact = fact
        self.dimensions: dict[str, DimensionTable] = {}

    def add_dimension(self, key_column: str, dimension: DimensionTable) -> None:
        """Attach a dimension, rejecting a key column absent from the fact grain."""
        raise NotImplementedError("TODO: validate key_column is in fact.grain")

    def aggregate(
        self,
        group_by: list[tuple[str, str]],
        measure: str,
        agg: str = "sum",
    ) -> dict[tuple[Any, ...], float]:
        """Group ``measure`` by ``(key_column, attribute)`` pairs.

        Resolve each fact row's surrogate keys back to dimension attributes, then
        reduce. Support sum, count, avg, min, max; reject anything else.
        """
        raise NotImplementedError("TODO: the star join, then group and reduce")


class MaterializedView:
    def __init__(
        self,
        name: str,
        source: StarSchema,
        definition: Callable[[StarSchema], dict],
        supports_incremental: bool = True,
    ) -> None:
        raise NotImplementedError("TODO: store the definition and the empty cache")

    @property
    def data(self) -> dict:
        """The cached result. Raise if it has never been refreshed."""
        raise NotImplementedError("TODO: return the cache or raise")

    @property
    def is_stale(self) -> bool:
        """True when the source has more (or fewer) fact rows than at last refresh."""
        raise NotImplementedError("TODO: compare current row count against the snapshot")

    def refresh(self) -> dict:
        """Full recompute."""
        raise NotImplementedError("TODO: recompute, snapshot the row count, count the refresh")

    def refresh_incremental(self, watermark: date) -> dict:
        """Recompute over rows after ``watermark`` and merge into the cache.

        Raise when ``supports_incremental`` is False - a non-additive measure
        cannot be merged from deltas, and quietly doing a full refresh instead
        breaks the caller's cost assumption.

        When there are no new rows, clear staleness *without* recomputing and
        without incrementing ``refresh_count``.
        """
        raise NotImplementedError("TODO: guard, compute the delta, merge additively")


@dataclass
class Task:
    name: str
    run: Callable[[dict[str, Any]], Any]
    depends_on: tuple[str, ...] = ()
    max_attempts: int = 1


class PipelineDAG:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._completed: set[tuple[str, str]] = set()
        self.attempts: dict[str, int] = defaultdict(int)
        self.skipped: list[str] = []

    def add_task(self, task: Task) -> None:
        raise NotImplementedError("TODO: register, rejecting a duplicate name")

    def topological_order(self) -> list[str]:
        """Kahn's algorithm. Raise on an unknown dependency or a cycle.

        Seed the queue in sorted order so the result is deterministic - otherwise
        the tests are testing dict iteration order.
        """
        raise NotImplementedError("TODO: Kahn's algorithm with cycle detection")

    def run(self, run_key: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run every task in dependency order.

        ``run_key`` scopes idempotency: a task already completed under this key is
        skipped and appended to ``self.skipped``. A task that exhausts
        ``max_attempts`` re-raises its last error and must NOT be marked complete,
        so the next run retries it. Downstream tasks must not run after an
        upstream failure.
        """
        raise NotImplementedError("TODO: order, skip-if-done, retry, re-raise")


class WatermarkStore:
    def __init__(self) -> None:
        self._marks: dict[str, date] = {}

    def get(self, source: str) -> date | None:
        raise NotImplementedError("TODO")

    def advance(self, source: str, observed: date) -> None:
        """Move the mark forward only. It must never go backwards."""
        raise NotImplementedError("TODO: monotonic advance")

    def extract(
        self,
        source: str,
        rows: list[dict[str, Any]],
        column: str = "updated_at",
    ) -> list[dict[str, Any]]:
        """Return rows newer than the mark, then advance to the max *observed*.

        Advancing to "now" instead skips anything written during the extract,
        permanently and silently.
        """
        raise NotImplementedError("TODO: filter, then advance to max(observed)")


class Backfill:
    def __init__(self, start: date, end: date, batch_days: int = 7) -> None:
        """Reject an inverted range and a batch size below 1."""
        raise NotImplementedError("TODO: validate and store the range")

    def batches(self) -> Iterator[tuple[date, date]]:
        """Yield inclusive (start, end) pairs tiling the range with no overlap."""
        raise NotImplementedError("TODO: walk the range in batch_days steps")

    @property
    def batch_count(self) -> int:
        raise NotImplementedError("TODO")
