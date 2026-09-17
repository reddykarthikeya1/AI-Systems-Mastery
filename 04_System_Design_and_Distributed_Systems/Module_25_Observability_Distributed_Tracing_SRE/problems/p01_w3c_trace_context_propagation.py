"""Problem 01 — W3C Trace Context Propagation

Topic: 25 Observability Distributed Tracing SRE
Target: Production-grade implementation

Parse, validate, and generate child W3C traceparent header.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def w3c_trace_context_propagation(traceparent_header: str, new_span_id: str) -> str:
    """W3C traceparent format: f"{version}-{trace_id}-{parent_id}-{trace_flags}".
    Valid format:
    - version: 2 hex characters ('00')
    - trace_id: 32 hex characters
    - parent_id: 16 hex characters
    - trace_flags: 2 hex characters
    Parse header, replace parent_id with new_span_id, and return valid child traceparent string.
    If header format is invalid, raise ValueError("Invalid W3C traceparent").
    """
    raise NotImplementedError("Implement w3c_trace_context_propagation")
