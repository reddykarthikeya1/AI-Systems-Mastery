"""Problem 01 — JWT Claims Invariant Validator

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def validate_jwt_claims(claims: dict, current_time: int, expected_aud: str, expected_iss: str) -> tuple[bool, str]:
    if 'exp' not in claims or claims['exp'] < current_time:
        return False, 'token_expired'
    if 'nbf' in claims and claims['nbf'] > current_time:
        return False, 'token_not_yet_valid'
    if claims.get('aud') != expected_aud:
        return False, 'audience_mismatch'
    if claims.get('iss') != expected_iss:
        return False, 'issuer_mismatch'
    return True, 'valid'
