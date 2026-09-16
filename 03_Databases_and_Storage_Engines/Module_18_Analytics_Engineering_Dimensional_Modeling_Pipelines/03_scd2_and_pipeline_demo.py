#!/usr/bin/env python3
"""Module 18 demo - SCD2, materialised aggregates and pipelines, measured.

Every number printed here is computed at runtime from the code in
``project_solution/``. Nothing is hardcoded, and nothing is asserted that is not
also demonstrated.

Run it::

    python 01_scd2_and_pipeline_demo.py
"""

from __future__ import annotations

import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from dimensional_engine import (  # noqa: E402
    Backfill,
    DimensionTable,
    FactTable,
    MaterializedView,
    PipelineDAG,
    StarSchema,
    SurrogateKeyAllocator,
    Task,
    WatermarkStore,
)
from warehouse_live import LiveWarehouse  # noqa: E402

RULE = "=" * 72


def header(title: str) -> None:
    print(f"\n{RULE}\n{title}\n{RULE}")


# ---------------------------------------------------------------------------
def demo_scd2_preserves_history() -> None:
    header("1. SCD TYPE 2 - THE AS-OF JOIN, AND WHY IT IS NOT `current()`")

    dim = DimensionTable("dim_customer", scd_type=2, tracked_attributes={"state"})
    ohio = dim.upsert("C1", {"state": "OH", "phone": "555-0100"}, date(2024, 1, 1))
    print(f"  2024-01-01  C1 loaded in OH             -> surrogate key {ohio}")

    same = dim.upsert("C1", {"state": "OH", "phone": "555-0999"}, date(2024, 2, 1))
    print(f"  2024-02-01  phone corrected (untracked) -> surrogate key {same} (no new version)")

    texas = dim.upsert("C1", {"state": "TX", "phone": "555-0999"}, date(2024, 6, 1))
    print(f"  2024-06-01  moved to TX (tracked)       -> surrogate key {texas} (new version)")

    print(f"\n  versions for C1: {dim.version_count('C1')}")
    for v in dim.rows:
        end = "open" if v.is_current else v.valid_to.isoformat()
        print(
            f"    sk={v.surrogate_key}  {v.attributes['state']}  "
            f"{v.valid_from} -> {end:<10} current={v.is_current}"
        )

    print("\n  as-of lookups:")
    for when in (date(2023, 12, 31), date(2024, 3, 15), date(2024, 5, 31), date(2024, 7, 15)):
        sk = dim.lookup_as_of("C1", when)
        label = "None (predates the dimension)" if sk is None else f"sk={sk}"
        print(f"    {when}  ->  {label}")

    current_sk = dim.current("C1").surrogate_key
    march_sk = dim.lookup_as_of("C1", date(2024, 3, 15))
    print(f"\n  current() would return sk={current_sk} for every date.")
    print(f"  The as-of join returns sk={march_sk} for March - which is the whole point.")
    print("  Using current() here moves March's revenue to Texas on the next backfill.")


# ---------------------------------------------------------------------------
def demo_history_survives_a_backfill() -> None:
    header("2. THE SAME FACTS, LOADED TWICE, MUST PRODUCE THE SAME NUMBERS")

    alloc = SurrogateKeyAllocator()
    customers = DimensionTable("dim_customer", 2, {"state"}, alloc)
    products = DimensionTable("dim_product", 2, {"category"}, alloc)
    product = products.upsert("P1", {"category": "widget"}, date(2024, 1, 1))
    customers.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    customers.upsert("C2", {"state": "OH"}, date(2024, 1, 1))

    sales = [
        (date(2024, 3, 1), "C1", 100.0),
        (date(2024, 3, 1), "C2", 50.0),
        (date(2024, 4, 1), "C1", 30.0),
        (date(2024, 7, 1), "C1", 25.0),
    ]

    def load(label: str) -> dict:
        fact = FactTable("fact_sales", ("customer_sk", "product_sk"), ("revenue",))
        star = StarSchema(fact)
        star.add_dimension("customer_sk", customers)
        star.add_dimension("product_sk", products)
        for when, who, revenue in sales:
            sk = customers.lookup_as_of(who, when)
            fact.insert({"customer_sk": sk, "product_sk": product}, {"revenue": revenue}, when)
        result = star.aggregate([("customer_sk", "state")], "revenue")
        pretty = {state[0]: round(total, 2) for state, total in sorted(result.items())}
        print(f"  {label:<44} {pretty}")
        return result

    first = load("first load (before C1 relocates)")
    customers.upsert("C1", {"state": "TX"}, date(2024, 6, 1))
    print("\n  ... C1 relocates to TX effective 2024-06-01 ...\n")
    second = load("reprocess of the same 4 sales, after")

    print(f"\n  identical: {first == second}")
    print("  With a current()-based lookup this prints False, and $130 of Ohio")
    print("  revenue silently becomes Texas revenue. Nothing errors.")


