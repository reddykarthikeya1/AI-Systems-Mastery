"""Reference Solution — Problem 01: Prepend Document Summary

Topic: 02 Contextual Retrieval Architecture
"""

from __future__ import annotations


def prepend_document_summary(doc_title: str, doc_summary: str, chunks: list[str]) -> list[str]:
    prefix = f"[{doc_title}: {doc_summary}] "
    return [f"{prefix}{c}" for c in chunks]
