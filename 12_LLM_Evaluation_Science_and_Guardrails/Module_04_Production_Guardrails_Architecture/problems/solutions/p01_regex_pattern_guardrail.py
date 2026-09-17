"""Reference Solution — Problem 01: Regex Pattern Guardrail

Topic: 04 Production Guardrails Architecture
"""

from __future__ import annotations


def regex_pattern_guardrail(text: str) -> tuple[str, int]:
    import re
    email_pat = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    ssn_pat = r'\b\d{3}-\d{2}-\d{4}\b'
    
    violations = len(re.findall(email_pat, text)) + len(re.findall(ssn_pat, text))
    t1 = re.sub(email_pat, '[REDACTED_EMAIL]', text)
    t2 = re.sub(ssn_pat, '[REDACTED_SSN]', t1)
    return (t2, violations)
