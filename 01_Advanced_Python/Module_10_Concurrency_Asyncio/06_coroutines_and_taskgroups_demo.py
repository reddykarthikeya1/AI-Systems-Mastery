#!/usr/bin/env python3
"""Module 10: Coroutines & asyncio.TaskGroup Demonstration.

This script demonstrates coroutines, non-blocking sleeps, and Python 3.11+
structured concurrency via asyncio.TaskGroup.
"""

from __future__ import annotations

import asyncio
import time


async def query_user_service(user_id: int) -> dict[str, str]:
    """Simulates async network call to user microservice."""
    await asyncio.sleep(0.05)
    return {"user_id": str(user_id), "status": "ACTIVE"}


async def query_payment_service(user_id: int) -> dict[str, str]:
    """Simulates async network call to payment microservice."""
    await asyncio.sleep(0.08)
    return {"user_id": str(user_id), "plan": "ENTERPRISE"}


async def demo_task_group() -> None:
    print("=" * 60)
    print("  1. Structured Concurrency with asyncio.TaskGroup")
    print("=" * 60)

    start = time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(query_user_service(101))
        t2 = tg.create_task(query_payment_service(101))

    # When context exits, all tasks are guaranteed complete
    duration = time.perf_counter() - start
    print(f"User Data    : {t1.result()}")
    print(f"Payment Data : {t2.result()}")
    print(f"Both services queried concurrently in {duration:.4f}s")


async def failing_worker():
    await asyncio.sleep(0.02)
    raise ValueError("Simulated network disconnection!")


async def healthy_worker():
    try:
        await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("  [CANCELLED] Healthy worker received cancellation signal cleanly.")
        raise


async def demo_taskgroup_cancellation() -> None:
    print("\n" + "=" * 60)
    print("  2. Automatic Sibling Cancellation on TaskGroup Error")
    print("=" * 60)

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(failing_worker())
            tg.create_task(healthy_worker())
    except* ValueError as eg:
        print(f"TaskGroup safely aborted and caught ExceptionGroup: {eg.exceptions}")


def main() -> None:
    asyncio.run(demo_task_group())
    asyncio.run(demo_taskgroup_cancellation())


if __name__ == "__main__":
    main()
