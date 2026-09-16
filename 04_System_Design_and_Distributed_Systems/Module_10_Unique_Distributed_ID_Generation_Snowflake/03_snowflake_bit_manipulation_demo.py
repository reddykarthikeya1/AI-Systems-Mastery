#!/usr/bin/env python3
"""Module 10 Demo: Snowflake 64-Bit Bitwise Layout & ID Generation."""

import sys
from datetime import UTC, datetime
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from snowflake_generator import SnowflakeGenerator


def main() -> None:
    print("=" * 72)
    print("  MODULE 10: TWITTER SNOWFLAKE 64-BIT ID GENERATION DEMO")
    print("=" * 72)

    # 1. Initialize generator: Datacenter 5, Worker 12
    gen = SnowflakeGenerator(datacenter_id=5, worker_id=12)

    print("\n--- 1. Generating Snowflake IDs ---")
    ids = [gen.next_id() for _ in range(5)]

    for idx, sid in enumerate(ids, 1):
        parsed = gen.parse_id(sid)
        dt = datetime.fromtimestamp(parsed.timestamp_ms / 1000.0, tz=UTC)
        binary_str = f"{sid:064b}"
        # Format binary string with spaces for readability: 1 bit sign, 41 timestamp, 5 dc, 5 worker, 12 seq
        b_sign = binary_str[0]
        b_time = binary_str[1:42]
        b_dc = binary_str[42:47]
        b_wrk = binary_str[47:52]
        b_seq = binary_str[52:]
        print(f"ID #{idx}: {sid}")
        print(f"  Binary: [{b_sign}] [{b_time}] [{b_dc}] [{b_wrk}] [{b_seq}]")
        print(f"  Parsed: Time={dt.isoformat()} | Datacenter={parsed.datacenter_id} | Worker={parsed.worker_id} | Seq={parsed.sequence}")

    # 2. Monotonicity & Throughput
    print("\n--- 2. High-Throughput Burst Monotonicity ---")
    burst_size = 10_000
    print(f"Generating {burst_size:,} IDs in tight loop...")
    t0 = datetime.now()
    burst_ids = [gen.next_id() for _ in range(burst_size)]
    elapsed = (datetime.now() - t0).total_seconds()

    is_monotonic = all(burst_ids[i] < burst_ids[i + 1] for i in range(len(burst_ids) - 1))
    unique_count = len(set(burst_ids))

    print(f"Generated {burst_size:,} IDs in {elapsed:.3f}s ({burst_size / elapsed:,.0f} IDs/sec)")
    print(f"Strict Monotonicity: {'PASS (100% strictly increasing)' if is_monotonic else 'FAIL'}")
    print(f"Collision Free:      {'PASS (0 duplicates detected)' if unique_count == burst_size else 'FAIL'}")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
