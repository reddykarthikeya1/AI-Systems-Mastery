"""Module 18 - The same warehouse, in real DuckDB (Track B: operation).

Track A builds the mechanisms by hand. This file drives a real analytical
engine: real DDL, a real two-statement SCD2 merge, a real materialised aggregate
with a watermark-incremental refresh, and real ``EXPLAIN`` output showing the
join order the optimiser actually chose.

DuckDB is embedded, so unlike the server-backed modules in this course these
tests need no Docker and never skip. That is deliberate - the reconciliation
test is the most important test in the module, and it should not be the one that
silently stops running on a bare machine.

The SCD2 merge, and why it is two statements
--------------------------------------------
Warehouses express this as ``MERGE`` (or DuckDB's newer ``MERGE INTO``). Written
out longhand it is:

1. ``UPDATE`` the open row - set ``valid_to`` to the day before the change and
   clear ``is_current``.
2. ``INSERT`` the new version with ``valid_from`` at the change date.

Both must happen inside one transaction. If step 1 commits alone the key has no
current row; if step 2 commits alone the key has two, and every join against the
dimension silently doubles that customer's revenue. ``load_scd2_change`` wraps
them, and ``test_scd2_merge_is_atomic`` proves a mid-merge failure leaves exactly
one current row.
"""

from __future__ import annotations

import os
import time
from datetime import date, timedelta
from typing import Any

try:
    import duckdb
except ImportError:  # pragma: no cover - exercised only on a machine without duckdb
    duckdb = None  # type: ignore[assignment]

END_OF_TIME = date(9999, 12, 31)


class WarehouseUnavailableError(RuntimeError):
    """Raised when DuckDB is not importable."""


