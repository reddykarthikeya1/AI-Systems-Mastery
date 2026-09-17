"""Reference Solution — Problem 01: Json Schema Tool Validator

Topic: 03 Tool Execution and Constrained Generation
"""

from __future__ import annotations


def json_schema_tool_validator(args: dict, schema: dict) -> tuple[bool, str | None]:
    for req in schema.get('required', []):
        if req not in args:
            return (False, f"Missing required property: {req}")
    type_map = {
        'string': str,
        'integer': int,
        'number': (int, float),
        'boolean': bool
    }
    for prop, prop_schema in schema.get('properties', {}).items():
        if prop in args:
            exp_type = type_map.get(prop_schema.get('type'))
            if exp_type and not isinstance(args[prop], exp_type):
                return (False, f"Invalid type for {prop}: expected {prop_schema.get('type')}")
    return (True, None)
