"""Beginner playground for Module 03 - Tool Execution & Constrained Generation.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import json

# -------------------------------------------- 1. JSON Schema Parameter Validation
tool_schema = {
    "name": "send_email",
    "required": ["recipient", "subject"],
    "properties": {"recipient": str, "subject": str, "body": str}
}

def validate_call(args, schema):
    for req in schema["required"]:
        if req not in args:
            return False, f"Missing required parameter: {req}"
        if not isinstance(args[req], schema["properties"][req]):
            return False, f"Invalid type for {req}"
    return True, "Valid"

ok, msg = validate_call({"recipient": "alice@example.com", "subject": "Hi"}, tool_schema)
bad, _ = validate_call({"recipient": "alice@example.com"}, tool_schema)

assert ok is True
assert bad is False
print(f"Tool validation: success={ok}, missing parameter detected={not bad}")

# -------------------------------------------- 2. Safe Tool Dispatcher Map
def add(a, b): return a + b
def multiply(a, b): return a * b
tools = {"add": add, "multiply": multiply}

res1 = tools["add"](10, 5)
res2 = tools["multiply"](10, 5)

assert res1 == 15
assert res2 == 50
print(f"Dispatched tool executions: add -> {res1}, multiply -> {res2}")

# -------------------------------------------- 3. Graceful Error Feedback Injection
tool_error = "ZeroDivisionError: division by zero"
feedback_prompt = f"Tool failed with error: {tool_error}. Please correct arguments and retry."
assert "ZeroDivisionError" in feedback_prompt
print(f"Self-correction feedback prepared: {feedback_prompt}")

print()
print("All checks passed.")
