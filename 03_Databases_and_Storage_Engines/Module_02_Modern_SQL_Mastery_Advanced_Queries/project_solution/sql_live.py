"""Module 02: Modern SQL Mastery & Advanced Analytical Queries (Track B).

Operates directly on SQLite / DuckDB SQL engines executing:
1. Hierarchical Recursive Common Table Expressions (CTEs) traversing org charts and tree graphs.
2. Advanced Window Functions (ROW_NUMBER, DENSE_RANK, LAG, LEAD, frame specs: ROWS BETWEEN).
3. Complex multi-table aggregations, rollup reporting, and EXPLAIN QUERY PLAN analysis.
"""

from __future__ import annotations

import sqlite3
from typing import Any


class SqlLiveEngine:
    """Production analytical SQL query runner executing complex modern SQL statements."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self) -> None:
        cur = self.conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                manager_id INTEGER,
                department TEXT NOT NULL,
                salary REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS daily_sales (
                sale_date TEXT NOT NULL,
                region TEXT NOT NULL,
                amount REAL NOT NULL,
                PRIMARY KEY (sale_date, region)
            );
        """)
        self.conn.commit()

    def seed_data(self) -> None:
        cur = self.conn.cursor()
        cur.executemany(
            "INSERT OR REPLACE INTO employees (emp_id, name, manager_id, department, salary) VALUES (?, ?, ?, ?, ?)",
            [
                (1, "Alice CEO", None, "Executive", 250000.0),
                (2, "Bob VP Eng", 1, "Engineering", 180000.0),
                (3, "Carol VP Sales", 1, "Sales", 175000.0),
                (4, "Dave Lead Dev", 2, "Engineering", 140000.0),
                (5, "Eve Senior Dev", 4, "Engineering", 120000.0),
                (6, "Frank Junior Dev", 4, "Engineering", 85000.0),
                (7, "Grace Sales Exec", 3, "Sales", 95000.0),
            ],
        )
        cur.executemany(
            "INSERT OR REPLACE INTO daily_sales (sale_date, region, amount) VALUES (?, ?, ?)",
            [
                ("2026-01-01", "North", 1200.0),
                ("2026-01-02", "North", 1500.0),
                ("2026-01-03", "North", 1100.0),
                ("2026-01-04", "North", 1800.0),
                ("2026-01-01", "South", 900.0),
                ("2026-01-02", "South", 950.0),
                ("2026-01-03", "South", 1300.0),
                ("2026-01-04", "South", 1400.0),
            ],
        )
        self.conn.commit()

    def get_management_hierarchy(self, root_emp_id: int = 1) -> list[dict[str, Any]]:
        """Executes a Recursive Common Table Expression (CTE) to traverse management depth."""
        sql = """
            WITH RECURSIVE org_tree AS (
                -- Anchor member: root manager
                SELECT emp_id, name, manager_id, department, 0 AS level, name AS path
                FROM employees
                WHERE emp_id = ?
                
                UNION ALL
                
                -- Recursive member: direct reports
                SELECT e.emp_id, e.name, e.manager_id, e.department, t.level + 1, (t.path || ' -> ' || e.name)
                FROM employees e
                JOIN org_tree t ON e.manager_id = t.emp_id
            )
            SELECT emp_id, name, manager_id, department, level, path
            FROM org_tree
            ORDER BY level, emp_id;
        """
        cur = self.conn.cursor()
        cur.execute(sql, (root_emp_id,))
        return [dict(r) for r in cur.fetchall()]

    def compute_moving_averages_and_rankings(self) -> list[dict[str, Any]]:
        """Executes window functions with framing specs (SUM, AVG, LAG, DENSE_RANK)."""
        sql = """
            SELECT
                sale_date,
                region,
                amount,
                SUM(amount) OVER (
                    PARTITION BY region
                    ORDER BY sale_date
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) AS running_total,
                AVG(amount) OVER (
                    PARTITION BY region
                    ORDER BY sale_date
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ) AS moving_avg_3day,
                LAG(amount, 1) OVER (
                    PARTITION BY region
                    ORDER BY sale_date
                ) AS prev_day_amount,
                DENSE_RANK() OVER (
                    PARTITION BY sale_date
                    ORDER BY amount DESC
                ) AS daily_region_rank
            FROM daily_sales
            ORDER BY region, sale_date;
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        return [dict(r) for r in cur.fetchall()]

    def explain_query_plan(self, sql: str) -> list[str]:
        cur = self.conn.cursor()
        cur.execute(f"EXPLAIN QUERY PLAN {sql}")
        return [str(dict(r)) for r in cur.fetchall()]
