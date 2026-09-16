"""Module 18 - Dimensional modelling and pipeline orchestration (Track A: internals).

This is an **in-process model**, not a warehouse. Everything lives in Python
dicts and lists so each mechanism can be read, stepped through and modified.
Track B (``warehouse_live.py``) runs the same logic against real DuckDB, and a
reconciliation test asserts the two agree - which is what turns this model from
a toy into a verified one.

What is actually built here
---------------------------
``SurrogateKeyAllocator``  monotonic keys, decoupled from the source system
``DimensionTable``         SCD Type 1 (overwrite) and Type 2 (versioned rows)
``FactTable``              append-only measures at one declared grain
``StarSchema``             the star join, run as an aggregation over dim + fact
``MaterializedView``       full and watermark-incremental refresh, staleness
``PipelineDAG``            topological execution, cycle detection, idempotency
``Backfill``               bounded batches over a date range

The one idea worth the whole module
-----------------------------------
A fact row must join to the dimension version that was current **when the event
happened**, not to the version that is current now. Get this wrong and every
historical report silently restates itself whenever a dimension changes - a
customer who moves from Ohio to Texas retroactively moves last year's revenue
with them. ``DimensionTable.lookup_as_of`` is the mechanism that prevents it,
and ``test_scd2_preserves_history`` is the test that proves it.
"""

from __future__ import annotations

import itertools
from collections import defaultdict, deque
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

# Sentinel end-date for the currently-active SCD2 version. A real warehouse uses
# 9999-12-31 for exactly this reason: it keeps ``valid_to`` NOT NULL so range
# predicates need no special case for the open interval.
END_OF_TIME = date(9999, 12, 31)


class DimensionalModelError(Exception):
    """Raised when a modelling invariant would be violated."""


# ---------------------------------------------------------------------------
# Surrogate keys
# ---------------------------------------------------------------------------
class SurrogateKeyAllocator:
    """Hands out monotonic integer keys, one sequence per dimension.

    Why not just use the source system's natural key? Three reasons, and all of
    them bite in production:

    1. **SCD2 needs several rows per natural key.** Once a customer has three
       historical versions, ``customer_id`` is no longer unique in the table, so
       it cannot be the primary key.
    2. **Natural keys change.** Source systems renumber, merge accounts, and
       re-use identifiers. A surrogate key is yours and never moves.
    3. **Narrow joins are cheaper.** A 4-byte integer beats a 40-character
       composite string across a billion-row fact scan.
    """

    def __init__(self) -> None:
        self._counters: dict[str, itertools.count] = {}

    def next_key(self, table: str) -> int:
        if table not in self._counters:
            self._counters[table] = itertools.count(1)
        return next(self._counters[table])


# ---------------------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------------------
@dataclass
class DimensionVersion:
    """One row of a dimension table: an attribute snapshot with a validity range.

    ``valid_from`` is inclusive, ``valid_to`` is inclusive, and consecutive
    versions of the same natural key must tile the timeline with no gap and no
    overlap. ``test_scd2_intervals_tile_the_timeline`` asserts that property.
    """

    surrogate_key: int
    natural_key: str
    attributes: dict[str, Any]
    valid_from: date
    valid_to: date = END_OF_TIME
    is_current: bool = True

    def covers(self, when: date) -> bool:
        return self.valid_from <= when <= self.valid_to


