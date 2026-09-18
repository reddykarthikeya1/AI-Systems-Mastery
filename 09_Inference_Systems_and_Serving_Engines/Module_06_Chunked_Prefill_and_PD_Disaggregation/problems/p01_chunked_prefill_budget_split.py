"""Problem 01 — Chunked Prefill Budget Split

Topic: 06 Chunked Prefill and PD Disaggregation
Target: Production-grade implementation

Split long prompt prefill tokens into chunked steps bounded by chunk_size.

Example:
    >>> chunked_prefill_budget_split([1, 2, 3, 4, 5, 6, 7], 3)
    [[1, 2, 3], [4, 5, 6], [7]]

Hints:
    Hint 1: This is plain sequential chunking of the prefill sequence, no
        scheduling or attention logic needed — walk `prompt_tokens` strictly
        in order, `chunk_size` tokens at a time.
    Hint 2: Slice with a stepped range: a list comprehension over
        `prompt_tokens[i:i + chunk_size]` for `i` stepping through
        `range(0, len(prompt_tokens), chunk_size)`.
    Hint 3: An empty `prompt_tokens` must return `[]`, not `[[]]`; Python
        slicing already truncates the final chunk cleanly when
        `len(prompt_tokens)` isn't a multiple of `chunk_size`, so no extra
        bounds handling is needed for the trailing partial chunk.
"""

from __future__ import annotations


def chunked_prefill_budget_split(prompt_tokens: list[int], chunk_size: int = 4) -> list[list[int]]:
    """Partition prompt_tokens into chunks of at most chunk_size."""
    raise NotImplementedError("Implement chunked_prefill_budget_split")