# ---------------------------------------------------------------------------
def demo_incremental_refresh() -> None:
    header("3. INCREMENTAL REFRESH - CHEAPER, AND ONLY VALID WHEN ADDITIVE")

    alloc = SurrogateKeyAllocator()
    customers = DimensionTable("dim_customer", 2, {"state"}, alloc)
    products = DimensionTable("dim_product", 2, {"category"}, alloc)
    product = products.upsert("P1", {"category": "widget"}, date(2024, 1, 1))

    fact = FactTable("fact_sales", ("customer_sk", "product_sk"), ("revenue",))
    star = StarSchema(fact)
    star.add_dimension("customer_sk", customers)
    star.add_dimension("product_sk", products)

    states = ["OH", "TX", "CA", "NY"]
    for i in range(400):
        sk = customers.upsert(f"C{i}", {"state": states[i % 4]}, date(2024, 1, 1))
        for day in range(1, 21):
            fact.insert(
                {"customer_sk": sk, "product_sk": product},
                {"revenue": 10.0},
                date(2024, 1, day),
            )
    print(f"  fact rows: {len(fact.rows):,}")

    def revenue_by_state(s: StarSchema) -> dict:
        return s.aggregate([("customer_sk", "state")], "revenue")

    view = MaterializedView("mv_revenue_by_state", star, revenue_by_state)
    view.refresh()
    print(f"  stale after first refresh: {view.is_stale}")

    watermark = date(2024, 1, 20)
    for i in range(400):
        sk = customers.lookup_as_of(f"C{i}", date(2024, 1, 21))
        fact.insert(
            {"customer_sk": sk, "product_sk": product}, {"revenue": 5.0}, date(2024, 1, 21)
        )
    print(f"  fact rows after one new day: {len(fact.rows):,}")
    print(f"  stale now: {view.is_stale}")

    started = time.perf_counter()
    incremental = view.refresh_incremental(watermark)
    inc_ms = (time.perf_counter() - started) * 1000

    full_view = MaterializedView("mv_full", star, revenue_by_state)
    started = time.perf_counter()
    full = full_view.refresh()
    full_ms = (time.perf_counter() - started) * 1000

    print(f"\n  incremental refresh: {inc_ms:7.3f} ms  (1 day of rows)")
    print(f"  full refresh:        {full_ms:7.3f} ms  ({len(fact.rows):,} rows)")
    print(f"  speedup:             {full_ms / inc_ms:7.2f}x")
    print(f"  results agree:       {incremental == full}")
    print("\n  Valid only because SUM is additive. A COUNT(DISTINCT) merged this")
    print("  way double-counts anything present in both windows.")

    guarded = MaterializedView("mv_distinct", star, revenue_by_state, supports_incremental=False)
    guarded.refresh()
    try:
        guarded.refresh_incremental(watermark)
    except Exception as exc:
        print(f"  non-additive view refuses: {type(exc).__name__}: {str(exc)[:58]}...")