class DimensionTable:
    """A dimension with a declared change-tracking strategy.

    ``scd_type=1`` overwrites in place - history is discarded, and that is
    sometimes correct (a corrected typo should not become a new version).

    ``scd_type=2`` closes the current row and opens a new one whenever a
    *tracked* attribute changes. Attributes outside ``tracked_attributes`` are
    treated as Type 1 even in a Type 2 dimension, which is how real warehouses
    avoid versioning on a phone-number correction.
    """

    def __init__(
        self,
        name: str,
        scd_type: int = 2,
        tracked_attributes: set[str] | None = None,
        allocator: SurrogateKeyAllocator | None = None,
    ) -> None:
        if scd_type not in (1, 2):
            raise DimensionalModelError(f"unsupported SCD type: {scd_type}")
        self.name = name
        self.scd_type = scd_type
        self.tracked_attributes = tracked_attributes
        self._allocator = allocator or SurrogateKeyAllocator()
        self._versions: dict[str, list[DimensionVersion]] = defaultdict(list)

    # -- reads --------------------------------------------------------------
    @property
    def rows(self) -> list[DimensionVersion]:
        """Every version, ordered by natural key then validity start."""
        out: list[DimensionVersion] = []
        for key in sorted(self._versions):
            out.extend(self._versions[key])
        return out

    def current(self, natural_key: str) -> DimensionVersion | None:
        for version in self._versions.get(natural_key, []):
            if version.is_current:
                return version
        return None

    def lookup_as_of(self, natural_key: str, when: date) -> int | None:
        """The surrogate key that was in effect on ``when``.

        This is the join key a fact row must carry. Using ``current()`` here
        instead is the single most common dimensional-modelling bug: it makes
        last year's numbers change whenever a dimension is updated today.
        """
        for version in self._versions.get(natural_key, []):
            if version.covers(when):
                return version.surrogate_key
        return None

    def version_count(self, natural_key: str) -> int:
        return len(self._versions.get(natural_key, []))

    # -- writes -------------------------------------------------------------
    def _tracked_changed(self, existing: DimensionVersion, attrs: dict[str, Any]) -> bool:
        keys = self.tracked_attributes if self.tracked_attributes is not None else set(attrs)
        return any(existing.attributes.get(k) != attrs.get(k) for k in keys)

    def upsert(self, natural_key: str, attributes: dict[str, Any], effective: date) -> int:
        """Apply a source row. Returns the surrogate key the fact should use.

        No-change upserts are a no-op. That matters more than it sounds: a daily
        full extract re-sends every row every day, so a naive SCD2 that versions
        on every load produces 365 identical versions per key per year.
        """
        existing = self.current(natural_key)

        if existing is None:
            version = DimensionVersion(
                surrogate_key=self._allocator.next_key(self.name),
                natural_key=natural_key,
                attributes=dict(attributes),
                valid_from=effective,
            )
            self._versions[natural_key].append(version)
            return version.surrogate_key

        if not self._tracked_changed(existing, attributes):
            # Untracked attributes still get corrected in place (Type 1 behaviour
            # inside a Type 2 dimension).
            existing.attributes.update(attributes)
            return existing.surrogate_key

        if self.scd_type == 1:
            existing.attributes.update(attributes)
            return existing.surrogate_key

        if effective <= existing.valid_from:
            raise DimensionalModelError(
                f"{self.name}: out-of-order load for {natural_key!r} - effective "
                f"{effective} is not after the open version's start {existing.valid_from}. "
                "Late-arriving dimension rows need an explicit correction path, "
                "not a silent insert."
            )

        existing.valid_to = effective - timedelta(days=1)
        existing.is_current = False
        version = DimensionVersion(
            surrogate_key=self._allocator.next_key(self.name),
            natural_key=natural_key,
            attributes=dict(attributes),
            valid_from=effective,
        )
        self._versions[natural_key].append(version)
        return version.surrogate_key


# ---------------------------------------------------------------------------
# Facts and the star
# ---------------------------------------------------------------------------
@dataclass
class FactTable:
    """Append-only measures at one explicitly declared grain.

    ``grain`` is documentation that the code enforces: every fact row must carry
    exactly these dimension keys. An undeclared grain is how a fact table ends up
    holding a mix of per-order and per-line rows, at which point every SUM is
    wrong and no query can tell you so.
    """

    name: str
    grain: tuple[str, ...]
    measures: tuple[str, ...]
    rows: list[dict[str, Any]] = field(default_factory=list)

    def insert(self, keys: dict[str, int], measures: dict[str, float], event_date: date) -> None:
        missing = set(self.grain) - set(keys)
        if missing:
            raise DimensionalModelError(f"{self.name}: row is missing grain keys {sorted(missing)}")
        extra = set(keys) - set(self.grain)
        if extra:
            raise DimensionalModelError(
                f"{self.name}: row carries keys outside the declared grain {sorted(extra)}"
            )
        unknown = set(measures) - set(self.measures)
        if unknown:
            raise DimensionalModelError(f"{self.name}: unknown measures {sorted(unknown)}")
        self.rows.append({**keys, **measures, "event_date": event_date})


