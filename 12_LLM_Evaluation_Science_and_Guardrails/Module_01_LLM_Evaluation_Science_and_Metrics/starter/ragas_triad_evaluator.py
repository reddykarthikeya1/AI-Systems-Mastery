"""Starter stub for RAG Triad Evaluator."""

from __future__ import annotations
from typing import Any, List


class RAGTriadEvaluator:
    def __init__(self, entailment_threshold: float = 0.5) -> None:
        raise NotImplementedError("RAGTriadEvaluator is not implemented yet.")

    def score_rag_turn(self, query: str, answer: str, context_chunks: List[str]) -> Any:
        raise NotImplementedError
