"""
Module 18: Background Worker Task Queue Simulator
Run: python try_it_yourself.py
"""

import queue
import time


def simulate_worker(q):
    processed = 0
    while not q.empty():
        job = q.get()
        print(f"  [Worker] Processing: {job}...")
        time.sleep(0.2)
        print(f"  [OK] Completed: {job}")
        q.task_done()
        processed += 1
    return processed


def main():
    print("=" * 60)
    print("  MODULE 18: TASK QUEUE & WORKER PLAYGROUND [*]")
    print("=" * 60)

    q = queue.Queue()
    jobs = ["Send Welcome Email", "Resize Avatar Image", "Generate Monthly PDF Report"]
    print(f"Enqueuing {len(jobs)} background tasks...")
    for j in jobs:
        q.put(j)

    print("\nStarting background worker pool:")
    total = simulate_worker(q)
    print(f"\n[OK] All {total} background jobs completed successfully!")


if __name__ == "__main__":
    main()