class StarSchema:
    """One fact table surrounded by conformed dimensions.

    ``aggregate`` performs the star join in the obvious way - resolve each fact
    row's surrogate keys back to dimension attributes, then group. A real
    warehouse pushes this into the engine; doing it by hand once makes it clear
    why the fact table stays narrow and the dimensions stay wide.
    """

    def __init__(self, fact: FactTable) -> None:
        self.fact = fact
        self.dimensions: dict[str, DimensionTable] = {}

    def add_dimension(self, key_column: str, dimension: DimensionTable) -> None:
        if key_column not in self.fact.grain:
            raise DimensionalModelError(
                f"{key_column!r} is not in {self.fact.name}'s grain {list(self.fact.grain)}"
            )
        self.dimensions[key_column] = dimension

    def _attr_index(self, key_column: str) -> dict[int, dict[str, Any]]:
        dim = self.dimensions[key_column]
        return {v.surrogate_key: v.attributes for v in dim.rows}

    def aggregate(
        self,
        group_by: list[tuple[str, str]],
        measure: str,
        agg: str = "sum",
    ) -> dict[tuple[Any, ...], float]:
        """Group ``measure`` by ``(key_column, attribute)`` pairs.

        Returns a plain dict so the reconciliation test can compare it directly
        against what DuckDB returns for the equivalent SQL.
        """
        if measure not in self.fact.measures:
            raise DimensionalModelError(f"unknown measure {measure!r}")
        if agg not in {"sum", "count", "avg", "min", "max"}:
            raise DimensionalModelError(f"unsupported aggregate {agg!r}")

        indexes = {kc: self._attr_index(kc) for kc, _ in group_by}
        buckets: dict[tuple[Any, ...], list[float]] = defaultdict(list)
        for row in self.fact.rows:
            label = tuple(indexes[kc].get(row[kc], {}).get(attr) for kc, attr in group_by)
            buckets[label].append(float(row[measure]))

        reducers: dict[str, Callable[[list[float]], float]] = {
            "sum": sum,
            "count": lambda vs: float(len(vs)),
            "avg": lambda vs: sum(vs) / len(vs),
            "min": min,
            "max": max,
        }
        reduce = reducers[agg]
        return {label: reduce(values) for label, values in buckets.items()}


# ---------------------------------------------------------------------------
# Materialised views
# ---------------------------------------------------------------------------
class MaterializedView:
    """A cached aggregate with an explicit staleness contract.

    The interesting part is not the caching, it is knowing when the cache is
    wrong. ``is_stale`` compares the source row count against the count at last
    refresh, so a view can answer "am I safe to serve?" instead of leaving the
    caller to guess.
    """

    def __init__(
        self,
        name: str,
        source: StarSchema,
        definition: Callable[[StarSchema], dict],
        supports_incremental: bool = True,
    ) -> None:
        self.name = name
        self.source = source
        self.definition = definition
        self.supports_incremental = supports_incremental
        self._data: dict | None = None
        self._rows_at_refresh = 0
        self.refresh_count = 0

    @property
    def data(self) -> dict:
        if self._data is None:
            raise DimensionalModelError(f"{self.name} has never been refreshed")
        return self._data

    @property
    def is_stale(self) -> bool:
        return self._data is None or len(self.source.fact.rows) != self._rows_at_refresh

    def refresh(self) -> dict:
        """Full recompute. Correct, and O(fact) every time."""
        self._data = self.definition(self.source)
        self._rows_at_refresh = len(self.source.fact.rows)
        self.refresh_count += 1
        return self._data

    def refresh_incremental(self, watermark: date) -> dict:
        """Recompute using only rows after ``watermark``, then merge.

        Only valid because SUM and COUNT are additive. A view over a
        non-additive measure - a distinct count, a median, a ratio - cannot be
        merged this way, and pretending otherwise is a silent-wrong-answer bug
        rather than a crash. ``supports_incremental`` is the guard, and it
        raises rather than quietly falling back to a full refresh: a caller who
        asked for incremental is making a cost assumption, and hiding an
        O(fact) recompute inside it is its own kind of lie.
        """
        if not self.supports_incremental:
            raise DimensionalModelError(
                f"{self.name} aggregates a non-additive measure, so deltas cannot be "
                "merged. Call refresh() for a full recompute."
            )
        if self._data is None:
            return self.refresh()

        new_rows = [r for r in self.source.fact.rows if r["event_date"] > watermark]
        if not new_rows:
            self._rows_at_refresh = len(self.source.fact.rows)
            return self._data

        delta_fact = FactTable(
            self.source.fact.name,
            self.source.fact.grain,
            self.source.fact.measures,
            new_rows,
        )
        delta_star = StarSchema(delta_fact)
        delta_star.dimensions = self.source.dimensions
        delta = self.definition(delta_star)

        merged = dict(self._data)
        for label, value in delta.items():
            merged[label] = merged.get(label, 0.0) + value
        self._data = merged
        self._rows_at_refresh = len(self.source.fact.rows)
        self.refresh_count += 1
        return merged


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------
@dataclass
class Task:
    name: str
    run: Callable[[dict[str, Any]], Any]
    depends_on: tuple[str, ...] = ()
    max_attempts: int = 1


