"""String matching engine: KMP, Z-algorithm, Rabin-Karp and Aho-Corasick.

Every algorithm here exists to beat the same baseline - the naive scan, which
compares the pattern at every offset and costs O(n*m). Each one beats it by
exploiting a different piece of structure:

| Algorithm      | Cost                | What it exploits                        |
| :------------- | :------------------ | :-------------------------------------- |
| Naive          | O(n*m)              | nothing                                 |
| KMP            | O(n + m)            | the pattern's own self-overlap          |
| Z-algorithm    | O(n + m)            | the same, computed as a prefix array    |
| Rabin-Karp     | O(n + m) expected   | a hash you can update in O(1) per shift |
| Aho-Corasick   | O(n + total + hits) | many patterns sharing prefixes          |

The choice between them is not taste:

- **One pattern, exact** -> KMP. Worst-case linear with no assumptions.
- **Many patterns at once** -> Aho-Corasick. Running KMP k times costs O(k*n).
- **Comparing substrings repeatedly, or 2-D** -> Rabin-Karp. A hash comparison
  is O(1) where a character comparison is O(m).

A note on Rabin-Karp that most write-ups skip: a hash match is *not* a match.
Two different strings can hash the same, so every candidate must be verified
by an actual comparison. `rabin_karp_search` does that, and
`rabin_karp_search_unverified` deliberately does not, so the test suite can
demonstrate the false positive rather than assert it is rare.
"""

from __future__ import annotations

from collections import deque

# ---------------------------------------------------------------------------
# 1. The baseline everything is measured against
# ---------------------------------------------------------------------------


def naive_search(text: str, pattern: str) -> list[int]:
    """Every starting offset where `pattern` occurs in `text`. O(n*m).

    Used throughout the tests as the correctness reference. Note that the
    comparison is a *slice* comparison, which CPython performs in C - so this
    is asymptotically quadratic but with a very small constant factor. See
    `naive_search_char_by_char` for why that distinction matters.
    """
    if not pattern:
        return list(range(len(text) + 1))
    found = []
    for start in range(len(text) - len(pattern) + 1):
        if text[start:start + len(pattern)] == pattern:
            found.append(start)
    return found


def naive_search_char_by_char(text: str, pattern: str) -> list[int]:
    """The same algorithm with the inner comparison written out in Python.

    This exists to make one point that a complexity table cannot:

        **An O(n*m) algorithm in C routinely beats an O(n + m) algorithm in
        Python at practical input sizes.**

    `naive_search` above is quadratic, but its inner loop is a C memcmp. A
    pure-Python KMP does asymptotically less work and executes far more Python
    bytecode per character, so on a 20,000-character text the quadratic C
    version *wins*. The crossover exists, but it is much further out than the
    big-O notation suggests.

    Compare KMP against this function and you are comparing algorithms.
    Compare it against `naive_search` and you are comparing implementations -
    which is a fair thing to measure, and a different question.
    """
    if not pattern:
        return list(range(len(text) + 1))
    found = []
    n, m = len(text), len(pattern)
    for start in range(n - m + 1):
        i = 0
        while i < m and text[start + i] == pattern[i]:
            i += 1
        if i == m:
            found.append(start)
    return found


# ---------------------------------------------------------------------------
# 2. KMP - the prefix function
# ---------------------------------------------------------------------------


def prefix_function(pattern: str) -> list[int]:
    """`pi[i]` = length of the longest proper prefix of `pattern[:i+1]`
    that is also a suffix of it.

    This is the whole idea of KMP. After matching `k` characters and then
    failing, the naive algorithm restarts at the next offset and re-reads
    characters it has already seen. `pi` says how much of that prefix is still
    valid, so the text pointer never moves backwards.

    For "ababaca": pi = [0, 0, 1, 2, 3, 0, 1]. At index 4 the first "aba" is
    also a suffix, so a failure there resumes with 3 characters already matched.
    """
    pi = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k
    return pi


def kmp_search(text: str, pattern: str) -> list[int]:
    """All occurrences, O(n + m), overlaps included.

    The text index `i` only ever increases - that is the guarantee. The inner
    `while` walks the *pattern* back, and because `pi[k-1] < k` strictly, the
    total number of those steps across the whole scan is bounded by n.
    """
    if not pattern:
        return list(range(len(text) + 1))
    pi = prefix_function(pattern)
    found = []
    k = 0
    for i, character in enumerate(text):
        while k > 0 and character != pattern[k]:
            k = pi[k - 1]
        if character == pattern[k]:
            k += 1
        if k == len(pattern):
            found.append(i - len(pattern) + 1)
            k = pi[k - 1]          # allow overlapping matches
    return found


