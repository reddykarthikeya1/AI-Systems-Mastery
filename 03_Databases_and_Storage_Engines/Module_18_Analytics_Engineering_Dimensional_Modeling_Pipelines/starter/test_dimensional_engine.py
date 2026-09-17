"""Track A tests: the dimensional model's invariants, asserted rather than asserted-to.

Each test here corresponds to a failure mode that produces *plausible wrong
numbers* rather than an exception - which is why they have to be tests and not
review comments.
"""

from __future__ import annotations

from datetime import date

import pytest
from dimensional_engine import (
    END_OF_TIME,
    Backfill,
    DimensionalModelError,
    DimensionTable,
    FactTable,
    MaterializedView,
    PipelineDAG,
    StarSchema,
    SurrogateKeyAllocator,
    Task,
    WatermarkStore,
)

# ---------------------------------------------------------------------------
# Surrogate keys
# ---------------------------------------------------------------------------


def test_surrogate_keys_are_monotonic_and_per_table():
    alloc = SurrogateKeyAllocator()
    assert [alloc.next_key("dim_customer") for _ in range(3)] == [1, 2, 3]
    # A second dimension starts its own sequence rather than continuing the first.
    assert alloc.next_key("dim_product") == 1


# ---------------------------------------------------------------------------
# SCD Type 2 - the core of the module
# ---------------------------------------------------------------------------


def _customer_dim() -> DimensionTable:
    return DimensionTable("dim_customer", scd_type=2, tracked_attributes={"state"})


def test_scd2_creates_a_new_version_when_a_tracked_attribute_changes():
    dim = _customer_dim()
    first = dim.upsert("C1", {"state": "OH", "phone": "555-0100"}, date(2024, 1, 1))
    second = dim.upsert("C1", {"state": "TX", "phone": "555-0100"}, date(2024, 6, 1))

    assert first != second
    assert dim.version_count("C1") == 2


def test_scd2_ignores_untracked_changes_and_corrects_them_in_place():
    """A daily full extract re-sends every row. Versioning on an untracked field
    would produce 365 versions per key per year."""
    dim = _customer_dim()
    key = dim.upsert("C1", {"state": "OH", "phone": "555-0100"}, date(2024, 1, 1))
    same = dim.upsert("C1", {"state": "OH", "phone": "555-0999"}, date(2024, 2, 1))

    assert same == key
    assert dim.version_count("C1") == 1
    assert dim.current("C1").attributes["phone"] == "555-0999"


def test_scd2_repeated_identical_load_is_a_noop():
    dim = _customer_dim()
    dim.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    for day in range(2, 10):
        dim.upsert("C1", {"state": "OH"}, date(2024, 1, day))
    assert dim.version_count("C1") == 1


def test_scd2_intervals_tile_the_timeline():
    """No gaps, no overlaps, and exactly one open version."""
    dim = _customer_dim()
    dim.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    dim.upsert("C1", {"state": "TX"}, date(2024, 6, 1))
    dim.upsert("C1", {"state": "CA"}, date(2024, 9, 1))

    versions = [v for v in dim.rows if v.natural_key == "C1"]
    assert len(versions) == 3
    for earlier, later in zip(versions, versions[1:], strict=False):
        # Inclusive ranges: the next version starts the day after the previous ends.
        assert (later.valid_from - earlier.valid_to).days == 1

    open_versions = [v for v in versions if v.is_current]
    assert len(open_versions) == 1
    assert open_versions[0].valid_to == END_OF_TIME


def test_scd2_preserves_history():
    """The test this module exists for.

    A customer moves OH -> TX in June. A January order must still resolve to the
    Ohio version. Joining on the *current* version instead would silently move
    January's revenue to Texas.
    """
    dim = _customer_dim()
    ohio_key = dim.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    texas_key = dim.upsert("C1", {"state": "TX"}, date(2024, 6, 1))

    assert dim.lookup_as_of("C1", date(2024, 3, 15)) == ohio_key
    assert dim.lookup_as_of("C1", date(2024, 7, 15)) == texas_key
    # And the naive approach would have used texas_key for both:
    assert dim.current("C1").surrogate_key == texas_key


def test_scd2_lookup_before_first_version_returns_none():
    """Not zero, not the earliest version - None. An event that predates the
    dimension is a data-quality problem, and silently attributing it to the
    first known version hides that."""
    dim = _customer_dim()
    dim.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    assert dim.lookup_as_of("C1", date(2023, 12, 31)) is None


