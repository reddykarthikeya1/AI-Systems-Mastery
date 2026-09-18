"""Tests for Bson Size Validator."""
from __future__ import annotations

import pytest
from p01_bson_size_validator import bson_size_validator


def test_bson_size_validator():
    doc = {"name": "Alice", "active": True, "score": 42}
    valid, sz = bson_size_validator(doc)
    assert valid is True
    assert sz > 20
    valid_small, _ = bson_size_validator(doc, max_bytes=10)
    assert valid_small is False
