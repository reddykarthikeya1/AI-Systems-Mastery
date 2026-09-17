"""High-Performance Polars and DuckDB Analytics Engine for Capstone Platform."""

from __future__ import annotations

import duckdb
import polars as pl

pl.Config.set_ascii_tables(True)


class CapstoneAnalytics:
    @staticmethod
    def aggregate_project_budgets(projects_data: list[dict]) -> pl.DataFrame:
        if not projects_data:
            return pl.DataFrame({"owner": [], "total_budget": [], "project_count": []})

        df = pl.DataFrame(projects_data)
        lazy_plan = (
            df.lazy()
            .group_by("owner")
            .agg([
                pl.col("budget").sum().alias("total_budget"),
                pl.col("name").count().alias("project_count"),
            ])
            .sort("total_budget", descending=True)
        )
        return lazy_plan.collect()

    @staticmethod
    def rank_projects_duckdb(projects_data: list[dict]) -> pl.DataFrame:
        if not projects_data:
            return pl.DataFrame({"name": [], "budget": [], "rank": []})

        df = pl.DataFrame(projects_data)  # noqa: F841 - DuckDB queries 'df' via dynamic Python frame inspection
        sql = """
            SELECT name, budget, owner,
                   RANK() OVER(ORDER BY budget DESC) as budget_rank
            FROM df
        """
        return duckdb.sql(sql).pl()
