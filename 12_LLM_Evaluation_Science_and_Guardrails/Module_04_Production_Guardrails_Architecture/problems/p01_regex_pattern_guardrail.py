"""Problem 01 — Regex Pattern Guardrail

Topic: 04 Production Guardrails Architecture
Target: Production-grade implementation

Detect and mask PII (email addresses and SSNs) in text with redaction tokens.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def regex_pattern_guardrail(text: str) -> tuple[str, int]:
    """Replace emails with '[REDACTED_EMAIL]' and SSN pattern (ddd-dd-dddd) with '[REDACTED_SSN]'.
    Returns (redacted_text, total_violations_count).
    """
    raise NotImplementedError("Implement regex_pattern_guardrail")
