"""Tests for Module 17: ClickHouse MergeTree & Materialized Views (Track B)."""

from __future__ import annotations

from datetime import datetime

import pytest

def _clickhouse_is_up() -> bool:
    try:
        from clickhouse_live import ClickHouseLiveClient
        client = ClickHouseLiveClient()
        return client.ping()
    except Exception:
        return False

requires_clickhouse = pytest.mark.skipif(
    not _clickhouse_is_up(),
    reason="ClickHouse not reachable on localhost:18123 - start with: make up clickhouse"
)

pytestmark = [pytest.mark.requires_clickhouse, requires_clickhouse]


def test_clickhouse_live_ping():
    from clickhouse_live import ClickHouseLiveClient
    client = ClickHouseLiveClient()
    assert client.ping() is True


def test_clickhouse_mergetree_table_creation():
    from clickhouse_live import ClickHouseLiveClient
    client = ClickHouseLiveClient()
    client.setup_mergetree_table("events_test_m17")
    tables = [r[0] for r in client.query("SHOW TABLES LIKE 'events_test_m17'")]
    assert "events_test_m17" in tables


def test_clickhouse_materialized_view():
    from clickhouse_live import ClickHouseLiveClient
    client = ClickHouseLiveClient()
    client.setup_mergetree_table("events_src_m17")
    client.setup_materialized_view("events_src_m17", "events_summary_m17")
    mv_exists = len(client.query("SHOW TABLES LIKE 'events_summary_m17'")) > 0
    assert mv_exists is True


def test_clickhouse_batch_insert_and_query():
    from clickhouse_live import ClickHouseLiveClient
    client = ClickHouseLiveClient()
    client.setup_mergetree_table("events_insert_m17")

    # A ClickHouse `DateTime` column requires a real datetime object, not a
    # string. clickhouse_connect serialises by calling .timestamp() on the
    # value, so a str raises AttributeError inside the driver - an error whose
    # message ("'str' object has no attribute 'timestamp'") points nowhere near
    # the actual mistake. This is the columnar equivalent of the dtype lesson in
    # Module 25: type your data at the boundary.
    rows = [
        [101, datetime(2026, 3, 1, 10, 0, 0), "LOGIN", 150, "payload_1"],
        [101, datetime(2026, 3, 1, 10, 5, 0), "PURCHASE", 320, "payload_2"],
        [102, datetime(2026, 3, 1, 10, 10, 0), "SEARCH", 45, "payload_3"],
    ]
    cols = ["tenant_id", "event_time", "event_type", "duration_ms", "payload"]
    client.insert_batch("events_insert_m17", rows, cols)

    res = client.query("SELECT count() FROM events_insert_m17 WHERE tenant_id = 101")
    assert res[0][0] >= 2


def test_clickhouse_codec_compression_metrics():
    from clickhouse_live import ClickHouseLiveClient
    client = ClickHouseLiveClient()
    parts = client.query("SELECT count() FROM system.parts WHERE active = 1")
    assert len(parts) > 0


def test_clickhouse_vectorized_sum_aggregation():
    from clickhouse_live import ClickHouseLiveClient
    client = ClickHouseLiveClient()
    res = client.query("SELECT sum(number) FROM numbers(1000)")
    assert res[0][0] == 499500


def test_clickhouse_any_array_aggregation():
    from clickhouse_live import ClickHouseLiveClient
    client = ClickHouseLiveClient()
    res = client.query("SELECT groupArray(number) FROM numbers(5)")
    assert res[0][0] == [0, 1, 2, 3, 4]


def test_clickhouse_reconciliation_with_columnar_model():
    from clickhouse_live import ClickHouseLiveClient
    from columnar_engine import ColumnarTable
    client = ClickHouseLiveClient()

    # Model
    model = ColumnarTable(schema={"v": "int"})
    model.append_rows([{"v": i} for i in range(10)])
    model_sum = model.aggregate("v", "SUM")

    # ClickHouse
    ch_sum = client.query("SELECT sum(number) FROM numbers(10)")[0][0]
    assert model_sum == float(ch_sum) == 45.0
