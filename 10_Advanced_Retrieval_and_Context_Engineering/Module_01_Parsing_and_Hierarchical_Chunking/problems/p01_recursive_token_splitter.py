"""Problem 01 — Recursive Token Splitter

Topic: 01 Parsing and Hierarchical Chunking
Target: Production-grade implementation

Split text by paragraph and word boundaries with chunk size and overlap limits.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def recursive_token_splitter(text: str, max_chunk_words: int = 5, overlap_words: int = 1) -> list[str]:
    """Split text into words.
    Create overlapping chunks of size at most max_chunk_words with overlap_words overlap.
    Returns list of chunk strings joined by space.
    """
    raise NotImplementedError("Implement recursive_token_splitter")
