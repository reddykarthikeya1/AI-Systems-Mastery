# 🐣 Interactive Foundations Playground: Backtracking & Constraint Satisfaction

> *"Backtracking is walking a maze: drop breadcrumbs forward, and rewind your steps whenever you hit a dead end."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import copy
```

---

## 1. Subsets Generation via Include / Exclude Decisions

At each element, binary branching creates a decision tree: branch 1 includes the item; branch 2 excludes it, generating all $2^N$ subsets.

```python
def subsets(nums):
    res = []
    def backtrack(idx, path):
        if idx == len(nums):
            res.append(path[:])
            return
        # Choice 1: Exclude
        backtrack(idx + 1, path)
        # Choice 2: Include
        path.append(nums[idx])
        backtrack(idx + 1, path)
        path.pop()  # Backtrack undo
    backtrack(0, [])
    return res

all_subsets = subsets([1, 2, 3])
assert len(all_subsets) == 8, "2^3 = 8 subsets"
assert [] in all_subsets and [1, 2, 3] in all_subsets
print(f"Generated {len(all_subsets)} subsets of [1, 2, 3]")
```

---

## 2. Permutations via Swapping and Backtracking

Generating all $N!$ permutations by placing each unused candidate at the current index, recursing, and un-doing the state change.

```python
def permutations(nums):
    res = []
    def backtrack(start):
        if start == len(nums):
            res.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # Backtrack
    backtrack(0)
    return res

perms = permutations([1, 2, 3])
assert len(perms) == 6, "3! = 6 permutations"
assert [1, 2, 3] in perms and [3, 2, 1] in perms
print(f"Generated {len(perms)} permutations of [1, 2, 3]")
```

---

## 3. N-Queens Valid Placement Pruning

Placing queens row-by-row and pruning columns and diagonals ($r - c$ and $r + c$) that already hold a queen.

```python
def solve_n_queens(n):
    cols, diag1, diag2 = set(), set(), set()
    solutions = 0
    def backtrack(r):
        nonlocal solutions
        if r == n:
            solutions += 1
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            backtrack(r + 1)
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
    backtrack(0)
    return solutions

assert solve_n_queens(4) == 2, "4-Queens has exactly 2 valid boards"
assert solve_n_queens(1) == 1
print(f"4-Queens has {solve_n_queens(4)} valid solutions.")
```

---
