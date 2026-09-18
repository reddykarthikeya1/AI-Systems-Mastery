# Debug Lab Solution & Forensic Post-Mortem

## Incident: PII Guardrail Passes Social Security Numbers, Card Numbers, and Emails Straight Through Unredacted

---

### 🔍 Forensic Root Cause Analysis
`sanitize()` is a pure pass-through:

```python
def sanitize(self, text):
    return text
```

It returns its input completely unmodified, with no pattern matching, redaction, or masking logic of any kind applied to it. Every category of PII the guardrail is nominally responsible for catching -- SSNs, credit card numbers, email addresses, and by extension anything else -- survives untouched into whatever the sanitized output feeds next (logs, downstream services, model context), because there is no detection step for a redaction step to act on in the first place. The function name and its position in the pipeline imply scrubbing happens here; the implementation performs none.

---

### 🛠️ Production Corrective Action & Code Fix

```python
import re

class FixedGuardrail:
    PATTERNS = {
        "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "CARD": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
        "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    }

    def sanitize(self, text):
        for label, pattern in self.PATTERNS.items():
            text = pattern.sub(f"[REDACTED_{label}]", text)
        return text
```

Matching against known PII patterns and substituting a redaction marker for each match means the guardrail now actually transforms its input, replacing SSNs, card numbers, and email addresses with clearly labeled placeholders instead of letting them through unchanged.

---

### 🛡️ Production Prevention Invariants
1. **Test That Known PII Is Actually Removed, Not Just That the Method Runs:** A guardrail's test suite must assert specific PII patterns disappear from the output, not merely that `sanitize()` executes without raising.
2. **Treat "Output Equals Input" as a CI-Breaking Regression Check:** Assert `sanitize(fixture) != fixture` on a fixture known to contain PII, so a no-op guardrail like this one cannot ship silently.
3. **Layer Pattern-Based Redaction With a Secondary PII-Detection Model:** Regexes alone will miss novel formats; use them as a fast first pass backed by a model-based detector as defense in depth.
