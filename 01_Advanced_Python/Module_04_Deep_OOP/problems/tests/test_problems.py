"""Tests for Data Descriptor Validation."""
from __future__ import annotations

import pytest
from p01_validate_descriptor import TypedField


import pytest

def test_validate_descriptor():
    class Person:
        age = TypedField(int)
    p = Person()
    p.age = 25
    assert p.age == 25
    with pytest.raises(TypeError):
        p.age = 'invalid'
