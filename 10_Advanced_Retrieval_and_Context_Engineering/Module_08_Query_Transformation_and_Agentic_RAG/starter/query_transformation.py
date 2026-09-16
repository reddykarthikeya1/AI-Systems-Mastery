from __future__ import annotations


class QueryTransformer:
    @staticmethod
    def decompose_query(complex_query: str) -> list[str]:
        raise NotImplementedError("Implement decompose_query")

    @staticmethod
    def generate_hyde_document(query: str) -> str:
        raise NotImplementedError("Implement generate_hyde_document")

    @staticmethod
    def grade_retrieval_relevance(query: str, retrieved_context: str) -> bool:
        raise NotImplementedError("Implement grade_retrieval_relevance")
