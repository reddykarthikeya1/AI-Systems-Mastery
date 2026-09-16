"""A nightly warehouse load that runs to completion and reports wrong numbers.

Run it::

    python broken_warehouse_pipeline.py

Nothing raises. Nothing warns. Exit code is 0. Every printed figure that is
wrong is also plausible, which is the entire problem: a crash gets fixed on
Tuesday, and this gets fixed after someone reconciles a quarterly report by hand.

Read SYMPTOMS.md for what the output should have been. Do not read ANSWERS.md
until you have found them yourself - the diagnostic reasoning is the skill this
lab is for, and reading the answer skips exactly the part worth practising.
"""

from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

END_OF_TIME = date(9999, 12, 31)


@dataclass
class DimensionVersion:
    surrogate_key: int
    natural_key: str
    attributes: dict[str, Any]
    valid_from: date
    valid_to: date = END_OF_TIME
    is_current: bool = True

    def covers(self, when: date) -> bool:
        return self.valid_from <= when <= self.valid_to


class DimensionTable:
    def __init__(self, name: str, tracked: set[str]) -> None:
        self.name = name
        self.tracked = tracked
        self._next_sk = 1
        self._versions: dict[str, list[DimensionVersion]] = defaultdict(list)

    def _allocate(self) -> int:
        sk = self._next_sk
        self._next_sk += 1
        return sk

    @property
    def rows(self) -> list[DimensionVersion]:
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
        version = self.current(natural_key)
        return version.surrogate_key if version else None

    def upsert(self, natural_key: str, attributes: dict[str, Any], effective: date) -> int:
        existing = self.current(natural_key)

        if existing is None:
            version = DimensionVersion(
                surrogate_key=self._allocate(),
                natural_key=natural_key,
                attributes=dict(attributes),
                valid_from=effective,
            )
            self._versions[natural_key].append(version)
            return version.surrogate_key

        changed = any(existing.attributes.get(k) != attributes.get(k) for k in self.tracked)
        if not changed:
            existing.attributes.update(attributes)
            return existing.surrogate_key

        existing.valid_to = effective
        existing.is_current = False
        version = DimensionVersion(
            surrogate_key=self._allocate(),
            natural_key=natural_key,
            attributes=dict(attributes),
            valid_from=effective,
        )
        self._versions[natural_key].append(version)
        return version.surrogate_key


@dataclass
class FactTable:
    name: str
    rows: list[dict[str, Any]] = field(default_factory=list)

    def insert(self, customer_sk: int, event_date: date, revenue: float) -> None:
        self.rows.append(
            {"customer_sk": customer_sk, "event_date": event_date, "revenue": revenue}
        )


