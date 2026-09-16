# Beginner Playground - Distributed Messaging and Event Streaming

> *"A queue is the deli ticket machine - take a number, get served once, ticket gone. A log is a tape everyone can rewind: each listener keeps their own bookmark."*

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 1. Queue or log - the difference is who owns the position

**Queue** (RabbitMQ, SQS): the broker tracks what has been delivered. A message is
handed to one consumer and removed once acknowledged. Add consumers and the work
splits between them.

**Log** (Kafka): the broker keeps an ordered file and every consumer group keeps
its *own* offset into it. The same message is read by analytics, by billing and by
search, independently, and a new consumer can start from the beginning.

Choose a queue for work distribution, a log for facts many systems care about.

```python
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
```

---

## 2. At-most-once, at-least-once, and why there is no third option

Acknowledge *before* processing and a crash loses the message: **at-most-once**.
Acknowledge *after* processing and a crash redelivers it: **at-least-once**.

There is no ordering of those two steps that gives you exactly once, because the
crash can land between them whichever way round you put them. This is not an
implementation weakness; it is the shape of the problem.

```python
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
```

---

## 3. At-least-once produces duplicates, and that is the good case

Acknowledge after processing. Now a crash between processing and acknowledging
means the broker redelivers - so the work happens twice.

A duplicate is recoverable. A lost charge, a lost order, a lost event is not. This
is why at-least-once is the default nearly everywhere.

```python
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
```

---

## 4. Idempotent consumers make the duplicate harmless

The consumer records which message ids it has already handled and ignores repeats.
Now "at-least-once delivery" plus "idempotent processing" behaves exactly like
exactly-once, from the outside.

The key must identify the *message*, not the request - a genuine second order from
the same customer for the same amount must still go through.

```python
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
```

---

## 5. Ordering, and the price of it

Kafka guarantees order only *within a partition*. Spread a customer's events
across partitions and "account created" can be processed after "account deleted".

The fix is to partition by a key that groups everything which must stay ordered -
customer id, account id, order id. The cost is that one hot key is one partition,
which is one consumer, which is your ceiling for that key.

```python
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
```

---

## 6. Predict before you run

A consumer processes a message and crashes before acknowledging it. The
broker redelivers it. What has now happened twice, and what stops that from
charging a customer twice?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Exactly-once delivery across a network is impossible, which is why every
real system is at-least-once plus an idempotent consumer. If someone claims
exactly-once, they mean at-least-once with deduplication - which is fine, but
it is worth knowing which one you are actually buying.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
