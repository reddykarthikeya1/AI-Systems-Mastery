#!/usr/bin/env python3
"""Module 10: Bridging Synchronous Code with asyncio.to_thread() Demonstration.

This script demonstrates how to run legacy blocking synchronous functions
without freezing the asynchronous Event Loop.
"""

from __future__ import annotations

import asyncio
import time


def legacy_blocking_file_read(file_id: int) -> str:
    """Simulates a legacy synchronous disk/database call using time.sleep()."""
    time.sleep(0.1)  # Synchronous blocking sleep
    return f"Data payload for file #{file_id}"


async def ticker_heartbeat() -> None:
    """Async background task that ticks every 20ms to verify loop responsiveness."""
    for i in range(5):
        await asyncio.sleep(0.02)
        print(f"  [Heartbeat] Event loop is responsive (Tick {i+1})")


async def main() -> None:
    print("=" * 60)
    print("  Bridging Synchronous Blocking Calls with asyncio.to_thread")
    print("=" * 60)

    # Launch background heartbeat
    heartbeat_task = asyncio.create_task(ticker_heartbeat())

    # Offload blocking operations to worker threads via asyncio.to_thread
    start = time.perf_counter()
    results = await asyncio.gather(*(asyncio.to_thread(legacy_blocking_file_read, i) for i in range(1, 4)))
    duration = time.perf_counter() - start

    await heartbeat_task
    print(f"\nAll 3 blocking operations completed in {duration:.4f}s without stalling the heartbeat!")
    print(f"Results: {results}")


if __name__ == "__main__":
    asyncio.run(main())
