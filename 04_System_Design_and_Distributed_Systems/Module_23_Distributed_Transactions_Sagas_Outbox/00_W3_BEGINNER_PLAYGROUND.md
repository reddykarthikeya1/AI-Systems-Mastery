# Beginner Playground - Distributed Transactions, Sagas and the Outbox

> *"Booking a flight, a hotel and a car. There is no single 'undo' button - if the car falls through you cancel the hotel and cancel the flight, and each cancellation is its own transaction."*

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

## 1. Why there is no BEGIN across two services

Two-phase commit exists and does work, but it requires every participant to hold
locks while waiting for a coordinator. If the coordinator dies mid-decision, those
locks are held indefinitely - the participants cannot safely guess.

That is unacceptable across service and company boundaries, so distributed systems
give up atomicity and buy it back with compensation: do each step for real, and if
a later step fails, perform an action that undoes the business effect of the
earlier ones.

```python
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
```

---

## 2. A saga is a list of steps, each with an undo

Run the steps in order. If one fails, run the compensations for the completed
steps in reverse order.

The state in between is visible to the outside world - the stock really was
reserved for a moment. A saga does not hide that; it guarantees you end up
somewhere consistent, not that nobody could observe the middle.

```python
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
```

---

## 3. Now fail the second step

Payment is declined. The stock reservation has already happened, so it must be
released - and nothing else has, so nothing else needs undoing.

Note what the audit log shows: the reservation and the release are both there. A
compensation is not a rollback that erases history; it is a new event.

```python
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
```

---

## 4. The dual-write problem, and the outbox that solves it

There is still a gap. Committing to your database and publishing an event are two
separate systems, so a crash between them leaves them disagreeing - and no amount
of retry logic closes a window you cannot make atomic.

The **outbox** closes it by moving the message into the transaction: write the
business row and the outgoing message to the same database, in one commit. A
relay process reads the outbox and publishes. If it crashes, the row is still
there and it tries again.

```python
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
```

---

## 5. Predict before you run

Your service commits to its database, then publishes an event. The commit
succeeds and the process dies before the publish. What does the rest of the
company believe happened? Can a database transaction prevent this?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Once data lives in more than one service, `BEGIN ... COMMIT` no longer spans
your operation. Sagas and the outbox are not exotic patterns - they are the
ordinary cost of having more than one database.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
