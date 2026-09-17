"""Problem 01 — Run Length Encoding Decompress

Topic: 17 Columnar OLAP DuckDB ClickHouse
Target: Production-grade implementation

Decompress run-length encoded columnar vector into full values list.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def run_length_encoding_decompress(runs: list[tuple[int, int]]) -> list[int]:
    """Each tuple is (count, value).
    Returns flat list of decompressed values.
    """
    raise NotImplementedError("Implement run_length_encoding_decompress")
