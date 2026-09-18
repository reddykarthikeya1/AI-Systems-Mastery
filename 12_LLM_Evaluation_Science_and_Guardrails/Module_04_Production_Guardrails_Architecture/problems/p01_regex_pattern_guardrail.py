"""Problem 01 — Regex Pattern Guardrail

Topic: 04 Production Guardrails Architecture
Target: Production-grade implementation

Detect and mask PII (email addresses and SSNs) in text with redaction tokens.

Example:
    >>> regex_pattern_guardrail('User contact is test@example.com and ssn 123-45-6789.')
    ('User contact is [REDACTED_EMAIL] and ssn [REDACTED_SSN].', 2)

Hints:
    Hint 1: There are two independent PII shapes to catch here, and the
        count you return has to reflect how many matches were found, not
        how many redaction tokens end up in the final text.
    Hint 2: Write one regex for email addresses and one for the
        ddd-dd-dddd SSN pattern, use re.findall with each to tally
        violations, then re.sub each pattern with its redaction token to
        build the final text.
    Hint 3: Anchor the SSN pattern with a \b word boundary so it doesn't
        match digit runs embedded in a longer number, and apply both
        substitutions to the same original text in sequence rather than
        re-scanning already-redacted output (so a token like
        "[REDACTED_EMAIL]" is never itself matched by the SSN pattern).
"""

from __future__ import annotations


def regex_pattern_guardrail(text: str) -> tuple[str, int]:
    """Replace emails with '[REDACTED_EMAIL]' and SSN pattern (ddd-dd-dddd) with '[REDACTED_SSN]'.
    Returns (redacted_text, total_violations_count).
    """
    raise NotImplementedError("Implement regex_pattern_guardrail")
