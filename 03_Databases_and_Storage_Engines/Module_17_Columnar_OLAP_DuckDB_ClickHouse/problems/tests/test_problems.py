"""Tests for Run Length Encoding Decompress."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_run_length_encoding_decompress import run_length_encoding_decompress
except ImportError:
    from p01_run_length_encoding_decompress import run_length_encoding_decompress


def test_run_length_encoding_decompress():
    assert run_length_encoding_decompress([(3, 100), (2, 200), (1, 300)]) == [100, 100, 100, 200, 200, 300]
    assert run_length_encoding_decompress([]) == []
