"""A text-processing service with three planted defects.

It runs to completion, raises nothing and exits 0. Every number it prints is
plausible. Three of them are wrong.

    python broken_string_search.py
    echo "exit=$?"
"""
from __future__ import annotations

from collections import deque


def naive_search(text: str, pattern: str) -> list[int]:
    """Correct. This is the reference the others should agree with."""
    if not pattern:
        return []
    return [i for i in range(len(text) - len(pattern) + 1)
            if text[i:i + len(pattern)] == pattern]


def prefix_function(pattern: str) -> list[int]:
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
    if not pattern:
        return []
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
            k = 0
    return found


def rolling_search(text: str, pattern: str, mod: int = 101) -> list[int]:
    n, m = len(text), len(pattern)
    if not pattern or m > n:
        return []
    base = 257
    high = pow(base, m - 1, mod)

    target = 0
    window = 0
    for i in range(m):
        target = (target * base + ord(pattern[i])) % mod
        window = (window * base + ord(text[i])) % mod

    found = []
    for start in range(n - m + 1):
        if window == target:
            found.append(start)
        if start + m < n:
            window = (window - ord(text[start]) * high) % mod
            window = (window * base + ord(text[start + m])) % mod
    return found


class Screen:
    """Multi-pattern matcher for a content filter."""

    def __init__(self) -> None:
        self.goto: list[dict[str, int]] = [{}]
        self.fail: list[int] = [0]
        self.output: list[list[str]] = [[]]

    def add(self, word: str) -> None:
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

    def build(self) -> Screen:
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
                queue.append(child)
        return self

    def search(self, text: str) -> list[tuple[int, str]]:
        node = 0
        hits = []
        for i, character in enumerate(text):
            while node and character not in self.goto[node]:
                node = self.fail[node]
            node = self.goto[node].get(character, 0)
            for word in self.output[node]:
                hits.append((i, word))
        return hits


def main() -> None:
    print("=" * 66)
    print("TEXT PROCESSING SERVICE - nightly report")
    print("=" * 66)

    print()
    print("[1] Counting occurrences of a repeated marker")
    log = "AAAAAAAA"
    marker = "AA"
    reference = naive_search(log, marker)
    fast = kmp_search(log, marker)
    print(f"    text={log!r} marker={marker!r}")
    print(f"    reference scan found : {len(reference)} at {reference}")
    print(f"    fast matcher found   : {len(fast)} at {fast}")

    print()
    print("[2] Scanning a document for a short token")
    document = ("the rain in spain falls mainly on the plain "
                "and the train remains in the main lane")
    token = "ain"
    reference = naive_search(document, token)
    rolled = rolling_search(document, token)
    print(f"    token={token!r}")
    print(f"    reference scan found : {len(reference)} at {reference}")
    print(f"    rolling hash found   : {len(rolled)} at {rolled}")

    print()
    print("[3] Content filter over a dictionary of terms")
    screen = Screen()
    for word in ("he", "she", "his", "hers"):
        screen.add(word)
    screen.build()
    sample = "ushers"
    hits = sorted({word for _, word in screen.search(sample)})
    expected = sorted({w for w in ("he", "she", "his", "hers")
                       if naive_search(sample, w)})
    print(f"    text={sample!r}")
    print(f"    reference scan flagged : {expected}")
    print(f"    filter flagged         : {hits}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()
