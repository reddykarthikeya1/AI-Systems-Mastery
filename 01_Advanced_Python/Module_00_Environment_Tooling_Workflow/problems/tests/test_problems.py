"""Tests for Parse pyproject.toml Dependencies."""
from __future__ import annotations

import pytest
from p01_parse_dependencies import parse_dependencies


def test_parse_dependencies():
    specs = ['fastapi>=0.100.0', ' uvicorn==0.28.0 ', '# test', 'pytest']
    r = parse_dependencies(specs)
    assert r['fastapi'] == '>=0.100.0'
    assert r['uvicorn'] == '==0.28.0'
    assert r['pytest'] == '*'
    assert parse_dependencies([]) == {}
