# Module 16 Problem Bank - String Algorithms

Six problems. Each has a stub here, a reference solution in `solutions/`, and a
test in `tests/`.

| # | Problem | Pattern | Difficulty |
| :-- | :--- | :--- | :--- |
| 01 | Build the KMP Prefix Table | KMP prefix function | Medium |
| 02 | Longest Prefix That Is Also a Suffix | KMP prefix function | Medium |
| 03 | Is the String a Repeated Block? | String period | Medium |
| 04 | Shortest Palindrome by Prepending | KMP on s + sep + reversed(s) | Hard |
| 05 | All Occurrences, Overlaps Included | Linear-time string search | Medium |
| 06 | Censor Every Banned Term in One Pass | Aho-Corasick | Hard |

Problems 01-04 are the same table applied four ways. That is deliberate: the
skill being built is recognising that a question about prefixes, suffixes,
periods or palindromic prefixes is a question the prefix function already
answers.

## Working on them

```bash
cd problems
python -m pytest tests -q              # grades YOUR stubs - must fail at first
python -m pytest tests -q -k p03       # just one problem
```

From the course root the same tests grade the reference solutions instead:

```bash
python -m pytest Module_16_String_Algorithms_and_Pattern_Matching/problems -q
```

Two tests assert *scale* rather than correctness - `test_p05_find_all_is_linear`
and `test_p06_censor_is_one_pass`. A correct but quadratic answer fails them,
which is the point: on these problems the complexity is the problem.
