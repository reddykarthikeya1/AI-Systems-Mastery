"""Unit tests for the Polars and DuckDB Analytics Engine."""

from __future__ import annotations

import time

import polars as pl
import pytest
from analytics_engine import MarketAnalyticsEngine, sample_market_data


def test_sector_metrics_lazy_computation() -> None:
    engine = MarketAnalyticsEngine(sample_market_data())
    res = engine.compute_sector_metrics_lazy(min_volume=10_000)

    assert isinstance(res, pl.DataFrame)
    assert len(res) == 3
    assert "sector" in res.columns
    assert "total_turnover" in res.columns

    # Technology should have highest total turnover (AAPL + NVDA + MSFT)
    assert res["sector"][0] == "Technology"


def test_duckdb_window_ranking() -> None:
    engine = MarketAnalyticsEngine(sample_market_data())
    ranked = engine.rank_stocks_within_sector_duckdb()

    assert isinstance(ranked, pl.DataFrame)
    assert "sector_price_rank" in ranked.columns

    # Highest price stock in Tech is MSFT ($420), should be rank 1
    tech_rank1 = ranked.filter((pl.col("sector") == "Technology") & (pl.col("sector_price_rank") == 1))
    assert tech_rank1["ticker"][0] == "MSFT"


def test_sector_metrics_volume_filter_threshold() -> None:
    """Test that higher min_volume filter excludes low-volume stocks."""
    engine = MarketAnalyticsEngine(sample_market_data())
    # UNH volume is 12,000; BAC is 80,000; NVDA is 120,000
    res = engine.compute_sector_metrics_lazy(min_volume=100_000)
    assert len(res) == 1
    assert res["sector"][0] == "Technology"
    assert res["asset_count"][0] == 1  # Only NVDA qualifies


def test_sector_metrics_asset_count() -> None:
    """Test asset count aggregation per sector."""
    engine = MarketAnalyticsEngine(sample_market_data())
    res = engine.compute_sector_metrics_lazy(min_volume=1_000)
    tech_row = res.filter(pl.col("sector") == "Technology")
    assert tech_row["asset_count"][0] == 3  # AAPL, NVDA, MSFT


def test_sector_metrics_avg_price_accuracy() -> None:
    """Test computed average price is mathematically accurate."""
    engine = MarketAnalyticsEngine(sample_market_data())
    res = engine.compute_sector_metrics_lazy(min_volume=1_000)
    fin_row = res.filter(pl.col("sector") == "Financials")
    expected_avg = (195.0 + 38.0) / 2
    assert abs(fin_row["avg_price"][0] - expected_avg) < 0.01


def test_duckdb_window_ranking_ranks_strictly_monotonic() -> None:
    """Test DuckDB rank numbers are positive and ordered within sector."""
    engine = MarketAnalyticsEngine(sample_market_data())
    ranked = engine.rank_stocks_within_sector_duckdb()
    tech_ranks = ranked.filter(pl.col("sector") == "Technology")["sector_price_rank"].to_list()
    assert tech_ranks == sorted(tech_ranks)
    assert tech_ranks[0] == 1


def test_duckdb_sector_avg_price_window_function() -> None:
    """Test DuckDB AVG(price) OVER (PARTITION BY sector) computed column."""
    engine = MarketAnalyticsEngine(sample_market_data())
    ranked = engine.rank_stocks_within_sector_duckdb()
    assert "sector_avg_price" in ranked.columns
    health_rows = ranked.filter(pl.col("sector") == "Healthcare")
    expected_avg = (28.0 + 510.0) / 2
    for avg in health_rows["sector_avg_price"].to_list():
        assert abs(avg - expected_avg) < 0.01


def test_market_engine_with_single_record() -> None:
    """Test engine handles single-row dataset without error."""
    single = [{"ticker": "SOLO", "sector": "Energy", "price": 100.0, "volume": 50_000}]
    engine = MarketAnalyticsEngine(single)
    res = engine.compute_sector_metrics_lazy(min_volume=10_000)
    assert len(res) == 1
    assert res["total_turnover"][0] == 5_000_000.0


def test_market_engine_filter_all_records_out() -> None:
    """Test when min_volume is higher than all records, returns empty DataFrame."""
    engine = MarketAnalyticsEngine(sample_market_data())
    res = engine.compute_sector_metrics_lazy(min_volume=1_000_000)
    assert len(res) == 0


@pytest.mark.perf
def test_perf_polars_lazy_scan_vs_eager() -> None:
    """Benchmark: Polars Lazy execution graph optimization on 50,000 synthetic market rows."""
    raw = [
        {"ticker": f"TICK{i}", "sector": f"Sector{i % 10}", "price": float(10 + (i % 500)), "volume": (i * 100) % 200_000}
        for i in range(50_000)
    ]
    engine = MarketAnalyticsEngine(raw)

    start = time.perf_counter()
    res = engine.compute_sector_metrics_lazy(min_volume=50_000)
    lazy_time = time.perf_counter() - start

    assert len(res) == 10
    assert lazy_time < 2.0, f"Polars lazy plan took unexpectedly long: {lazy_time:.3f}s"
