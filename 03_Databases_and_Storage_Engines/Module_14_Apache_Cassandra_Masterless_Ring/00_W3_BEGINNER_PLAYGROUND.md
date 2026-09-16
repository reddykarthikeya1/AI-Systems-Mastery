# Beginner Playground - Cassandra - the Masterless Ring

> *"There is no manager. Ask three neighbours, trust the majority, and make sure the group you asked overlaps the group that was told."*

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

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import hashlib
```

---

## 1. A ring with no boss

Every node in a Cassandra cluster is identical. There is no primary to fail over
and no single node whose loss stops writes.

Placement is by **token**: hash the partition key to a point on a ring, and the
node that owns that point stores it - along with the next N-1 nodes clockwise,
which hold the replicas.

```python
ring_nodes = ["node_A", "node_B", "node_C", "node_D"]
RING_SIZE = 2 ** 16


def token(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % RING_SIZE


node_positions = sorted((token(n), n) for n in ring_nodes)


def replicas_for(key, count=3):
    position = token(key)
    ordered = [n for pos, n in node_positions if pos >= position]
    ordered += [n for pos, n in node_positions if pos < position]
    return ordered[:count]


for key in ["user:42", "user:99"]:
    print(f"{key} lives on {replicas_for(key)}")
assert len(replicas_for("user:42")) == 3, "N = 3 replicas, chosen by position"
```

---

## 2. Ask few, get stale answers

N = 3 replicas. Write with W = 1: the coordinator returns as soon as *one* replica
has it. Read with R = 1: the coordinator asks *one* replica.

If the one you wrote to and the one you read from are different nodes, you read
the old value. No error, no warning, just yesterday's answer.

```python
replica_state = {"node_A": "old", "node_B": "old", "node_C": "old"}
N = 3


def write(value, w):
    targets = list(replica_state)[:w]
    for node in targets:
        replica_state[node] = value
    return targets


def read(r):
    answers = list(replica_state)[-r:]
    return [replica_state[node] for node in answers], answers


written_to = write("new", w=1)
values, asked = read(r=1)
print(f"wrote to {written_to}, read from {asked} -> {values}")
assert 1 + 1 <= N, "W + R = 2, which is NOT greater than N = 3"
assert values == ["old"], "the read missed the write entirely"
```

---

## 3. R + W > N forces an overlap

Write to 2 and read from 2. Two sets of size 2, drawn from 3 nodes, *must* share
at least one member - there is nowhere else for them to be. That shared node has
the new value, so the read cannot miss it.

That is the whole rule. `R + W > N` means the read set and the write set overlap,
and an overlap means at least one up-to-date answer.

```python
for node in replica_state:
    replica_state[node] = "old"

written_to = write("new", w=2)
values, asked = read(r=2)
overlap = set(written_to) & set(asked)
print(f"wrote to {written_to}, read from {asked}, overlap = {overlap}")
assert 2 + 2 > N, "R + W > N"
assert overlap, "the two sets cannot avoid each other"
assert "new" in values, "so the freshest value is guaranteed to be in the answer"
print("The coordinator returns the newest of what it got. Correct, every time.")
```

---

## 4. Last write wins, and the clock you must not trust

When replicas disagree, Cassandra keeps the value with the newest timestamp. Which
means a node whose clock is running fast can win an argument it should have lost,
and the correct value is silently discarded.

This is why production Cassandra clusters run NTP as a hard requirement rather
than a nice-to-have, and why "last write wins" is a data model decision, not an
implementation detail.

```python
def resolve(candidates):
    return max(candidates, key=lambda pair: pair[1])[0]


correct = ("alice@new-address.com", 1_000)            # written second, real time
from_skewed_node = ("alice@old-address.com", 5_000)   # written first, bad clock

print("resolved value:", resolve([correct, from_skewed_node]))
assert resolve([correct, from_skewed_node]) == "alice@old-address.com"
print("The older write won because its node's clock was ahead. Run NTP.")
```

---

## 5. Predict before you run

With 3 replicas, you write to 1 and read from 1. Can the read miss the write?
Now write to 2 and read from 2. Can it still miss? Work out the overlap before
you run it.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

R + W > N is the whole of tunable consistency in one line, and it is the
sentence to have ready in an interview. Cassandra lets you choose per query,
which means you can have strong consistency where it matters and speed
everywhere else.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
