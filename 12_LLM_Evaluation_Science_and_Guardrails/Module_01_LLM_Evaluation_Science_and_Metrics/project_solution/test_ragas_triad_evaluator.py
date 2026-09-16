"""Unit tests for RAG Triad Evaluator."""

from __future__ import annotations

from ragas_triad_evaluator import (
    RAGTriadEvaluator,
    exact_match_score,
    token_f1_score,
)


def test_exact_match():
    assert exact_match_score("NVIDIA H100", "nvidia h100") == 1.0
    assert exact_match_score("NVIDIA H100!", "nvidia h100") == 1.0
    assert exact_match_score("NVIDIA A100", "nvidia h100") == 0.0


def test_token_f1_overlap():
    pred = "The GPU has 80GB memory"
    target = "GPU has 80GB memory and high bandwidth"
    f1 = token_f1_score(pred, target)
    assert 0.6 < f1 < 0.9


def test_faithfulness_and_hallucination_detection():
    evaluator = RAGTriadEvaluator(entailment_threshold=0.5)
    context = "NVIDIA H100 SXM5 GPU features 80GB of HBM3 memory. It delivers 3.35 TB/s bandwidth."

    # Completely grounded answer
    grounded_answer = "NVIDIA H100 features 80GB of HBM3 memory. It delivers high bandwidth."
    score, unsupported = evaluator.evaluate_faithfulness(grounded_answer, context)
    assert score == 1.0
    assert len(unsupported) == 0

    # Answer containing hallucination
    hallucinated_answer = "NVIDIA H100 has 80GB memory. It consumes only 50 Watts of power."
    score, unsupported = evaluator.evaluate_faithfulness(hallucinated_answer, context)
    assert score < 1.0
    assert len(unsupported) == 1
    assert "50 Watts" in unsupported[0]


def test_score_rag_turn():
    evaluator = RAGTriadEvaluator()
    query = "What is the memory capacity of NVIDIA H100?"
    answer = "The NVIDIA H100 features 80GB of HBM3 memory."
    chunks = [
        "NVIDIA H100 GPU features 80GB HBM3 memory.",
        "Unrelated document about networking switches.",
    ]

    report = evaluator.score_rag_turn(query, answer, chunks)
    assert report.faithfulness == 1.0
    assert report.answer_relevance > 0.5
    assert report.context_precision == 0.5
    assert report.overall_score > 0.6
