# Beginner Playground: Production Guardrails & PII Masking

Welcome to Production Guardrails! Deploying LLMs to real users without guardrails risks data leaks, toxic responses, and regulatory fines.

---

## 1. The Core Mental Model: Pre-Flight, In-Flight, and Post-Flight

```
 [ User Input ]
       |
       v
 [ Pre-Flight Guardrail ]    --> (Detects prompt injection & masks incoming PII)
       |
       v
 [ LLM Inference Engine ]    --> (Streams generated tokens)
       |
       v
 [ Post-Flight Guardrail ]   --> (Redacts SSNs/Credit Cards & verifies topic boundaries)
       |
       v
 [ Safe Clean Output ]
```

---

## 2. Interactive Pure-Python Experiment: Zero-Dependency PII Anonymizer

```python
import re

PII_PATTERNS = {
    "EMAIL": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "CREDIT_CARD": re.compile(r"\b(?:\d{4}[- ]?){3}\d{4}\b"),
}

def mask_pii(text: str) -> tuple[str, list]:
    detected = []
    sanitized = text
    for pii_type, pattern in PII_PATTERNS.items():
        matches = pattern.findall(sanitized)
        if matches:
            detected.extend([(pii_type, m) for m in matches])
            sanitized = pattern.sub(f"[REDACTED_{pii_type}]", sanitized)
    return sanitized, detected

sample = "Contact John at john.doe@enterprise.com with SSN 123-45-6789 for payment."
clean_text, leaked = mask_pii(sample)
print("Original Text:", sample)
print("Sanitized Text:", clean_text)
print("Leaked Entities Detected:", leaked)
```