class WatermarkStore:
    def __init__(self) -> None:
        self._marks: dict[str, date] = {}

    def get(self, source: str) -> date | None:
        return self._marks.get(source)

    def extract(self, source: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        mark = self.get(source)
        new = [r for r in rows if mark is None or r["updated_at"] > mark]
        self._marks[source] = date.today()
        return new


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
        self._tasks[task.name] = task

    def topological_order(self) -> list[str]:
        indegree = {name: 0 for name in self._tasks}
        dependents: dict[str, list[str]] = defaultdict(list)
        for task in self._tasks.values():
            for dep in task.depends_on:
                indegree[task.name] += 1
                dependents[dep].append(task.name)

        queue = deque(sorted(n for n, d in indegree.items() if d == 0))
        order: list[str] = []
        while queue:
            name = queue.popleft()
            order.append(name)
            for child in sorted(dependents[name]):
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)
        return order

    def run(self, run_key: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context if context is not None else {}
        results: dict[str, Any] = {}
        for name in self.topological_order():
            if (run_key, name) in self._completed:
                self.skipped.append(name)
                continue
            task = self._tasks[name]
            self._completed.add((run_key, name))
            for _ in range(task.max_attempts):
                self.attempts[name] += 1
                try:
                    results[name] = task.run(ctx)
                    break
                except Exception:  # noqa: BLE001, S110
                    pass
        return results


class RevenueByStateView:
    def __init__(self, fact: FactTable, dim: DimensionTable) -> None:
        self.fact = fact
        self.dim = dim
        self._data: dict[str, float] = {}

    def _compute(self, rows: list[dict[str, Any]]) -> dict[str, float]:
        attrs = {v.surrogate_key: v.attributes for v in self.dim.rows}
        totals: dict[str, float] = defaultdict(float)
        for row in rows:
            state = attrs.get(row["customer_sk"], {}).get("state", "UNKNOWN")
            totals[state] += row["revenue"]
        return dict(totals)

    def refresh_full(self) -> dict[str, float]:
        self._data = self._compute(self.fact.rows)
        return self._data

    def refresh_incremental(self, watermark: date) -> dict[str, float]:
        new_rows = [r for r in self.fact.rows if r["event_date"] > watermark]
        delta = self._compute(new_rows)
        self._data.update(delta)
        return self._data


# ---------------------------------------------------------------------------
# The nightly run
# ---------------------------------------------------------------------------
def main() -> None:
    customers = DimensionTable("dim_customer", tracked={"state"})
    fact = FactTable("fact_sales")

    print("=" * 68)
    print("NIGHTLY WAREHOUSE LOAD")
    print("=" * 68)

    # --- January: two Ohio customers, three sales -------------------------
    customers.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    customers.upsert("C2", {"state": "OH"}, date(2024, 1, 1))

    for when, revenue, who in [
        (date(2024, 3, 1), 100.0, "C1"),
        (date(2024, 3, 1), 50.0, "C2"),
        (date(2024, 4, 1), 30.0, "C1"),
    ]:
        sk = customers.lookup_as_of(who, when)
        fact.insert(sk, when, revenue)

    # --- June: C1 relocates to Texas --------------------------------------
    customers.upsert("C1", {"state": "TX"}, date(2024, 6, 1))

    # --- July: one more sale, now genuinely in Texas ----------------------
    sk = customers.lookup_as_of("C1", date(2024, 7, 1))
    fact.insert(sk, date(2024, 7, 1), 25.0)

    view = RevenueByStateView(fact, customers)
    print("\n[1] Revenue by state, full refresh")
    for state, total in sorted(view.refresh_full().items()):
        print(f"      {state}: {total:>8.2f}")

    # --- August: the March partition is reprocessed -----------------------
    # An upstream correction arrived, so the March window is re-extracted and
    # re-loaded. This is an ordinary operation that happens most weeks.
    print("\n[1b] Revenue by state after reprocessing the March partition")
    reprocessed = FactTable("fact_sales_reprocessed")
    for when, revenue, who in [
        (date(2024, 3, 1), 100.0, "C1"),
        (date(2024, 3, 1), 50.0, "C2"),
        (date(2024, 4, 1), 30.0, "C1"),
        (date(2024, 7, 1), 25.0, "C1"),
    ]:
        reprocessed.insert(customers.lookup_as_of(who, when), when, revenue)
    for state, total in sorted(RevenueByStateView(reprocessed, customers).refresh_full().items()):
        print(f"      {state}: {total:>8.2f}")

    # --- SCD2 validity ranges ---------------------------------------------
    print("\n[2] dim_customer validity ranges")
    for v in customers.rows:
        end = "open" if v.valid_to == END_OF_TIME else v.valid_to.isoformat()
        print(
            f"      sk={v.surrogate_key} {v.natural_key} "
            f"{v.attributes['state']}  {v.valid_from} -> {end}"
        )

    overlaps = 0
    for key in {v.natural_key for v in customers.rows}:
        versions = [v for v in customers.rows if v.natural_key == key]
        for earlier, later in zip(versions, versions[1:], strict=False):
            if later.valid_from <= earlier.valid_to:
                overlaps += 1
    print(f"      overlapping version pairs: {overlaps}")

    # --- incremental refresh vs full --------------------------------------
    print("\n[3] Incremental refresh vs full refresh")
    inc = RevenueByStateView(fact, customers)
    inc.refresh_full()
    fact.insert(customers.lookup_as_of("C2", date(2024, 8, 1)), date(2024, 8, 1), 40.0)

    incremental = dict(inc.refresh_incremental(date(2024, 7, 1)))
    full = dict(RevenueByStateView(fact, customers).refresh_full())
    print(f"      incremental: { {k: round(v, 2) for k, v in sorted(incremental.items())} }")
    print(f"      full:        { {k: round(v, 2) for k, v in sorted(full.items())} }")
    print(f"      agree: {incremental == full}")

    # --- incremental extraction -------------------------------------------
    print("\n[4] Incremental extraction from the source system")
    source = [
        {"id": 1, "updated_at": date(2024, 1, 1)},
        {"id": 2, "updated_at": date(2024, 1, 2)},
    ]
    marks = WatermarkStore()
    first = marks.extract("orders", source)
    source.append({"id": 3, "updated_at": date(2024, 1, 3)})
    second = marks.extract("orders", source)
    print(f"      first  extract: {[r['id'] for r in first]}")
    print(f"      second extract: {[r['id'] for r in second]}")

    # --- retry behaviour ---------------------------------------------------
    print("\n[5] Retry behaviour on a transient failure")
    state = {"calls": 0}

    def flaky(_ctx):
        state["calls"] += 1
        if state["calls"] < 3:
            raise RuntimeError("transient connection reset")
        return "loaded"

    dag = PipelineDAG()
    dag.add_task(Task("extract", lambda c: "extracted"))
    dag.add_task(Task("load", flaky, depends_on=("extract",), max_attempts=3))

    run_one = dag.run("2024-08-01")
    print(f"      run 1 results: {run_one}")
    print(f"      attempts:      {dict(dag.attempts)}")

    run_two = dag.run("2024-08-01")
    print(f"      run 2 results: {run_two}")
    print(f"      run 2 skipped: {dag.skipped}")

    # --- a task that never succeeds ---------------------------------------
    print("\n[6] A task whose target table does not exist")
    audit = PipelineDAG()
    audit.add_task(
        Task(
            "load_audit",
            lambda c: (_ for _ in ()).throw(RuntimeError("relation 'audit_log' does not exist")),
            max_attempts=2,
        )
    )
    audit.add_task(Task("notify", lambda c: "emailed the analysts", depends_on=("load_audit",)))

    first_run = audit.run("2024-08-01")
    print(f"      run 1 results: {first_run}")
    print(f"      run 1 attempts: {dict(audit.attempts)}")
    second_run = audit.run("2024-08-01")
    print(f"      run 2 results: {second_run}")
    print(f"      run 2 skipped: {audit.skipped}")

    print("\n" + "=" * 68)
    print("Load complete. Exit code 0.")
    print("=" * 68)


if __name__ == "__main__":
    main()
