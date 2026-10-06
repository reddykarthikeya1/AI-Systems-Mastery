"""Example 5: an agent evaluation harness: repeated trials, pass@k vs pass^k, confidence intervals.

Uses the ex01 tool loop with a deliberately flaky scripted model so the statistics are visible.
Run: python ex05_eval_harness.py
"""
import math
import random

from ex01_tool_loop import run_agent
from llm import FakeLLM

TASKS = [("ACME", 7, "106.2"), ("ACME", 3, "106.2"), ("ACME", 5, "106.2"), ("ACME", 2, "106.2")]


def flaky_llm(p_correct: float, rng: random.Random, ticker: str, days: int):
    """With probability p the model makes the right tool call then answers; otherwise it answers without tools (a failure)."""
    if rng.random() < p_correct:
        return FakeLLM([
            {"tool_calls": [{"id": "1", "name": "get_history", "args": {"ticker": ticker, "days": days}}]},
            {"content": "ACME closed at 106.2 most recently."},
        ])
    return FakeLLM([{"content": "ACME is probably around 90."}])  # hallucinated, no tool use


def grade(out: dict, expected: str) -> bool:
    used_tool = any(m["role"] == "tool" for m in out["messages"])
    return bool(out["answer"]) and used_tool and expected in out["answer"]   # outcome AND process check


def wilson(successes: int, n: int, z: float = 1.96) -> tuple:
    """Wilson score interval: better than the normal approximation for small n or p near 0/1."""
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (centre - half, centre + half)


def evaluate(p_correct: float, trials: int = 8, seed: int = 0) -> dict:
    rng = random.Random(seed)
    per_task = []
    for ticker, days, expected in TASKS * 25:                    # 100 task instances
        results = [grade(run_agent("price?", flaky_llm(p_correct, rng, ticker, days)), expected) for _ in range(trials)]
        per_task.append(results)
    n = len(per_task)
    single = sum(r[0] for r in per_task) / n                      # pass@1-style: first trial
    pass_at_k = sum(any(r) for r in per_task) / n                 # at least one success in k trials
    pass_hat_k = sum(all(r) for r in per_task) / n                # ALL k trials succeed (consistency)
    lo, hi = wilson(sum(r[0] for r in per_task), n)
    return {"single": single, "pass@k": pass_at_k, "pass^k": pass_hat_k, "ci95": (round(lo, 3), round(hi, 3)), "n": n}


if __name__ == "__main__":
    r = evaluate(p_correct=0.9, trials=8)
    print(r)
    # theory: pass^8 = 0.9^8 = 0.43 while pass@8 = 1 - 0.1^8 ~ 1.0 and single-trial success ~ 0.9
    assert abs(r["pass^k"] - 0.9 ** 8) < 0.12, r
    assert r["pass@k"] > 0.99 and r["pass^k"] < r["single"], r
    assert r["ci95"][0] < 0.9 < r["ci95"][1] + 0.08, r             # CI around the single-trial rate
    lo, hi = wilson(80, 100)
    assert round(lo, 2) == 0.71 and round(hi, 2) == 0.87           # known value for 80/100
    print("OK")
