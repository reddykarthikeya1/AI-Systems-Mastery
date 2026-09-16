"""Module 17: Real ClickHouse Columnar OLAP Client (Track B).

Interacts with a live ClickHouse server via clickhouse-connect to demonstrate:
1. MergeTree engine table creation with primary key ordering.
2. Real-time aggregating materialized views with SumMingMergeTree.
3. Column compression codecs comparison (LZ4 vs ZSTD vs Delta).
4. High-throughput vectorized batch inserts.
"""

from __future__ import annotations

import os

from typing import Any

try:
    import clickhouse_connect
except ImportError:
    clickhouse_connect = None  # type: ignore


class ClickHouseLiveClient:
    """Production ClickHouse client wrapper."""

    def __init__(self, host: str = os.environ.get("COURSE_DB_HOST", "localhost"), port: int = int(os.environ.get("COURSE_CLICKHOUSE_PORT", "18123")), username: str = "default", password: str = ""):
        if clickhouse_connect is None:
            raise RuntimeError("clickhouse-connect is not installed. Install with: pip install clickhouse-connect")
        self.client = clickhouse_connect.get_client(host=host, port=port, username=username, password=password)

    def ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except Exception:
            return False

    def setup_mergetree_table(self, table_name: str = "events_log") -> None:
        """Creates a MergeTree table partitioned by month and ordered by tenant and timestamp."""
        self.client.command(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                tenant_id UInt32,
                event_time DateTime CODEC(DoubleDelta, LZ4),
                event_type LowCardinality(String),
                duration_ms UInt32 CODEC(T64, ZSTD(1)),
                payload String CODEC(ZSTD(3))
            ) ENGINE = MergeTree()
            PARTITION BY toYYYYMM(event_time)
            ORDER BY (tenant_id, event_time, event_type)
        """)

    def setup_materialized_view(self, source_table: str = "events_log", mv_table: str = "events_daily_summary") -> None:
        """Sets up an aggregating materialized view with SummingMergeTree."""
        self.client.command(f"""
            CREATE TABLE IF NOT EXISTS {mv_table} (
                event_date Date,
                tenant_id UInt32,
                event_count UInt64,
                total_duration_ms UInt64
            ) ENGINE = SummingMergeTree()
            PRIMARY KEY (event_date, tenant_id)
        """)

        self.client.command(f"""
            CREATE MATERIALIZED VIEW IF NOT EXISTS {mv_table}_mv TO {mv_table} AS
            SELECT
                toDate(event_time) AS event_date,
                tenant_id,
                count() AS event_count,
                sum(duration_ms) AS total_duration_ms
            FROM {source_table}
            GROUP BY event_date, tenant_id
        """)

    def insert_batch(self, table_name: str, rows: list[list[Any]], column_names: list[str]) -> None:
        self.client.insert(table_name, rows, column_names=column_names)

    def query(self, sql: str) -> Any:
        return self.client.query(sql).result_rows
