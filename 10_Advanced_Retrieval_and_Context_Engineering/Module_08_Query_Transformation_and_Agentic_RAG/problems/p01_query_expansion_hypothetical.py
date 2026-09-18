"""Problem 01 — Query Expansion Hypothetical

Topic: 08 Query Transformation and Agentic RAG
Target: Production-grade implementation

Combine original query with hypothetical document answer tokens.

Example:
    >>> query_expansion_hypothetical("  What is Raft?  ", "Raft is a consensus algorithm.  ")
    'Query: What is Raft? | Context: Raft is a consensus algorithm.'

Hints:
    Hint 1: This is the HyDE technique — you're building one embeddable
        string that fuses the user's literal question with a model-generated
        hypothetical answer, so both pieces must land in a single, clearly
        labeled string.
    Hint 2: A single f-string using the exact template `"Query: {...} |
        Context: {...}"` with both inputs already stripped of surrounding
        whitespace — no loops or data structures needed.
    Hint 3: Match the literal separator text exactly (the "Query: " and " |
        Context: " labels with their spacing), and call `.strip()` on each
        input individually before inserting it, not on the final combined
        string.
"""

from __future__ import annotations


def query_expansion_hypothetical(original_query: str, hyde_doc: str) -> str:
    """Concatenate original query and Hyde generated response for dense embedding.
    Format: f"Query: {original_query.strip()} | Context: {hyde_doc.strip()}".
    """
    raise NotImplementedError("Implement query_expansion_hypothetical")
