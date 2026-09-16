#!/usr/bin/env python3
"""Broken Extension Demo demonstrating debug build slowdown and GIL starvation traps."""

import time
import threading

def simulate_native_computation(iterations: int, release_gil: bool):
    # holds the GIL and starves all concurrent Python threads!
    if not release_gil:
        # GIL is retained:
        total = 0
        for i in range(iterations):
            total = (total + i * 3) & 0xFFFFFFFFFFFFFFFF
        return total

def background_monitor():
    for _ in range(5):
        time.sleep(0.1)
        print("[Heartbeat] Python background thread responsive")

if __name__ == "__main__":
    t = threading.Thread(target=background_monitor, daemon=True)
    t.start()

    print("Running heavy CPU calculation without GIL release...")
    simulate_native_computation(20_000_000, release_gil=False)
    print("Computation finished. Notice background heartbeat thread was starved!")
