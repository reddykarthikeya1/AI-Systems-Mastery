"""Track B tests: the same warehouse against real DuckDB, plus reconciliation.

The last test in this file is the one that matters most. It runs one logical
aggregation through the hand-built model in ``dimensional_engine.py`` and through
real SQL in DuckDB, and asserts the two agree. Where they disagree, the model is
wrong - and the test says so instead of the learner discovering it later.
"""

from __future__ import annotations

from datetime import date

import pytest
from dimensional_engine import (
    DimensionTable,
    FactTable,
    StarSchema,
    SurrogateKeyAllocator,
)
from warehouse_live import LiveWarehouse, WarehouseUnavailableError

pytest.importorskip("duckdb", reason="Track B requires duckdb")


@pytest.fixture()
def wh():
    """A fresh in-memory warehouse per test. Idempotent by construction."""
    try:
        warehouse = LiveWarehouse(":memory:")
    except WarehouseUnavailableError as exc:  # pragma: no cover
        pytest.skip(str(exc))
    warehouse.create_schema()
    yield warehouse
    warehouse.close()


# ---------------------------------------------------------------------------
# DDL and basic loads
# ---------------------------------------------------------------------------


def test_schema_is_created_with_the_expected_tables(wh):
    names = {row[0] for row in wh.query("SHOW TABLES")}
    assert {"dim_customer", "dim_product", "fact_sales"} <= names


def test_create_schema_is_idempotent(wh):
    wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    wh.create_schema()
    assert wh.query("SELECT COUNT(*) FROM dim_customer")[0][0] == 0


def test_surrogate_keys_come_from_a_real_sequence(wh):
    first = wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    second = wh.insert_customer_version("C2", "TX", date(2024, 1, 1))
    assert second == first + 1


# ---------------------------------------------------------------------------
# The real SCD2 merge
# ---------------------------------------------------------------------------


def test_scd2_merge_leaves_exactly_one_current_row(wh):
    """Two current rows would double that customer's revenue in every join."""
    wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    wh.load_scd2_change("C1", "TX", date(2024, 6, 1))

    current = wh.query(
        "SELECT COUNT(*) FROM dim_customer WHERE customer_id = 'C1' AND is_current"
    )[0][0]
    assert current == 1
    assert wh.query("SELECT COUNT(*) FROM dim_customer WHERE customer_id = 'C1'")[0][0] == 2


def test_scd2_merge_closes_the_previous_row_the_day_before(wh):
    wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    wh.load_scd2_change("C1", "TX", date(2024, 6, 1))

    closed = wh.query(
        "SELECT valid_to FROM dim_customer WHERE customer_id = 'C1' AND NOT is_current"
    )[0][0]
    assert closed == date(2024, 5, 31)


def test_scd2_intervals_tile_the_timeline_in_sql(wh):
    """The SQL form of the Track A tiling invariant: no gaps, no overlaps."""
    wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    wh.load_scd2_change("C1", "TX", date(2024, 6, 1))
    wh.load_scd2_change("C1", "CA", date(2024, 9, 1))

    gaps = wh.query(
        """
        SELECT COUNT(*) FROM (
            SELECT valid_to,
                   LEAD(valid_from) OVER (PARTITION BY customer_id ORDER BY valid_from) AS next_from
            FROM dim_customer WHERE customer_id = 'C1'
        ) t
        WHERE next_from IS NOT NULL AND next_from <> valid_to + INTERVAL 1 DAY
        """
    )[0][0]
    assert gaps == 0


def test_scd2_change_to_the_same_value_is_a_noop(wh):
    sk = wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    assert wh.load_scd2_change("C1", "OH", date(2024, 6, 1)) == sk
    assert wh.query("SELECT COUNT(*) FROM dim_customer")[0][0] == 1


def test_scd2_change_without_an_open_row_is_rejected(wh):
    with pytest.raises(ValueError, match="no open version"):
        wh.load_scd2_change("GHOST", "TX", date(2024, 6, 1))


