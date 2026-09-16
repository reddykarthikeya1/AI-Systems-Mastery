"""Beginner playground for Module 01 - The Physics of Scalability and Capacity Math.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# -------------------------------------------- 1. The numbers worth memorising
NANOSECOND = 1e-9
timings_ns = {
    "l1_cache": 1,
    "memory": 100,
    "ssd_read": 100_000,
    "datacentre_rtt": 500_000,
    "atlantic_rtt": 150_000_000,
}

for name, ns in timings_ns.items():
    print(f"  {name:<16} {ns * NANOSECOND * 1000:>10.3f} ms")

assert timings_ns["atlantic_rtt"] / timings_ns["memory"] == 1_500_000
print("One Atlantic round trip costs as much as 1.5 million memory reads.")


# ------------------- 2. Little's Law: the only queueing formula you must know
arrival_rate = 500          # requests per second
time_in_system = 0.2        # seconds each

concurrent = arrival_rate * time_in_system
print(f"{arrival_rate} req/s x {time_in_system}s each = {concurrent:.0f} in flight")
assert concurrent == 100

# Same law, rearranged: a thread pool of 50 caps you at a known throughput.
pool_size = 50
max_throughput = pool_size / time_in_system
print(f"a pool of {pool_size} threads can sustain {max_throughput:.0f} req/s, no more")
assert max_throughput == 250
print("Beyond that the queue grows without limit. This is arithmetic, not tuning.")


# ---------------------- 3. Why 99% utilisation is a different planet from 90%
service_rate = 100          # requests per second the server can complete


def time_in_system_at(load):
    return 1 / (service_rate - load)


print(f"{'load':>6} {'utilisation':>12} {'latency':>12}")
for load in (50, 80, 90, 95, 99):
    print(f"{load:>6} {load / service_rate:>11.0%} "
          f"{time_in_system_at(load) * 1000:>10.0f} ms")

at_90 = time_in_system_at(90)
at_99 = time_in_system_at(99)
print(f"\n10% more traffic, {at_99 / at_90:.0f}x the latency")
assert round(at_99 / at_90) == 10
print("Plan for 60-70% utilisation. The headroom IS the design.")


# --------------------------- 4. Amdahl's Law: the part you cannot parallelise
def speedup(serial_fraction, workers):
    return 1 / (serial_fraction + (1 - serial_fraction) / workers)


for workers in (1, 10, 100, 1_000, 1_000_000):
    print(f"  {workers:>9,} workers -> {speedup(0.05, workers):>6.1f}x faster")

ceiling = 1 / 0.05
print(f"ceiling with 5% serial work: {ceiling:.0f}x, no matter what you spend")
assert speedup(0.05, 1_000_000) < ceiling
assert speedup(0.05, 1_000) > speedup(0.05, 100)
assert speedup(0.05, 1_000_000) - speedup(0.05, 1_000) < 1, "the last 999,000 add nothing"


print()
print("All checks passed.")
