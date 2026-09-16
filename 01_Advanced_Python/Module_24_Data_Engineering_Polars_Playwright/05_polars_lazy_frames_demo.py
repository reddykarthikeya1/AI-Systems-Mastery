#!/usr/bin/env python3
"""Module 22: Polars LazyFrame Execution Plan Demonstration.

This script demonstrates defining query plans with Polars LazyFrames and
executing them via parallel multi-threading.
"""

from __future__ import annotations

import polars as pl

pl.Config.set_ascii_tables(True)


def build_market_lazy_pipeline() -> pl.LazyFrame:
    df = pl.DataFrame({
        "ticker": ["AAPL", "GOOGL", "MSFT", "AMZN", "NVDA", "TSLA", "META"],
        "price": [220.50, 175.20, 415.00, 185.30, 125.00, 210.00, 495.00],
        "volume": [45_000, 28_000, 19_000, 32_000, 85_000, 60_000, 14_000],
        "sector": ["Tech", "Tech", "Tech", "Consumer", "Tech", "Auto", "Tech"],
    }).lazy()

    query = (
        df.filter(pl.col("sector") == "Tech")
        .with_columns((pl.col("price") * pl.col("volume")).alias("market_turnover"))
        .filter(pl.col("market_turnover") > 5_000_000)
        .sort("market_turnover", descending=True)
    )
    return query


def main() -> None:
    print("=" * 60)
    print("  Polars LazyFrame Query Optimization & Execution")
    print("=" * 60)

    query_plan = build_market_lazy_pipeline()
    print("Optimized Logical Plan:")
    print(query_plan.explain())

    print("\nExecuting query across multi-threaded Rayon engine:")
    result_df = query_plan.collect()
    print(result_df)


if __name__ == "__main__":
    main()
