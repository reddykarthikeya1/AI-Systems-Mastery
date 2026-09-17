# 🐣 Interactive Foundations Playground: Dynamic Arrays & Amortized Doubling

> *"A dynamic array is a hotel that doubles its capacity every time the last room is booked."*

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
import sys
```

---

## 1. Geometric Growth and Total Element Copies

When appending $N$ items with geometric factor 2, copies happen at sizes 1, 2, 4, 8, ... summing to at most $2N$. Thus, average per-append cost is strictly bounded by $O(1)$ amortized time.

```python
def simulate_growth(n):
    capacity = 1
    total_copies = 0
    for i in range(1, n + 1):
        if i > capacity:
            total_copies += (i - 1)
            capacity *= 2
    return total_copies, capacity

copies, cap = simulate_growth(1000)
assert cap == 1024, "Smallest power of 2 >= 1000"
assert copies < 2 * 1000, "Amortized doubling copies must be < 2N"
print(f"Appended 1000 items: final capacity={cap}, total copies={copies}")
```

---

## 2. Two-Pointer In-Place Array Reversal

Two pointers starting at opposite ends swap values and advance toward each other, reversing the array in $O(N)$ time with $O(1)$ auxiliary memory.

```python
arr = [1, 2, 3, 4, 5]
left, right = 0, len(arr) - 1
while left < right:
    arr[left], arr[right] = arr[right], arr[left]
    left += 1
    right -= 1

assert arr == [5, 4, 3, 2, 1]
assert arr[0] == 5 and arr[-1] == 1
print(f"Reversed array in-place: {arr}")
```

---

## 3. Prefix Sums for O(1) Range Queries

Precomputing prefix sums $P[i] = \sum_{j=0}^{i-1} A[j]$ turns any arbitrary range query $\sum_{j=L}^{R} A[j]$ into a single subtraction $P[R+1] - P[L]$.

```python
data = [2, 4, 6, 8, 10]
prefix = [0] * (len(data) + 1)
for i, x in enumerate(data):
    prefix[i + 1] = prefix[i] + x

def query(l, r):
    return prefix[r + 1] - prefix[l]

assert query(1, 3) == 18, "4 + 6 + 8 = 18"
assert query(0, 4) == 30, "Sum of all elements"
print(f"Prefix table: {prefix}, Query(1, 3) = {query(1, 3)}")
```

---
