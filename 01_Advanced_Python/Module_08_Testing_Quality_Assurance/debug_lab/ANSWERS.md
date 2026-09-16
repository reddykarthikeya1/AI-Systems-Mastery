# Debug Lab Answers: Module 08

<details>
<summary>Bug 1: Test order dependence via shared mutable global state</summary>

### Root Cause
Tests sharing global state create hidden execution coupling. If pytest runs tests in parallel (`pytest -n auto`) or randomized order (`pytest-random-order`), tests fail unpredictably.

### Fix
Use pytest fixtures with appropriate teardown / clean state injection:
```python
import pytest

@pytest.fixture
def clean_state():
    return []
```
</details>

<details>
<summary>Bug 2: Asserting a tuple: assert (cond, msg)</summary>

### Root Cause
`assert (a == b, "msg")` parses as `assert (<tuple>)`. In Python, `bool((False, "msg"))` is `True`. The assertion is completely vacuous and will never catch bugs!

### Fix
Remove parentheses so it parses as `assert <condition>, <message>`:
```python
assert computed_val == expected_val, "Values should match!"
```
</details>

<details>
<summary>Bug 3: Exact float comparison in test assertion</summary>

### Root Cause
IEEE-754 precision limits mean binary float representations cannot represent exact decimal sums.

### Fix
Use `pytest.approx()`:
```python
import pytest

assert val == pytest.approx(0.3)
```
</details>
