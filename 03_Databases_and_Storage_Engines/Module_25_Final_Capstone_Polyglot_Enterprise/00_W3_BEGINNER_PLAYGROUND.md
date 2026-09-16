# Beginner Playground - Capstone - Polyglot Persistence

> *"A kitchen has a knife, a blender and a grater. Nobody argues about which one is best - they argue about which one you should be holding right now."*

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

## 1. Match the store to the access pattern

Every store in this course is excellent at something and poor at something else.
The skill is naming the access pattern first, then picking.

| Access pattern | Store | Why |
| :--- | :--- | :--- |
| Money, must balance exactly | PostgreSQL | transactions and constraints |
| Session token, read constantly | Redis | in-memory, expires by itself |
| "Sum revenue by month by region" | DuckDB / ClickHouse | columnar |
| "Find products matching 'blue running shoe'" | Elasticsearch | inverted index |
| "Show me similar images" | pgvector / Qdrant | nearest-neighbour search |
| "How is this account linked to that one" | Neo4j | traversal, not joins |

```python
def choose_store(pattern):
    routing = {
        "transactional_money": "postgresql",
        "ephemeral_session": "redis",
        "analytical_aggregate": "duckdb",
        "full_text_search": "elasticsearch",
        "similarity_search": "qdrant",
        "relationship_traversal": "neo4j",
    }
    return routing[pattern]


for pattern in ("transactional_money", "analytical_aggregate", "full_text_search"):
    print(f"  {pattern:<24} -> {choose_store(pattern)}")
assert choose_store("transactional_money") == "postgresql"
assert choose_store("analytical_aggregate") == "duckdb"
```

---

## 2. The bill for polyglot: no transaction spans two stores

Write the order to PostgreSQL, then publish an event to the queue. Two systems,
two separate commits, and a gap between them where the process can die.

Commit succeeded, publish failed: the order exists and nothing downstream knows.
Publish succeeded, commit rolled back: the world is told about an order that does
not exist. There is no `BEGIN` that covers both.

```python
database_orders = []
published_events = []


def place_order_naive(order_id, fail_after_commit):
    database_orders.append(order_id)                  # commit 1: succeeded
    if fail_after_commit:
        raise RuntimeError("process died before publishing")
    published_events.append(order_id)                 # commit 2: never happened


try:
    place_order_naive("order-1", fail_after_commit=True)
except RuntimeError as exc:
    print("crash:", exc)

print("orders in the database:", database_orders)
print("events published:      ", published_events)
assert database_orders == ["order-1"] and published_events == []
print("The order is real and the warehouse will never hear about it.")
```

---

## 3. The outbox pattern fixes it with one insight

You cannot make two systems commit together. You *can* make the intent to publish
part of the same transaction as the data.

Write the order and the outgoing message to the same database, in one commit. A
separate process then reads the outbox and publishes. If it crashes, the row is
still there and it retries.

You trade "might never publish" for "might publish twice", which is a far better
problem - consumers can deduplicate on the message id.

```python
database_orders.clear()
published_events.clear()
outbox = []


def place_order_outbox(order_id):
    # ONE transaction, ONE database: the order and the intent to publish.
    database_orders.append(order_id)
    outbox.append({"id": f"msg-{order_id}", "order": order_id, "sent": False})


def relay(crash_after_publish=False):
    for message in outbox:
        if message["sent"]:
            continue
        published_events.append(message["order"])
        if crash_after_publish:
            return False                  # died before recording success
        message["sent"] = True
    return True


place_order_outbox("order-1")
relay(crash_after_publish=True)
print("after a crash mid-relay -> published:", published_events,
      "outbox marked sent:", [m["sent"] for m in outbox])

relay()
print("after the retry          -> published:", published_events)
assert published_events == ["order-1", "order-1"], "at-least-once: a duplicate"
assert all(m["sent"] for m in outbox), "and now it is definitely recorded"
```

---

## 4. Which is why consumers must be idempotent

At-least-once delivery means duplicates are normal, not exceptional. The consumer
keeps the ids it has already processed and ignores repeats.

That is the contract the whole architecture rests on: the producer guarantees the
message arrives, the consumer guarantees processing it twice is the same as once.

```python
processed_ids = set()
warehouse_picks = []


def handle(message_id, order_id):
    if message_id in processed_ids:
        return "duplicate ignored"
    processed_ids.add(message_id)
    warehouse_picks.append(order_id)
    return "picked"


print("first delivery: ", handle("msg-order-1", "order-1"))
print("second delivery:", handle("msg-order-1", "order-1"))
assert warehouse_picks == ["order-1"], "shipped once, despite two deliveries"
print()
print("PostgreSQL for the money. Redis for the session. Columnar for the report.")
print("And a deliberate pattern for every write that crosses between them.")
```

---

## 5. Predict before you run

Your order service writes to PostgreSQL and then publishes to a message
queue. The database commit succeeds and the publish fails. What state is the
system in, and can a transaction fix it?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Real systems run four or five data stores. The hard part is never choosing
them - it is that no transaction spans them, so every cross-store write needs
a deliberate pattern rather than hope.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
