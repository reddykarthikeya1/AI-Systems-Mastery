from __future__ import annotations


class QueryTransformer:
    """Simulates Query Transformation: Decomposition, HyDE, and Relevance Grading."""

    @staticmethod
    def decompose_query(complex_query: str) -> list[str]:
        """Decomposes multi-faceted comparison queries into discrete sub-queries."""
        if " and " in complex_query.lower() or " vs " in complex_query.lower():
            # Split comparison
            parts = complex_query.replace(" vs ", " and ").split(" and ")
            return [f"Details on {p.strip()}" for p in parts if p.strip()]
        return [complex_query]

    @staticmethod
    def generate_hyde_document(query: str) -> str:
        """Generates a hypothetical answer passage to align vector search space."""
        return f"Hypothetical answer discussing {query} with comprehensive factual explanations."

    @staticmethod
    def grade_retrieval_relevance(query: str, retrieved_context: str) -> bool:
        """Evaluator agent checking if retrieved documents satisfy the query."""
        q_words = set(query.lower().split())
        c_words = set(retrieved_context.lower().split())
        overlap = q_words.intersection(c_words)
        # Passed if at least 50% of query keywords appear in retrieved context
        return len(overlap) / max(len(q_words), 1) >= 0.5
