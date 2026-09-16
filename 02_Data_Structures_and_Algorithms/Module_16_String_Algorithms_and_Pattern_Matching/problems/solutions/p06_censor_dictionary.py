"""Reference solution - Problem 06: Censor Every Banned Term in One Pass

Pattern:    Aho-Corasick
Complexity: Time O(n + total + hits), Space O(total)
"""

from __future__ import annotations

from collections import deque


def censor(text: str, banned: list[str]) -> str:
    words = [w for w in banned if w]
    if not words or not text:
        return text

    goto: list[dict[str, int]] = [{}]
    fail = [0]
    output: list[list[int]] = [[]]        # word lengths ending at this node

    for word in words:
        node = 0
        for character in word:
            nxt = goto[node].get(character)
            if nxt is None:
                nxt = len(goto)
                goto.append({})
                fail.append(0)
                output.append([])
                goto[node][character] = nxt
            node = nxt
        output[node].append(len(word))

    queue: deque[int] = deque(goto[0].values())
    while queue:
        node = queue.popleft()
        for character, child in goto[node].items():
            fallback = fail[node]
            while fallback and character not in goto[fallback]:
                fallback = fail[fallback]
            fail[child] = goto[fallback].get(character, 0)
            if fail[child] == child:
                fail[child] = 0
            output[child] += output[fail[child]]
            queue.append(child)

    censored = [False] * len(text)
    node = 0
    for i, character in enumerate(text):
        while node and character not in goto[node]:
            node = fail[node]
        node = goto[node].get(character, 0)
        for length in output[node]:
            for j in range(i - length + 1, i + 1):
                censored[j] = True

    return "".join("*" if flag else character
                   for character, flag in zip(text, censored, strict=True))
