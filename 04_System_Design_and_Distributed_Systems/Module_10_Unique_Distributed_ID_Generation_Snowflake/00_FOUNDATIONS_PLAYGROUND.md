# Beginner Playground - Distributed Unique ID Generation (Snowflake)

> *"A cloakroom ticket that has the time printed on it and the desk number stamped on it. No two desks can print the same ticket, and the tickets come out in order."*


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
import time
```

---

## 1. Three ways to make an id, and what each one costs

| Approach | Unique? | Ordered? | Needs coordination? |
| :--- | :--- | :--- | :--- |
| Database auto-increment | yes | yes | **yes** - one machine hands them all out |
| Random UUID v4 | yes | **no** | no |
| Snowflake | yes | yes | no, after a one-off machine id |

Ordering is not a nicety. An id that sorts by time means "newest 20 posts" is a
range scan on the primary key, and it means new rows are appended at the end of
the index rather than scattered through it - which is the difference between a
tidy B-tree and a badly fragmented one.

```python
uuid_like = ["c9f0", "1a2b", "7e4d", "03ff"]
print("random ids in creation order:", uuid_like)
print("the same ids sorted:         ", sorted(uuid_like))
assert sorted(uuid_like) != uuid_like, "sort order tells you nothing about time"
```

---

## 2. Sixty-four bits, divided up

A Snowflake id is one 64-bit integer split into fields:

| Bits | Field | Buys you |
| ---: | :--- | :--- |
| 1 | unused | keeps the number positive |
| 41 | milliseconds since a custom epoch | ~69 years of ids |
| 10 | machine id | 1,024 generators |
| 12 | sequence within the millisecond | 4,096 ids per machine per ms |

41 bits of time at the top is what makes the ids sort chronologically: compare
two ids as plain integers and you are comparing their timestamps first.

```python
EPOCH_MS = 1_700_000_000_000
MACHINE_BITS, SEQUENCE_BITS = 10, 12
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1


class Snowflake:
    def __init__(self, machine_id):
        assert 0 <= machine_id < (1 << MACHINE_BITS)
        self.machine_id = machine_id
        self.last_ms = -1
        self.sequence = 0

    def next_id(self, now_ms):
        if now_ms < self.last_ms:
            raise RuntimeError("clock moved backwards; refusing to issue an id")
        if now_ms == self.last_ms:
            self.sequence += 1
            if self.sequence > MAX_SEQUENCE:
                raise RuntimeError("4096 ids in one millisecond; wait for the next")
        else:
            self.sequence = 0
        self.last_ms = now_ms
        return (((now_ms - EPOCH_MS) << (MACHINE_BITS + SEQUENCE_BITS))
                | (self.machine_id << SEQUENCE_BITS)
                | self.sequence)


generator = Snowflake(machine_id=7)
ids = [generator.next_id(now_ms=EPOCH_MS + 1_000) for _ in range(3)]
print("three ids from one machine in one millisecond:", ids)
assert ids == sorted(ids), "the sequence field keeps them ordered within the ms"
assert len(set(ids)) == 3
```

---

## 3. Two machines, no conversation between them

The whole point: two generators that have never communicated cannot collide,
because the machine id occupies its own bits.

No lock, no shared counter, no round trip. Just arithmetic.

```python
machine_a = Snowflake(machine_id=1)
machine_b = Snowflake(machine_id=2)
same_instant = EPOCH_MS + 5_000

batch_a = {machine_a.next_id(same_instant) for _ in range(1_000)}
batch_b = {machine_b.next_id(same_instant) for _ in range(1_000)}

print(f"machine 1 issued {len(batch_a):,} ids, machine 2 issued {len(batch_b):,}")
print("overlap:", len(batch_a & batch_b))
assert batch_a & batch_b == set(), "collision is impossible, not merely unlikely"
assert len(batch_a | batch_b) == 2_000
```

---

## 4. Unpacking an id, and the failure you must handle

Because the layout is fixed, any id can be taken apart again - you can read the
creation time straight out of a primary key with no extra column.

The failure mode worth knowing: **the clock going backwards**, from an NTP
correction or a VM migration. Reusing a millisecond you have already issued ids
for means issuing duplicate ids. The only safe response is to refuse until the
clock catches up, which is exactly what real implementations do.

```python
def unpack(snowflake_id):
    sequence = snowflake_id & MAX_SEQUENCE
    machine = (snowflake_id >> SEQUENCE_BITS) & ((1 << MACHINE_BITS) - 1)
    timestamp = (snowflake_id >> (MACHINE_BITS + SEQUENCE_BITS)) + EPOCH_MS
    return timestamp, machine, sequence


sample = Snowflake(machine_id=42).next_id(EPOCH_MS + 9_876)
timestamp, machine, sequence = unpack(sample)
print(f"id {sample} -> t+{timestamp - EPOCH_MS} ms, machine {machine}, seq {sequence}")
assert (machine, sequence) == (42, 0)
assert timestamp == EPOCH_MS + 9_876

clock_skewed = Snowflake(machine_id=3)
clock_skewed.next_id(EPOCH_MS + 10_000)
try:
    clock_skewed.next_id(EPOCH_MS + 9_000)      # NTP stepped the clock back
    raise AssertionError("it should have refused")
except RuntimeError as exc:
    print("clock went backwards ->", exc)

print("Refusing to issue is correct. Issuing a duplicate id is unrecoverable.")
print("(time.time() is available here too:", int(time.time()) > 0, ")")
```

---

## 5. Predict before you run

Why not just use a random UUID? It is unique, it needs no coordination, and
every language has one built in. Name the thing it costs you that an ordered
id gives you for free.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Twitter built Snowflake because auto-increment needs one database to hand out
every id, and that database is a bottleneck and a single point of failure.
Discord, Instagram and Sony all ship variations of the same 64 bits.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
