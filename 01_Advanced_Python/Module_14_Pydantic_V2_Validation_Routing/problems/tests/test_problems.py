"""Tests for Pydantic Schema Field Pruner."""
from __future__ import annotations

import pytest
from p01_schema_field_pruner import prune_sensitive_fields


def test_schema_field_pruner():
    data = {'user': 'alice', 'password_hash': 'secret', 'meta': {'token': 'abc', 'active': True}}
    c = prune_sensitive_fields(data, {'password_hash', 'token'})
    assert 'password_hash' not in c
    assert 'token' not in c['meta']
    assert c['meta']['active'] is True
