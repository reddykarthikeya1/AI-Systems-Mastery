"""Beginner playground for Module 25 - Capstone - Polyglot Persistence.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations


# ----------------------------------- 1. Match the store to the access pattern
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


# ------------------ 2. The bill for polyglot: no transaction spans two stores
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


# ---------------------------- 3. The outbox pattern fixes it with one insight
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


# ------------------------------- 4. Which is why consumers must be idempotent
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


print()
print("All checks passed.")
