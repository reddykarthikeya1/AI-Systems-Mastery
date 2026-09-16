"""Module 10: MongoDB BSON Wire Encoding & Schema Design Patterns Demo.

Demonstrates:
1. BSON binary wire layout (type tags, length prefixes, ObjectId structure).
2. The Bucket Pattern for IoT time-series data reduction.
3. Chronological sorting of 12-byte ObjectIds.
"""

from __future__ import annotations

import os
import struct
import time


def generate_object_id() -> bytes:
    """Generates a 12-byte BSON ObjectId (4B timestamp + 5B random + 3B counter)."""
    ts = int(time.time())
    random_bytes = os.urandom(5)
    counter = 42
    return struct.pack(">I 5s 3s", ts, random_bytes, counter.to_bytes(3, "big"))


def demo_bson_binary_packing() -> None:
    print("=" * 75)
    print("    1. BSON WIRE PROTOCOL BINARY PACKING & DECOMPOSITION")
    print("=" * 75)

    oid = generate_object_id()
    extracted_ts = struct.unpack(">I", oid[:4])[0]
    print(f"Generated 12-byte ObjectId : {oid.hex().upper()}")
    print(f"Extracted Epoch Timestamp   : {extracted_ts} ({time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(extracted_ts))})")

    # Simple BSON Element packing: Type 0x02 (String), Key 'username', Val 'Karthikeya'
    key_bytes = b"username\x00"
    val = "Karthikeya"
    val_bytes = struct.pack("<I", len(val) + 1) + val.encode("utf-8") + b"\x00"
    element = b"\x02" + key_bytes + val_bytes

    total_len = 4 + len(element) + 1  # 4B doc len + elements + null terminator
    doc_bytes = struct.pack("<I", total_len) + element + b"\x00"

    print(f"\nConstructed BSON Document ({len(doc_bytes)} bytes):")
    print(f"  Hex Dump: {doc_bytes.hex()}")
    print("  -> First 4 Bytes (Total Length):", struct.unpack("<I", doc_bytes[:4])[0])
    print("  -> Element Type Tag: 0x02 (String)")
    print("  -> Null Terminator at End: 0x00")


def demo_bucket_pattern() -> None:
    print("\n" + "=" * 75)
    print("    2. THE BUCKET PATTERN: IOT TIME-SERIES STORAGE COMPARISON")
    print("=" * 75)

    # Simulating 3,600 temperature readings (1 per second for 1 hour)
    readings = [(i, 20.0 + (i % 50) * 0.1) for i in range(3600)]

    # Model A: Unbucketed (1 document per reading) -> 3,600 documents in collection
    unbucketed_docs = [
        {"sensor_id": "SENSOR_01", "timestamp": r[0], "temperature": r[1]}
        for r in readings
    ]

    # Model B: Bucket Pattern (1 document per hour with 3,600 array entries)
    bucketed_doc = {
        "sensor_id": "SENSOR_01",
        "hour_bucket": 14,
        "count": len(readings),
        "readings": [{"sec": r[0], "temp": r[1]} for r in readings],
    }

    print(f"Unbucketed Model Document Count : {len(unbucketed_docs):,} documents (High Index Overhead!)")
    print(f"Bucket Pattern Document Count   : 1 document ({len(bucketed_doc['readings'])} pre-aggregated readings!)")
    print(f"Index Reduction Factor          : {len(unbucketed_docs)}x fewer index entries in RAM!")


def main() -> None:
    demo_bson_binary_packing()
    demo_bucket_pattern()


if __name__ == "__main__":
    main()