def test_scd2_rejects_out_of_order_loads():
    dim = _customer_dim()
    dim.upsert("C1", {"state": "OH"}, date(2024, 6, 1))
    with pytest.raises(DimensionalModelError, match="out-of-order"):
        dim.upsert("C1", {"state": "TX"}, date(2024, 1, 1))


def test_scd1_overwrites_without_versioning():
    dim = DimensionTable("dim_customer", scd_type=1, tracked_attributes={"state"})
    first = dim.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    second = dim.upsert("C1", {"state": "TX"}, date(2024, 6, 1))

    assert first == second
    assert dim.version_count("C1") == 1
    # History is gone - a January lookup now reports Texas. That is what Type 1
    # means, and it is why the choice has to be deliberate.
    assert dim.lookup_as_of("C1", date(2024, 3, 1)) == first
    assert dim.current("C1").attributes["state"] == "TX"


def test_unsupported_scd_type_is_rejected_at_construction():
    with pytest.raises(DimensionalModelError, match="unsupported SCD type"):
        DimensionTable("dim_bad", scd_type=3)


# ---------------------------------------------------------------------------
# Fact grain
# ---------------------------------------------------------------------------


def _sales_fact() -> FactTable:
    return FactTable("fact_sales", grain=("customer_sk", "product_sk"), measures=("revenue",))


def test_fact_rejects_a_row_missing_a_grain_key():
    fact = _sales_fact()
    with pytest.raises(DimensionalModelError, match="missing grain keys"):
        fact.insert({"customer_sk": 1}, {"revenue": 10.0}, date(2024, 1, 1))


def test_fact_rejects_a_row_outside_the_declared_grain():
    """Mixed-grain fact tables make every SUM wrong with no error anywhere."""
    fact = _sales_fact()
    with pytest.raises(DimensionalModelError, match="outside the declared grain"):
        fact.insert(
            {"customer_sk": 1, "product_sk": 2, "store_sk": 3},
            {"revenue": 10.0},
            date(2024, 1, 1),
        )


def test_fact_rejects_unknown_measures():
    fact = _sales_fact()
    with pytest.raises(DimensionalModelError, match="unknown measures"):
        fact.insert(
            {"customer_sk": 1, "product_sk": 2}, {"profit": 3.0}, date(2024, 1, 1)
        )


# ---------------------------------------------------------------------------
# The star join
# ---------------------------------------------------------------------------


def _built_star() -> tuple[StarSchema, DimensionTable]:
    alloc = SurrogateKeyAllocator()
    customers = DimensionTable("dim_customer", 2, {"state"}, alloc)
    products = DimensionTable("dim_product", 2, {"category"}, alloc)

    oh = customers.upsert("C1", {"state": "OH"}, date(2024, 1, 1))
    tx = customers.upsert("C1", {"state": "TX"}, date(2024, 6, 1))
    c2 = customers.upsert("C2", {"state": "OH"}, date(2024, 1, 1))
    widget = products.upsert("P1", {"category": "widget"}, date(2024, 1, 1))

    fact = _sales_fact()
    star = StarSchema(fact)
    star.add_dimension("customer_sk", customers)
    star.add_dimension("product_sk", products)

    fact.insert({"customer_sk": oh, "product_sk": widget}, {"revenue": 100.0}, date(2024, 3, 1))
    fact.insert({"customer_sk": c2, "product_sk": widget}, {"revenue": 50.0}, date(2024, 3, 1))
    fact.insert({"customer_sk": tx, "product_sk": widget}, {"revenue": 25.0}, date(2024, 7, 1))
    return star, customers


def test_star_aggregate_groups_by_the_historical_dimension_version():
    star, _ = _built_star()
    by_state = star.aggregate([("customer_sk", "state")], "revenue")

    # 100 + 50 booked while both customers were in Ohio; 25 after the move.
    assert by_state == {("OH",): 150.0, ("TX",): 25.0}


def test_star_aggregate_supports_multiple_grouping_columns():
    star, _ = _built_star()
    result = star.aggregate([("customer_sk", "state"), ("product_sk", "category")], "revenue")
    assert result == {("OH", "widget"): 150.0, ("TX", "widget"): 25.0}


def test_star_aggregate_count_and_avg():
    star, _ = _built_star()
    assert star.aggregate([("customer_sk", "state")], "revenue", agg="count") == {
        ("OH",): 2.0,
        ("TX",): 1.0,
    }
    assert star.aggregate([("customer_sk", "state")], "revenue", agg="avg") == {
        ("OH",): 75.0,
        ("TX",): 25.0,
    }