# ---------------------------------------------------------------------------
def demo_pipeline_idempotency() -> None:
    header("4. PIPELINE IDEMPOTENCY - AND ITS HARDER HALF")

    loaded: list[str] = []
    dag = PipelineDAG()
    dag.add_task(Task("extract", lambda c: loaded.append("extract")))
    dag.add_task(Task("load_dim", lambda c: loaded.append("load_dim"), depends_on=("extract",)))
    dag.add_task(
        Task("load_fact", lambda c: loaded.append("load_fact"), depends_on=("load_dim",))
    )
    dag.add_task(
        Task("refresh_view", lambda c: loaded.append("refresh_view"), depends_on=("load_fact",))
    )

    print(f"  topological order: {dag.topological_order()}")
    dag.run("2024-03-01")
    print(f"  run 1 executed:    {loaded}")
    dag.run("2024-03-01")
    print(f"  run 2 executed:    {loaded}  (unchanged)")
    print(f"  run 2 skipped:     {dag.skipped}")
    print("\n  Without this, a retried pipeline double-loads the fact table and")
    print("  every measure doubles - plausibly enough to survive review.")

    print("\n  The harder half: a FAILED task must not be marked complete.")
    attempts = {"n": 0}

    def always_fails(_ctx):
        attempts["n"] += 1
        raise RuntimeError("relation 'audit_log' does not exist")

    ran_downstream: list[str] = []
    audit = PipelineDAG()
    audit.add_task(Task("load_audit", always_fails, max_attempts=2))
    audit.add_task(
        Task("notify", lambda c: ran_downstream.append("notify"), depends_on=("load_audit",))
    )

    for run in (1, 2):
        try:
            audit.run("2024-03-01")
            print(f"  run {run}: returned normally  <-- would be a green pipeline")
        except RuntimeError as exc:
            print(f"  run {run}: raised {type(exc).__name__}: {exc}")
    print(f"  total attempts on load_audit: {attempts['n']} (retried, not skipped)")
    print(f"  downstream 'notify' ran:      {bool(ran_downstream)}")


# ---------------------------------------------------------------------------
def demo_watermarks_and_backfill() -> None:
    header("5. WATERMARKS AND BOUNDED BACKFILLS")

    marks = WatermarkStore()
    source = [
        {"id": 1, "updated_at": date(2024, 1, 1)},
        {"id": 2, "updated_at": date(2024, 1, 2)},
    ]
    print(f"  extract 1: {[r['id'] for r in marks.extract('orders', source)]}")
    print(f"  mark now:  {marks.get('orders')}  (max observed, NOT today)")
    print(f"  extract 2: {[r['id'] for r in marks.extract('orders', source)]}  (nothing new)")

    source.append({"id": 3, "updated_at": date(2024, 1, 3)})
    print(f"  extract 3: {[r['id'] for r in marks.extract('orders', source)]}  (only the new row)")

    marks.advance("orders", date(2023, 1, 1))
    print(f"  after a backwards advance: {marks.get('orders')}  (refused)")

    print("\n  Setting the mark to today() instead would skip row 3 permanently,")
    print("  with no error and no gap in any row count.")

    bf = Backfill(date(2024, 1, 1), date(2024, 3, 31), batch_days=14)
    print(f"\n  backfill 2024-01-01 .. 2024-03-31 in {bf.batch_days}-day batches:")
    for start, end in bf.batches():
        print(f"    {start} -> {end}")
    print(f"  batches: {bf.batch_count} (one transaction each, resumable)")


