"""Beginner playground for Module 04 - Production Guardrails Architecture.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import re

# -------------------------------------------- 1. Input PII Redaction Regex Filter
user_input = "My SSN is 123-45-6789, please check my loan."
ssn_pattern = r"\b\d{3}-\d{2}-\d{4}\b"
sanitized = re.sub(ssn_pattern, "[REDACTED_SSN]", user_input)

assert "[REDACTED_SSN]" in sanitized
assert "123-45-6789" not in sanitized
print(f"Sanitized query: '{sanitized}'")

# -------------------------------------------- 2. Output Toxicity and Policy Interceptor
banned_keywords = {"explosive", "malware", "ransomware"}
def check_safety(output):
    for word in banned_keywords:
        if word in output.lower():
            return False, f"Policy violation: {word}"
    return True, "Safe"

safe_out, _ = check_safety("Python is an interpreted programming language.")
bad_out, reason = check_safety("How to write ransomware code")

assert safe_out is True
assert bad_out is False
print(f"Safety interceptor blocked unsafe generation: '{reason}'")

# -------------------------------------------- 3. Pipeline Latency Overhead Budget
guardrail_latency_ms = 18.5
sla_limit_ms = 50.0
assert guardrail_latency_ms < sla_limit_ms
print(f"Guardrail overhead: {guardrail_latency_ms} ms (within {sla_limit_ms} ms SLA).")

print()
print("All checks passed.")
