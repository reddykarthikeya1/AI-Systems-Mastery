#!/usr/bin/env python3
"""Module 22: DuckDB In-Process OLAP Demonstration.

This script demonstrates executing analytical window functions and queries
with DuckDB on structured datasets.
"""

from __future__ import annotations

import duckdb
import polars as pl

pl.Config.set_ascii_tables(True)


def run_olap_window_analysis() -> pl.DataFrame:
    df = pl.DataFrame({  # noqa: F841 - DuckDB queries 'df' via dynamic Python frame inspection
        "employee": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"],
        "department": ["Sales", "Sales", "Engineering", "Engineering", "Engineering", "Sales"],
        "salary": [95_000, 80_000, 140_000, 125_000, 160_000, 105_000],
    })

    query = """
        SELECT
            employee,
            department,
            salary,
            AVG(salary) OVER(PARTITION BY department) as dept_avg_salary,
            RANK() OVER(PARTITION BY department ORDER BY salary DESC) as dept_salary_rank
        FROM df
        ORDER BY department, dept_salary_rank
    """
    return duckdb.sql(query).pl()


def main() -> None:
    print("=" * 60)
    print("  DuckDB In-Process Analytical SQL Demonstration")
    print("=" * 60)

    result = run_olap_window_analysis()
    print(result)


if __name__ == "__main__":
    main()
