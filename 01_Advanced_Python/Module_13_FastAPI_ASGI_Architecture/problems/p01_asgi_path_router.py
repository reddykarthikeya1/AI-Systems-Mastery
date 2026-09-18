"""Problem 01 — ASGI Trie Path Router

Target: Production-grade implementation

Example:
    >>> routes = {'/users/{id}': 'get_user', '/items': 'list_items'}
    >>> match_asgi_route(routes, '/users/42')
    ('get_user', {'id': '42'})
    >>> match_asgi_route(routes, '/unknown')
    ('', {})

Hints:
    Hint 1: A route pattern and a request path line up segment by segment —
        most segments must match literally, but a `{name}` segment matches
        anything and captures it instead.
    Hint 2: Split both the pattern and the path on `/` (after stripping
        leading/trailing slashes) and zip the two part-lists together,
        building a `params` dict for any `{...}` segment as you go.
    Hint 3: Reject a pattern outright when its part count differs from the
        path's (no partial-length matches), and when nothing matches, return
        `('', {})` rather than `None` or raising — the tests check the empty
        string sentinel specifically for unknown paths.
"""

from __future__ import annotations


def match_asgi_route(routes: dict[str, str], path: str) -> tuple[str, dict]:
    raise NotImplementedError('Implement match_asgi_route')
