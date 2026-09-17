"""Problem 01 — Json Schema Tool Validator

Topic: 03 Tool Execution and Constrained Generation
Target: Production-grade implementation

Validate tool arguments against simple JSON schema requirements.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def json_schema_tool_validator(args: dict, schema: dict) -> tuple[bool, str | None]:
    """schema contains:
    - 'required': list of required property names
    - 'properties': dict mapping prop -> {'type': 'string'|'integer'|'number'|'boolean'}
    Returns (is_valid, error_message).
    """
    raise NotImplementedError("Implement json_schema_tool_validator")
