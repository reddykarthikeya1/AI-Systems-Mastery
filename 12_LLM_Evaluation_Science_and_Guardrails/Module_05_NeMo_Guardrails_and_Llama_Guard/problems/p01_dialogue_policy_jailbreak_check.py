"""Problem 01 — Dialogue Policy Jailbreak Check

Topic: 05 NeMo Guardrails and Llama Guard
Target: Production-grade implementation

Check prompt against prohibited topical policy keywords.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def dialogue_policy_jailbreak_check(prompt: str, prohibited_topics: list[str] | None = None) -> tuple[bool, str | None]:
    """If prohibited_topics is None, default to ['weapons', 'malware', 'biohazard'].
    If any topic appears in prompt.lower(): return (False, f"Blocked: {topic} policy").
    Else: return (True, None).
    """
    raise NotImplementedError("Implement dialogue_policy_jailbreak_check")
