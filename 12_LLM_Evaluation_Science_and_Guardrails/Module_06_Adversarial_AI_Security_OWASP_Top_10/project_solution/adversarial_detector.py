"""Production Adversarial Security Scanner for LLM Prompt Injections."""

from __future__ import annotations

import base64
import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ThreatReport:
    is_safe: bool
    owasp_category: Optional[str] = None
    threat_level: str = "LOW"  # LOW, MEDIUM, CRITICAL
    detected_patterns: List[str] = field(default_factory=list)
    decoded_payloads: List[str] = field(default_factory=list)


class AdversarialSecurityScanner:
    """Scans inputs for direct injection, obfuscation, and prompt extraction."""

    INJECTION_PATTERNS = [
        (re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions", re.IGNORECASE), "LLM01", "CRITICAL"),
        (re.compile(r"you\s+are\s+now\s+(?:in\s+)?developer\s+mode", re.IGNORECASE), "LLM01", "CRITICAL"),
        (re.compile(r"(?:\bDAN\b|do\s+anything\s+now)", re.IGNORECASE), "LLM01", "CRITICAL"),
        (re.compile(r"disregard\s+(?:all\s+)?safety\s+guidelines", re.IGNORECASE), "LLM01", "CRITICAL"),
        (re.compile(r"print\s+(?:your\s+)?(?:system\s+prompt|initial\s+instructions)", re.IGNORECASE), "LLM02", "HIGH"),
        (re.compile(r"repeat\s+the\s+words\s+above", re.IGNORECASE), "LLM02", "MEDIUM"),
    ]

    BASE64_REGEX = re.compile(r"[A-Za-z0-9+/]{12,}={0,2}")

    def decode_obfuscations(self, text: str) -> List[str]:
        """Finds and decodes valid Base64 payload strings."""
        decoded_strings = []
        for candidate in self.BASE64_REGEX.findall(text):
            if len(candidate) % 4 != 0:
                continue
            try:
                raw_bytes = base64.b64decode(candidate)
                decoded_str = raw_bytes.decode("utf-8")
                # Ensure it's legible text
                if all(c.isprintable() or c.isspace() for c in decoded_str) and len(decoded_str) > 4:
                    decoded_strings.append(decoded_str)
            except Exception:
                continue
        return decoded_strings

    def scan(self, text: str) -> ThreatReport:
        """Performs multi-layer adversarial threat audit."""
        detected_patterns = []
        highest_threat = "LOW"
        primary_owasp = None

        # Check raw text
        for pattern, owasp, level in self.INJECTION_PATTERNS:
            if pattern.search(text):
                detected_patterns.append(f"Pattern '{pattern.pattern}' in raw input")
                highest_threat = level
                primary_owasp = owasp

        # Check decoded obfuscations
        decoded_payloads = self.decode_obfuscations(text)
        for payload in decoded_payloads:
            for pattern, owasp, level in self.INJECTION_PATTERNS:
                if pattern.search(payload):
                    detected_patterns.append(f"Pattern '{pattern.pattern}' in obfuscated Base64: '{payload}'")
                    highest_threat = "CRITICAL"
                    primary_owasp = owasp

        is_safe = len(detected_patterns) == 0

        return ThreatReport(
            is_safe=is_safe,
            owasp_category=primary_owasp,
            threat_level=highest_threat if not is_safe else "LOW",
            detected_patterns=detected_patterns,
            decoded_payloads=decoded_payloads,
        )
