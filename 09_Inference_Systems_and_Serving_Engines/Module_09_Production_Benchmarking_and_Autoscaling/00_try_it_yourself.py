"""Beginner playground for Module 09 - Production Benchmarking & Autoscaling.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Little's Law for LLM Serving
arrival_rate = 20.0     # req/sec
avg_latency_sec = 1.5   # seconds
concurrent_in_flight = arrival_rate * avg_latency_sec

assert concurrent_in_flight == 30.0
print(f"System requires support for {concurrent_in_flight:.0f} concurrent requests.")

# -------------------------------------------- 2. Queue Delay Knee Point
def queue_delay(utilization, service_rate=10.0):
    return utilization / (service_rate * (1.0 - utilization))

q_70 = queue_delay(0.70)
q_95 = queue_delay(0.95)
q_ratio = q_95 / q_70

assert q_ratio > 7.0
assert round(q_ratio, 1) == 8.1
print(f"Queue delay explodes {q_ratio:.1f}x when utilization goes from 70% to 95%.")

# -------------------------------------------- 3. Autoscaling Target Utilization Policy
target_utilization = 0.70
current_requests = 140
capacity_per_replica = 20
required_replicas = math.ceil(current_requests / (capacity_per_replica * target_utilization))

assert required_replicas == 10
assert required_replicas * capacity_per_replica * target_utilization >= current_requests
print(f"Autoscaler provisioned {required_replicas} GPU replicas to maintain 70% utilization target.")

print()
print("All checks passed.")