def test_scd2_rejects_out_of_order_effective_date(wh):
    wh.insert_customer_version("C1", "OH", date(2024, 6, 1))
    with pytest.raises(ValueError, match="out-of-order"):
        wh.load_scd2_change("C1", "TX", date(2024, 1, 1))


def test_scd2_merge_is_atomic(wh):
    """A failure between the UPDATE and the INSERT must leave the dimension
    with exactly one current row, not zero."""
    wh.insert_customer_version("C1", "OH", date(2024, 1, 1))

    original = wh.insert_customer_version

    def exploding(*_args, **_kwargs):
        raise RuntimeError("simulated crash between UPDATE and INSERT")

    wh.insert_customer_version = exploding  # type: ignore[method-assign]
    with pytest.raises(RuntimeError, match="simulated crash"):
        wh.load_scd2_change("C1", "TX", date(2024, 6, 1))
    wh.insert_customer_version = original  # type: ignore[method-assign]

    current = wh.query(
        "SELECT COUNT(*) FROM dim_customer WHERE customer_id = 'C1' AND is_current"
    )[0][0]
    assert current == 1


# ---------------------------------------------------------------------------
# The as-of join
# ---------------------------------------------------------------------------


def test_resolve_customer_sk_returns_the_historically_correct_version(wh):
    ohio = wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    texas = wh.load_scd2_change("C1", "TX", date(2024, 6, 1))

    assert wh.resolve_customer_sk("C1", date(2024, 3, 1)) == ohio
    assert wh.resolve_customer_sk("C1", date(2024, 7, 1)) == texas


def test_resolve_customer_sk_before_the_first_version_is_none(wh):
    wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    assert wh.resolve_customer_sk("C1", date(2023, 12, 31)) is None


def test_revenue_stays_with_the_state_it_was_earned_in(wh):
    """The business-visible consequence of the as-of join."""
    ohio = wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    product = wh.insert_product("P1", "widget", date(2024, 1, 1))
    wh.insert_sale(ohio, product, date(2024, 3, 1), 100.0)

    texas = wh.load_scd2_change("C1", "TX", date(2024, 6, 1))
    wh.insert_sale(texas, product, date(2024, 7, 1), 25.0)

    assert wh.revenue_by_state() == {("OH",): 100.0, ("TX",): 25.0}


# ---------------------------------------------------------------------------
# Plans and the materialised aggregate
# ---------------------------------------------------------------------------


def test_explain_shows_a_hash_join_over_the_fact_table(wh):
    wh.seed_scale(customers=20, days=10, rows=500)
    plan = wh.explain_star_join()
    assert "HASH_JOIN" in plan.upper()
    assert "FACT_SALES" in plan.upper()


def test_explain_analyze_reports_actual_cardinality(wh):
    wh.seed_scale(customers=20, days=10, rows=500)
    plan = wh.explain_star_join(analyze=True)
    assert plan.strip()
    assert "fact_sales" in plan.lower()


def test_materialized_aggregate_matches_the_live_query(wh):
    wh.seed_scale(customers=20, days=10, rows=500)
    wh.create_materialized_aggregate()
    assert wh.aggregate_contents() == pytest.approx(wh.revenue_by_state())


def test_incremental_refresh_matches_a_full_refresh(wh):
    """The additive-merge property, asserted against a real engine."""
    wh.seed_scale(customers=20, days=10, rows=500)
    watermark = date(2024, 1, 5)

    wh.conn.execute(
        """
        CREATE TABLE mv_revenue_by_state AS
        SELECT c.state, SUM(f.revenue) AS revenue, MAX(f.event_date) AS max_event_date
        FROM fact_sales f JOIN dim_customer c ON f.customer_sk = c.customer_sk
        WHERE f.event_date <= ?
        GROUP BY c.state
        """,
        [watermark],
    )
    consumed = wh.refresh_aggregate_incremental(watermark)
    assert consumed > 0
    incremental = wh.aggregate_contents()

    wh.refresh_aggregate_full()
    full = wh.aggregate_contents()

    assert incremental.keys() == full.keys()
    for state, revenue in full.items():
        assert incremental[state] == pytest.approx(revenue), (
            f"incremental and full refresh disagree for {state}"
        )


