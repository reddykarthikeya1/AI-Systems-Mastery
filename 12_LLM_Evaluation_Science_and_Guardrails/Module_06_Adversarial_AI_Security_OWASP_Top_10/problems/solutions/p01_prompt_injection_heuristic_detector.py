"""Reference Solution — Problem 01: Prompt Injection Heuristic Detector

Topic: 06 Adversarial AI Security OWASP Top 10
"""

from __future__ import annotations


def prompt_injection_heuristic_detector(prompt: str) -> tuple[bool, float]:
    signatures = [
        'ignore previous instructions',
        'system prompt override',
        'you are now in developer mode',
        'dan mode'
    ]
    p = prompt.lower()
    matches = sum(1 for s in signatures if s in p)
    if matches >= 2:
        return (True, 0.99)
    elif matches == 1:
        return (True, 0.75)
    return (False, 0.05)
