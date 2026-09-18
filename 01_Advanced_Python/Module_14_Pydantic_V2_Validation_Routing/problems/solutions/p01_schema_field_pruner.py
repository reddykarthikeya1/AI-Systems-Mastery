"""Problem 01 — Pydantic Schema Field Pruner

Target: Production-grade implementation
"""

from __future__ import annotations


def prune_sensitive_fields(payload: dict, disallowed: set[str]) -> dict:
    cleaned = {}
    for k, v in payload.items():
        if k in disallowed: continue
        if isinstance(v, dict):
            cleaned[k] = prune_sensitive_fields(v, disallowed)
        elif isinstance(v, list):
            cleaned[k] = [prune_sensitive_fields(i, disallowed) if isinstance(i, dict) else i for i in v]
        else:
            cleaned[k] = v
    return cleaned
