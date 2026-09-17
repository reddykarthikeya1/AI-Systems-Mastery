"""Reference Solution — Problem 01: Run Length Encoding Decompress

Topic: 17 Columnar OLAP DuckDB ClickHouse
"""

from __future__ import annotations


def run_length_encoding_decompress(runs: list[tuple[int, int]]) -> list[int]:
    res = []
    for count, val in runs:
        res.extend([val] * count)
    return res