def smallest_period(word: str) -> int:
    """Length of the shortest string whose repetition builds `word`.

    Falls straight out of the prefix function: `n - pi[n-1]` is the period, and
    it tiles the word exactly when it divides n. "abcabcabc" -> 3, "abcd" -> 4.
    """
    if not word:
        return 0
    candidate = len(word) - prefix_function(word)[-1]
    return candidate if len(word) % candidate == 0 else len(word)


# ---------------------------------------------------------------------------
# 3. Z-algorithm
# ---------------------------------------------------------------------------


def z_function(text: str) -> list[int]:
    """`z[i]` = length of the longest substring starting at `i` that is also a
    prefix of `text`. `z[0]` is defined here as len(text).

    Same information as the prefix function, arranged differently. The trick is
    the `[left, right)` window: the segment already known to match the prefix.
    Inside it, a previously computed answer can be reused instead of re-scanned.
    """
    n = len(text)
    z = [0] * n
    if n == 0:
        return z
    z[0] = n
    left = right = 0
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < n and text[z[i]] == text[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


def z_search(text: str, pattern: str, separator: str = "\x00") -> list[int]:
    """Find `pattern` by running the Z-function over `pattern + sep + text`.

    The separator must not appear in either string, or a z-value could run past
    the join and report a match that does not exist. Using NUL by default makes
    that unlikely; the assertion makes it impossible to do silently.
    """
    if not pattern:
        return list(range(len(text) + 1))
    if separator in text or separator in pattern:
        raise ValueError("separator must not occur in the text or the pattern")
    combined = pattern + separator + text
    z = z_function(combined)
    offset = len(pattern) + 1
    return [i - offset for i in range(offset, len(combined))
            if z[i] >= len(pattern)]


# ---------------------------------------------------------------------------
# 4. Rabin-Karp - the rolling hash
# ---------------------------------------------------------------------------

BASE = 257
MOD = (1 << 61) - 1          # a Mersenne prime; large enough to make collisions rare


class RollingHash:
    """Polynomial hash over a sliding window.

    hash(s) = (s[0]*B^(m-1) + s[1]*B^(m-2) + ... + s[m-1]) mod P

    Sliding one character right costs O(1): subtract the outgoing character's
    contribution, multiply by the base, add the incoming one.
    """

    def __init__(self, window: int, base: int = BASE, mod: int = MOD) -> None:
        self.window = window
        self.base = base
        self.mod = mod
        self.high = pow(base, window - 1, mod) if window else 1
        self.value = 0

    @classmethod
    def of(cls, text: str, base: int = BASE, mod: int = MOD) -> int:
        value = 0
        for character in text:
            value = (value * base + ord(character)) % mod
        return value

    def push(self, character: str) -> int:
        self.value = (self.value * self.base + ord(character)) % self.mod
        return self.value

    def roll(self, outgoing: str, incoming: str) -> int:
        self.value = (self.value - ord(outgoing) * self.high) % self.mod
        self.value = (self.value * self.base + ord(incoming)) % self.mod
        return self.value


def rabin_karp_search(text: str, pattern: str) -> list[int]:
    """All occurrences, O(n + m) expected.

    Note the verification step. A hash match is a *candidate*; the slice
    comparison is what makes the answer correct. Skipping it is the classic
    Rabin-Karp bug - see `rabin_karp_search_unverified`.
    """
    n, m = len(text), len(pattern)
    if not pattern:
        return list(range(n + 1))
    if m > n:
        return []

    target = RollingHash.of(pattern)
    window = RollingHash(m)
    for character in text[:m]:
        window.push(character)

    found = []
    for start in range(n - m + 1):
        if window.value == target and text[start:start + m] == pattern:
            found.append(start)
        if start + m < n:
            window.roll(text[start], text[start + m])
    return found


def rabin_karp_search_unverified(text: str, pattern: str, mod: int = 101) -> list[int]:
    """Deliberately broken: trusts the hash and never compares the strings.

    Kept because the failure is instructive and a test asserts it. With a tiny
    modulus, collisions are common, so this reports matches that are not there.
    In production the modulus is large and the same bug fires once a month on
    one input nobody can reproduce.
    """
    n, m = len(text), len(pattern)
    if not pattern or m > n:
        return []
    target = RollingHash.of(pattern, mod=mod)
    window = RollingHash(m, mod=mod)
    for character in text[:m]:
        window.push(character)

    found = []
    for start in range(n - m + 1):
        if window.value == target:
            found.append(start)             # no verification - this is the bug
        if start + m < n:
            window.roll(text[start], text[start + m])
    return found


def rabin_karp_2d(grid: list[str], pattern: list[str]) -> list[tuple[int, int]]:
    """Find a 2-D `pattern` block inside a 2-D `grid`. Returns (row, col) origins.

    Two passes of the same idea:

    1. Hash every horizontal run of width `pw` in the grid, giving a smaller
       grid of row-hashes.
    2. Hash vertically down that grid over `ph` rows, and compare against the
       pattern's own column of row-hashes.

    Candidates are verified, for the reason given above.
    """
    if not pattern or not pattern[0] or not grid or not grid[0]:
        return []
    ph, pw = len(pattern), len(pattern[0])
    gh, gw = len(grid), len(grid[0])
    if ph > gh or pw > gw:
        return []

    def row_hashes(row: str) -> list[int]:
        window = RollingHash(pw)
        for character in row[:pw]:
            window.push(character)
        out = [window.value]
        for start in range(gw - pw):
            out.append(window.roll(row[start], row[start + pw]))
        return out

    grid_rows = [row_hashes(row) for row in grid]
    pattern_rows = [RollingHash.of(row) for row in pattern]
    pattern_column = 0
    for value in pattern_rows:
        pattern_column = (pattern_column * BASE + value) % MOD

    high = pow(BASE, ph - 1, MOD)
    found = []
    for col in range(gw - pw + 1):
        column = 0
        for row in range(ph):
            column = (column * BASE + grid_rows[row][col]) % MOD
        for row in range(gh - ph + 1):
            if column == pattern_column:
                block = [grid[row + r][col:col + pw] for r in range(ph)]
                if block == pattern:
                    found.append((row, col))
            if row + ph < gh:
                column = (column - grid_rows[row][col] * high) % MOD
                column = (column * BASE + grid_rows[row + ph][col]) % MOD
    return sorted(found)


# ---------------------------------------------------------------------------
# 5. Aho-Corasick - many patterns in one pass
# ---------------------------------------------------------------------------


class AhoCorasick:
    """Match every pattern in a dictionary in a single pass over the text.

    A trie of the patterns, plus **failure links**. A failure link points at the
    longest proper suffix of the current string that is also a node in the trie -
    exactly the KMP prefix function, generalised from one pattern to a set.

    Cost is O(total pattern length) to build and O(n + number of matches) to
    search, regardless of how many patterns there are. Running KMP once per
    pattern would cost O(k*n).

    This is what a spam filter, an intrusion detector or a profanity screen
    actually runs.
    """

    def __init__(self) -> None:
        self.goto: list[dict[str, int]] = [{}]
        self.fail: list[int] = [0]
        self.output: list[list[str]] = [[]]
        self._built = False

    def add(self, word: str) -> None:
        if self._built:
            raise RuntimeError("add all patterns before calling build()")
        if not word:
            raise ValueError("the empty pattern matches everywhere; reject it")
        node = 0
        for character in word:
            nxt = self.goto[node].get(character)
            if nxt is None:
                nxt = len(self.goto)
                self.goto.append({})
                self.fail.append(0)
                self.output.append([])
                self.goto[node][character] = nxt
            node = nxt
        self.output[node].append(word)

    def build(self) -> AhoCorasick:
        """Breadth-first: a node's failure link is computed from its parent's.

        Output sets are merged along failure links, so a node reports not only
        the word ending there but every dictionary word that is a suffix of it.
        Without this merge, "she" would be found and the "he" inside it missed.
        """
        queue: deque[int] = deque()
        for child in self.goto[0].values():
            self.fail[child] = 0
            queue.append(child)
        while queue:
            node = queue.popleft()
            for character, child in self.goto[node].items():
                fallback = self.fail[node]
                while fallback and character not in self.goto[fallback]:
                    fallback = self.fail[fallback]
                self.fail[child] = self.goto[fallback].get(character, 0)
                if self.fail[child] == child:
                    self.fail[child] = 0
                self.output[child] += self.output[self.fail[child]]
                queue.append(child)
        self._built = True
        return self

    def search(self, text: str) -> list[tuple[int, str]]:
        """(end_index, word) for every occurrence of every pattern."""
        if not self._built:
            raise RuntimeError("call build() before search()")
        node = 0
        hits = []
        for i, character in enumerate(text):
            while node and character not in self.goto[node]:
                node = self.fail[node]
            node = self.goto[node].get(character, 0)
            for word in self.output[node]:
                hits.append((i, word))
        return hits

    def contains_any(self, text: str) -> bool:
        """Short-circuiting membership test - stops at the first hit."""
        node = 0
        for character in text:
            while node and character not in self.goto[node]:
                node = self.fail[node]
            node = self.goto[node].get(character, 0)
            if self.output[node]:
                return True
        return False


def build_automaton(patterns: list[str]) -> AhoCorasick:
    automaton = AhoCorasick()
    for word in patterns:
        automaton.add(word)
    return automaton.build()
