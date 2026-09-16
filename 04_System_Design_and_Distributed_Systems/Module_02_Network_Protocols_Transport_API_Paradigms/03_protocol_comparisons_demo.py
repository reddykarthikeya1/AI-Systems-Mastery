"""Module 02: Network Protocols & Serialization Benchmark Demo.

Compares JSON serialization overhead against compact binary packing (Protobuf-style)
and illustrates the benefits of HTTP/2 stream multiplexing over HTTP/1.1 head-of-line blocking.
"""

from __future__ import annotations

import json
import struct
import time


def benchmark_serialization() -> None:
    print("=" * 75)
    print("    1. PAYLOAD SERIALIZATION BENCHMARK: JSON vs COMPACT BINARY")
    print("=" * 75)

    # Simulated microservice telemetry payload
    records = [
        {
            "device_id": 1024 + i,
            "timestamp": 1700000000 + i,
            "cpu_usage": 42.5 + (i % 10),
            "memory_mb": 8192,
            "is_healthy": True,
        }
        for i in range(10_000)
    ]

    # 1. JSON Serialization
    start = time.perf_counter()
    json_bytes = json.dumps(records).encode("utf-8")
    json_duration = time.perf_counter() - start
    json_size = len(json_bytes)

    # 2. Compact Binary Packing (Simulating Protobuf schema: int32, int64, float32, int32, bool)
    # Format: '>I Q f I ?' (4 + 8 + 4 + 4 + 1 = 21 bytes per record vs ~110 bytes in JSON)
    record_format = ">I Q f I ?"
    start = time.perf_counter()
    binary_parts = []
    for r in records:
        binary_parts.append(
            struct.pack(
                record_format,
                r["device_id"],
                r["timestamp"],
                r["cpu_usage"],
                r["memory_mb"],
                r["is_healthy"],
            )
        )
    binary_bytes = b"".join(binary_parts)
    binary_duration = time.perf_counter() - start
    binary_size = len(binary_bytes)

    print(f"JSON Total Size       : {json_size / 1024:.2f} KB (Avg: {json_size / len(records):.1f} bytes/record)")
    print(f"Binary Total Size     : {binary_size / 1024:.2f} KB (Avg: {binary_size / len(records):.1f} bytes/record)")
    print(f"Bandwidth Reduction   : {(1 - (binary_size / json_size)) * 100:.1f}% bandwidth saved!")
    print(f"JSON Serialize Time   : {json_duration * 1000:.2f} ms")
    print(f"Binary Serialize Time : {binary_duration * 1000:.2f} ms ({json_duration / binary_duration:.1f}x faster)")


def simulate_multiplexing_vs_head_of_line_blocking() -> None:
    print("\n" + "=" * 75)
    print("    2. HTTP/1.1 HEAD-OF-LINE BLOCKING vs HTTP/2 STREAM MULTIPLEXING")
    print("=" * 75)

    print("Scenario: Client sends 3 requests over 1 TCP connection.")
    print("  Request #1: Heavy report (takes 100ms)")
    print("  Request #2: Fast cache check (takes 5ms)")
    print("  Request #3: Fast user profile (takes 5ms)")

    print("\n[HTTP/1.1 Pipeline / Sequential Connection]:")
    print("  --> Req #1 dispatched. Socket BLOCKED for 100ms.")
    print("  --> Req #2 forced to wait 100ms in line before transmitting! (Total latency: 105ms)")
    print("  --> Req #3 forced to wait 105ms in line before transmitting! (Total latency: 110ms)")
    print("  --> Total Wall-Clock Time: 110ms (Heavy request delayed small requests)")

    print("\n[HTTP/2 Multiplexed Binary Streams]:")
    print("  --> Req #1, #2, #3 interleaved across frames on the same TCP socket simultaneously.")
    print("  --> Req #2 completes in ~5ms!")
    print("  --> Req #3 completes in ~5ms!")
    print("  --> Req #1 completes in ~100ms!")
    print("  --> Result: Small requests return immediately without waiting for slow ones!")


def main() -> None:
    benchmark_serialization()
    simulate_multiplexing_vs_head_of_line_blocking()


if __name__ == "__main__":
    main()
