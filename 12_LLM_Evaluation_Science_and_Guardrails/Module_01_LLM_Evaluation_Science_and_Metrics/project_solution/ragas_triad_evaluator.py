"""Production LLM Evaluation Metrics and RAG Triad Evaluator."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Set


@dataclass
class RAGTriadScore:
    faithfulness: float
    answer_relevance: float
    context_precision: float
    overall_score: float
    unsupported_claims: List[str]


def normalize_text(text: str) -> str:
    """Normalizes text by lowercasing, stripping punctuation and redundant whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def get_tokens(text: str) -> Set[str]:
    """Extracts set of alphanumeric tokens."""
    return set(normalize_text(text).split())


def exact_match_score(prediction: str, ground_truth: str) -> float:
    """Computes exact string match after normalization."""
    return 1.0 if normalize_text(prediction) == normalize_text(ground_truth) else 0.0


def token_f1_score(prediction: str, ground_truth: str) -> float:
    """Computes token-level F1 overlap score."""
    pred_tokens = get_tokens(prediction)
    truth_tokens = get_tokens(ground_truth)

    if not pred_tokens or not truth_tokens:
        return 0.0

    common = pred_tokens.intersection(truth_tokens)
    if not common:
        return 0.0

    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(truth_tokens)
    return 2 * (precision * recall) / (precision + recall)


class RAGTriadEvaluator:
    """Evaluates RAG generation against Context Relevance, Faithfulness, and Answer Relevance."""

    def __init__(self, entailment_threshold: float = 0.5) -> None:
        self.entailment_threshold = entailment_threshold

    def decompose_claims(self, answer: str) -> List[str]:
        """Decomposes an answer into atomic propositional sentences."""
        clean = answer.strip()
        for abbrev in ["dr.", "mr.", "mrs.", "ms.", "e.g.", "i.e."]:
            clean = re.sub(re.escape(abbrev), abbrev.replace(".", "@DOT@"), clean, flags=re.IGNORECASE)
        sentences = re.split(r"\.\s+|\?\s+|\!\s+", clean)
        claims = [s.replace("@DOT@", ".").strip() for s in sentences if len(s.strip()) > 3]
        return claims or [answer]

    def evaluate_faithfulness(self, answer: str, context: str) -> tuple[float, List[str]]:
        """Scores proportion of claims supported by the context."""
        claims = self.decompose_claims(answer)
        if not claims:
            return 1.0, []

        context_tokens = get_tokens(context)
        unsupported = []
        supported_count = 0

        for claim in claims:
            claim_tokens = get_tokens(claim)
            if not claim_tokens:
                continue
            overlap = claim_tokens.intersection(context_tokens)
            ratio = len(overlap) / len(claim_tokens)
            if ratio >= self.entailment_threshold:
                supported_count += 1
            else:
                unsupported.append(claim)

        score = supported_count / len(claims) if claims else 1.0
        return score, unsupported

    def evaluate_answer_relevance(self, query: str, answer: str) -> float:
        """Scores token overlap relevance between user query and generated answer."""
        q_tokens = get_tokens(query)
        a_tokens = get_tokens(answer)
        if not q_tokens or not a_tokens:
            return 0.0
        overlap = q_tokens.intersection(a_tokens)
        return len(overlap) / len(q_tokens)

    def evaluate_context_precision(self, query: str, context_chunks: List[str]) -> float:
        """Computes mean precision of retrieved chunks containing query keywords."""
        if not context_chunks:
            return 0.0
        q_tokens = get_tokens(query)
        hits = 0
        for chunk in context_chunks:
            c_tokens = get_tokens(chunk)
            if len(q_tokens.intersection(c_tokens)) > 0:
                hits += 1
        return hits / len(context_chunks)

    def score_rag_turn(
        self,
        query: str,
        answer: str,
        context_chunks: List[str],
    ) -> RAGTriadScore:
        """Scores full RAG interaction across the Triad."""
        full_context = " ".join(context_chunks)
        faithfulness, unsupported = self.evaluate_faithfulness(answer, full_context)
        answer_rel = self.evaluate_answer_relevance(query, answer)
        context_prec = self.evaluate_context_precision(query, context_chunks)

        overall = (faithfulness * 0.4) + (answer_rel * 0.3) + (context_prec * 0.3)

        return RAGTriadScore(
            faithfulness=faithfulness,
            answer_relevance=answer_rel,
            context_precision=context_prec,
            overall_score=overall,
            unsupported_claims=unsupported,
        )
