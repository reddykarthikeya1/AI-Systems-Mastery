#!/usr/bin/env python3
"""
===============================================================================
LLD Concurrency Lab: Readers-Writer Lock (RWLock) vs Standard Mutex Benchmark
===============================================================================
Metaphor:
  A public train station arrivals display board:
  - 100 passengers can all read the train arrival board at the SAME TIME!
    Nobody needs to wait in line just to look at the screen.
  - BUT when the station attendant updates the delay info with a pen, everyone
    must pause looking for half a second.
  - A standard Mutex forces 100 passengers to line up single-file to read!
===============================================================================
"""

import time
import threading
from typing import List


class StandardMutexCache:
    """Naive thread safety: single exclusive lock for both reads and writes."""
    def __init__(self):
        self.data = {"price": 100.0}
        self.lock = threading.Lock()

    def read(self) -> float:
        with self.lock:
            # Simulate tiny read processing latency
            time.sleep(0.001)
            return self.data["price"]

    def write(self, new_price: float) -> None:
        with self.lock:
            time.sleep(0.005)
            self.data["price"] = new_price


class ReadersWriterLock:
    """
    Staff implementation:
    - Multiple concurrent readers permitted simultaneously.
    - Writers have exclusive access (blocks all readers and other writers).
    """
    def __init__(self):
        self._readers = 0
        self._mutex = threading.Lock()
        self._write_lock = threading.Lock()

    def acquire_read(self) -> None:
        with self._mutex:
            self._readers += 1
            if self._readers == 1:
                # First reader locks out all writers
                self._write_lock.acquire()

    def release_read(self) -> None:
        with self._mutex:
            self._readers -= 1
            if self._readers == 0:
                # Last reader releases lock, allowing writers in
                self._write_lock.release()

    def acquire_write(self) -> None:
        self._write_lock.acquire()

    def release_write(self) -> None:
        self._write_lock.release()


class RWLockCache:
    """Production thread-safe cache leveraging ReadersWriterLock."""
    def __init__(self):
        self.data = {"price": 100.0}
        self.rwlock = ReadersWriterLock()

    def read(self) -> float:
        self.rwlock.acquire_read()
        try:
            time.sleep(0.001)
            return self.data["price"]
        finally:
            self.rwlock.release_read()

    def write(self, new_price: float) -> None:
        self.rwlock.acquire_write()
        try:
            time.sleep(0.005)
            self.data["price"] = new_price
        finally:
            self.rwlock.release_write()


def run_benchmark():
    print("=" * 70)
    print(" CONCURRENCY STRESS TEST: RWLOCK VS STANDARD MUTEX")
    print("=" * 70)

    NUM_READERS = 30
    NUM_WRITERS = 2
    READ_OPS = 20
    WRITE_OPS = 2

    # 1. Benchmark Standard Mutex
    print("\n[*] Running Benchmark on Standard Mutex (Exclusive read + write)...")
    mutex_cache = StandardMutexCache()
    start_t = time.perf_counter()

    threads: List[threading.Thread] = []

    def reader_worker(cache):
        for _ in range(READ_OPS):
            cache.read()

    def writer_worker(cache):
        for i in range(WRITE_OPS):
            cache.write(100.0 + i)

    for _ in range(NUM_READERS):
        threads.append(threading.Thread(target=reader_worker, args=(mutex_cache,)))
    for _ in range(NUM_WRITERS):
        threads.append(threading.Thread(target=writer_worker, args=(mutex_cache,)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    mutex_duration = time.perf_counter() - start_t
    print(f"    Standard Mutex Total Execution Time: {mutex_duration:.3f} seconds")

    # 2. Benchmark RWLock
    print("\n[*] Running Benchmark on RWLock (Concurrent reads allowed)...")
    rw_cache = RWLockCache()
    start_t = time.perf_counter()

    threads = []
    for _ in range(NUM_READERS):
        threads.append(threading.Thread(target=reader_worker, args=(rw_cache,)))
    for _ in range(NUM_WRITERS):
        threads.append(threading.Thread(target=writer_worker, args=(rw_cache,)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    rw_duration = time.perf_counter() - start_t
    print(f"    RWLock Total Execution Time        : {rw_duration:.3f} seconds")

    speedup = mutex_duration / rw_duration
    print("-" * 70)
    print(f" RWLock Throughput Speedup: {speedup:.2f}x FASTER!")
    assert speedup > 1.2, f"Expected RWLock to be faster than Mutex, got {speedup}"
    print(" [PASS] Multiple readers executed concurrently without serialization bottleneck.")
    print("=" * 70)


if __name__ == "__main__":
    run_benchmark()
