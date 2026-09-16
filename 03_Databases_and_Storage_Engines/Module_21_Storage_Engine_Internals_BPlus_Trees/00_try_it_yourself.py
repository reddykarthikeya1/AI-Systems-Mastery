"""Beginner playground for Module 21 - Storage Engine Internals - B+ Trees.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import bisect
import math

# --------------------------------------------- 1. Why not just sort the rows?
sorted_keys = list(range(0, 1_000_000, 2))
comparisons = {"linear": 0, "binary": 0}

target = 999_998
for key in sorted_keys:
    comparisons["linear"] += 1
    if key == target:
        break

low, high = 0, len(sorted_keys)
while low < high:
    comparisons["binary"] += 1
    mid = (low + high) // 2
    if sorted_keys[mid] < target:
        low = mid + 1
    else:
        high = mid

print(f"linear scan: {comparisons['linear']:,} comparisons")
print(f"binary search: {comparisons['binary']:,} comparisons")
assert sorted_keys[bisect.bisect_left(sorted_keys, target)] == target
assert comparisons["binary"] < 25, "halving 500,000 items takes about 19 steps"


# --------------------------------------- 2. The drawer, the section, the card
def tree_height(rows, keys_per_page):
    return math.ceil(math.log(rows, keys_per_page))


print(f"{'rows':>15} | {'binary (fanout 2)':>18} | {'B+ tree (fanout 400)':>20}")
for rows in (1_000, 1_000_000, 1_000_000_000):
    print(f"{rows:>15,} | {tree_height(rows, 2):>18} | {tree_height(rows, 400):>20}")

assert tree_height(1_000_000, 400) == 3, "a million rows, three page reads"
assert tree_height(1_000_000_000, 400) == 4, "a BILLION rows, four"
print()
print("Multiply the table by 1,000 and pay one extra read. That is the whole point.")


# -------------------------------------- 3. Why the leaves are linked together
leaves = [list(range(i, i + 4)) for i in range(0, 20, 4)]
leaf_reads = {"count": 0}


def range_scan(start, end):
    found = []
    for leaf_index, leaf in enumerate(leaves):
        if leaf[-1] < start:
            continue
        leaf_reads["count"] += 1
        found += [k for k in leaf if start <= k <= end]
        if leaf[-1] >= end:
            print(f"  stopped at leaf {leaf_index}; no need to look further")
            break
    return found


result = range_scan(6, 13)
print("keys between 6 and 13:", result)
print("leaf pages read:", leaf_reads["count"], "of", len(leaves))
assert result == list(range(6, 14))
assert leaf_reads["count"] < len(leaves), "sorted leaves mean you can stop early"


# ------------------------------------------ 4. What makes a tree stop helping
table_rows = 1_000_000
for distinct_values, label in ((2, "status"), (1_000_000, "email")):
    rows_matched = table_rows / distinct_values
    selectivity = rows_matched / table_rows
    verdict = "index used" if selectivity < 0.05 else "index IGNORED, full scan"
    print(f"  index on {label:<7}: one value matches {rows_matched:>10,.0f} rows "
          f"-> {verdict}")

phone_book = sorted([("Dublin", "ahern"), ("Cork", "byrne"), ("Dublin", "casey")])
print()
print("index on (city, surname) sorted as:", phone_book)
print("query 'surname = byrne' with no city: nothing to seek to - full scan")
assert phone_book[0][0] == "Cork", "sorted by city FIRST, which is all the index knows"


print()
print("All checks passed.")