class LiveWarehouse:
    """A real star schema in DuckDB.

    ``db_path`` defaults to in-memory. Set ``DUCKDB_WAREHOUSE_PATH`` to persist,
    which is how you inspect the tables with the DuckDB CLI after a test run.
    """

    def __init__(self, db_path: str | None = None) -> None:
        if duckdb is None:
            raise WarehouseUnavailableError(
                "duckdb is not installed. Install with: pip install duckdb"
            )
        self.db_path = db_path or os.getenv("DUCKDB_WAREHOUSE_PATH", ":memory:")
        self.conn = duckdb.connect(self.db_path)

    # -- lifecycle ----------------------------------------------------------
    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> LiveWarehouse:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def query(self, sql: str, params: list[Any] | None = None) -> list[tuple[Any, ...]]:
        return self.conn.execute(sql, params or []).fetchall()

    # -- DDL ----------------------------------------------------------------
    def create_schema(self) -> None:
        """Build the star. Idempotent, because every test in this course must be.

        Note the column types: surrogate keys are INTEGER, natural keys VARCHAR.
        The fact table carries only keys, one date and one measure - it stays
        narrow so a scan touches as few bytes per row as possible, which is the
        entire economic argument for dimensional modelling on columnar storage.
        """
        self.conn.execute("DROP TABLE IF EXISTS fact_sales")
        self.conn.execute("DROP TABLE IF EXISTS dim_customer")
        self.conn.execute("DROP TABLE IF EXISTS dim_product")
        self.conn.execute("DROP TABLE IF EXISTS mv_revenue_by_state")
        self.conn.execute("DROP SEQUENCE IF EXISTS seq_customer_sk")
        self.conn.execute("DROP SEQUENCE IF EXISTS seq_product_sk")

        self.conn.execute("CREATE SEQUENCE seq_customer_sk START 1")
        self.conn.execute("CREATE SEQUENCE seq_product_sk START 1")

        self.conn.execute(
            """
            CREATE TABLE dim_customer (
                customer_sk  INTEGER PRIMARY KEY,
                customer_id  VARCHAR NOT NULL,
                state        VARCHAR NOT NULL,
                phone        VARCHAR,
                valid_from   DATE    NOT NULL,
                valid_to     DATE    NOT NULL,
                is_current   BOOLEAN NOT NULL
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE dim_product (
                product_sk  INTEGER PRIMARY KEY,
                product_id  VARCHAR NOT NULL,
                category    VARCHAR NOT NULL,
                valid_from  DATE    NOT NULL,
                valid_to    DATE    NOT NULL,
                is_current  BOOLEAN NOT NULL
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE fact_sales (
                customer_sk INTEGER NOT NULL,
                product_sk  INTEGER NOT NULL,
                event_date  DATE    NOT NULL,
                revenue     DOUBLE  NOT NULL
            )
            """
        )

    # -- dimension loads ----------------------------------------------------
    def insert_customer_version(
        self,
        customer_id: str,
        state: str,
        valid_from: date,
        phone: str | None = None,
        valid_to: date = END_OF_TIME,
        is_current: bool = True,
    ) -> int:
        row = self.conn.execute(
            """
            INSERT INTO dim_customer
            VALUES (nextval('seq_customer_sk'), ?, ?, ?, ?, ?, ?)
            RETURNING customer_sk
            """,
            [customer_id, state, phone, valid_from, valid_to, is_current],
        ).fetchone()
        return int(row[0])

    def insert_product(self, product_id: str, category: str, valid_from: date) -> int:
        row = self.conn.execute(
            """
            INSERT INTO dim_product
            VALUES (nextval('seq_product_sk'), ?, ?, ?, ?, TRUE)
            RETURNING product_sk
            """,
            [product_id, category, valid_from, END_OF_TIME],
        ).fetchone()
        return int(row[0])

    def load_scd2_change(self, customer_id: str, new_state: str, effective: date) -> int:
        """Close the open version and open a new one, atomically.

        Returns the new surrogate key. Raises if the customer has no open row -
        an SCD2 update against a key that was never inserted is a pipeline
        ordering bug, and inserting silently would hide it.
        """
        open_row = self.conn.execute(
            "SELECT customer_sk, state, phone, valid_from FROM dim_customer "
            "WHERE customer_id = ? AND is_current",
            [customer_id],
        ).fetchone()
        if open_row is None:
            raise ValueError(
                f"no open version for customer_id={customer_id!r} - load the initial "
                "row before applying a change"
            )

        _sk, current_state, phone, valid_from = open_row
        if current_state == new_state:
            return int(_sk)
        if effective <= valid_from:
            raise ValueError(
                f"out-of-order load for {customer_id!r}: effective {effective} is not "
                f"after the open version's start {valid_from}"
            )

        self.conn.execute("BEGIN TRANSACTION")
        try:
            self.conn.execute(
                "UPDATE dim_customer SET valid_to = ?, is_current = FALSE "
                "WHERE customer_id = ? AND is_current",
                [effective - timedelta(days=1), customer_id],
            )
            new_sk = self.insert_customer_version(
                customer_id, new_state, effective, phone=phone
            )
            self.conn.execute("COMMIT")
            return new_sk
        except Exception:
            self.conn.execute("ROLLBACK")
            raise

    # -- fact loads ---------------------------------------------------------
    def resolve_customer_sk(self, customer_id: str, when: date) -> int | None:
        """The as-of join. This is the SQL form of ``lookup_as_of``.

        ``BETWEEN`` works only because ``valid_to`` is NOT NULL - that is what the
        9999-12-31 sentinel buys.
        """
        row = self.conn.execute(
            "SELECT customer_sk FROM dim_customer "
            "WHERE customer_id = ? AND ? BETWEEN valid_from AND valid_to",
            [customer_id, when],
        ).fetchone()
        return int(row[0]) if row else None

    def insert_sale(
        self, customer_sk: int, product_sk: int, event_date: date, revenue: float
    ) -> None:
        self.conn.execute(
            "INSERT INTO fact_sales VALUES (?, ?, ?, ?)",
            [customer_sk, product_sk, event_date, revenue],
        )

    # -- queries ------------------------------------------------------------
    def revenue_by_state(self) -> dict[tuple[str], float]:
        """The star join, in SQL. Shape matches Track A's ``aggregate`` output so
        the reconciliation test can compare the two dicts directly."""
        rows = self.conn.execute(
            """
            SELECT c.state, SUM(f.revenue) AS revenue
            FROM fact_sales f
            JOIN dim_customer c ON f.customer_sk = c.customer_sk
            GROUP BY c.state
            ORDER BY c.state
            """
        ).fetchall()
        return {(state,): float(revenue) for state, revenue in rows}

    def revenue_by_state_and_category(self) -> dict[tuple[str, str], float]:
        rows = self.conn.execute(
            """
            SELECT c.state, p.category, SUM(f.revenue) AS revenue
            FROM fact_sales f
            JOIN dim_customer c ON f.customer_sk = c.customer_sk
            JOIN dim_product  p ON f.product_sk  = p.product_sk
            GROUP BY c.state, p.category
            ORDER BY c.state, p.category
            """
        ).fetchall()
        return {(state, cat): float(rev) for state, cat, rev in rows}

    def explain_star_join(self, analyze: bool = False) -> str:
        """The optimiser's actual plan for the two-dimension star join.

        Worth reading rather than trusting: a star join should show the small
        dimension tables built into hash tables and the large fact table probing
        them. If the plan shows the reverse, the row-count estimates are wrong and
        the usual cause is stale statistics.
        """
        prefix = "EXPLAIN ANALYZE " if analyze else "EXPLAIN "
        rows = self.conn.execute(
            prefix
            + """
            SELECT c.state, p.category, SUM(f.revenue)
            FROM fact_sales f
            JOIN dim_customer c ON f.customer_sk = c.customer_sk
            JOIN dim_product  p ON f.product_sk  = p.product_sk
            GROUP BY c.state, p.category
            """
        ).fetchall()
        return "\n".join(str(cell) for row in rows for cell in row)

    # -- materialised aggregate --------------------------------------------
    def create_materialized_aggregate(self) -> None:
        """DuckDB has no incrementally-maintained materialised view, so this is
        the pattern every warehouse uses underneath one: a real table plus an
        explicit refresh path. Making that explicit is the point - a
        "materialised view" is always a cache with a refresh policy, and the
        policy is the part that goes wrong."""
        self.conn.execute("DROP TABLE IF EXISTS mv_revenue_by_state")
        self.conn.execute(
            """
            CREATE TABLE mv_revenue_by_state AS
            SELECT c.state, SUM(f.revenue) AS revenue, MAX(f.event_date) AS max_event_date
            FROM fact_sales f
            JOIN dim_customer c ON f.customer_sk = c.customer_sk
            GROUP BY c.state
            """
        )

    def refresh_aggregate_full(self) -> None:
        self.create_materialized_aggregate()

    def refresh_aggregate_incremental(self, watermark: date) -> int:
        """Merge only rows after ``watermark``. Returns rows consumed.

        Correct for SUM because SUM is additive. The same shape applied to a
        ``COUNT(DISTINCT ...)`` returns a number that is wrong and plausible,
        which is worse than a crash.
        """
        delta = self.conn.execute(
            """
            SELECT c.state, SUM(f.revenue) AS revenue, COUNT(*) AS n
            FROM fact_sales f
            JOIN dim_customer c ON f.customer_sk = c.customer_sk
            WHERE f.event_date > ?
            GROUP BY c.state
            """,
            [watermark],
        ).fetchall()

        consumed = 0
        for state, revenue, n in delta:
            consumed += int(n)
            existing = self.conn.execute(
                "SELECT revenue FROM mv_revenue_by_state WHERE state = ?", [state]
            ).fetchone()
            if existing is None:
                self.conn.execute(
                    "INSERT INTO mv_revenue_by_state VALUES (?, ?, ?)",
                    [state, float(revenue), watermark],
                )
            else:
                self.conn.execute(
                    "UPDATE mv_revenue_by_state SET revenue = revenue + ? WHERE state = ?",
                    [float(revenue), state],
                )
        return consumed

    def aggregate_contents(self) -> dict[tuple[str], float]:
        rows = self.conn.execute(
            "SELECT state, revenue FROM mv_revenue_by_state ORDER BY state"
        ).fetchall()
        return {(state,): float(revenue) for state, revenue in rows}

    # -- measurement --------------------------------------------------------
    def time_query(self, sql: str, repeats: int = 3) -> float:
        """Best-of-N wall clock in milliseconds.

        Best-of rather than mean: this is a latency floor measurement, and the
        mean on a laptop measures whatever else the OS decided to do.
        """
        best = float("inf")
        for _ in range(repeats):
            started = time.perf_counter()
            self.conn.execute(sql).fetchall()
            best = min(best, (time.perf_counter() - started) * 1000)
        return best

    def seed_scale(self, customers: int = 200, days: int = 90, rows: int = 20_000) -> None:
        """Generate a fact table big enough that the aggregate table actually wins.

        Uses DuckDB's own ``range`` and ``setseed`` so generation happens inside
        the engine and stays reproducible across runs.
        """
        self.conn.execute("SELECT setseed(0.42)")
        for i in range(customers):
            state = ["OH", "TX", "CA", "NY"][i % 4]
            self.insert_customer_version(f"C{i}", state, date(2024, 1, 1))
        self.insert_product("P1", "widget", date(2024, 1, 1))

        self.conn.execute(
            """
            INSERT INTO fact_sales
            SELECT
                (CAST(floor(random() * ?) AS INTEGER) + 1) AS customer_sk,
                1                                          AS product_sk,
                DATE '2024-01-01' + CAST(floor(random() * ?) AS INTEGER) AS event_date,
                round(random() * 100, 2)                   AS revenue
            FROM range(?)
            """,
            [customers, days, rows],
        )
