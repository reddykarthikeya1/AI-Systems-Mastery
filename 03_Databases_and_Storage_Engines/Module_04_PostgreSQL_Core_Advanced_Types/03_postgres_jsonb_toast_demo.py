"""Module 04: PostgreSQL JSONB vs JSON & TOAST Simulation Demonstration.

Demonstrates:
1. Binary JSONB decomposition vs raw JSON text parsing overhead.
2. Generalized Inverted Index (GIN) path extraction for sub-document search.
3. The Oversized-Attribute Storage Technique (TOAST) for payloads > 2KB.
"""

from __future__ import annotations

import json
import time
import zlib


def demo_json_vs_jsonb_parsing() -> None:
    print("=" * 75)
    print("    1. POSTGRESQL JSON (TEXT) vs JSONB (DECOMPOSED BINARY) BENCHMARK")
    print("=" * 75)

    raw_data = {
        "user_id": 98765,
        "name": "Karthikeya",
        "settings": {
            "theme": "dark",
            "notifications": {"email": True, "sms": False, "push": True},
            "beta_tester": True,
        },
        "roles": ["developer", "architect", "dba"],
        "metadata": {"login_count": 420, "last_ip": "192.168.1.100"},
    }

    # Simulate 20,000 queries accessing deep property: settings.notifications.push
    json_text = json.dumps(raw_data)
    jsonb_binary = json.loads(json_text)  # pre-parsed in-memory representation

    # JSON Text Access (Must parse string on every single query)
    start = time.perf_counter()
    for _ in range(20_000):
        doc = json.loads(json_text)
        val = doc["settings"]["notifications"]["push"]
        assert val is True
    json_time = time.perf_counter() - start

    # JSONB Binary Access (Direct in-memory dictionary traversal without text parsing)
    start = time.perf_counter()
    for _ in range(20_000):
        val = jsonb_binary["settings"]["notifications"]["push"]
        assert val is True
    jsonb_time = time.perf_counter() - start

    print(f"JSON Text Re-parsing Time (20k lookups) : {json_time * 1000:.2f} ms")
    print(f"JSONB Binary Offset Time (20k lookups)  : {jsonb_time * 1000:.2f} ms")
    print(f"JSONB is {json_time / jsonb_time:.1f}x faster on property extraction!")


def demo_toast_compression_and_chunking() -> None:
    print("\n" + "=" * 75)
    print("    2. TOAST (THE OVERSIZED-ATTRIBUTE STORAGE TECHNIQUE) SIMULATION")
    print("=" * 75)

    page_threshold = 2048  # 2KB threshold (1/4 of 8KB PostgreSQL page)
    large_payload = (
        "PostgreSQL enterprise storage engine internals with MVCC, WAL, and TOAST. " * 100
    ).encode("utf-8")
    raw_size = len(large_payload)

    print(f"Raw Attribute Payload Size : {raw_size} bytes")
    print(f"Standard Page Budget Limit : {page_threshold} bytes")

    if raw_size > page_threshold:
        print("  -> Payload exceeds 2KB! TOAST engine triggered.")
        # Step 1: Compress with zlib/lz4
        compressed = zlib.compress(large_payload, level=6)
        comp_size = len(compressed)
        print(f"  -> Compressed Size (pglz/lz4) : {comp_size} bytes ({(1 - comp_size/raw_size)*100:.1f}% reduction)")

        # Step 2: If still > 2KB, slice into out-of-line 2KB chunks for pg_toast_<oid>
        chunk_size = 2000
        chunks = [compressed[i : i + chunk_size] for i in range(0, comp_size, chunk_size)]
        print(f"  -> Sliced into {len(chunks)} out-of-line TOAST chunks for pg_toast table.")
        print("  -> Main table row stores 24-byte pointer (va_toast_pointer) with OID and Chunk Count.")
    else:
        print("  -> Fits inline in the 8KB table page.")


def main() -> None:
    demo_json_vs_jsonb_parsing()
    demo_toast_compression_and_chunking()


if __name__ == "__main__":
    main()
