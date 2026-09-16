"""Module 17: Columnar Storage, Compression & Analytics Engine (Solution).

This is a pure-Python MODEL of columnar vector chunk storage, SIMD-style compression, and zone-map pruning, built to make the
mechanism visible. It does not connect to DuckDB or ClickHouse. For the real driver,
real queries and real operational behaviour, see `duckdb_live.py` and `clickhouse_live.py`.

Implements:
1. Encoders: RLE, Dictionary Encoding, and Frame-of-Reference (FoR).
2. ColumnChunk with zone map min/max statistics and aggregations.
3. RowGroup with Parquet-style Zone Map Pruning (predicate pushdown).
4. ColumnarTable for vectorized analytical queries.
"""

from __future__ import annotations

from typing import Any, Literal

AggFunc = Literal["SUM", "AVG", "MIN", "MAX"]


class RLEEncoder:
    """Run-Length Encoding for low-cardinality or sorted columnar data."""

    @staticmethod
    def encode(values: list[Any]) -> list[tuple[Any, int]]:
        if not values:
            return []

        runs: list[tuple[Any, int]] = []
        curr_val = values[0]
        count = 1

        for val in values[1:]:
            if val == curr_val:
                count += 1
            else:
                runs.append((curr_val, count))
                curr_val = val
                count = 1
        runs.append((curr_val, count))
        return runs

    @staticmethod
    def decode(runs: list[tuple[Any, int]]) -> list[Any]:
        decoded: list[Any] = []
        for val, count in runs:
            decoded.extend([val] * count)
        return decoded


class DictionaryEncoder:
    """Dictionary Encoding replacing repetitive strings with compact integer IDs."""

    @staticmethod
    def encode(values: list[str]) -> tuple[list[str], list[int]]:
        unique_vals = list(dict.fromkeys(values))
        val_to_id = {v: idx for idx, v in enumerate(unique_vals)}
        encoded_ids = [val_to_id[v] for v in values]
        return unique_vals, encoded_ids

    @staticmethod
    def decode(dictionary: list[str], ids: list[int]) -> list[str]:
        return [dictionary[i] for i in ids]


class FrameOfReferenceEncoder:
    """Frame of Reference (FoR) integer compression using baseline subtraction."""

    @staticmethod
    def encode(values: list[int]) -> tuple[int, list[int], int]:
        if not values:
            return 0, [], 0

        baseline = min(values)
        deltas = [v - baseline for v in values]
        max_delta = max(deltas) if deltas else 0
        bit_width = max_delta.bit_length() if max_delta > 0 else 1
        return baseline, deltas, bit_width

    @staticmethod
    def decode(baseline: int, deltas: list[int]) -> list[int]:
        return [baseline + d for d in deltas]


class ColumnChunk:
    """A contiguous array for a single column with zone map metadata."""

    def __init__(self, col_name: str, data: list[Any]) -> None:
        self.col_name = col_name
        self.data = list(data)
        non_nulls = [x for x in self.data if x is not None]
        self.min_val: Any = min(non_nulls) if non_nulls else None
        self.max_val: Any = max(non_nulls) if non_nulls else None
        self.null_count: int = len(self.data) - len(non_nulls)

    def sum(self) -> float:
        return float(sum(x for x in self.data if x is not None))

    def avg(self) -> float:
        valid = [x for x in self.data if x is not None]
        return float(sum(valid) / len(valid)) if valid else 0.0

    def min(self) -> Any:
        return self.min_val

    def max(self) -> Any:
        return self.max_val


class RowGroup:
    """A collection of column chunks representing a horizontal slice of rows."""

    def __init__(self, columns: dict[str, ColumnChunk], row_count: int) -> None:
        self.columns = columns
        self.row_count = row_count

    def can_skip(self, col_name: str, op: str, threshold: Any) -> bool:
        """Evaluate Zone Map pruning: return True if this Row Group can be skipped without scanning."""
        if col_name not in self.columns:
            return False

        chunk = self.columns[col_name]
        if chunk.min_val is None or chunk.max_val is None:
            return False

        if op == ">" and chunk.max_val <= threshold:
            return True
        elif op == ">=" and chunk.max_val < threshold:
            return True
        elif op == "<" and chunk.min_val >= threshold:
            return True
        elif op == "<=" and chunk.min_val > threshold:
            return True
        elif op == "==" and (threshold < chunk.min_val or threshold > chunk.max_val):
            return True

        return False


class ColumnarTable:
    """An analytical columnar table organizing data into Row Groups with vectorized queries."""

    def __init__(self, schema: dict[str, str], row_group_size: int = 1000) -> None:
        self.schema = schema
        self.row_group_size = row_group_size
        self.row_groups: list[RowGroup] = []

    def append_rows(self, rows: list[dict[str, Any]]) -> None:
        if not rows:
            return

        for start_idx in range(0, len(rows), self.row_group_size):
            batch = rows[start_idx : start_idx + self.row_group_size]
            columns: dict[str, ColumnChunk] = {}

            for col in self.schema:
                col_data = [r.get(col) for r in batch]
                columns[col] = ColumnChunk(col_name=col, data=col_data)

            self.row_groups.append(RowGroup(columns=columns, row_count=len(batch)))

    def aggregate(
        self,
        target_col: str,
        agg_func: AggFunc,
        filter_predicate: tuple[str, str, Any] | None = None,
    ) -> float:
        matching_values: list[float] = []

        for rg in self.row_groups:
            if filter_predicate is not None:
                p_col, op, p_val = filter_predicate
                # Predicate Pushdown / Zone Map check
                if rg.can_skip(p_col, op, p_val):
                    continue

                p_chunk = rg.columns[p_col]
                t_chunk = rg.columns[target_col]

                for i in range(rg.row_count):
                    val = p_chunk.data[i]
                    if val is None:
                        continue

                    passes = False
                    if op == ">" and val > p_val:
                        passes = True
                    elif op == ">=" and val >= p_val:
                        passes = True
                    elif op == "<" and val < p_val:
                        passes = True
                    elif op == "<=" and val <= p_val:
                        passes = True
                    elif op == "==" and val == p_val:
                        passes = True

                    if passes and t_chunk.data[i] is not None:
                        matching_values.append(float(t_chunk.data[i]))
            else:
                t_chunk = rg.columns[target_col]
                for v in t_chunk.data:
                    if v is not None:
                        matching_values.append(float(v))

        if not matching_values:
            return 0.0

        if agg_func == "SUM":
            return float(sum(matching_values))
        elif agg_func == "AVG":
            return float(sum(matching_values) / len(matching_values))
        elif agg_func == "MIN":
            return float(min(matching_values))
        elif agg_func == "MAX":
            return float(max(matching_values))

        raise ValueError(f"Unknown aggregation function: {agg_func}")
