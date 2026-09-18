"""Problem 01 — Prepend Document Summary

Topic: 02 Contextual Retrieval Architecture
Target: Production-grade implementation

Prepend document-level context summary to each passage chunk.

Example:
    >>> prepend_document_summary("Q3 Earnings", "Revenue up 15%", ["Operating margin was 24%"])
    ['[Q3 Earnings: Revenue up 15%] Operating margin was 24%']

Hints:
    Hint 1: This is the "contextual retrieval" trick — every chunk from the
        same document needs the identical document-level context glued onto
        it so it stays meaningful and searchable on its own.
    Hint 2: Build the `f"[{doc_title}: {doc_summary}] "` prefix once, then
        map it over every chunk with a list comprehension rather than
        recomputing it per chunk.
    Hint 3: Match the exact literal format the tests check: square brackets
        around `title: summary`, a single space after the closing bracket
        before the chunk text, and the chunk's own text left completely
        unmodified (no trimming or extra separators).
"""

from __future__ import annotations


def prepend_document_summary(doc_title: str, doc_summary: str, chunks: list[str]) -> list[str]:
    """Format each chunk as: f"[{doc_title}: {doc_summary}] {chunk}".
    Returns list of enriched chunk strings.
    """
    raise NotImplementedError("Implement prepend_document_summary")
