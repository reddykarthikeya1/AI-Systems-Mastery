"""AeroTrade Core - Columnar Market Analytics

Demonstrates concepts from Chapter 17:
- Columnar batch processing and SIMD vectorization with Polars.
- Volume-Weighted Average Price (VWAP) calculation.
- Dual-mode execution: uses Polars if installed, with a zero-dependency pure-Python fallback.
"""
from __future__ import annotations
from typing import List, Dict, Any
from domain import Trade

try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False


class MarketAnalytics:
    """Computes real-time market metrics from executed trades."""

    @staticmethod
    def calculate_vwap(trades: List[Trade]) -> float:
        """Volume-Weighted Average Price: sum(Price * Quantity) / sum(Quantity)."""
        if not trades:
            return 0.0

        if HAS_POLARS:
            df = pl.DataFrame({
                "price": [t.price for t in trades],
                "quantity": [t.quantity for t in trades],
            })
            vwap = (df["price"] * df["quantity"]).sum() / df["quantity"].sum()
            return round(float(vwap), 4)
        else:
            total_notional = sum(t.price * t.quantity for t in trades)
            total_volume = sum(t.quantity for t in trades)
            return round(total_notional / total_volume, 4)

    @staticmethod
    def trade_summary(trades: List[Trade]) -> Dict[str, Any]:
        """Summary statistics of executed trades."""
        if not trades:
            return {"total_trades": 0, "total_volume": 0, "vwap": 0.0, "min_price": 0.0, "max_price": 0.0}

        prices = [t.price for t in trades]
        volumes = [t.quantity for t in trades]

        return {
            "total_trades": len(trades),
            "total_volume": sum(volumes),
            "vwap": MarketAnalytics.calculate_vwap(trades),
            "min_price": min(prices),
            "max_price": max(prices),
            "engine_backend": "polars_columnar" if HAS_POLARS else "pure_python_vector",
        }
