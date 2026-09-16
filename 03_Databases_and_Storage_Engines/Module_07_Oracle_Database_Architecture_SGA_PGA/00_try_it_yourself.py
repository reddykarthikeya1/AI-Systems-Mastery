"""Beginner playground for Module 07 - Oracle Architecture - SGA and PGA.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------------------------- 1. Shared memory versus private memory
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


# ------------------------------------ 2. Hit ratio, and why it can lie to you
for block in [42, 43, 42, 44, 42, 43, 45, 42]:
    read_block(block)

total_requests = 3 + 8
hits = total_requests - disk_reads["count"]
ratio = hits / total_requests
print(f"requests: {total_requests}, disk reads: {disk_reads['count']}, "
      f"hit ratio: {ratio:.0%}")
assert disk_reads["count"] == 4, "blocks 42, 43, 44, 45 were each read once"
assert ratio > 0.6


# ------------------------------- 3. The PGA is private, and that is the point
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


print()
print("All checks passed.")