def test_star_rejects_a_dimension_not_in_the_fact_grain():
    star = StarSchema(_sales_fact())
    with pytest.raises(DimensionalModelError, match="not in fact_sales's grain"):
        star.add_dimension("store_sk", DimensionTable("dim_store"))


def test_star_rejects_unknown_measure_and_aggregate():
    star, _ = _built_star()
    with pytest.raises(DimensionalModelError, match="unknown measure"):
        star.aggregate([("customer_sk", "state")], "profit")
    with pytest.raises(DimensionalModelError, match="unsupported aggregate"):
        star.aggregate([("customer_sk", "state")], "revenue", agg="median")


# ---------------------------------------------------------------------------
# Materialised views
# ---------------------------------------------------------------------------


def _revenue_by_state(star: StarSchema) -> dict:
    return star.aggregate([("customer_sk", "state")], "revenue")


def test_view_raises_before_first_refresh():
    star, _ = _built_star()
    view = MaterializedView("mv_revenue", star, _revenue_by_state)
    assert view.is_stale is True
    with pytest.raises(DimensionalModelError, match="never been refreshed"):
        _ = view.data


def test_view_detects_staleness_after_a_new_fact_row():
    star, _ = _built_star()
    view = MaterializedView("mv_revenue", star, _revenue_by_state)
    view.refresh()
    assert view.is_stale is False

    star.fact.insert({"customer_sk": 1, "product_sk": 1}, {"revenue": 7.0}, date(2024, 8, 1))
    assert view.is_stale is True


def test_incremental_refresh_matches_a_full_refresh():
    """The property that makes incremental refresh safe for additive measures."""
    star, _ = _built_star()
    incremental = MaterializedView("mv_inc", star, _revenue_by_state)
    incremental.refresh()

    watermark = date(2024, 7, 1)
    star.fact.insert({"customer_sk": 2, "product_sk": 1}, {"revenue": 40.0}, date(2024, 8, 1))
    merged = incremental.refresh_incremental(watermark)

    full = MaterializedView("mv_full", star, _revenue_by_state)
    assert merged == full.refresh()


def test_incremental_refresh_with_no_new_rows_clears_staleness_without_recomputing():
    star, _ = _built_star()
    view = MaterializedView("mv_revenue", star, _revenue_by_state)
    view.refresh()
    refreshes = view.refresh_count

    view.refresh_incremental(date(2024, 12, 31))
    assert view.refresh_count == refreshes
    assert view.is_stale is False


def test_non_additive_view_refuses_incremental_refresh():
    """A median cannot be merged from deltas. Raising beats a wrong number."""
    star, _ = _built_star()
    view = MaterializedView(
        "mv_median", star, _revenue_by_state, supports_incremental=False
    )
    view.refresh()
    with pytest.raises(DimensionalModelError, match="non-additive"):
        view.refresh_incremental(date(2024, 1, 1))


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------


def test_topological_order_respects_dependencies():
    dag = PipelineDAG()
    dag.add_task(Task("load_fact", lambda c: None, depends_on=("load_dim", "extract")))
    dag.add_task(Task("load_dim", lambda c: None, depends_on=("extract",)))
    dag.add_task(Task("extract", lambda c: None))
    dag.add_task(Task("refresh_view", lambda c: None, depends_on=("load_fact",)))

    order = dag.topological_order()
    assert order.index("extract") < order.index("load_dim")
    assert order.index("load_dim") < order.index("load_fact")
    assert order.index("load_fact") < order.index("refresh_view")


def test_cycle_is_reported_as_an_error_not_a_hang():
    dag = PipelineDAG()
    dag.add_task(Task("a", lambda c: None, depends_on=("b",)))
    dag.add_task(Task("b", lambda c: None, depends_on=("a",)))
    with pytest.raises(DimensionalModelError, match="dependency cycle"):
        dag.topological_order()


def test_unknown_dependency_is_rejected():
    dag = PipelineDAG()
    dag.add_task(Task("a", lambda c: None, depends_on=("nope",)))
    with pytest.raises(DimensionalModelError, match="unknown task"):
        dag.topological_order()


def test_duplicate_task_name_is_rejected():
    dag = PipelineDAG()
    dag.add_task(Task("a", lambda c: None))
    with pytest.raises(DimensionalModelError, match="duplicate task"):
        dag.add_task(Task("a", lambda c: None))


def test_rerunning_the_same_run_key_does_not_double_load():
    """The idempotency property. Without it a retry doubles every measure, and
    the result looks plausible enough to survive review."""
    loaded: list[int] = []
    dag = PipelineDAG()
    dag.add_task(Task("load", lambda c: loaded.append(1)))

    dag.run("2024-03-01")
    dag.run("2024-03-01")

    assert len(loaded) == 1
    assert dag.skipped == ["load"]


