# 🐣 Interactive Foundations Playground: Error Handling, Logging & Robustness

> *"Defensive programming makes failure modes explicit and trackable."*

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
import logging
```

---

## 1. Custom Exception Hierarchies

Domain-specific exceptions enable precise error handling and categorization.

```python
class DomainError(Exception):
    pass

class ValidationFailure(DomainError):
    pass

def validate_age(age):
    if age < 0:
        raise ValidationFailure("Age cannot be negative")
    return True

assert validate_age(20) is True
try:
    validate_age(-5)
except ValidationFailure as exc:
    assert isinstance(exc, DomainError)
    print(f"Caught expected domain error: {exc}")
```

---

## 2. Exception Chaining with 'from'

Explicit exception chaining preserves the root cause in the `__cause__` attribute.

```python
def parse_config(value):
    try:
        return int(value)
    except ValueError as err:
        raise DomainError("Configuration integer required") from err

try:
    parse_config("invalid")
except DomainError as err:
    assert isinstance(err.__cause__, ValueError)
    print(f"Exception chained from root cause: {type(err.__cause__).__name__}")
```

---

## 3. Configuring Standard Logging

The standard logging module allows setting log thresholds and custom formatters.

```python
logger = logging.getLogger("module06_test")
logger.setLevel(logging.INFO)
assert logger.level == logging.INFO
assert logger.isEnabledFor(logging.INFO)
assert not logger.isEnabledFor(logging.DEBUG)
print("Logger configured with level INFO.")
```

---
