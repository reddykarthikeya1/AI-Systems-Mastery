#!/usr/bin/env python3
"""Broken Concurrency Pipeline demonstrating race conditions, deadlocks, and daemon thread traps."""

import threading
import time

shared_counter = 0
lock_a = threading.Lock()
lock_b = threading.Lock()

def race_increment():
    global shared_counter
    for _ in range(50_000):
        val = shared_counter
        time.sleep(0.000001)
        shared_counter = val + 1

def deadlock_worker_one():
    with lock_a:
        time.sleep(0.01)
        with lock_b:
            pass

def deadlock_worker_two():
    with lock_b:
        time.sleep(0.01)
        with lock_a:
            pass

def daemon_file_writer():
    with open("daemon_output.tmp", "w") as f:
        for i in range(100):
            f.write(f"Record {i}\n")
            time.sleep(0.01)

if __name__ == "__main__":
    t1 = threading.Thread(target=race_increment)
    t2 = threading.Thread(target=race_increment)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(f"Final counter: {shared_counter} (Expected: 100,000, got far less due to race condition!)")

    print("Demonstrating deadlock risk with inverse lock order...")
    # Workers demonstrate classic AB/BA deadlock pattern
