"""Tests for Chunked Prefill Budget Split."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_chunked_prefill_budget_split import chunked_prefill_budget_split
except ImportError:
    from p01_chunked_prefill_budget_split import chunked_prefill_budget_split


def test_chunked_prefill_budget_split():
    assert chunked_prefill_budget_split([1, 2, 3, 4, 5, 6, 7], 3) == [[1, 2, 3], [4, 5, 6], [7]]
    assert chunked_prefill_budget_split([], 4) == []
