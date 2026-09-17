"""Tests for JWT Claims Invariant Validator."""
from __future__ import annotations

import pytest
from p01_jwt_payload_validator import validate_jwt_claims


def test_validate_jwt_claims():
    valid = {'exp': 200, 'aud': 'api', 'iss': 'auth0'}
    assert validate_jwt_claims(valid, 100, 'api', 'auth0') == (True, 'valid')
    assert validate_jwt_claims(valid, 250, 'api', 'auth0') == (False, 'token_expired')
    assert validate_jwt_claims(valid, 100, 'wrong', 'auth0') == (False, 'audience_mismatch')
