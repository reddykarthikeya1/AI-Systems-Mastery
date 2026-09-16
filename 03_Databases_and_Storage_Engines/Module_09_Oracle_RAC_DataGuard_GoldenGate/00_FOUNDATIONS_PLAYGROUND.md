# Beginner Playground - Oracle RAC, Data Guard and GoldenGate

> *"RAC is several cashiers sharing one till. Data Guard is the backup generator in the basement. They solve different disasters, and people confuse them constantly."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

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

## 1. Two different disasters

| Disaster | What saves you | What does not |
| :--- | :--- | :--- |
| A server dies | **RAC** - other nodes share the same storage and carry on | Data Guard, which is a different building |
| The whole site dies | **Data Guard** - a standby database elsewhere | RAC, whose nodes share the storage that just died |

RAC is *scale and node failure*. Data Guard is *site failure*. GoldenGate is a
third thing again: it ships changes between databases that are not even the same
product, which is how you migrate Oracle to PostgreSQL without downtime.

```python
shared_storage = {"balance": 1000}
rac_nodes = ["node1", "node2", "node3"]
alive = set(rac_nodes)


def serve(node, delta):
    if node not in alive:
        return None
    shared_storage["balance"] += delta
    return shared_storage["balance"]


print("node1 serves a request:", serve("node1", 100))
alive.remove("node1")
print("node1 has died. node2 serves the next request:", serve("node2", 100))
assert shared_storage["balance"] == 1200, "the data was never on node1 - it is on the SAN"
print("RAC survives a NODE failure because the data was never on the node.")
```

---

## 2. Why RAC is not free

Every node caches blocks. When node2 wants a block node1 has already modified,
the block must travel across the interconnect. That is **cache fusion**, and it
is fast - but it is not free, and an application whose sessions all fight over
the same hot rows can be *slower* on RAC than on one machine.

The fix is almost never more nodes. It is partitioning the workload so different
nodes touch different data.

```python
block_owner = {}
interconnect_transfers = {"count": 0}


def node_writes(node, block_id):
    if block_owner.get(block_id) not in (None, node):
        interconnect_transfers["count"] += 1
    block_owner[block_id] = node


for i in range(6):
    node_writes(rac_nodes[i % 3], block_id="hot_counter")
print("all three nodes fighting over one block ->",
      interconnect_transfers["count"], "interconnect transfers")
assert interconnect_transfers["count"] == 5

interconnect_transfers["count"] = 0
block_owner.clear()
for i in range(6):
    node_writes(rac_nodes[i % 3], block_id=f"partition_{i % 3}")
print("each node owning its own partition ->",
      interconnect_transfers["count"], "interconnect transfers")
assert interconnect_transfers["count"] == 0, "no contention, no transfers"
```

---

## 3. Data Guard: how much are you willing to lose?

The standby is a second database kept up to date by shipping redo. The only
question that matters is *when the primary is allowed to say "committed"*.

- **Maximum performance (async):** commit now, ship the redo shortly after. Fast,
  and a site loss costs you whatever had not shipped yet.
- **Maximum protection (sync):** ship the redo, wait for the standby to confirm,
  *then* commit. Zero loss, and every commit now pays a network round trip.

There is no third option where you get both. Pick which one the business is
actually buying.

```python
committed_on_primary = []
received_by_standby = []


def commit_transaction(txn, mode):
    if mode == "sync":
        received_by_standby.append(txn)
        committed_on_primary.append(txn)
        return 2.0  # ms: a round trip to the standby, on every commit
    committed_on_primary.append(txn)
    return 0.1  # ms: local only; shipping happens in the background


async_cost = sum(commit_transaction(f"txn{i}", "async") for i in range(5))
print("primary has committed:", committed_on_primary)
print("standby has received: ", received_by_standby)

lost = [t for t in committed_on_primary if t not in received_by_standby]
print("site is destroyed now. Transactions lost:", lost)
assert len(lost) == 5, "async means confirmed-but-not-yet-shipped work can vanish"
```

---

## 4. The same five transactions, paid for properly

Switch to synchronous and the loss goes to zero. Watch the commit cost.

```python
committed_on_primary.clear()
received_by_standby.clear()
sync_cost = sum(commit_transaction(f"txn{i}", "sync") for i in range(5))

lost_now = [t for t in committed_on_primary if t not in received_by_standby]
print("Transactions lost with synchronous shipping:", lost_now)
assert lost_now == [], "RPO of zero - nothing committed is unprotected"

print(f"commit cost: async {async_cost:.1f} ms total, sync {sync_cost:.1f} ms total")
assert sync_cost > async_cost, "zero data loss is bought with latency, every commit"
print("RPO = how much you may lose. RTO = how long until you are back.")
```

---

## 5. Predict before you run

In asynchronous standby mode the primary confirms a commit *before* the
standby has the data. If the primary is destroyed one second later, how many
committed transactions can you lose - zero, a handful, or all of them?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

RPO and RTO are contract terms, not engineering preferences. "We lose at most
zero transactions" and "we lose at most five seconds" are priced differently
because they require different architectures, and the difference is the
handful of lines below.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
