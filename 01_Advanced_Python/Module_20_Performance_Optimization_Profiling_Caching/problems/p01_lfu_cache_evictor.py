"""Problem 01 — LFU Cache Eviction Frequency Counter

Target: Production-grade implementation

Example:
    >>> freqs = {'a': 3, 'b': 1, 'c': 1}
    >>> order = ['c', 'b', 'a']  # c was accessed earlier than b
    >>> lfu_eviction_candidate(freqs, order)
    'c'
    >>> lfu_eviction_candidate({}, []) is None
    True

Hints:
    Hint 1: LFU eviction needs a tie-breaker — frequency alone rarely picks a
        single key, so a second signal (recency) decides among the least-used
        ones.
    Hint 2: Find `min(freq_map.values())`, collect every key whose frequency
        equals that minimum into a candidate set, then scan `recency_order`
        (oldest-accessed first) and return the first entry that's also a
        candidate.
    Hint 3: `recency_order` is least-recently-used first, so among tied
        frequencies you must evict the one that appears earliest in that
        list, not just any tied key; an empty `freq_map` must return `None`
        rather than raising on `min()` of an empty sequence.
"""

from __future__ import annotations


def lfu_eviction_candidate(freq_map: dict[str, int], recency_order: list[str]) -> str | None:
    raise NotImplementedError('Implement lfu_eviction_candidate')
