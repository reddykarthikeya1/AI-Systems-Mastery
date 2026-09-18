"""Problem 01 — W3C Trace Context Propagation

Topic: 25 Observability Distributed Tracing SRE
Target: Production-grade implementation

Parse, validate, and generate child W3C traceparent header.

Example:
    >>> w3c_trace_context_propagation("00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01", "5c35626a576a3a4b")
    '00-4bf92f3577b34da6a3ce929d0e0e4736-5c35626a576a3a4b-01'

Hints:
    Hint 1: The traceparent header is a fixed 4-field, dash-delimited
        record -- validating it is about checking exact field COUNT and
        exact per-field character length, not general string parsing.
    Hint 2: Split the header on '-', verify it produced exactly 4 parts,
        check each part's length (2 / 32 / 16 / 2 characters for
        version / trace_id / parent_id / trace_flags), then rebuild the
        string with `new_span_id` swapped in for the parent_id field.
    Hint 3: Any malformed input -- wrong part count OR any field length
        off -- must raise `ValueError("Invalid W3C traceparent")` rather
        than let an IndexError leak out of the parsing; `new_span_id`
        itself must also be checked for exactly 16 characters before
        being spliced into the child header.
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
