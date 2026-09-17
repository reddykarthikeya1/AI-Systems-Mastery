"""Tests for Json Schema Tool Validator."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_json_schema_tool_validator import json_schema_tool_validator
except ImportError:
    from p01_json_schema_tool_validator import json_schema_tool_validator


def test_json_schema_tool_validator():
    schema = {
        'required': ['city'],
        'properties': {'city': {'type': 'string'}, 'days': {'type': 'integer'}}
    }
    ok, err = json_schema_tool_validator({'city': 'Tokyo', 'days': 3}, schema)
    assert ok is True and err is None
    ok2, err2 = json_schema_tool_validator({'days': 3}, schema)
    assert ok2 is False
