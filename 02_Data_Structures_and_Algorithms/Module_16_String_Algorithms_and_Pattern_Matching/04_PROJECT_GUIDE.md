# Project Guide - Module 16

Build the string matching engine in [`starter/string_matching_engine.py`](starter/string_matching_engine.py).

```bash
cd starter
python -m pytest ../project_solution -q      # must FAIL until you write the code
```

## Tier 1 - the baseline and the table

1. `naive_search`. Write it first; it is the reference every other function is
   checked against, and the tests compare them directly on random input.
2. `prefix_function`. The one piece everything else needs.
3. `kmp_search`. Watch the fallback after a *successful* match.
4. `smallest_period`. Two lines once you have the table.

At this point 12 or so tests pass.

## Tier 2 - the other two single-pattern methods

5. `z_function` and `z_search`. Reject a separator that occurs in the input.
6. `RollingHash`, then `rabin_karp_search`. Verify every candidate.
7. `rabin_karp_search_unverified`. Keep the bug - a test asserts it produces a
   false positive.

## Tier 3 - two dimensions and many patterns

8. `rabin_karp_2d`. Hash row windows first, then roll down the columns.
9. `AhoCorasick`. Build the trie, then the failure links breadth-first, then
   merge output sets along them.

## Checkpoints

- After tier 1: `test_matches_naive_on_random_input[kmp_search]` passes.
- After tier 2: the unverified-hash test passes - meaning you reproduced the bug
  on purpose.
- After tier 3: `test_aho_corasick_agrees_with_running_naive_per_pattern`, which
  is the one that catches a missing output merge.

## If you are stuck

The prefix function is the hard part and it is 8 lines. Write it on paper for
`aabaaab` before you write it in Python. If your table has an entry equal to its
own index, you have allowed the whole string to count as a proper prefix.
