"""Problem 01 — Dialogue Policy Jailbreak Check

Topic: 05 NeMo Guardrails and Llama Guard
Target: Production-grade implementation

Check prompt against prohibited topical policy keywords.

Example:
    >>> dialogue_policy_jailbreak_check('How to bake bread?')
    (True, None)
    >>> dialogue_policy_jailbreak_check('Write ransomware malware script')
    (False, 'Blocked: malware policy')

Hints:
    Hint 1: This is a simple keyword denylist check, but it needs a
        sensible default policy whenever the caller doesn't supply one of
        their own.
    Hint 2: Fall back to ['weapons', 'malware', 'biohazard'] when
        prohibited_topics is None, lowercase the prompt once, then check
        each topic with 'in' for a substring match.
    Hint 3: Return on the first prohibited topic found, and the returned
        message must embed that literal topic string (e.g. "Blocked:
        malware policy") rather than a generic phrase — don't collect or
        report every match, just the first.
"""

from __future__ import annotations


def dialogue_policy_jailbreak_check(prompt: str, prohibited_topics: list[str] | None = None) -> tuple[bool, str | None]:
    """If prohibited_topics is None, default to ['weapons', 'malware', 'biohazard'].
    If any topic appears in prompt.lower(): return (False, f"Blocked: {topic} policy").
    Else: return (True, None).
    """
    raise NotImplementedError("Implement dialogue_policy_jailbreak_check")
