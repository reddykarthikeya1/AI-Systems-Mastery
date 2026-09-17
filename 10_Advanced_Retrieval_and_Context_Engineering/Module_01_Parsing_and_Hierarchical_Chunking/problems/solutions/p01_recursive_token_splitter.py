"""Reference Solution — Problem 01: Recursive Token Splitter

Topic: 01 Parsing and Hierarchical Chunking
"""

from __future__ import annotations


def recursive_token_splitter(text: str, max_chunk_words: int = 5, overlap_words: int = 1) -> list[str]:
    words = text.strip().split()
    if not words:
        return []
    chunks = []
    step = max(1, max_chunk_words - overlap_words)
    for i in range(0, len(words), step):
        chunk = words[i:i + max_chunk_words]
        chunks.append(" ".join(chunk))
        if i + max_chunk_words >= len(words):
            break
    return chunks