class PipelineDAG:
    """Dependency-ordered task execution with idempotency and bounded retries.

    Three properties, each one a production incident if missing:

    **Topological order** - a task never runs before its inputs exist.
    **Cycle detection** - reported as an error, not as a hang.
    **Idempotency** - a task that already succeeded for a given run key is
    skipped on re-run. Without it, a retried pipeline double-loads the fact
    table, and the resulting numbers are merely plausible rather than obviously
    broken, so nobody notices for a quarter.
    """

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._completed: set[tuple[str, str]] = set()
        self.attempts: dict[str, int] = defaultdict(int)
        self.skipped: list[str] = []

    def add_task(self, task: Task) -> None:
        if task.name in self._tasks:
            raise DimensionalModelError(f"duplicate task {task.name!r}")
        self._tasks[task.name] = task

    def topological_order(self) -> list[str]:
        indegree = {name: 0 for name in self._tasks}
        dependents: dict[str, list[str]] = defaultdict(list)
        for task in self._tasks.values():
            for dep in task.depends_on:
                if dep not in self._tasks:
                    raise DimensionalModelError(f"{task.name!r} depends on unknown task {dep!r}")
                indegree[task.name] += 1
                dependents[dep].append(task.name)

        # Sorted seeding makes the order deterministic, which makes the tests
        # meaningful and the logs diffable.
        queue = deque(sorted(n for n, d in indegree.items() if d == 0))
        order: list[str] = []
        while queue:
            name = queue.popleft()
            order.append(name)
            for child in sorted(dependents[name]):
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)

        if len(order) != len(self._tasks):
            stuck = sorted(set(self._tasks) - set(order))
            raise DimensionalModelError(f"dependency cycle among tasks: {stuck}")
        return order

    def run(self, run_key: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute every task in order. ``run_key`` scopes idempotency.

        Convention: one run key per logical interval (a date, an hour). Re-running
        the same key resumes rather than duplicates.
        """
        ctx = context if context is not None else {}
        results: dict[str, Any] = {}
        for name in self.topological_order():
            if (run_key, name) in self._completed:
                self.skipped.append(name)
                continue
            task = self._tasks[name]
            last_error: Exception | None = None
            for _ in range(task.max_attempts):
                self.attempts[name] += 1
                try:
                    results[name] = task.run(ctx)
                    self._completed.add((run_key, name))
                    last_error = None
                    break
                except Exception as exc:  # noqa: BLE001 - re-raised below if terminal
                    last_error = exc
            if last_error is not None:
                raise last_error
        return results


class WatermarkStore:
    """High-water marks for incremental extraction.

    Extracting ``WHERE updated_at > watermark`` is the difference between a
    pipeline that costs O(new rows) and one that costs O(all rows) every night.
    The subtlety: the watermark must advance to the maximum value *observed*, not
    to "now", or rows written during the extract are skipped forever.
    """

    def __init__(self) -> None:
        self._marks: dict[str, date] = {}

    def get(self, source: str) -> date | None:
        return self._marks.get(source)

    def advance(self, source: str, observed: date) -> None:
        current = self._marks.get(source)
        if current is None or observed > current:
            self._marks[source] = observed

    def extract(
        self,
        source: str,
        rows: list[dict[str, Any]],
        column: str = "updated_at",
    ) -> list[dict[str, Any]]:
        mark = self.get(source)
        new = [r for r in rows if mark is None or r[column] > mark]
        if new:
            self.advance(source, max(r[column] for r in new))
        return new


class Backfill:
    """Bounded batches over a date range.

    A single-transaction backfill over two years of history holds locks for
    hours, blows out the WAL, and cannot be resumed after a failure. Chunking is
    not an optimisation here - it is the only version that finishes.
    """

    def __init__(self, start: date, end: date, batch_days: int = 7) -> None:
        if end < start:
            raise DimensionalModelError(f"empty range: {start} .. {end}")
        if batch_days < 1:
            raise DimensionalModelError("batch_days must be at least 1")
        self.start, self.end, self.batch_days = start, end, batch_days

    def batches(self) -> Iterator[tuple[date, date]]:
        cursor = self.start
        while cursor <= self.end:
            stop = min(cursor + timedelta(days=self.batch_days - 1), self.end)
            yield cursor, stop
            cursor = stop + timedelta(days=1)

    @property
    def batch_count(self) -> int:
        return sum(1 for _ in self.batches())
