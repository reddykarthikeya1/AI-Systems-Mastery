"""Broken guardrail with zero regex escaping or PII detection."""

class BrokenGuardrail:
    def sanitize(self, text):
        # BUG: Returns raw text without PII sanitization
        return text
