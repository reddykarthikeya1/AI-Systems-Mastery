"""
Module 09: Interactive Threading vs Sync Demo
Run: python try_it_yourself.py
"""

import threading
import time


def worker(task_name, duration):
    print(f"  [+] Starting {task_name} (takes {duration}s)...")
    time.sleep(duration)
    print(f"  [OK] Finished {task_name}!")


def run_sequential():
    print("\n1. Running tasks SEQUENTIALLY (one after another):")
    start = time.time()
    worker("Task A", 0.5)
    worker("Task B", 0.5)
    total = time.time() - start
    print(f"--> Total Sequential Time: {total:.2f}s")


def run_threaded():
    print("\n2. Running tasks CONCURRENTLY (with 2 Threads):")
    start = time.time()
    t1 = threading.Thread(target=worker, args=("Task A", 0.5))
    t2 = threading.Thread(target=worker, args=("Task B", 0.5))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    total = time.time() - start
    print(f"--> Total Threaded Time: {total:.2f}s (Nearly 2x faster!)")


def main():
    print("=" * 60)
    print("  MODULE 09: THREADING PLAYGROUND [*]")
    print("=" * 60)
    run_sequential()
    run_threaded()
    print("\nConclusion: Threads let you overlap waiting time!")
    print("Proceed to Module 10 for AsyncIO.")


if __name__ == "__main__":
    main()
