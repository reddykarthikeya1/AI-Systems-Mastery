"""Problem 01 — Prompt Injection Heuristic Detector

Topic: 06 Adversarial AI Security OWASP Top 10
Target: Production-grade implementation

Detect prompt injection signatures such as 'ignore previous instructions'.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def prompt_injection_heuristic_detector(prompt: str) -> tuple[bool, float]:
    """Check for injection phrases:
    - 'ignore previous instructions'
    - 'system prompt override'
    - 'you are now in developer mode'
    - 'dan mode'
    If 1 phrase found: return (True, 0.75).
    If >= 2 phrases found: return (True, 0.99).
    If 0 found: return (False, 0.05).
    """
    raise NotImplementedError("Implement prompt_injection_heuristic_detector")
