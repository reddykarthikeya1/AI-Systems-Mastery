#!/usr/bin/env python3
"""Broken Data Pipeline demonstrating hardcoded sleep and schema inference traps."""

import polars as pl
import time

def process_scraped_market_data():
    raw = [
        {"ticker": "AAPL", "price": "220.5"},
        {"ticker": "MSFT", "price": "N/A"},  # Uncleaned sentinel
        {"ticker": "GOOG", "price": "180.2"},
    ]
    df = pl.DataFrame(raw)
    print(f"Polars inferred price schema: {df.schema['price']}")
    try:
        mean_price = df.select(pl.col("price").mean())
    except Exception as err:
        print(f"Mean computation failed on inferred string column: {err}")

if __name__ == "__main__":
    process_scraped_market_data()
