"""Problem 01 — ASGI Trie Path Router

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def match_asgi_route(routes: dict[str, str], path: str) -> tuple[str, dict]:
    path_parts = path.strip('/').split('/')
    for pattern, endpoint in routes.items():
        pat_parts = pattern.strip('/').split('/')
        if len(path_parts) != len(pat_parts): continue
        params = {}
        matched = True
        for pp, patp in zip(path_parts, pat_parts):
            if patp.startswith('{') and patp.endswith('}'):
                params[patp[1:-1]] = pp
            elif pp != patp:
                matched = False
                break
        if matched:
            return endpoint, params
    return '', {}
