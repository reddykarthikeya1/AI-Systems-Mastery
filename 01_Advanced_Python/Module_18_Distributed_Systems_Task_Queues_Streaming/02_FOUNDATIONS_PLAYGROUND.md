# 🐣 Interactive Foundations Playground: Distributed Systems: Task Queues & Streaming

> *"Asynchronous task queues decouple request intake from intensive background processing."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import heapq
import time
```

---

## 1. Priority Task Scheduling with Heapq

A binary min-heap schedules highest-priority tasks first with $O(\log N)$ insertion.

```python
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
```

---

## 2. Dead-Letter Queue (DLQ) Pattern

Tasks exceeding maximum retry limits are routed to a dead-letter queue for forensic debugging.

```python
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
```

---

## 3. At-Least-Once Delivery Idempotency

Idempotency keys prevent duplicate processing when messages are redelivered.

```python
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
```

---