def test_aggregate_table_beats_the_raw_star_join(wh):
    """The reason the aggregate exists. A pre-aggregated table over 20k fact rows
    should read faster than re-joining and re-grouping them.

    Asserted with generous headroom - this is a shared-CI-runner measurement, and
    a tight threshold here would be a flaky test rather than a strong one.
    """
    wh.seed_scale(customers=200, days=90, rows=20_000)
    wh.create_materialized_aggregate()

    raw_ms = wh.time_query(
        """
        SELECT c.state, SUM(f.revenue)
        FROM fact_sales f JOIN dim_customer c ON f.customer_sk = c.customer_sk
        GROUP BY c.state
        """
    )
    mv_ms = wh.time_query("SELECT state, revenue FROM mv_revenue_by_state")

    assert mv_ms < raw_ms, f"aggregate {mv_ms:.3f}ms did not beat raw join {raw_ms:.3f}ms"


# ---------------------------------------------------------------------------
# Reconciliation: the hand-built model vs. the real engine
# ---------------------------------------------------------------------------


def test_model_and_duckdb_agree_on_revenue_by_state(wh):
    """The most important test in the module.

    The same three sales, one SCD2 move, and one aggregation - once through the
    Python model and once through DuckDB SQL. If these ever diverge, the model
    taught in Track A is lying about how a warehouse behaves.
    """
    # --- real engine ---
    live_ohio = wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    live_c2 = wh.insert_customer_version("C2", "OH", date(2024, 1, 1))
    live_product = wh.insert_product("P1", "widget", date(2024, 1, 1))
    wh.insert_sale(live_ohio, live_product, date(2024, 3, 1), 100.0)
    wh.insert_sale(live_c2, live_product, date(2024, 3, 1), 50.0)
    live_texas = wh.load_scd2_change("C1", "TX", date(2024, 6, 1))
    wh.insert_sale(live_texas, live_product, date(2024, 7, 1), 25.0)

    # --- hand-built model ---
    alloc = SurrogateKeyAllocator()
    customers = DimensionTable("dim_customer", 2, {"state"}, alloc)
    products = DimensionTable("dim_product", 2, {"category"}, alloc)
    fact = FactTable("fact_sales", ("customer_sk", "product_sk"), ("revenue",))
    star = StarSchema(fact)
    star.add_dimension("customer_sk", customers)
    star.add_dimension("product_sk", products)

    model_ohio = customers.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    model_c2 = customers.upsert("C2", {"state": "OH"}, date(2024, 1, 1))
    model_product = products.upsert("P1", {"category": "widget"}, date(2024, 1, 1))
    fact.insert(
        {"customer_sk": model_ohio, "product_sk": model_product},
        {"revenue": 100.0},
        date(2024, 3, 1),
    )
    fact.insert(
        {"customer_sk": model_c2, "product_sk": model_product},
        {"revenue": 50.0},
        date(2024, 3, 1),
    )
    model_texas = customers.upsert("C1", {"state": "TX"}, date(2024, 6, 1))
    fact.insert(
        {"customer_sk": model_texas, "product_sk": model_product},
        {"revenue": 25.0},
        date(2024, 7, 1),
    )

    assert star.aggregate([("customer_sk", "state")], "revenue") == wh.revenue_by_state()


def test_model_and_duckdb_agree_on_the_as_of_lookup(wh):
    """Reconcile the mechanism, not just the total."""
    wh.insert_customer_version("C1", "OH", date(2024, 1, 1))
    wh.load_scd2_change("C1", "TX", date(2024, 6, 1))

    dim = DimensionTable("dim_customer", 2, {"state"})
    dim.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    dim.upsert("C1", {"state": "TX"}, date(2024, 6, 1))

    for when in (date(2024, 2, 1), date(2024, 5, 31), date(2024, 6, 1), date(2024, 12, 1)):
        assert dim.lookup_as_of("C1", when) == wh.resolve_customer_sk("C1", when), (
            f"model and DuckDB disagree on the version in effect at {when}"
        )
