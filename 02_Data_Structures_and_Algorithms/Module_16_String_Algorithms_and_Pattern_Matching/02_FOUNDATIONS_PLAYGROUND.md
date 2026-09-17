# 🐣 Interactive Foundations Playground: String Algorithms & Pattern Matching

> *"KMP is reading a book and never reading the same letter twice when searching for a phrase."*

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
import math
```

---

## 1. KMP Prefix Function (Pi Array)

The prefix table $\pi[i]$ stores the length of the longest proper prefix that is also a suffix of `pattern[0..i]`, preventing backward backtracking.

```python
def compute_pi(pattern: str) -> list[int]:
    pi = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi

pi_table = compute_pi("aabaabaaa")
assert pi_table[0] == 0
assert pi_table[1] == 1, "'aa' prefix 'a'"
assert pi_table[4] == 2, "'aabaa' prefix 'aa'"
print(f"KMP Pi table for 'aabaabaaa': {pi_table}")
```

---

## 2. KMP Linear-Time Substring Search

When a mismatch occurs, instead of restarting at text index $i+1$, KMP shifts the pattern according to the precomputed $\pi$ table in $O(N + M)$ total time.

```python
def kmp_search(text: str, pattern: str) -> list[int]:
    pi = compute_pi(pattern)
    matches = []
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - j + 1)
            j = pi[j - 1]
    return matches

hits = kmp_search("sadbutsad", "sad")
assert hits == [0, 6]
assert kmp_search("leetcode", "leeto") == []
print(f"KMP matches found at indices: {hits}")
```

---

## 3. Rabin-Karp Rolling Hash Matching

Updating a polynomial rolling hash as a sliding window shifts takes $O(1)$ time, checking equality only on hash collisions.

```python
def rolling_hash(s, base=256, mod=1000000007):
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % mod
    return h

h1 = rolling_hash("apple")
h2 = rolling_hash("apple")
h3 = rolling_hash("apply")
assert h1 == h2
assert h1 != h3
print(f"Rolling hash values: 'apple'={h1}, 'apply'={h3}")
```

---
