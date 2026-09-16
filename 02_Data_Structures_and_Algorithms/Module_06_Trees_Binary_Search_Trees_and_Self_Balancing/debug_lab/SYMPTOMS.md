# Debug Lab 06 — Symptoms

> A tree-validation service: BST checking, depth, balance and level grouping. It
approves trees for use as search indexes.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_tree_validator.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — A tree that is not a BST is approved

```
[1] -> 2 (expected 1)
      [] -> 1 (expected 0)
      [1, 2] -> 3 (expected 2)
```

**Questions to answer:**

- Compare the `reported` column with `strictly increasing`. Which rows disagree?
- For `[5, 1, 4, None, None, 3, 6]`, node 3 sits in node 5's right subtree. Is 3 greater than 5? Does the function ever compare them?
- Which nodes does `is_valid_bst` compare each node against? Which nodes *constrain* it?

## Symptom 2 — Every depth is one too large

```
[2] Maximum depth
      [3, 9, 20, None, None, 15, 7] -> 4 (expected 3)
```

**Questions to answer:**

- Compare each reported depth with the expected one. Is the error constant?
- What does the function return for an empty tree, and what should the depth of an empty tree be?
- For a single node, how many times does the base case contribute to the total?

## Symptom 3 — An unbalanced tree is reported as balanced

```
[3] Height balance
      [3, 9, 20, None, None, 15, 7] -> True (expected True)
      [1, 2, 2, 3, 3, None, None, 4, 4] -> False (expected False)
      [1, 2, None, 3] -> False (expected False)
      root balanced but left subtree deep -> False (expected False)
```

**Questions to answer:**

- Which rows disagree with the expected column? Look at the last one in particular.
- The definition requires the balance condition to hold at EVERY node. At how many nodes does this function check it?
- The `height` helper is correct. What is the caller failing to do with it?

## Symptom 4 — Level order returns one node per level

```
[4] Level order grouping
      [3, 9, 20, None, None, 15, 7]
          reported [[3], [9], [20], [15], [7]]
          expected [[3], [9, 20], [15, 7]]
      [1, 2, 3, 4, 5, 6, 7]
          reported [[1], [2], [3], [4], [5], [6], [7]]
          expected [[1], [2, 3], [4, 5, 6, 7]]

====================================================================
Validation complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Compare the reported and expected structures. How many groups are there, and how many nodes are in each?
- The BFS visits the nodes in the right order. What is wrong with how they are grouped?
- What has to be measured at the top of each outer iteration to know where one level ends and the next begins?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p04_is_valid_bst` |
| 2 | `test_p03_max_depth` |
| 3 | `test_p07_is_balanced` |
| 4 | `test_p02_level_order` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
