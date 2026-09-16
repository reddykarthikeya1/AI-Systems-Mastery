"""Production Guardrail Pipeline with PII Masking and Policy Enforcement."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class GuardrailResult:
    is_safe: bool
    sanitized_text: str
    violations: List[str] = field(default_factory=list)
    entities_masked: List[str] = field(default_factory=list)


class ProductionGuardrailPipeline:
    """Multi-stage input and output safety guardrail pipeline."""

    PII_RULES = {
        "EMAIL": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
        "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "CREDIT_CARD": re.compile(r"\b(?:\d{4}[- ]?){3}\d{4}\b"),
        "PHONE": re.compile(r"\b(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b"),
    }

    FORBIDDEN_KEYWORDS = {
        "drop table",
        "rm -rf",
        "bypass security",
        "ignore all previous instructions",
    }

    def __init__(self, blocked_topics: Optional[List[str]] = None) -> None:
        self.blocked_topics = [t.lower() for t in (blocked_topics or [])]

    def scan_and_mask_pii(self, text: str) -> tuple[str, List[str]]:
        """Detects and masks PII entities with canonical placeholders."""
        sanitized = text
        masked_types = []

        for pii_name, pattern in self.PII_RULES.items():
            matches = pattern.findall(sanitized)
            if matches:
                masked_types.append(pii_name)
                sanitized = pattern.sub(f"[REDACTED_{pii_name}]", sanitized)

        return sanitized, masked_types

    def inspect_input_safety(self, text: str) -> GuardrailResult:
        """Pre-flight inspection: checks forbidden keywords and masks PII."""
        lower_text = text.lower()
        violations = []

        for kw in self.FORBIDDEN_KEYWORDS:
            if kw in lower_text:
                violations.append(f"Forbidden command/injection pattern: '{kw}'")

        for topic in self.blocked_topics:
            if topic in lower_text:
                violations.append(f"Blocked topic detected: '{topic}'")

        sanitized, masked = self.scan_and_mask_pii(text)
        is_safe = len(violations) == 0

        return GuardrailResult(
            is_safe=is_safe,
            sanitized_text=sanitized if is_safe else "Input rejected by safety policy.",
            violations=violations,
            entities_masked=masked,
        )

    def inspect_output_safety(self, text: str) -> GuardrailResult:
        """Post-flight inspection: masks any accidentally emitted PII or credentials."""
        sanitized, masked = self.scan_and_mask_pii(text)
        return GuardrailResult(
            is_safe=True,
            sanitized_text=sanitized,
            violations=[],
            entities_masked=masked,
        )
