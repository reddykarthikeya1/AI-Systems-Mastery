"""
================================================================================
LAB 02: Asyncio Event Loop Starvation & Threadpool Offloading
================================================================================
Zero-Prerequisite Intuition:
Imagine a single waiter in a busy coffee shop taking orders from 10 customers.
Customer 1 asks: "Wait for me while I think for 2 seconds."
If the waiter stands frozen staring at Customer 1, all 9 other customers are trapped!
In Python Asyncio, the Event Loop is that single waiter.
If you execute synchronous blocking calls (time.sleep, requests, bcrypt) inside
an 'async def' function, the waiter freezes and your entire web server stalls!

Run this script to observe the latency spike, and see how asyncio.to_thread fixes it!
================================================================================
"""

import asyncio
import time

# --- PART 1: The Catastrophic Anti-Pattern (Freezing the Event Loop) ---
async def bad_blocking_task(task_id: int):
    # FATAL MISTAKE: Calling synchronous time.sleep inside async def!
    time.sleep(0.5) 
    return f"Task {task_id} done"

async def demonstrate_starvation():
    print("--- [EXPERIMENT 1] Freezing the Event Loop with Synchronous Blocking I/O ---")
    start = time.perf_counter()
    
    # Run 4 tasks concurrently using asyncio.gather
    # Since they block synchronously, they will execute sequentially (4 * 0.5s = ~2.0s)!
    results = await asyncio.gather(
        bad_blocking_task(1),
        bad_blocking_task(2),
        bad_blocking_task(3),
        bad_blocking_task(4)
    )
    elapsed = time.perf_counter() - start
    print(f"Elapsed Time with Blocking I/O: {elapsed:.2f} seconds")
    print("[ALERT] NOTICE: The event loop was completely frozen! Concurrency was destroyed.")


# --- PART 2: The Senior Engineer Fix (asyncio.to_thread) ---
def legacy_blocking_worker(task_id: int):
    """Synchronous CPU or legacy I/O library."""
    time.sleep(0.5)
    return f"Task {task_id} done"

async def good_non_blocking_task(task_id: int):
    # Offload the blocking work to an OS background worker thread!
    # The event loop stays 100% free to serve other requests immediately!
    return await asyncio.to_thread(legacy_blocking_worker, task_id)

async def demonstrate_proper_concurrency():
    print("\n--- [EXPERIMENT 2] Offloading Blocking I/O to Threadpool (asyncio.to_thread) ---")
    start = time.perf_counter()
    
    # Run 4 tasks concurrently on worker threads
    # All 4 execute in parallel on separate threads (~0.5s total)!
    results = await asyncio.gather(
        good_non_blocking_task(1),
        good_non_blocking_task(2),
        good_non_blocking_task(3),
        good_non_blocking_task(4)
    )
    elapsed = time.perf_counter() - start
    print(f"Elapsed Time with Threadpool Offload: {elapsed:.2f} seconds")
    print(f"[SPEEDUP] {2.0 / elapsed:.1f}x faster! Event loop remained completely responsive.")

async def main():
    await demonstrate_starvation()
    await demonstrate_proper_concurrency()

if __name__ == "__main__":
    asyncio.run(main())
