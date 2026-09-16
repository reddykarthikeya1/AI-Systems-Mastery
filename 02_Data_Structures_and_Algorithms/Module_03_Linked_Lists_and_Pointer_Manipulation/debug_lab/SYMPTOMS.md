# Debug Lab 03 — Symptoms

> A linked-list utility module: reversal, cycle detection, midpoint, and merging.
Pointer bugs here do not usually crash — they quietly drop or duplicate nodes.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_list_surgery.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — Reversal returns a one-element list

```
[1] -> 1   (expected 1)
```

**Questions to answer:**

- Every multi-element case returned a single value. Which one, and where was it in the original list?
- Trace `reverse_list` on `[1, 2]` by hand, one statement at a time. What is `cur.next` immediately after the first assignment?
- The loop reads `cur = cur.next` at the end. Has `cur.next` still got the value it had at the top of the loop?

## Symptom 2 — Cycle detection never detects a cycle

```
[2] Cycle detection
      [3, 2, 0, -4] cycle_at=1   -> True   (expected True)
      [1, 2] cycle_at=0   -> True   (expected True)
```

**Questions to answer:**

- Every case reported False, including the ones with a cycle. Is the function ever returning True?
- How far does `slow` advance per iteration? How far does `fast` advance?
- If both pointers move at the same speed, can the gap between them ever change? What has to be true for two runners on a circular track to meet?

## Symptom 3 — The middle of an even-length list is off by one

```
[3] Middle node
      [1, 2, 3, 4, 5] -> 3   (expected 3)
      [1, 2, 3, 4, 5, 6] -> 3   (expected 4)
      [1, 2] -> 1   (expected 2)
```

**Questions to answer:**

- Which rows disagree with the expected value — the odd-length ones, the even-length ones, or both?
- The problem asks for the SECOND of the two middle nodes when the length is even. Which one is being returned?
- Compare the loop condition with `while fast and fast.next`. Which additional term does this version test, and what does that extra condition stop the loop one step early on?

## Symptom 4 — Merging drops the tail of the longer list

```
[4] Merging two sorted lists
      [1, 2, 4] + [1, 3, 4] -> [1, 1, 2, 3, 4]   (expected [1, 1, 2, 3, 4, 4])
      [1, 2, 3] + [4, 5] -> [1, 2, 3]   (expected [1, 2, 3, 4, 5])
      [] + [1, 2] -> []   (expected [1, 2])
```

**Questions to answer:**

- Compare each result with the expected list. What is missing, and where was it in the input?
- The `while` loop ends as soon as one list is exhausted. What is still sitting in the other one at that moment?
- Count the nodes in the output versus the two inputs. Where did the difference go?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_reverse_list` |
| 2 | `test_p02_has_cycle` |
| 3 | `test_p04_middle_node` |
| 4 | `test_p05_merge_sorted` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
