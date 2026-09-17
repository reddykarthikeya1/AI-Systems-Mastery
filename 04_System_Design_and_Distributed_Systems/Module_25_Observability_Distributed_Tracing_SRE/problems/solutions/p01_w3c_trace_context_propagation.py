"""Reference Solution — Problem 01: W3C Trace Context Propagation

Topic: 25 Observability Distributed Tracing SRE
"""

from __future__ import annotations


def w3c_trace_context_propagation(traceparent_header: str, new_span_id: str) -> str:
    parts = traceparent_header.strip().split('-')
    if len(parts) != 4:
        raise ValueError("Invalid W3C traceparent")
    version, trace_id, parent_id, flags = parts
    if len(version) != 2 or len(trace_id) != 32 or len(parent_id) != 16 or len(flags) != 2:
        raise ValueError("Invalid W3C traceparent")
    if len(new_span_id) != 16:
        raise ValueError("Invalid child span id")
    return f"{version}-{trace_id}-{new_span_id}-{flags}"
