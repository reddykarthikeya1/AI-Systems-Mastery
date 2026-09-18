"""Problem 01 — Run Length Encoding Decompress

Topic: 17 Columnar OLAP DuckDB ClickHouse
Target: Production-grade implementation

Decompress run-length encoded columnar vector into full values list.

Example:
    >>> run_length_encoding_decompress([(3, 100), (2, 200), (1, 300)])
    [100, 100, 100, 200, 200, 300]

Hints:
    Hint 1: Each run tuple is a compact stand-in for a repeated stretch of
        the original column, so decompression is just re-expanding each run
        back to its full length, in order.
    Hint 2: A single pass that extends an output list with [value] * count
        for each (count, value) run needs no extra bookkeeping.
    Hint 3: Preserve run order in the output (runs are not sorted or merged
        by value — three separate runs of the same value stay three
        separate stretches) and return [] for an empty runs list without
        special-casing it.
"""

from __future__ import annotations


def run_length_encoding_decompress(runs: list[tuple[int, int]]) -> list[int]:
    """Each tuple is (count, value).
    Returns flat list of decompressed values.
    """
    raise NotImplementedError("Implement run_length_encoding_decompress")
