"""Module 01: Hardware Latency Hierarchy & Memory vs Disk Benchmark Demo.

Demonstrates the physical time differences between L1/L2 cache, RAM,
sequential vs random I/O, and network packet simulation.
"""

from __future__ import annotations

import os
import tempfile
import time


def benchmark_ram_access() -> tuple[float, float]:
    """Benchmarks sequential memory reading vs random memory access in RAM."""
    size = 2_000_000
    data = list(range(size))

    # Sequential Read
    start = time.perf_counter()
    total_seq = sum(data)
    seq_duration = time.perf_counter() - start

    # Pseudo-random lookup (strided access to force cache line misses)
    stride = 997  # prime stride
    start = time.perf_counter()
    total_rand = 0
    idx = 0
    for _ in range(500_000):
        total_rand += data[idx]
        idx = (idx + stride) % size
    rand_duration = time.perf_counter() - start

    # Prevent unused variable warnings
    assert total_seq > 0 and total_rand > 0

    return seq_duration, rand_duration


def benchmark_disk_io() -> tuple[float, float]:
    """Benchmarks sequential write to disk vs forced durable fsync writes."""
    test_data = b"X" * 4096  # 4KB block
    num_writes = 500

    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_name = f.name

    try:
        # 1. Buffered OS Disk Write (Page Cache)
        start = time.perf_counter()
        with open(temp_name, "wb") as f:
            for _ in range(num_writes):
                f.write(test_data)
        buffered_duration = time.perf_counter() - start

        # 2. Durable Fsync Write (Flushing physical drive platters/NAND cells)
        start = time.perf_counter()
        with open(temp_name, "wb") as f:
            for _ in range(100):  # fewer writes because fsync is slow
                f.write(test_data)
                f.flush()
                os.fsync(f.fileno())
        fsync_duration = (time.perf_counter() - start) * (num_writes / 100)  # normalized

        return buffered_duration, fsync_duration
    finally:
        if os.path.exists(temp_name):
            os.remove(temp_name)


def main() -> None:
    print("=" * 75)
    print("       SYSTEM DESIGN LATENCY HIERARCHY & HARDWARE REALITY BENCHMARK")
    print("=" * 75)

    print("\n[1] Benchmarking RAM (Sequential vs Strided Cache-Miss Access)...")
    seq_time, rand_time = benchmark_ram_access()
    print(f"  -> Sequential 2,000,000 ints read: {seq_time * 1000:.2f} ms")
    print(f"  -> Strided (Cache-Miss) 500,000 lookups: {rand_time * 1000:.2f} ms")
    print(f"  -> Sequential RAM access was {rand_time / (seq_time / 4):.1f}x faster per element!")

    print("\n[2] Benchmarking Disk I/O (Page Cache vs Physical Fsync Durability)...")
    buffered_time, fsync_time = benchmark_disk_io()
    print(f"  -> Buffered Page-Cache Writes (500 x 4KB): {buffered_time * 1000:.2f} ms")
    print(f"  -> Physical Disk Fsync Writes (500 x 4KB): {fsync_time * 1000:.2f} ms")
    print(f"  -> Fsync was {fsync_time / buffered_time:.1f}x slower than memory-buffered I/O!")

    print("\n" + "=" * 75)
    print("                   THE ARCHITECT'S LATENCY COMPARISON TABLE")
    print("=" * 75)
    print(f"{'Operation':<35} | {'Real Latency':<15} | {'Normalized (1 ns = 1s)':<20}")
    print("-" * 75)
    latencies = [
        ("L1 CPU Cache Reference", "0.5 ns", "0.5 seconds"),
        ("Branch Mispredict Penalty", "5.0 ns", "5.0 seconds"),
        ("L2 CPU Cache Reference", "7.0 ns", "7.0 seconds"),
        ("Mutex Lock / Unlock", "25.0 ns", "25.0 seconds"),
        ("Main RAM Memory Reference", "100.0 ns", "1.7 minutes"),
        ("Compress 1KB with Snappy", "2,000 ns (2 �s)", "33.3 minutes"),
        ("Send 2KB over 1 Gbps Network", "20,000 ns (20 �s)", "5.5 hours"),
        ("SSD Random Read (NVMe)", "100,000 ns (100 �s)", "1.1 days"),
        ("Roundtrip in Same Datacenter", "500,000 ns (500 �s)", "5.8 days"),
        ("HDD Disk Seek (Rotational)", "10,000,000 ns (10 ms)", "3.8 months"),
        ("Transatlantic Packet Roundtrip", "150,000,000 ns (150 ms)", "4.7 years!"),
    ]
    for op, real_val, scaled_val in latencies:
        print(f"{op:<35} | {real_val:<15} | {scaled_val:<20}")
    print("=" * 75)


if __name__ == "__main__":
    main()
