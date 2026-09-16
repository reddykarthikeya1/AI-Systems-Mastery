# Beginner Playground - Oracle Architecture - SGA and PGA

> *"The SGA is the office whiteboard everyone reads. The PGA is the notebook on your own desk. Sizing one of them wrong is the most expensive mistake in Oracle tuning."*


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

## 1. Shared memory versus private memory

Oracle splits its memory in two, and the split explains most of its behaviour.

**SGA - System Global Area.** One shared pool for the whole instance. Its biggest
part is the *buffer cache*: copies of data blocks read from disk. Shared, so a
block one session pays to read is free for everybody else.

**PGA - Program Global Area.** Private per session. Sorting, hashing, temporary
working space. Not shared, because your half-finished sort is no use to anyone.

A disk read is roughly 100,000 times slower than a memory read. The buffer cache
is the difference between those two numbers.

```python
disk_reads = {"count": 0}
buffer_cache = {}


def read_block(block_id):
    if block_id in buffer_cache:
        return buffer_cache[block_id], "cache hit"
    disk_reads["count"] += 1
    buffer_cache[block_id] = f"data for block {block_id}"
    return buffer_cache[block_id], "DISK READ"


print("session A asks for block 42:", read_block(42)[1])
print("session B asks for block 42:", read_block(42)[1])
print("session C asks for block 42:", read_block(42)[1])
assert disk_reads["count"] == 1, "one disk read served three sessions"
```

---

## 2. Hit ratio, and why it can lie to you

Divide cache hits by total requests and you get the *buffer cache hit ratio*. It
is the first number people quote and the one most likely to mislead: a query
scanning the same useless table over and over posts a magnificent 99% hit ratio
while doing no useful work at all.

Use it to notice a change, never as a goal in itself.

```python
for block in [42, 43, 42, 44, 42, 43, 45, 42]:
    read_block(block)

total_requests = 3 + 8
hits = total_requests - disk_reads["count"]
ratio = hits / total_requests
print(f"requests: {total_requests}, disk reads: {disk_reads['count']}, "
      f"hit ratio: {ratio:.0%}")
assert disk_reads["count"] == 4, "blocks 42, 43, 44, 45 were each read once"
assert ratio > 0.6
```

---

## 3. The PGA is private, and that is the point

Two sessions each sorting a million rows need two sort areas. Nothing is shared,
because there is nothing worth sharing.

Size the work area too small and Oracle *spills* the sort to temporary disk. The
query still returns the right answer, just far slower - which is exactly the kind
of failure that never shows up in testing with small data.

```python
def sort_in_session(rows, work_area_rows):
    if len(rows) <= work_area_rows:
        return sorted(rows), "in memory"
    chunk = work_area_rows
    runs = [sorted(rows[i:i + chunk]) for i in range(0, len(rows), chunk)]
    merged = sorted(r for run in runs for r in run)
    return merged, f"spilled to disk in {len(runs)} passes"


data = [(i * 37) % 1000 for i in range(1000)]
small_result, small_note = sort_in_session(data, work_area_rows=100)
big_result, big_note = sort_in_session(data, work_area_rows=5000)

print("work area 100 rows :", small_note)
print("work area 5000 rows:", big_note)
assert small_result == big_result, "same answer either way - only the cost differs"
assert "spilled" in small_note and big_note == "in memory"
print("Correct but slow is the hardest kind of problem to notice.")
```

---

## 4. Predict before you run

Two sessions ask for the same block of data. The first read costs a trip to
disk. What does the second one cost - and does your answer change if the two
sessions belong to completely different applications?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

"Add more RAM" is the most common and least useful Oracle advice. Which pool
the RAM goes to decides whether you speed up every session at once or one
session at a time.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
