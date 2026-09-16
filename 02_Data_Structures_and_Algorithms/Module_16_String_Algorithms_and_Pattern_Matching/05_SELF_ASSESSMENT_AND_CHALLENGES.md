# Self-Assessment - Module 16

## Quiz

1. What exactly does `pi[i] = 3` tell you?
2. Why can the text pointer in KMP never move backwards, and why does that make
   the algorithm linear rather than quadratic?
3. You reset `k = 0` after a successful match. Which inputs change their answer,
   and in which direction?
4. A Rabin-Karp hash comparison succeeds. What have you proved?
5. Why is Rabin-Karp "expected" `O(n + m)` rather than worst case?
6. What must be true of the separator in `pattern + sep + text`, and what goes
   wrong if it is not?
7. Aho-Corasick over 5,000 patterns and a 1 MB document: what is the cost, and
   which of those two numbers does it *not* depend on?
8. Why must output sets be merged along failure links? Give an input that
   distinguishes the two versions.
9. `smallest_period("abcabca")` is 7, not 3. Why?
10. When is `str.find` the right answer?

## Challenges

**A. Wildcards.** Extend `kmp_search` so the pattern may contain `?`, matching
any single character. Does the prefix function still work unchanged? (It does
not - work out why before you look it up.)

**B. Streaming.** Rewrite Aho-Corasick's `search` so it accepts the text one
character at a time and yields matches as they occur, holding no more than the
automaton in memory. This is what a network intrusion detector actually needs.

**C. Longest common substring.** Use a rolling hash plus binary search on the
answer length to find the longest substring common to two strings in
`O((n + m) log min(n, m))` expected time. State clearly where a collision could
make your answer wrong and how you guard against it.
