# Debug Lab 03 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — Reversal returns a one-element list

**Location:** `reverse_list`, the loop body

**The bug:**

```python
while cur is not None:
    cur.next = prev         # destroys the link to the rest of the list
    prev = cur
    cur = cur.next          # ...so this now reads the link we just overwrote
```

**The fix:**

```python
while cur is not None:
    nxt = cur.next          # save it BEFORE overwriting
    cur.next = prev
    prev = cur
    cur = nxt
```

**Why it matters.** `cur.next = prev` overwrites the only pointer to the remainder of the list. The
very next statement then reads that same field, so `cur` walks backwards into
`prev` instead of forwards, the loop ends after one step, and everything past the
head is unreachable.

Nothing raises. A one-element list comes back, which is a structurally valid
linked list — so a caller that checks "did I get a list?" sees nothing wrong.
Only comparing the contents reveals that the data is gone.

Three pointers, and the save comes first. That ordering is the whole technique.

**Proved by:** `test_p01_reverse_list`

## Defect 2 — Cycle detection never detects a cycle

**Location:** `has_cycle`, the advance of `fast`

**The bug:**

```python
slow = slow.next
fast = fast.next            # same speed as slow - the gap never closes
```

**The fix:**

```python
slow = slow.next
fast = fast.next.next       # twice the speed, so the gap shrinks by one per step
```

**Why it matters.** Floyd's algorithm works because the two pointers move at *different* speeds: the
gap between them shrinks by one node per iteration, so inside a cycle they must
eventually coincide. Moving both by one keeps the gap constant forever, and they
never meet.

The function then falls out of its loop and reports False. On an acyclic list
that is the right answer, which is why half the test cases still look correct —
and on a cyclic list it is wrong, silently.

Note the iteration cap in this code: without it the same bug would hang instead
of lying. A guard that turns an infinite loop into a wrong answer is not a fix,
and is worth recognising as a smell in its own right.

**Proved by:** `test_p02_has_cycle`

## Defect 3 — The middle of an even-length list is off by one

**Location:** `middle_node`, the loop condition

**The bug:**

```python
while fast is not None and fast.next is not None and fast.next.next is not None:
    slow = slow.next
    fast = fast.next.next   # stops one step early on even lengths
```

**The fix:**

```python
while fast is not None and fast.next is not None:
    slow = slow.next
    fast = fast.next.next
```

**Why it matters.** The extra `fast.next.next is not None` term makes the loop exit one iteration
sooner whenever the length is even, so `slow` lands on the *first* middle node
rather than the second.

Odd-length lists are unaffected, which is exactly why this survives casual
testing: the examples people reach for first are usually odd.

Off-by-one in a loop condition is the most common linked-list bug there is, and
the reliable defence is to state which element you want for both parities and
then test both.

**Proved by:** `test_p04_middle_node`

## Defect 4 — Merging drops the tail of the longer list

**Location:** `merge_sorted`, after the loop

**The bug:**

```python
tail = tail.next
return dummy.next           # whatever remains in a or b is never attached
```

**The fix:**

```python
tail = tail.next
# At most one list still has nodes; splice the whole remainder on.
tail.next = a if a is not None else b
return dummy.next
```

**Why it matters.** The loop is correct while both lists have nodes, and stops the moment either
runs out. At that point the other list still holds every remaining node, and
they are simply never linked in.

The output is sorted and non-empty, so it passes an "is this sorted?" check
perfectly. It is merely incomplete — and how incomplete depends on how unbalanced
the inputs are, so the size of the loss varies with the data.

The tail splice is a single line, and it is the line people forget. A count
assertion — output length equals the sum of the input lengths — catches it every
time.

**Proved by:** `test_p05_merge_sorted`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | Reversal returns a one-element list | No |
| 2 | Cycle detection never detects a cycle | No |
| 3 | The middle of an even-length list is off by one | No |
| 4 | Merging drops the tail of the longer list | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
