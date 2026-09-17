"""Tests for Prepend Document Summary."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_prepend_document_summary import prepend_document_summary
except ImportError:
    from p01_prepend_document_summary import prepend_document_summary


def test_prepend_document_summary():
    enriched = prepend_document_summary("Q3 Earnings", "Revenue up 15%", ["Operating margin was 24%"])
    assert enriched[0] == "[Q3 Earnings: Revenue up 15%] Operating margin was 24%"
