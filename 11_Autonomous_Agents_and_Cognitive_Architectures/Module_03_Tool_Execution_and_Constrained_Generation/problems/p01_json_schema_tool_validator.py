"""Problem 01 — Json Schema Tool Validator

Topic: 03 Tool Execution and Constrained Generation
Target: Production-grade implementation

Validate tool arguments against simple JSON schema requirements.

Example:
    >>> schema = {'required': ['city'], 'properties': {'city': {'type': 'string'}, 'days': {'type': 'integer'}}}
    >>> json_schema_tool_validator({'city': 'Tokyo', 'days': 3}, schema)
    (True, None)
    >>> json_schema_tool_validator({'days': 3}, schema)
    (False, 'Missing required property: city')

Hints:
    Hint 1: Validation is two separate passes over the schema — first
        confirm every name in schema['required'] is present in args at
        all, then, independently, check the type of whichever properties
        happen to be present.
    Hint 2: Loop over schema['required'] checking membership in args, then
        loop over schema['properties'].items() and use isinstance() against
        a type map ('string'->str, 'integer'->int, 'number'->(int, float),
        'boolean'->bool) to check each present property's value.
    Hint 3: A missing required property must be reported before any type
        check runs, and 'number' has to accept both int and float (unlike
        'integer', which is int only) — build the same string-to-type
        lookup the reference solution uses rather than ad hoc if/elif
        checks.
"""

from __future__ import annotations


def json_schema_tool_validator(args: dict, schema: dict) -> tuple[bool, str | None]:
    """schema contains:
    - 'required': list of required property names
    - 'properties': dict mapping prop -> {'type': 'string'|'integer'|'number'|'boolean'}
    Returns (is_valid, error_message).
    """
    raise NotImplementedError("Implement json_schema_tool_validator")
