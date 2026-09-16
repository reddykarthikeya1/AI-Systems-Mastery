# Beginner Playground - Storage Engine Internals - B+ Trees

> *"A library card catalog. You do not read the shelves - you open the A-D drawer, then the AB-AC section, then the card. Three steps, out of a million books."*

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
import math
```

---

## 1. Why not just sort the rows?

Sorted data with binary search is already good: halve the search space each step,
20 steps for a million rows.

The problem is *keeping* it sorted. Inserting a row in the middle of a sorted file
means shifting everything after it. A B+ tree gets the same search behaviour while
letting inserts happen in place.

```python
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
```

---

## 2. The drawer, the section, the card

A B+ tree is that binary search made *wide*. Each node is one disk page holding
hundreds of keys, so one read narrows the search by a factor of hundreds rather
than two.

The catalog analogy is exact:

| Catalog | B+ tree | Cost |
| :--- | :--- | :--- |
| Pick the A-D drawer | root node | 1 read |
| Find the AB-AC divider | internal node | 1 read |
| Read the card | leaf node | 1 read |

Three reads. The card tells you the shelf; it is not the book itself. In a B+
tree, all the actual data lives in the leaves - internal nodes are signposts only.

```python
def tree_height(rows, keys_per_page):
    return math.ceil(math.log(rows, keys_per_page))


print(f"{'rows':>15} | {'binary (fanout 2)':>18} | {'B+ tree (fanout 400)':>20}")
for rows in (1_000, 1_000_000, 1_000_000_000):
    print(f"{rows:>15,} | {tree_height(rows, 2):>18} | {tree_height(rows, 400):>20}")

assert tree_height(1_000_000, 400) == 3, "a million rows, three page reads"
assert tree_height(1_000_000_000, 400) == 4, "a BILLION rows, four"
print()
print("Multiply the table by 1,000 and pay one extra read. That is the whole point.")
```

---

## 3. Why the leaves are linked together

The `+` in B+ tree means the leaves form a linked list. Once you have found the
first matching card, a range scan walks sideways along the leaves instead of
climbing back up the tree for each row.

That is why `WHERE date BETWEEN ... AND ...` and `ORDER BY indexed_column` are
both fast: the index already holds the rows in order.

```python
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
```

---

## 4. What makes a tree stop helping

Two things degrade a real index, and both are worth recognising:

1. **Low selectivity.** An index on a `status` column with two values points at
   half the table. The database will ignore it and scan, correctly - following a
   million index entries back to a million rows is slower than reading the table.
2. **Wrong leading column.** An index on `(city, surname)` cannot answer "find by
   surname" any more than a phone book sorted by city can. Leftmost prefix first.

```python
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
```

---

## 5. Predict before you run

A million rows, and a lookup takes 3 disk reads. Grow the table to a
*billion* rows. How many disk reads does the same lookup take - 3,000? 300? Or
something that will surprise you?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Every PostgreSQL, MySQL and Oracle index you will ever create is a B+ tree.
When someone says an index makes lookups "logarithmic", this drawer-within-a-drawer
structure is the thing they are describing.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
