"""Module 17: Columnar Storage, RLE & Predicate Pushdown Demo.

Demonstrates:
1. Column-oriented vs Row-oriented memory scanning.
2. Run-Length Encoding (RLE) and Dictionary encoding compression ratios.
3. Parquet-style Row Group Predicate Pushdown and Zone Map pruning.
"""

from __future__ import annotations


def demo_rle_and_dictionary_compression() -> None:
    print("=" * 75)
    print("    1. COLUMNAR COMPRESSION: RLE & DICTIONARY ENCODING")
    print("=" * 75)

    # 1,000 status codes: 800 'SUCCESS', 150 'PENDING', 50 'FAILED'
    raw_statuses = ["SUCCESS"] * 800 + ["PENDING"] * 150 + ["FAILED"] * 50
    raw_bytes = sum(len(s.encode("utf-8")) for s in raw_statuses)

    # 1. Dictionary Encoding
    unique_vals = list(dict.fromkeys(raw_statuses))
    val_to_id = {val: idx for idx, val in enumerate(unique_vals)}
    encoded_ids = [val_to_id[s] for s in raw_statuses]  # Can be stored as 1-byte uint8

    dict_bytes = sum(len(v.encode("utf-8")) for v in unique_vals) + len(encoded_ids)  # 1 byte per row

    print(f"Raw Column Size (Strings)   : {raw_bytes:,} bytes")
    print(f"Dictionary Encoded Size     : {dict_bytes:,} bytes ({(1 - dict_bytes / raw_bytes) * 100:.1f}% compression!)")

    # 2. Run-Length Encoding (RLE)
    rle_chunks: list[tuple[str, int]] = []
    current_val = raw_statuses[0]
    count = 1

    for val in raw_statuses[1:]:
        if val == current_val:
            count += 1
        else:
            rle_chunks.append((current_val, count))
            current_val = val
            count = 1
    rle_chunks.append((current_val, count))

    rle_bytes = len(rle_chunks) * (8 + 4)  # 8 bytes pointer + 4 byte int count
    print(f"RLE Encoded Size ({len(rle_chunks)} tuples) : {rle_bytes} bytes ({(1 - rle_bytes / raw_bytes) * 100:.1f}% compression!)")


def demo_predicate_pushdown_zone_maps() -> None:
    print("\n" + "=" * 75)
    print("    2. PARQUET ROW GROUP PRUNING (PREDICATE PUSHDOWN)")
    print("=" * 75)

    # Simulated Parquet file with 3 Row Groups (each representing 100,000 transactions)
    row_groups = [
        {"id": "RG_01", "count": 100_000, "min_amount": 10.0, "max_amount": 450.0},
        {"id": "RG_02", "count": 100_000, "min_amount": 451.0, "max_amount": 950.0},
        {"id": "RG_03", "count": 100_000, "min_amount": 951.0, "max_amount": 5000.0},
    ]

    target_query = "SELECT * FROM sales WHERE amount > 1000.0"
    target_threshold = 1000.0
    print(f"Executing Analytical Query: '{target_query}'")
    print("Evaluating Zone Map (Min/Max statistics) in Parquet footer:\n")

    scanned_rows = 0
    skipped_rows = 0

    for rg in row_groups:
        rg_id = rg["id"]
        min_v = rg["min_amount"]
        max_v = rg["max_amount"]
        count = rg["count"]

        # If max_amount <= threshold, no row in this group can match!
        if max_v <= target_threshold:
            print(f"  [{rg_id}] Min: ${min_v:>7.1f} | Max: ${max_v:>7.1f} -> [PRUNED / SKIPPED] (Max <= 1000.0)")
            skipped_rows += count
        else:
            print(f"  [{rg_id}] Min: ${min_v:>7.1f} | Max: ${max_v:>7.1f} -> [SCANNED / READ]")
            scanned_rows += count

    print(f"\nResult: Read {scanned_rows:,} rows | Skipped {skipped_rows:,} rows ({(skipped_rows / (scanned_rows + skipped_rows)) * 100:.1f}% disk I/O eliminated!)")


def main() -> None:
    demo_rle_and_dictionary_compression()
    demo_predicate_pushdown_zone_maps()


if __name__ == "__main__":
    main()
