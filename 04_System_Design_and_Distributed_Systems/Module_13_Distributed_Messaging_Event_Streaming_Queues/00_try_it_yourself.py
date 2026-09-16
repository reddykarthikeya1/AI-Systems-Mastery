"""Beginner playground for Module 13 - Distributed Messaging and Event Streaming.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------ 1. Queue or log - the difference is who owns the position
queue = ["msg-1", "msg-2", "msg-3"]
delivered = queue.pop(0)
print("queue: consumer took", delivered, "- remaining:", queue)
assert len(queue) == 2, "a queue hands a message out once, then it is gone"

log = ["msg-1", "msg-2", "msg-3"]
offsets = {"billing": 0, "analytics": 0}
offsets["billing"] += 1
print("log: billing is at", offsets["billing"], "analytics at", offsets["analytics"])
assert log == ["msg-1", "msg-2", "msg-3"], "the log is unchanged by reading"
assert offsets["analytics"] == 0, "analytics can still read from the start"


# ----------- 2. At-most-once, at-least-once, and why there is no third option
processed = []
broker = ["charge-order-7"]


def consume_ack_first(message, crash):
    broker.remove(message)
    if crash:
        return "lost"
    processed.append(message)
    return "done"


print("ack first, then crash:", consume_ack_first("charge-order-7", crash=True))
print("  broker still holds:", broker, "processed:", processed)
assert broker == [] and processed == [], "at-most-once: the message is simply gone"


# ------------ 3. At-least-once produces duplicates, and that is the good case
broker = ["charge-order-7"]
charges = []


def consume_process_first(message, crash_before_ack):
    charges.append(message)                 # the side effect happens
    if crash_before_ack:
        return "crashed before acknowledging - broker will redeliver"
    broker.remove(message)
    return "done"


print(consume_process_first("charge-order-7", crash_before_ack=True))
print(consume_process_first("charge-order-7", crash_before_ack=False))
print("charges recorded:", charges)
assert charges == ["charge-order-7"] * 2, "the customer was charged twice"
assert broker == []


# ------------------------ 4. Idempotent consumers make the duplicate harmless
seen_message_ids = set()
ledger = []


def handle(message_id, order_id, amount):
    if message_id in seen_message_ids:
        return "duplicate - ignored"
    seen_message_ids.add(message_id)
    ledger.append((order_id, amount))
    return "charged"


print("first delivery: ", handle("msg-a1", "order-7", 50))
print("redelivery:     ", handle("msg-a1", "order-7", 50))
print("a genuine second order:", handle("msg-b2", "order-8", 50))
assert ledger == [("order-7", 50), ("order-8", 50)]
print("Two deliveries of one message, one charge. Two orders, two charges.")


# ------------------------------------------- 5. Ordering, and the price of it
def partition_for(key, partitions=3):
    return sum(key.encode()) % partitions


events = [("user:1", "created"), ("user:1", "updated"), ("user:1", "deleted"),
          ("user:2", "created")]
placement = {}
for key, event in events:
    placement.setdefault(partition_for(key), []).append((key, event))

for part, contents in sorted(placement.items()):
    print(f"  partition {part}: {[e for _, e in contents]}")

user1_partitions = {partition_for(key) for key, _ in events if key == "user:1"}
assert len(user1_partitions) == 1, "all of user:1's events share one partition"
print("Same key, same partition, guaranteed order. Different keys, no promise.")


print()
print("All checks passed.")
