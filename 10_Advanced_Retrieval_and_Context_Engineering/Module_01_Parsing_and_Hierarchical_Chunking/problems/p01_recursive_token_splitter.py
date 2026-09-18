"""Problem 01 — Recursive Token Splitter

Topic: 01 Parsing and Hierarchical Chunking
Target: Production-grade implementation

Split text by paragraph and word boundaries with chunk size and overlap limits.

Example:
    >>> recursive_token_splitter("one two three four five six seven eight", max_chunk_words=4, overlap_words=1)
    ['one two three four', 'four five six seven', 'seven eight']

Hints:
    Hint 1: Think in terms of a word-index window sliding across the token
        stream, where the window advances by LESS than its own width so
        consecutive chunks share a border of `overlap_words` words.
    Hint 2: Split `text` into a word list, then slide a window of
        `max_chunk_words` words forward by `step = max_chunk_words -
        overlap_words` each iteration, joining each window's words with a
        single space.
    Hint 3: Clamp `step` to at least 1 — an `overlap_words` at or above
        `max_chunk_words` would otherwise never advance the window; empty or
        whitespace-only `text` must return `[]`; and the loop must stop as
        soon as a window reaches the end of the word list, rather than
        continuing to emit extra short chunks past the last real one.
"""

from __future__ import annotations


def recursive_token_splitter(text: str, max_chunk_words: int = 5, overlap_words: int = 1) -> list[str]:
    """Split text into words.
    Create overlapping chunks of size at most max_chunk_words with overlap_words overlap.
    Returns list of chunk strings joined by space.
    """
    raise NotImplementedError("Implement recursive_token_splitter")
