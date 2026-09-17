"""Problem 01 — LLM Context Window Token Truncator

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def fit_prompt_budget(system_msg: str, user_msgs: list[str], max_tokens: int) -> list[str]:
    sys_tokens = max(1, len(system_msg) // 4)
    budget = max_tokens - sys_tokens
    if budget <= 0:
        return [system_msg]
    kept = []
    for msg in reversed(user_msgs):
        t = max(1, len(msg) // 4)
        if budget >= t:
            kept.append(msg)
            budget -= t
        else:
            break
    return [system_msg] + list(reversed(kept))
