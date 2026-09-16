# Beginner Playground - Redis Sentinel, Clustering and Lua

> *"Sentinel is a set of night watchmen who must agree before waking anyone. A Lua script is a queue barrier: once you step up, nobody cuts in front of you."*

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

## 1. Why one watchman is not enough

Sentinel processes watch the primary. If one of them cannot reach it, that proves
very little - the *watchman's* network may be the broken part.

So failover requires a **quorum**: a configured number of Sentinels must
independently agree the primary is down. Set the quorum to 1 and a single
watchman with a bad cable can demote a perfectly healthy primary, which is a much
worse outage than the one it was guarding against.

```python
QUORUM = 2


def should_fail_over(reports):
    down_votes = sum(1 for reachable in reports.values() if not reachable)
    return down_votes >= QUORUM


one_bad_cable = {"sentinel1": False, "sentinel2": True, "sentinel3": True}
really_down = {"sentinel1": False, "sentinel2": False, "sentinel3": False}

print("one sentinel cannot see the primary ->", should_fail_over(one_bad_cable))
print("all three cannot see the primary   ->", should_fail_over(really_down))
assert not should_fail_over(one_bad_cable), "one opinion is not evidence"
assert should_fail_over(really_down)
```

---

## 2. The last item in stock

Three commands - read, decide, write - with a gap between them. Two customers
land in that gap simultaneously and both see `stock = 1`.

Nothing here is slow or badly written. It is wrong because it is *interruptible*.

```python
stock = {"tickets": 1}
sold = []


def buy_naive(customer):
    current = stock["tickets"]          # 1. read
    if current > 0:                     # 2. decide
        return ("decided_to_buy", customer, current)
    return ("sold_out", customer, current)


decision_a = buy_naive("alice")
decision_b = buy_naive("bob")           # both read before either wrote

for _, customer, _ in (decision_a, decision_b):
    stock["tickets"] -= 1               # 3. write
    sold.append(customer)

print("tickets sold:", sold, " stock now:", stock["tickets"])
assert len(sold) == 2 and stock["tickets"] == -1, "we sold a ticket that did not exist"
print("Negative stock. Somebody is getting an apology email.")
```

---

## 3. Make it one indivisible step

Redis runs a Lua script to completion with nothing else interleaved. Read, decide
and write become a single command that cannot be split.

The Python below models exactly that property: the whole decision happens before
any other caller can observe the state.

```python
stock = {"tickets": 1}
sold = []


def buy_atomic(customer):
    # Everything inside this function is the Lua script: it runs start to finish
    # with no other client able to see or change `stock` partway through.
    if stock["tickets"] > 0:
        stock["tickets"] -= 1
        sold.append(customer)
        return "bought"
    return "sold out"


print("alice:", buy_atomic("alice"))
print("bob:  ", buy_atomic("bob"))
print("tickets sold:", sold, " stock now:", stock["tickets"])
assert sold == ["alice"], "exactly one ticket existed, exactly one was sold"
assert stock["tickets"] == 0, "stock can never go negative now"
```

---

## 4. Cluster mode: 16,384 slots and the multi-key rule

Redis Cluster hashes each key to one of 16,384 **slots**, and each node owns a
range of slots. A command touching two keys only works if both keys are in the
same slot - otherwise the two keys live on different machines and there is no
single place to run it.

The escape hatch is a **hash tag**: only the part inside `{}` is hashed. So
`{user:1}:cart` and `{user:1}:orders` are guaranteed to land together.

```python
def slot_of(key):
    tag_start = key.find("{")
    tag_end = key.find("}", tag_start + 1)
    if tag_start != -1 and tag_end > tag_start + 1:
        key = key[tag_start + 1:tag_end]
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % 16_384


plain_a, plain_b = slot_of("user:1:cart"), slot_of("user:1:orders")
print(f"user:1:cart -> slot {plain_a},  user:1:orders -> slot {plain_b}")
assert plain_a != plain_b, "similar-looking keys land on different machines"

tagged_a, tagged_b = slot_of("{user:1}:cart"), slot_of("{user:1}:orders")
print(f"{{user:1}}:cart -> slot {tagged_a},  {{user:1}}:orders -> slot {tagged_b}")
assert tagged_a == tagged_b, "the hash tag forces them into the same slot"
print("Same slot means same node, which means multi-key commands are possible.")
```

---

## 5. Predict before you run

Two customers each read `stock = 1`, each decide "there is one left", and each
buy it. How many items did you sell, and how many did you have? Which single
line of the naive version causes it?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Overselling the last item is the canonical concurrency bug, and it is not
fixed by making the code faster or the check stricter. It is fixed by making
read-decide-write one indivisible step.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
