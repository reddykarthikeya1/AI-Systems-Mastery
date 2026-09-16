"""Standardized Benchmark Harness with Pass@k Estimation and Decontamination."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Set


@dataclass
class MathBenchmarkItem:
    item_id: str
    question: str
    gold_answer: float


class BenchmarkHarness:
    """Production Benchmark Runner with Pass@k and Contamination Detection."""

    @staticmethod
    def extract_numeric_answer(text: str) -> float | None:
        """Extracts final numeric value following standard #### delimiter or trailing number."""
        match = re.search(r"####\s*(-?[0-9,]+(?:\.[0-9]+)?)", text)
        if match:
            clean_str = match.group(1).replace(",", "")
            return float(clean_str)

        # Fallback: look for last number in text
        numbers = re.findall(r"-?[0-9,]+(?:\.[0-9]+)?", text)
        if numbers:
            try:
                return float(numbers[-1].replace(",", ""))
            except ValueError:
                return None
        return None

    @staticmethod
    def compute_pass_at_k(n: int, c: int, k: int) -> float:
        """Computes unbiased Pass@k estimate (Chen et al., 2021)."""
        if n < k:
            raise ValueError(f"Sample size n ({n}) must be >= k ({k})")
        if n - c < k:
            return 1.0
        return 1.0 - (math.comb(n - c, k) / math.comb(n, k))

    @staticmethod
    def check_ngram_contamination(
        test_text: str,
        training_documents: List[str],
        n_gram_size: int = 8,
    ) -> bool:
        """Detects benchmark test leakage in training data via n-gram intersection."""
        def extract_ngrams(s: str, n: int) -> Set[str]:
            words = re.findall(r"\w+", s.lower())
            if len(words) < n:
                return set()
            return {" ".join(words[i : i + n]) for i in range(len(words) - n + 1)}

        test_ngrams = extract_ngrams(test_text, n_gram_size)
        if not test_ngrams:
            return False

        for doc in training_documents:
            doc_ngrams = extract_ngrams(doc, n_gram_size)
            if test_ngrams.intersection(doc_ngrams):
                return True
        return False

    def evaluate_math_suite(
        self,
        items: List[MathBenchmarkItem],
        model_generate_fn: Callable[[str], str],
    ) -> Dict[str, Any]:
        """Evaluates a suite of math reasoning problems."""
        correct = 0
        details = []

        for item in items:
            raw_gen = model_generate_fn(item.question)
            extracted = self.extract_numeric_answer(raw_gen)
            is_correct = (extracted is not None) and math.isclose(extracted, item.gold_answer, abs_tol=1e-3)
            if is_correct:
                correct += 1

            details.append({
                "item_id": item.item_id,
                "gold": item.gold_answer,
                "extracted": extracted,
                "correct": is_correct,
            })

        acc = correct / len(items) if items else 0.0
        return {
            "total": len(items),
            "correct": correct,
            "accuracy": acc,
            "details": details,
        }
