"""Reference Solution — Problem 01: Dialogue Policy Jailbreak Check

Topic: 05 NeMo Guardrails and Llama Guard
"""

from __future__ import annotations


def dialogue_policy_jailbreak_check(prompt: str, prohibited_topics: list[str] | None = None) -> tuple[bool, str | None]:
    if prohibited_topics is None:
        prohibited_topics = ['weapons', 'malware', 'biohazard']
    p = prompt.lower()
    for t in prohibited_topics:
        if t in p:
            return (False, f"Blocked: {t} policy")
    return (True, None)
