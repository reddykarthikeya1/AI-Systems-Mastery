# 🐣 Interactive Foundations Playground: Production Guardrails Architecture

> *"Guardrails are the security checkpoint at an airport: scan bags coming in, check passports going out."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import re
```

---

## 1. Input PII Redaction Regex Filter

Scanning user queries to redact Social Security Numbers and Credit Card numbers before sending data to external APIs.

```python
user_input = "My SSN is 123-45-6789, please check my loan."
ssn_pattern = r"\b\d{3}-\d{2}-\d{4}\b"
sanitized = re.sub(ssn_pattern, "[REDACTED_SSN]", user_input)

assert "[REDACTED_SSN]" in sanitized
assert "123-45-6789" not in sanitized
print(f"Sanitized query: '{sanitized}'")
```

---

## 2. Output Toxicity and Policy Interceptor

Intercepting generated responses that trigger banned policy violation categories.

```python
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
```

---

## 3. Pipeline Latency Overhead Budget

Guardrail evaluation must complete in under 50 ms to avoid degrading user experience.

```python
guardrail_latency_ms = 18.5
sla_limit_ms = 50.0
assert guardrail_latency_ms < sla_limit_ms
print(f"Guardrail overhead: {guardrail_latency_ms} ms (within {sla_limit_ms} ms SLA).")
```

---
