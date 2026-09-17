# 🐣 Interactive Foundations Playground: Pydantic & Data Validation

> *"Type hints become runtime contracts that validate, sanitize, and enforce data boundaries."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from typing import get_type_hints
```

---

## 1. Introspecting Type Annotations

Python's `typing.get_type_hints` inspects dataclass and function signatures at runtime.

```python
class UserSchema:
    name: str
    age: int
    active: bool

hints = get_type_hints(UserSchema)
assert hints["name"] is str
assert hints["age"] is int
assert hints["active"] is bool
print(f"Extracted type hints: {hints}")
```

---

## 2. Runtime Type Coercion and Validation

Validating fields against type hints ensures input payloads match the expected schema.

```python
def validate_payload(data, schema):
    hints = get_type_hints(schema)
    validated = {}
    for key, expected_type in hints.items():
        if key not in data:
            raise ValueError(f"Missing field {key}")
        raw = data[key]
        validated[key] = expected_type(raw)
    return validated

data = {"name": "Charlie", "age": "28", "active": 1}
res = validate_payload(data, UserSchema)
assert res["age"] == 28
assert isinstance(res["age"], int)
assert res["name"] == "Charlie"
print(f"Validated and coerced payload: {res}")
```

---

## 3. Field Constraint Checking

Custom validators check value ranges and string patterns beyond simple primitive types.

```python
def check_age_bounds(age):
    assert 0 <= age <= 120, "Age out of bounds"
    return True

assert check_age_bounds(25) is True
assert check_age_bounds(0) is True
print("Age boundary constraints verified.")
```

---