# ---------------------------------------------------------------------------
def demo_real_duckdb() -> None:
    header("6. THE SAME MODEL IN REAL DUCKDB, AND RECONCILIATION")

    with LiveWarehouse(":memory:") as wh:
        wh.create_schema()
        print(f"  tables: {sorted(r[0] for r in wh.query('SHOW TABLES'))}")

        ohio = wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
        c2 = wh.insert_customer_version("C2", "OH", date(2024, 1, 1))
        product = wh.insert_product("P1", "widget", date(2024, 1, 1))
        wh.insert_sale(ohio, product, date(2024, 3, 1), 100.0)
        wh.insert_sale(c2, product, date(2024, 3, 1), 50.0)
        texas = wh.load_scd2_change("C1", "TX", date(2024, 6, 1))
        wh.insert_sale(texas, product, date(2024, 7, 1), 25.0)

        print("\n  dim_customer after the SCD2 merge:")
        for row in wh.query(
            "SELECT customer_sk, customer_id, state, valid_from, valid_to, is_current "
            "FROM dim_customer ORDER BY customer_sk"
        ):
            sk, cid, state, vf, vt, cur = row
            end = "open" if cur else str(vt)
            print(f"    sk={sk}  {cid}  {state}  {vf} -> {end:<12} current={cur}")

        gaps = wh.query(
            """
            SELECT COUNT(*) FROM (
                SELECT valid_to, LEAD(valid_from) OVER (
                    PARTITION BY customer_id ORDER BY valid_from) AS next_from
                FROM dim_customer
            ) t
            WHERE next_from IS NOT NULL AND next_from <> valid_to + INTERVAL 1 DAY
            """
        )[0][0]
        print(f"\n  gap/overlap pairs in dim_customer: {gaps}  (must be 0)")
        print(f"  revenue by state (SQL): {wh.revenue_by_state()}")

        # --- the same thing through the hand-built model -------------------
        alloc = SurrogateKeyAllocator()
        customers = DimensionTable("dim_customer", 2, {"state"}, alloc)
        products = DimensionTable("dim_product", 2, {"category"}, alloc)
        fact = FactTable("fact_sales", ("customer_sk", "product_sk"), ("revenue",))
        star = StarSchema(fact)
        star.add_dimension("customer_sk", customers)
        star.add_dimension("product_sk", products)

        m_ohio = customers.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
        m_c2 = customers.upsert("C2", {"state": "OH"}, date(2024, 1, 1))
        m_product = products.upsert("P1", {"category": "widget"}, date(2024, 1, 1))
        fact.insert({"customer_sk": m_ohio, "product_sk": m_product}, {"revenue": 100.0},
                    date(2024, 3, 1))
        fact.insert({"customer_sk": m_c2, "product_sk": m_product}, {"revenue": 50.0},
                    date(2024, 3, 1))
        m_texas = customers.upsert("C1", {"state": "TX"}, date(2024, 6, 1))
        fact.insert({"customer_sk": m_texas, "product_sk": m_product}, {"revenue": 25.0},
                    date(2024, 7, 1))

        model = star.aggregate([("customer_sk", "state")], "revenue")
        live = wh.revenue_by_state()
        print(f"  revenue by state (model): {model}")
        print(f"\n  RECONCILED: {model == live}")

        # --- the aggregate table actually earns its keep -------------------
        wh.create_schema()
        wh.seed_scale(customers=200, days=90, rows=20_000)
        wh.create_materialized_aggregate()
        raw_ms = wh.time_query(
            "SELECT c.state, SUM(f.revenue) FROM fact_sales f "
            "JOIN dim_customer c ON f.customer_sk = c.customer_sk GROUP BY c.state"
        )
        mv_ms = wh.time_query("SELECT state, revenue FROM mv_revenue_by_state")
        print("\n  20,000 fact rows, best of 3:")
        print(f"    raw star join:      {raw_ms:7.3f} ms")
        print(f"    aggregate table:    {mv_ms:7.3f} ms")
        print(f"    speedup:            {raw_ms / mv_ms:7.2f}x")

        # DuckDB renders EXPLAIN as a box-drawing diagram. Those glyphs are not
        # encodable in the Windows console's default cp1252 code page, so strip
        # them rather than crash - a demo that dies on the default terminal of
        # the platform it ships on is a broken demo.
        plan = wh.explain_star_join()
        operators = sorted(
            {
                token
                for token in plan.replace("│", " ").split()
                if token.isupper() and token.isalpha() and len(token) > 3
            }
        )
        print(f"\n  optimiser plan operators: {', '.join(operators)}")
        print(f"  hash joins in the plan:   {plan.upper().count('HASH_JOIN')}")


# ---------------------------------------------------------------------------
def main() -> None:
    print(RULE)
    print("MODULE 18 - ANALYTICS ENGINEERING: DIMENSIONAL MODELLING & PIPELINES")
    print(RULE)
    print("Every number below is measured at runtime. Nothing is hardcoded.")

    demo_scd2_preserves_history()
    demo_history_survives_a_backfill()
    demo_incremental_refresh()
    demo_pipeline_idempotency()
    demo_watermarks_and_backfill()
    demo_real_duckdb()

    header("TAKEAWAYS")
    print("  1. A fact joins to the dimension version current WHEN THE EVENT")
    print("     HAPPENED. current() is not that, and the bug is dormant until")
    print("     the first backfill.")
    print("  2. Closed intervals mean valid_to = effective - 1 day. Off by one")
    print("     here double-counts one day per change, per key.")
    print("  3. Incremental refresh is valid for additive measures only. Refuse")
    print("     rather than approximate.")
    print("  4. Idempotency has two halves: skip completed work, and never mark")
    print("     failed work complete.")
    print("  5. Advance a watermark to the max OBSERVED value, never to now().")
    print("  6. In analytics, silence is not success. Reconcile two independent")
    print("     computations - that is the only evidence a number is right.")
    print()


if __name__ == "__main__":
    main()
