# Debug Lab 16 - Answers

Read only after writing your own diagnosis for all three.

---

## Defect 1 - resuming from zero after a match

**Where:** `kmp_search`, the line after a full match is recorded.

```python
if k == len(pattern):
    found.append(i - len(pattern) + 1)
    k = 0                     # <-- throws away everything already matched
```

**Why it produces that output.** Setting `k = 0` says "start the pattern again
from nothing". For `AA` in `AAAAAAAA` that means after matching at offset 0 the
search will not consider offset 1 at all, because the `A` at index 1 has been
consumed as part of the previous match and forgotten. You get every *other*
offset: 0, 2, 4, 6 - four hits instead of seven.

**The fix.** After a match, fall back the same way you do after a mismatch:

```python
k = pi[k - 1]
```

That keeps the longest prefix of the pattern that is still alive as a suffix of
what you just read, which for `AA` is one character - so offset 1 is found.

**The general lesson.** Overlapping matches are the default in KMP, not a
special case. If your matcher cannot find `aa` twice in `aaa`, it is this line.
Whether you *want* overlaps is a product decision, but it should be a decision,
not an accident.

---

## Defect 2 - trusting the hash

**Where:** `rolling_search`, inside the loop.

```python
if window == target:
    found.append(start)       # <-- no verification
```

**Why it produces that output.** A hash is a lossy summary. With `mod = 101`
there are only 101 possible hash values, so different three-character strings
collide constantly. Equal hashes mean "these might be equal"; the algorithm
treats it as "these are equal".

Every real occurrence is still found - a true match always hashes equal, so
there are no false negatives. The error is one-sided, which is exactly why it
survives casual testing: the output looks like a superset, not like garbage.

**The fix.** Verify the candidate:

```python
if window == target and text[start:start + m] == pattern:
    found.append(start)
```

The slice comparison is O(m), but it only runs on candidates, so the expected
cost stays O(n + m).

**The general lesson.** This is the entire reason Rabin-Karp is described as
"expected" linear rather than "worst-case" linear. And note what makes it
dangerous in production: with a 61-bit modulus a collision is rare rather than
impossible, so the bug fires once a quarter on one input nobody can reproduce.
Rare is worse than frequent.

---

## Defect 3 - failure links built, output sets not merged

**Where:** `Screen.build`. The failure links are computed correctly, but the
line that propagates output along them is absent.

```python
self.fail[child] = self.goto[fallback].get(character, 0)
if self.fail[child] == child:
    self.fail[child] = 0
queue.append(child)           # <-- missing: inherit the failure node's output
```

**Why it produces that output.** A node reports only the word that ends exactly
there. When the automaton reaches the node for `she`, the text it has consumed
also ends with `he` - but `he` lives at a different node, reachable only by
following the failure link. Without inheriting that node's output, the shorter
term is never reported.

So the filter finds any term that ends at a node it actually visits, and misses
any term that is a proper suffix of one. `she` and `hers` are found; the `he`
inside them is not.

**The fix.** One line, in the same loop:

```python
self.output[child] += self.output[self.fail[child]]
```

Because the loop is breadth-first, `self.fail[child]` has already been processed
and already carries its own inherited outputs, so a single assignment
transitively collects the whole chain.

**The general lesson.** This is the defect with real consequences. A content
filter that misses terms nested inside other terms is trivially bypassed by
padding, and it will pass every test written with non-overlapping examples.
Test a multi-pattern matcher with a dictionary where one word is a suffix of
another - `he`/`she`, `is`/`his` - or you are not testing the mechanism that
makes it an automaton rather than a trie.
