# 🐣 Interactive Foundations Playground: Tool Execution & Constrained Generation

> *"Tool calling gives LLMs hands: validating JSON schemas ensures the LLM does not try to pass a square peg into a round hole."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import json
```

---

## 1. JSON Schema Parameter Validation

Validating extracted function arguments against declared required parameters and expected types.

```python
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
```

---

## 2. Safe Tool Dispatcher Map

Mapping string tool names to concrete Python callable functions with safe exception boundaries.

```python
def add(a, b): return a + b
def multiply(a, b): return a * b
tools = {"add": add, "multiply": multiply}

res1 = tools["add"](10, 5)
res2 = tools["multiply"](10, 5)

assert res1 == 15
assert res2 == 50
print(f"Dispatched tool executions: add -> {res1}, multiply -> {res2}")
```

---

## 3. Graceful Error Feedback Injection

When a tool execution fails, inject the error message as an observation so the agent can self-correct.

```python
tool_error = "ZeroDivisionError: division by zero"
feedback_prompt = f"Tool failed with error: {tool_error}. Please correct arguments and retry."
assert "ZeroDivisionError" in feedback_prompt
print(f"Self-correction feedback prepared: {feedback_prompt}")
```

---
