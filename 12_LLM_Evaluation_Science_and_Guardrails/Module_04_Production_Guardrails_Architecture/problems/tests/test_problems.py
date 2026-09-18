"""Tests for Regex Pattern Guardrail."""
from __future__ import annotations

import pytest
from p01_regex_pattern_guardrail import regex_pattern_guardrail


def test_regex_pattern_guardrail():
    text = "User contact is test@example.com and ssn 123-45-6789."
    red, count = regex_pattern_guardrail(text)
    assert count == 2
    assert "[REDACTED_EMAIL]" in red
    assert "[REDACTED_SSN]" in red
