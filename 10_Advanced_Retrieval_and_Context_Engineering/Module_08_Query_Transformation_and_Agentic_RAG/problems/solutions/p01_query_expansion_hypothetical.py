"""Reference Solution — Problem 01: Query Expansion Hypothetical

Topic: 08 Query Transformation and Agentic RAG
"""

from __future__ import annotations


def query_expansion_hypothetical(original_query: str, hyde_doc: str) -> str:
    return f"Query: {original_query.strip()} | Context: {hyde_doc.strip()}"
