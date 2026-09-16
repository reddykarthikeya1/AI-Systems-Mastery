"""Module 17: Columnar Storage, Compression & Analytics Engine (Starter).

This template defines columnar OLAP storage and vectorized operations:
1. Column encoders: Run-Length Encoding (RLE), Dictionary Encoding, Frame-of-Reference (FoR).
2. ColumnChunk with column statistics (Min, Max, Null count) and aggregations.
3. RowGroup with Zone Map Pruning (predicate pushdown).
4. ColumnarTable for vectorized analytical queries (SUM, AVG, MIN, MAX).
"""

from __future__ import annotations

from typing import Any, Literal

AggFunc = Literal["SUM", "AVG", "MIN", "MAX"]


class RLEEncoder:
    """Run-Length Encoding for low-cardinality or sorted columnar data."""

    @staticmethod
    def encode(values: list[Any]) -> list[tuple[Any, int]]:
        """Compress list of values into (value, count) runs."""
        raise NotImplementedError("Implement RLE encode")

    @staticmethod
    def decode(runs: list[tuple[Any, int]]) -> list[Any]:
        """Decompress (value, count) runs into full value list."""
        raise NotImplementedError("Implement RLE decode")


class DictionaryEncoder:
    """Dictionary Encoding replacing repetitive strings with compact integer IDs."""

    @staticmethod
    def encode(values: list[str]) -> tuple[list[str], list[int]]:
        """Encode list of strings into unique dictionary and integer IDs."""
        raise NotImplementedError("Implement Dictionary encode")

    @staticmethod
    def decode(dictionary: list[str], ids: list[int]) -> list[str]:
        """Decode integer IDs back into original strings using dictionary."""
        raise NotImplementedError("Implement Dictionary decode")


class FrameOfReferenceEncoder:
    """Frame of Reference (FoR) integer compression using baseline subtraction."""

    @staticmethod
    def encode(values: list[int]) -> tuple[int, list[int], int]:
        """Subtract min baseline and calculate required bit-width for deltas."""
        raise NotImplementedError("Implement Frame of Reference encode")

    @staticmethod
    def decode(baseline: int, deltas: list[int]) -> list[int]:
        """Reconstruct original integers by adding baseline to deltas."""
        raise NotImplementedError("Implement Frame of Reference decode")


class ColumnChunk:
    """A contiguous array for a single column with zone map metadata."""

    def __init__(self, col_name: str, data: list[Any]) -> None:
        raise NotImplementedError("Initialize column chunk and compute min/max statistics")

    def sum(self) -> float:
        raise NotImplementedError("Vectorized sum")

    def avg(self) -> float:
        raise NotImplementedError("Vectorized average")

    def min(self) -> Any:
        raise NotImplementedError("Vectorized min")

    def max(self) -> Any:
        raise NotImplementedError("Vectorized max")


class RowGroup:
    """A collection of column chunks representing a horizontal slice of rows (e.g. Parquet row group)."""

    def __init__(self, columns: dict[str, ColumnChunk], row_count: int) -> None:
        raise NotImplementedError("Initialize row group")

    def can_skip(self, col_name: str, op: str, threshold: Any) -> bool:
        """Evaluate Zone Map pruning: return True if this Row Group can be skipped without scanning."""
        raise NotImplementedError("Implement zone map predicate pruning")


class ColumnarTable:
    """An analytical columnar table organizing data into Row Groups with vectorized queries."""

    def __init__(self, schema: dict[str, str], row_group_size: int = 1000) -> None:
        raise NotImplementedError("Initialize columnar table schema and row group size")

    def append_rows(self, rows: list[dict[str, Any]]) -> None:
        """Pivot row-oriented records into contiguous columnar Row Groups."""
        raise NotImplementedError("Pivot rows into columnar row groups")

    def aggregate(
        self,
        target_col: str,
        agg_func: AggFunc,
        filter_predicate: tuple[str, str, Any] | None = None,
    ) -> float:
        """Execute vectorized aggregation with Row Group predicate pushdown pruning."""
        raise NotImplementedError("Implement vectorized query with zone map pruning")
