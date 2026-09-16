"""Beginner playground for Module 23 - Distributed Transactions, Sagas and the Outbox.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------------------- 1. Why there is no BEGIN across two services
inventory = {"widget": 10}
payments = []
shipments = []
audit = []


def reserve_stock(item, qty):
    if inventory[item] < qty:
        raise RuntimeError("out of stock")
    inventory[item] -= qty
    audit.append(f"reserved {qty} {item}")
    return f"reservation:{item}:{qty}"


def release_stock(item, qty):
    inventory[item] += qty
    audit.append(f"released {qty} {item}")


print("starting stock:", inventory)
assert inventory["widget"] == 10


# ---------------------------- 2. A saga is a list of steps, each with an undo
def take_payment(amount, fail=False):
    if fail:
        raise RuntimeError("card declined")
    payments.append(amount)
    audit.append(f"charged {amount}")
    return f"payment:{amount}"


def refund(amount):
    payments.remove(amount)
    audit.append(f"refunded {amount}")


def run_saga(steps):
    completed = []
    try:
        for do, undo in steps:
            do()
            completed.append(undo)
        return "committed"
    except RuntimeError as exc:
        for undo in reversed(completed):
            undo()
        return f"compensated after: {exc}"


result = run_saga([
    (lambda: reserve_stock("widget", 3), lambda: release_stock("widget", 3)),
    (lambda: take_payment(50), lambda: refund(50)),
    (lambda: shipments.append("ship-1"), lambda: shipments.remove("ship-1")),
])
print(result, "| stock:", inventory, "| payments:", payments, "| shipments:", shipments)
assert result == "committed"
assert inventory["widget"] == 7 and payments == [50] and shipments == ["ship-1"]


# ------------------------------------------------ 3. Now fail the second step
audit.clear()
result = run_saga([
    (lambda: reserve_stock("widget", 3), lambda: release_stock("widget", 3)),
    (lambda: take_payment(50, fail=True), lambda: refund(50)),
])
print(result)
print("audit trail:", audit)
print("stock restored to:", inventory)
assert result.startswith("compensated")
assert inventory["widget"] == 7, "back to where we were before this saga"
assert audit == ["reserved 3 widget", "released 3 widget"]
print("A refund is not an un-charge. Both appear on the customer's statement.")


# ------------------- 4. The dual-write problem, and the outbox that solves it
orders_table = []
outbox_table = []
message_bus = []


def place_order_with_outbox(order_id):
    # One transaction, one database, both rows.
    orders_table.append(order_id)
    outbox_table.append({"id": f"msg-{order_id}", "order": order_id, "sent": False})


def relay(crash_after_publish=False):
    for message in outbox_table:
        if message["sent"]:
            continue
        message_bus.append(message["id"])
        if crash_after_publish:
            return "crashed before marking sent"
        message["sent"] = True
    return "all published"


place_order_with_outbox("order-1")
print(relay(crash_after_publish=True))
print("  bus:", message_bus, "| outbox sent flags:", [m["sent"] for m in outbox_table])
print(relay())
print("  bus:", message_bus)
assert message_bus == ["msg-order-1", "msg-order-1"], "at-least-once, so a duplicate"
assert all(m["sent"] for m in outbox_table)
print("Never lost, sometimes duplicated. Consumers deduplicate on the message id.")


print()
print("All checks passed.")
