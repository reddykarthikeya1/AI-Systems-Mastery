"""Tests for W3C Trace Context Propagation."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_w3c_trace_context_propagation import w3c_trace_context_propagation
except ImportError:
    from p01_w3c_trace_context_propagation import w3c_trace_context_propagation


def test_w3c_trace_context_propagation():
    parent = "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
    child = w3c_trace_context_propagation(parent, "5c35626a576a3a4b")
    assert child == "00-4bf92f3577b34da6a3ce929d0e0e4736-5c35626a576a3a4b-01"
    import pytest
    with pytest.raises(ValueError):
        w3c_trace_context_propagation("invalid-header", "1234567890abcdef")
