"""Problem 01 — Prepend Document Summary

Topic: 02 Contextual Retrieval Architecture
Target: Production-grade implementation

Prepend document-level context summary to each passage chunk.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def prepend_document_summary(doc_title: str, doc_summary: str, chunks: list[str]) -> list[str]:
    """Format each chunk as: f"[{doc_title}: {doc_summary}] {chunk}".
    Returns list of enriched chunk strings.
    """
    raise NotImplementedError("Implement prepend_document_summary")
