"""Module 17 Test Suite: Columnar Storage, Compression & Analytics Engine."""

from __future__ import annotations

from columnar_engine import (
    ColumnChunk,
    ColumnarTable,
    DictionaryEncoder,
    FrameOfReferenceEncoder,
    RLEEncoder,
    RowGroup,
)


def test_rle_encoding_and_decoding() -> None:
    original = ["NY", "NY", "NY", "CA", "CA", "TX", "TX", "TX", "TX"]
    runs = RLEEncoder.encode(original)
    assert runs == [("NY", 3), ("CA", 2), ("TX", 4)]

    decoded = RLEEncoder.decode(runs)
    assert decoded == original


def test_dictionary_encoding_and_decoding() -> None:
    raw_statuses = ["PENDING", "PENDING", "APPROVED", "FAILED", "APPROVED", "PENDING"]
    dictionary, ids = DictionaryEncoder.encode(raw_statuses)

    assert dictionary == ["PENDING", "APPROVED", "FAILED"]
    assert ids == [0, 0, 1, 2, 1, 0]

    decoded = DictionaryEncoder.decode(dictionary, ids)
    assert decoded == raw_statuses


def test_frame_of_reference_encoding() -> None:
    years = [1985, 1986, 1988, 1990, 1995]
    baseline, deltas, bit_width = FrameOfReferenceEncoder.encode(years)

    assert baseline == 1985
    assert deltas == [0, 1, 3, 5, 10]
    # Max delta 10 requires 4 bits (1010 in binary)
    assert bit_width == 4

    decoded = FrameOfReferenceEncoder.decode(baseline, deltas)
    assert decoded == years


def test_zone_map_pruning_and_predicate_pushdown() -> None:
    chunk_low = ColumnChunk("amount", [10.0, 50.0, 120.0, 250.0])
    rg_low = RowGroup({"amount": chunk_low}, row_count=4)

    chunk_high = ColumnChunk("amount", [600.0, 750.0, 890.0, 1200.0])
    rg_high = RowGroup({"amount": chunk_high}, row_count=4)

    # Filter: amount > 500.0
    # rg_low has max 250.0 <= 500.0 -> Must be pruned (skipped)!
    assert rg_low.can_skip("amount", ">", 500.0) is True
    # rg_high has max 1200.0 > 500.0 -> Must NOT be skipped
    assert rg_high.can_skip("amount", ">", 500.0) is False

    # Filter: amount < 100.0
    assert rg_low.can_skip("amount", "<", 100.0) is False
    assert rg_high.can_skip("amount", "<", 100.0) is True


def test_columnar_table_vectorized_aggregations() -> None:
    schema = {"id": "int", "amount": "float", "dept": "str"}
    # Small row group size = 5 to force multi-rowgroup partitioning
    table = ColumnarTable(schema=schema, row_group_size=5)

    rows = [
        {"id": i, "amount": float(i * 10), "dept": "ENG" if i % 2 == 0 else "SALES"}
        for i in range(1, 11)  # 1 to 10: amounts 10, 20, 30 ... 100
    ]
    table.append_rows(rows)

    assert len(table.row_groups) == 2

    # Unfiltered Aggregations
    # Amounts: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 (Sum = 550, Avg = 55)
    assert table.aggregate("amount", "SUM") == 550.0
    assert table.aggregate("amount", "AVG") == 55.0
    assert table.aggregate("amount", "MIN") == 10.0
    assert table.aggregate("amount", "MAX") == 100.0

    # Filtered Aggregation with Predicate Pushdown: amount > 60
    # Matching amounts: 70, 80, 90, 100 -> Sum = 340, Avg = 85
    filtered_sum = table.aggregate("amount", "SUM", filter_predicate=("amount", ">", 60.0))
    assert filtered_sum == 340.0

    filtered_avg = table.aggregate("amount", "AVG", filter_predicate=("amount", ">", 60.0))
    assert filtered_avg == 85.0