def test_a_different_run_key_loads_again():
    loaded: list[int] = []
    dag = PipelineDAG()
    dag.add_task(Task("load", lambda c: loaded.append(1)))

    dag.run("2024-03-01")
    dag.run("2024-03-02")
    assert len(loaded) == 2


def test_retry_succeeds_within_max_attempts():
    state = {"calls": 0}

    def flaky(_ctx):
        state["calls"] += 1
        if state["calls"] < 3:
            raise RuntimeError("transient")
        return "ok"

    dag = PipelineDAG()
    dag.add_task(Task("flaky", flaky, max_attempts=3))
    assert dag.run("k")["flaky"] == "ok"
    assert dag.attempts["flaky"] == 3


def test_retry_gives_up_and_reraises_the_last_error():
    dag = PipelineDAG()
    dag.add_task(
        Task("always_fails", lambda c: (_ for _ in ()).throw(RuntimeError("boom")), max_attempts=2)
    )
    with pytest.raises(RuntimeError, match="boom"):
        dag.run("k")
    assert dag.attempts["always_fails"] == 2


def test_a_failed_task_is_not_marked_complete():
    """So the next run retries it rather than skipping it."""
    dag = PipelineDAG()
    dag.add_task(Task("f", lambda c: (_ for _ in ()).throw(RuntimeError("boom"))))
    with pytest.raises(RuntimeError):
        dag.run("k")
    with pytest.raises(RuntimeError):
        dag.run("k")
    assert dag.attempts["f"] == 2


def test_downstream_task_does_not_run_when_upstream_fails():
    ran: list[str] = []
    dag = PipelineDAG()
    dag.add_task(Task("up", lambda c: (_ for _ in ()).throw(RuntimeError("boom"))))
    dag.add_task(Task("down", lambda c: ran.append("down"), depends_on=("up",)))
    with pytest.raises(RuntimeError):
        dag.run("k")
    assert ran == []


# ---------------------------------------------------------------------------
# Watermarks
# ---------------------------------------------------------------------------


def test_watermark_extract_returns_only_new_rows():
    store = WatermarkStore()
    rows = [
        {"id": 1, "updated_at": date(2024, 1, 1)},
        {"id": 2, "updated_at": date(2024, 1, 2)},
    ]
    assert len(store.extract("orders", rows)) == 2
    assert store.extract("orders", rows) == []

    rows.append({"id": 3, "updated_at": date(2024, 1, 3)})
    assert [r["id"] for r in store.extract("orders", rows)] == [3]


def test_watermark_advances_to_the_max_observed_not_to_now():
    """Advancing to "now" skips rows written during the extract, permanently."""
    store = WatermarkStore()
    store.extract("orders", [{"id": 1, "updated_at": date(2024, 1, 5)}])
    assert store.get("orders") == date(2024, 1, 5)

    # A row that was mid-flight during the previous extract still arrives.
    late = [{"id": 2, "updated_at": date(2024, 1, 6)}]
    assert len(store.extract("orders", late)) == 1


def test_watermark_never_moves_backwards():
    store = WatermarkStore()
    store.advance("orders", date(2024, 6, 1))
    store.advance("orders", date(2024, 1, 1))
    assert store.get("orders") == date(2024, 6, 1)


# ---------------------------------------------------------------------------
# Backfill
# ---------------------------------------------------------------------------


def test_backfill_batches_cover_the_range_exactly_once():
    bf = Backfill(date(2024, 1, 1), date(2024, 1, 31), batch_days=7)
    batches = list(bf.batches())

    assert batches[0][0] == date(2024, 1, 1)
    assert batches[-1][1] == date(2024, 1, 31)
    for earlier, later in zip(batches, batches[1:], strict=False):
        assert (later[0] - earlier[1]).days == 1
    assert bf.batch_count == 5


def test_backfill_single_day_range_is_one_batch():
    bf = Backfill(date(2024, 1, 1), date(2024, 1, 1), batch_days=7)
    assert list(bf.batches()) == [(date(2024, 1, 1), date(2024, 1, 1))]


def test_backfill_rejects_an_inverted_range_and_a_zero_batch():
    with pytest.raises(DimensionalModelError, match="empty range"):
        Backfill(date(2024, 2, 1), date(2024, 1, 1))
    with pytest.raises(DimensionalModelError, match="at least 1"):
        Backfill(date(2024, 1, 1), date(2024, 2, 1), batch_days=0)
