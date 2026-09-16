# Troubleshooting - Module 16

## The empty pattern

`naive_search(text, "")` in this engine returns every offset including
`len(text)`. That is a convention, not a law - other libraries return `[]`. The
tests pin the convention down; pick one and document it, because the silent
disagreement between two functions in the same codebase is the real bug.

`AhoCorasick.add("")` raises. An empty pattern matches at every position, which
makes every output set infinite and every search useless.

## My prefix table has `pi[i] == i + 1` somewhere

You have allowed the whole string to count as a prefix of itself. `pi` measures
*proper* prefixes, so `pi[i] <= i` always. Check the `while k > 0` guard.

## KMP finds half the matches I expect

You reset `k = 0` after a match instead of `k = pi[k - 1]`. See debug lab
defect 1.

## KMP hangs

Your fallback is `k = pi[k]` rather than `k = pi[k - 1]`. Since `pi[k]` can equal
`k`, the loop never shrinks.

## Rabin-Karp reports matches that are not there

You are not verifying candidates. Debug lab defect 2.

## Rabin-Karp gives different results on different runs

You used Python's built-in `hash()`. It is randomised per process for `str` by
default, so anything relying on its value across runs is unreproducible. Use an
explicit polynomial hash.

## Negative hash values

Python's `%` returns a non-negative result for a positive modulus, so this
should not happen - but if you port the code to C or Java it will, because their
`%` keeps the sign of the dividend. Add the modulus and take `%` again.

## Aho-Corasick misses short words inside long ones

Output sets are not merged along failure links. Debug lab defect 3.

## Aho-Corasick loops forever on build

A node's failure link points at itself. The guard is the
`if self.fail[child] == child` check; without it, a single-character pattern can
create the cycle.

## Unicode

Everything here works on any sequence of comparable items, including emoji and
combining characters - but `len()` counts code points, not what a reader would
call a character. `"e\u0301"` is length 2. If you are matching user-visible
text, normalise first (`unicodedata.normalize("NFC", s)`).
