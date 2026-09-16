#!/usr/bin/env python3
"""Module 10: Async Queues & Semaphores Demonstration.

This script demonstrates rate limiting using asyncio.Semaphore and
asynchronous producer-consumer worker pools with asyncio.Queue.
"""

from __future__ import annotations

import asyncio


async def worker_consumer(worker_id: int, queue: asyncio.Queue[str]) -> None:
    """Async worker continuously processing jobs from the queue."""
    while True:
        job = await queue.get()
        print(f"  [Worker #{worker_id}] Processing: {job}")
        await asyncio.sleep(0.05)  # Simulate I/O work
        queue.task_done()


async def demo_async_queue_pipeline() -> None:
    print("=" * 60)
    print("  1. Asynchronous Producer-Consumer Pipeline (asyncio.Queue)")
    print("=" * 60)

    queue: asyncio.Queue[str] = asyncio.Queue()

    # Launch 3 background worker consumer tasks
    workers = [asyncio.create_task(worker_consumer(i, queue)) for i in range(1, 4)]

    # Producer: Enqueue 6 jobs
    for i in range(1, 7):
        await queue.put(f"ScrapeJob_#{i}")

    # Wait until all items in the queue have been processed
    await queue.join()

    # Cancel background worker tasks cleanly
    for w in workers:
        w.cancel()
    print("All queue tasks completed successfully!")


async def demo_semaphore() -> None:
    print("\n" + "=" * 60)
    print("  2. Rate Limiting with asyncio.Semaphore")
    print("=" * 60)

    # Restrict concurrent API requests to at most 2
    sem = asyncio.Semaphore(2)

    async def call_api(req_id: int) -> None:
        async with sem:
            print(f"  [Req #{req_id}] Sent request...")
            await asyncio.sleep(0.04)
            print(f"  [Req #{req_id}] Received response.")

    await asyncio.gather(*(call_api(i) for i in range(1, 5)))


def main() -> None:
    asyncio.run(demo_async_queue_pipeline())
    asyncio.run(demo_semaphore())


if __name__ == "__main__":
    main()
