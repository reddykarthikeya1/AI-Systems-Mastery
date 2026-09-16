#!/usr/bin/env python3
"""Competitive Market Intelligence & Polars Analytics Engine.

Module 22 (Modern Data Engineering) Turnkey Project Implementation.
Demonstrates Polars LazyFrames, Apache Arrow columnar processing, and DuckDB OLAP window queries.
"""

from __future__ import annotations

import duckdb
import polars as pl

pl.Config.set_ascii_tables(True)


class MarketAnalyticsEngine:
    """High-throughput analytical engine combining Polars and DuckDB."""

    def __init__(self, raw_records: list[dict]) -> None:
        self.raw_df = pl.DataFrame(raw_records)

    def compute_sector_metrics_lazy(self, min_volume: int = 10_000) -> pl.DataFrame:
        """Executes optimized lazy query graph in Polars."""
        lazy_plan = (
            self.raw_df.lazy()
            .filter(pl.col("volume") >= min_volume)
            .with_columns((pl.col("price") * pl.col("volume")).alias("turnover"))
            .group_by("sector")
            .agg([
                pl.col("turnover").sum().alias("total_turnover"),
                pl.col("price").mean().alias("avg_price"),
                pl.col("ticker").count().alias("asset_count"),
            ])
            .sort("total_turnover", descending=True)
        )
        return lazy_plan.collect()

    def rank_stocks_within_sector_duckdb(self) -> pl.DataFrame:
        """Uses DuckDB in-process SQL to run analytical ranking window functions."""
        df = self.raw_df  # noqa: F841 - DuckDB queries 'df' via dynamic Python frame inspection
        sql = """
            SELECT
                ticker,
                sector,
                price,
                volume,
                RANK() OVER(PARTITION BY sector ORDER BY price DESC) as sector_price_rank,
                AVG(price) OVER(PARTITION BY sector) as sector_avg_price
            FROM df
            ORDER BY sector, sector_price_rank
        """
        return duckdb.sql(sql).pl()


def sample_market_data() -> list[dict]:
    return [
        {"ticker": "AAPL", "sector": "Technology", "price": 225.0, "volume": 50_000},
        {"ticker": "NVDA", "sector": "Technology", "price": 120.0, "volume": 120_000},
        {"ticker": "MSFT", "sector": "Technology", "price": 420.0, "volume": 30_000},
        {"ticker": "JPM", "sector": "Financials", "price": 195.0, "volume": 25_000},
        {"ticker": "BAC", "sector": "Financials", "price": 38.0, "volume": 80_000},
        {"ticker": "PFE", "sector": "Healthcare", "price": 28.0, "volume": 95_000},
        {"ticker": "UNH", "sector": "Healthcare", "price": 510.0, "volume": 12_000},
    ]


def main() -> None:
    print("=" * 65)
    print("      POLARS & DUCKDB MARKET ANALYTICS ENGINE DEMO")
    print("=" * 65)

    engine = MarketAnalyticsEngine(sample_market_data())

    print("\n--- Sector Metrics (Polars Lazy Execution) ---")
    sector_summary = engine.compute_sector_metrics_lazy()
    print(sector_summary)

    print("\n--- Stock Rankings within Sector (DuckDB Window SQL) ---")
    rankings = engine.rank_stocks_within_sector_duckdb()
    print(rankings)


if __name__ == "__main__":
    main()
