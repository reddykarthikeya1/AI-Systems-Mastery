"""Problem 01 — JWT Claims Invariant Validator

Target: Production-grade implementation

Example:
    >>> valid = {'exp': 200, 'aud': 'api', 'iss': 'auth0'}
    >>> validate_jwt_claims(valid, 100, 'api', 'auth0')
    (True, 'valid')
    >>> validate_jwt_claims(valid, 250, 'api', 'auth0')
    (False, 'token_expired')

Hints:
    Hint 1: Several claims can be wrong at once, but the caller only gets one
        reason string back — decide the priority order the checks run in
        (expiry, then not-before, then audience, then issuer works well).
    Hint 2: This is a straight sequence of guard clauses over the claims
        dict, each returning `(False, "<reason>")` as soon as it fails, with
        a final `(True, "valid")` if everything passes.
    Hint 3: A missing `exp` claim must fail closed (treat it like an expired
        token) rather than raising a KeyError, and `nbf` is optional — only
        check it when the claim is actually present.
"""

from __future__ import annotations


def validate_jwt_claims(claims: dict, current_time: int, expected_aud: str, expected_iss: str) -> tuple[bool, str]:
    raise NotImplementedError('Implement validate_jwt_claims')
