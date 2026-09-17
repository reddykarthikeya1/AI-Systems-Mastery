"""Tests for Safe Type Coercion Utility."""
from __future__ import annotations

import pytest
from p01_safe_coerce import safe_coerce


def test_safe_coerce():
    assert safe_coerce('42', 'int') == 42
    assert safe_coerce('bad', 'int', default=-1) == -1
    assert safe_coerce('true', 'bool') is True
    assert safe_coerce('no', 'bool') is False
    assert safe_coerce(None, 'int', default=0) == 0
