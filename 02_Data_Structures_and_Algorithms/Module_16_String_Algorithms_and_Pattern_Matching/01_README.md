# Module 16: String Algorithms and Pattern Matching

> **Brand new to this topic?** Start with
> [`02_W3_BEGINNER_PLAYGROUND.md`](02_W3_BEGINNER_PLAYGROUND.md) - the same ideas
> in plain language with runnable code.

Every algorithm in this module beats the same baseline: the naive scan, which
tries the pattern at every offset and costs `O(n*m)`. Each one beats it by
noticing something the naive scan throws away.

| Algorithm | Cost | What it exploits |
| :--- | :--- | :--- |
| Naive | `O(n*m)` | nothing |
| KMP | `O(n + m)` | the pattern's own self-overlap |
| Z-algorithm | `O(n + m)` | the same, arranged as a prefix array |
| Rabin-Karp | `O(n + m)` expected | a hash you can update in `O(1)` per shift |
| Aho-Corasick | `O(n + total + hits)` | many patterns sharing prefixes |

## Learning path

| Step | File | What you do |
| :---: | :--- | :--- |
| 1 | [`02_W3_BEGINNER_PLAYGROUND.md`](02_W3_BEGINNER_PLAYGROUND.md) | Plain-language version, runnable |
| 2 | This README | The mechanisms and when each applies |
| 3 | [`03_try_it_yourself.py`](03_try_it_yourself.py) | Watch the prefix table being built |
| 4 | [`starter/`](starter) | Implement the engine yourself |
| 5 | [`problems/`](problems) | Six problems, stubs and reference solutions |
| 6 | [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md) | Diagnose three planted defects |
| 7 | [`04_PROJECT_GUIDE.md`](04_PROJECT_GUIDE.md) | Build the whole engine |

---

## 1. Why the naive scan is wasteful

Search for `aaaab` in `aaaaaaaaab`. At offset 0 you compare four `a`s and fail on
the `b`. The naive scan then restarts at offset 1 and compares four `a`s again -
characters it has already read and already knows about.

That repeated reading is the entire inefficiency, and it becomes quadratic
exactly when the pattern overlaps itself. On random English text the naive scan
is fine; on repetitive data - DNA, logs, binary formats - it collapses.

## 2. KMP: the prefix function

`pi[i]` is the length of the longest proper prefix of `pattern[:i+1]` that is
also a suffix of it.

For `ababaca`:

```
index :  0  1  2  3  4  5  6
char  :  a  b  a  b  a  c  a
pi    :  0  0  1  2  3  0  1
```

At index 4 the value is 3, because `aba` is both a prefix and a suffix of
`ababa`. So if a match fails after five characters, you do not restart - three
characters are still legitimately matched, and you resume from there.

The consequence is a guarantee: **the text pointer never moves backwards**.
Every character of the text is read once. The inner `while` loop only walks the
*pattern* back, and since `pi[k-1] < k` strictly, the total number of those steps
across the whole scan is bounded by `n`.

### The trap

After a *successful* match, you must also fall back to `pi[k-1]` rather than
resetting to 0. Reset to 0 and `aa` is found twice in `aaaa` instead of three
times. Whether you want overlapping matches is a product decision; getting it by
accident is not. This is planted defect 1 in the debug lab.

## 3. Z-algorithm: the same information, differently shaped

`z[i]` is the length of the longest substring starting at `i` that is also a
prefix of the whole string. The implementation maintains a window `[left, right)`
already known to match the prefix, and reuses previously computed answers inside
it rather than rescanning.

Searching with it is a trick: run the Z-function over `pattern + separator +
text` and look for entries equal to `len(pattern)`. The separator must appear in
neither string, or a match can run across the join and report a hit that does not
exist. The implementation raises rather than allowing that silently.

Use Z when you want the prefix-match lengths themselves - string periodicity,
comparing many substrings. Use KMP when you want occurrences.

## 4. Rabin-Karp: hashing a sliding window

Treat the window as a number in base 257 modulo a large prime. Sliding one
character right is `O(1)`: subtract the outgoing character's contribution,
multiply by the base, add the incoming one.

**A hash match is not a match.** Different strings can hash the same, so every
candidate must be verified with a real comparison. Skipping that check is the
classic Rabin-Karp bug, and it is one-sided: you never miss a real occurrence,
you only report extra ones. That is precisely what makes it survive testing -
the output looks like a superset rather than garbage.

`rabin_karp_search_unverified` in the engine keeps the bug deliberately, and a
test demonstrates a concrete false positive rather than asserting collisions are
rare.

Where Rabin-Karp genuinely wins is when hashing is reusable: comparing many
substrings against each other, or **2-D search**, where you hash every row
window and then roll vertically down the resulting grid. `rabin_karp_2d` does
exactly that.

## 5. Aho-Corasick: many patterns in one pass

Build a trie of all the patterns, then add **failure links**: from each node, a
pointer to the longest proper suffix of the current string that is also a node.
That is the KMP prefix function generalised from one pattern to a set.

Cost is `O(total pattern length)` to build and `O(n + hits)` to search,
*regardless of how many patterns there are*. Running KMP once per pattern costs
`O(k*n)`.

### The trap

Output sets must be merged along the failure links. Without that, a node reports
only the word ending exactly there - so `she` is found and the `he` inside it is
missed. A content filter with this bug is bypassed by padding and passes every
test written with non-overlapping examples. This is planted defect 3.

---

## Choosing between them

| Situation | Use |
| :--- | :--- |
| One pattern, exact, worst-case guarantee needed | KMP |
| Many patterns at once | Aho-Corasick |
| Comparing many substrings, or 2-D | Rabin-Karp |
| Periodicity, borders, prefix lengths | Z-algorithm |
| One pattern, ordinary text, no guarantee needed | `str.find` - genuinely |

That last row is not a joke. CPython's `str.find` uses a tuned hybrid and beats
a Python-level KMP on almost all real input. Write KMP because you need to
understand the mechanism and because interviews ask for it - not because
`in` is slow.

---

## You have mastered this when you can

- [ ] Write the prefix function from memory and explain why the text pointer
      never moves backwards.
- [ ] Say what `pi[i] = 3` means about `pattern[:i+1]`, in one sentence.
- [ ] Explain why resetting `k = 0` after a match loses overlapping occurrences.
- [ ] State what a Rabin-Karp hash match proves, and what it does not.
- [ ] Explain why Rabin-Karp is *expected* linear rather than worst-case linear.
- [ ] Draw the failure links for the dictionary `{he, she, his, hers}` and say
      why `he` is found inside `ushers`.
- [ ] Give the cost of Aho-Corasick and say why it does not depend on the number
      of patterns.
- [ ] Recognise "longest prefix that is also a suffix", "is this string a
      repeated block" and "shortest palindrome by prepending" as the same table.
