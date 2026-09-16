# Beginner Playground - Consistent Hashing and Distributed Partitioning

> *"A roulette wheel. Keys and servers both get a slot on the rim, and a key belongs to the first server clockwise from where it lands. Remove a server and only its arc moves."*


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

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import bisect
import hashlib
```

---

## 1. The obvious way, and why it collapses

`hash(key) % number_of_servers` is the first thing anyone writes. It spreads keys
perfectly evenly, which is the only good thing about it.

Change the server count and the divisor changes, so *almost every key* computes a
different answer. For a cache that means a near-total miss storm; for a database
it means moving nearly all your data.

```python
KEYS = [f"user:{i}" for i in range(20_000)]


def stable_hash(text):
    return int(hashlib.md5(text.encode()).hexdigest(), 16)


def modulo_placement(key, servers):
    return stable_hash(key) % servers


before = {k: modulo_placement(k, 4) for k in KEYS}
after = {k: modulo_placement(k, 5) for k in KEYS}
moved = sum(1 for k in KEYS if before[k] != after[k])

print(f"adding a 5th server moved {moved:,} of {len(KEYS):,} keys "
      f"({moved / len(KEYS):.0%})")
assert moved / len(KEYS) > 0.75, "adding one server rehomed most of the data"
print("Ideally we would move 1/5 of them. We moved four times that.")
```

---

## 2. The wheel

Put both servers and keys on the rim of a wheel, using the same hash function to
decide where each lands. A key belongs to the **first server clockwise** from its
position.

Now remove a server: only the keys in the arc between it and its
counter-clockwise neighbour move, and they move to the next server round. Every
other key is untouched, because nothing about its own position changed.

```python
RING = 2 ** 32


class HashRing:
    def __init__(self, servers, vnodes=1):
        self.vnodes = vnodes
        self.ring = {}
        for server in servers:
            self.add(server)

    def add(self, server):
        for v in range(self.vnodes):
            self.ring[stable_hash(f"{server}#{v}") % RING] = server
        self.sorted_points = sorted(self.ring)

    def remove(self, server):
        self.ring = {p: s for p, s in self.ring.items() if s != server}
        self.sorted_points = sorted(self.ring)

    def server_for(self, key):
        point = stable_hash(key) % RING
        index = bisect.bisect_left(self.sorted_points, point)
        if index == len(self.sorted_points):
            index = 0                                # wrapped past 12 o'clock
        return self.ring[self.sorted_points[index]]


ring = HashRing(["s1", "s2", "s3", "s4"])
print("user:1 lives on", ring.server_for("user:1"))
assert ring.server_for("user:1") == ring.server_for("user:1"), "placement is stable"
```

---

## 3. Add a server and count what actually moves

Same experiment as before. This time only the keys in the new server's arc are
affected.

```python
ring_before = {k: ring.server_for(k) for k in KEYS}
ring.add("s5")
ring_after = {k: ring.server_for(k) for k in KEYS}
ring_moved = sum(1 for k in KEYS if ring_before[k] != ring_after[k])

print(f"modulo hashing moved:     {moved / len(KEYS):>6.1%} of keys")
print(f"consistent hashing moved: {ring_moved / len(KEYS):>6.1%} of keys")
assert ring_moved < moved / 3, "an order of magnitude less data movement"
print("Everything that did move went to the new server. Nothing else shifted.")
```

---

## 4. Virtual nodes: the fix for the lumpy wheel

With one point per server the arcs come out uneven - it is a hash, not a ruler.
One server can easily own three times the arc of another, and therefore three
times the data.

The fix is to give each server *many* points on the rim under different names.
The law of large numbers does the rest: with 150 virtual nodes each, the arcs
even out. This is also how you give a bigger machine a bigger share - give it
more points.

```python
def spread(vnodes):
    test_ring = HashRing(["s1", "s2", "s3", "s4"], vnodes=vnodes)
    counts = dict.fromkeys(["s1", "s2", "s3", "s4"], 0)
    for key in KEYS:
        counts[test_ring.server_for(key)] += 1
    return counts


one_point = spread(1)
many_points = spread(150)
imbalance_1 = max(one_point.values()) / min(one_point.values())
imbalance_150 = max(many_points.values()) / min(many_points.values())

print("1 point per server:  ", one_point, f"-> {imbalance_1:.2f}x imbalance")
print("150 points per server:", many_points, f"-> {imbalance_150:.2f}x imbalance")
assert imbalance_150 < imbalance_1, "virtual nodes smooth the arcs out"
assert imbalance_150 < 1.25, "close enough to even for production"
```

---

## 5. Predict before you run

You have 4 cache servers and 1,000,000 keys placed with `hash(key) % 4`. You
add a fifth server. What fraction of keys now live on a different machine -
a fifth of them, or almost all of them?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

This is the mechanism behind Cassandra's ring, DynamoDB's partitioning,
Memcached client libraries and every CDN's origin selection. The interview
question is 'what happens when a node joins', and the modulo answer is what
separates a candidate who has thought about it from one who has not.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
