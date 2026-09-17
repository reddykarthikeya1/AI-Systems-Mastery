"""Beginner playground for Module 18 - Distributed Systems: Task Queues & Streaming.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import heapq
import time

# -------------------------------------------- 1. Priority Task Scheduling with Heapq
tasks = []
heapq.heappush(tasks, (3, "low_priority_email"))
heapq.heappush(tasks, (1, "critical_fraud_alert"))
heapq.heappush(tasks, (2, "medium_invoice_gen"))

first = heapq.heappop(tasks)
second = heapq.heappop(tasks)
third = heapq.heappop(tasks)

assert first == (1, "critical_fraud_alert")
assert second == (2, "medium_invoice_gen")
assert third == (3, "low_priority_email")
print(f"Tasks processed in priority order: {first[1]} -> {second[1]} -> {third[1]}")

# -------------------------------------------- 2. Dead-Letter Queue (DLQ) Pattern
dlq = []
def execute_task(task, max_retries=2):
    attempts = 0
    while attempts < max_retries:
        attempts += 1
    dlq.append((task, "exceeded_max_retries"))

execute_task("send_sms_555")
assert len(dlq) == 1
assert dlq[0][0] == "send_sms_555"
assert dlq[0][1] == "exceeded_max_retries"
print(f"Task safely diverted to DLQ: {dlq}")

# -------------------------------------------- 3. At-Least-Once Delivery Idempotency
processed_ids = set()
def process_message(msg_id, payload):
    if msg_id in processed_ids:
        return "duplicate_ignored"
    processed_ids.add(msg_id)
    return f"processed_{payload}"

assert process_message("msg-101", "payment") == "processed_payment"
assert process_message("msg-101", "payment") == "duplicate_ignored"
assert len(processed_ids) == 1
print("Idempotency filter prevented duplicate execution.")

print()
print("All checks passed.")
