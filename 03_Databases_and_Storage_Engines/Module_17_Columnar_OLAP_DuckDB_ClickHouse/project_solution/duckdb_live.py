"""Module 17: Real DuckDB Columnar OLAP Engine (Track B).

Interacts directly with DuckDB to demonstrate:
1. Zero-copy querying of Parquet files directly from disk without loading.
2. EXPLAIN and EXPLAIN ANALYZE physical execution plan inspection.
3. Columnar scan performance: projection pushdown measuring 1-column vs 20-column aggregations.
4. Analytical SQL window functions with running frames and partitions.
5. Automatic CSV schema sniffing via read_csv_auto.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

try:
    import duckdb
except ImportError:
    duckdb = None  # type: ignore


class DuckDBLiveEngine:
    """Production DuckDB vectorized query runner."""

    def __init__(self, db_path: str = ":memory:"):
        if duckdb is None:
            raise RuntimeError("duckdb is not installed. Install with: pip install duckdb")
        self.conn = duckdb.connect(db_path)

    def query(self, sql: str, params: list[Any] | None = None) -> list[tuple[Any, ...]]:
        """Executes a SQL query and fetches all rows."""
        if params:
            return self.conn.execute(sql, params).fetchall()
        return self.conn.execute(sql).fetchall()

    def explain_query(self, sql: str, analyze: bool = False) -> str:
        """Returns the physical plan string from EXPLAIN [ANALYZE]."""
        prefix = "EXPLAIN ANALYZE " if analyze else "EXPLAIN "
        rows = self.conn.execute(prefix + sql).fetchall()
        # rows format: [(plan_type, plan_string), ...]
        return "\n".join(str(r[1]) if len(r) > 1 else str(r[0]) for r in rows)

    def create_parquet_dataset(self, output_path: Path, row_count: int = 50_000) -> None:
        """Generates a Parquet dataset directly using DuckDB\'s parquet writer."""
        self.conn.execute(f"""
            COPY (
                SELECT
                    range AS id,
                    (range % 10) AS category_id,
                    'Product_' || (range % 500) AS product_name,
                    random() * 1000.0 AS price,
                    CURRENT_DATE - INTERVAL (range % 365) DAY AS created_date
                FROM range({row_count})
            ) TO '{output_path.as_posix()}' (FORMAT PARQUET, COMPRESSION 'ZSTD')
        """)

    def query_parquet_direct(self, parquet_path: Path, min_price: float = 500.0) -> list[tuple[Any, ...]]:
        """Queries a Parquet file directly from disk without loading it into a table."""
        sql = f"""
            SELECT category_id, COUNT(*) AS count, AVG(price) AS avg_price
            FROM '{parquet_path.as_posix()}'
            WHERE price > ?
            GROUP BY category_id
            ORDER BY avg_price DESC
        """
        return self.conn.execute(sql, [min_price]).fetchall()

    def benchmark_columnar_vs_row_scan(self, n_rows: int = 100_000) -> dict[str, float]:
        """Demonstrates columnar projection pushdown speedup."""
        # Generate wide table with 15 columns
        cols = ", ".join(f"random() * 100 AS col_{i}" for i in range(15))
        self.conn.execute(f"""
            CREATE OR REPLACE TABLE wide_bench AS
            SELECT range AS id, {cols} FROM range({n_rows})
        """)

        # 1. Single-column scan: only 1 column loaded from columnar storage
        start_single = time.perf_counter()
        self.conn.execute("SELECT SUM(col_0) FROM wide_bench").fetchall()
        single_time = time.perf_counter() - start_single

        # 2. All-columns scan: touching every single column across all rows
        sum_all = " + ".join(f"col_{i}" for i in range(15))
        start_all = time.perf_counter()
        self.conn.execute(f"SELECT SUM({sum_all}) FROM wide_bench").fetchall()
        all_time = time.perf_counter() - start_all

        return {
            "rows": float(n_rows),
            "single_column_time_s": single_time,
            "all_columns_time_s": all_time,
            "ratio": all_time / single_time if single_time > 0 else 1.0,
        }

    def execute_window_analytics(self) -> list[tuple[Any, ...]]:
        """Runs complex analytical window queries with running cumulative totals and moving averages."""
        self.conn.execute("""
            CREATE OR REPLACE TEMP TABLE sales_daily AS
            SELECT
                i AS day_idx,
                (i % 3) AS dept_id,
                100.0 + (i * 5.5) AS revenue
            FROM range(30) t(i)
        """)
        sql = """
            SELECT
                day_idx,
                dept_id,
                revenue,
                SUM(revenue) OVER (
                    PARTITION BY dept_id
                    ORDER BY day_idx
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) AS running_total,
                AVG(revenue) OVER (
                    PARTITION BY dept_id
                    ORDER BY day_idx
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ) AS moving_avg_3day
            FROM sales_daily
            ORDER BY dept_id, day_idx
        """
        return self.conn.execute(sql).fetchall()

    def query_csv_auto(self, csv_path: Path) -> list[tuple[Any, ...]]:
        """Queries CSV file with automatic delimiter, quote, and type sniffing."""
        return self.conn.execute(f"SELECT * FROM read_csv_auto('{csv_path.as_posix()}')").fetchall()
