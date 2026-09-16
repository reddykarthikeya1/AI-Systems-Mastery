# Module 08: Self-Assessment Quiz & Mastery Challenges

Test your understanding of unit testing, `pytest` fixtures, mocking, and property-based testing before moving to **Module 09**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **The Test Pyramid:** What proportion of tests in a healthy codebase should be Unit Tests versus End-to-End (E2E) tests, and why?
2. **Assertion Rewriting:** Why does `pytest` allow using plain Python `assert a == b` instead of requiring special assertion methods like `self.assertEqual(a, b)`?
3. **Parametrization:** What is the primary advantage of `@pytest.mark.parametrize` over running a `for` loop of assertions inside a single test function?
4. **Fixture Scoping:** What are the 4 fixture scopes supported by `pytest`, and what is the default scope?
5. **Teardown Lifecycle:** How do you execute cleanup code in a Pytest fixture after a test finishes running?
6. **Mocking Rules:** State the golden rule of "Where to Patch" when using `unittest.mock.patch`.
7. **Mock Behavior:** What is the difference in behavior between setting `mock_fn.return_value = 10` and `mock_fn.side_effect = Exception("Crash")`?
8. **Mock Safety:** Why is `MagicMock(autospec=True)` safer than an unconstrained `MagicMock()`?
9. **Property-Based Testing:** How does property-based testing with `hypothesis` differ fundamentally from standard example-based unit tests?
10. **Coverage Metrics:** What is the difference between Statement Coverage and Branch Coverage in `pytest-cov`?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
Approximately **70% Unit Tests, 20% Integration Tests, and 10% E2E Tests**. Unit tests run in milliseconds and pinpoint exact code failures, whereas E2E tests are slow, expensive to maintain, and brittle.

#### Answer 2:
`pytest` intercepts and rewrites Python's AST bytecode at test discovery time, extracting sub-expression values so that failing `assert a == b` statements print detailed visual diffs without verbose helper methods.

#### Answer 3:
If an assertion fails inside a `for` loop, the test stops immediately and skips all remaining inputs. `@pytest.mark.parametrize` treats each parameter combination as an **independent test case**, reporting exact passes and failures for every single vector.

#### Answer 4:
1. `function` (Default: runs fresh for every test function)
2. `class` (runs once per test class)
3. `module` (runs once per `.py` test file)
4. `session` (runs once per entire test suite execution)

#### Answer 5:
Use a **`yield` fixture**: Code before `yield` runs during setup; the value yielded is injected into the test; code after `yield` runs during teardown.

#### Answer 6:
**"Patch where an object is looked up, not where it is defined."** If `module_a.py` does `import requests`, patch `'module_a.requests'`, not `'requests.get'`.

#### Answer 7:
- `return_value` returns the specified object every time the mock is called.
- `side_effect` can raise an exception when called, or yield different return values sequentially if passed an iterable.

#### Answer 8:
`autospec=True` inspects the real class signature and raises an `AttributeError` if your test calls a nonexistent method or passes incorrect arguments, preventing mock attribute drift.

#### Answer 9:
Example-based tests test specific hardcoded inputs chosen by the developer. Property-based tests define universal invariants (e.g. "Sorting never loses elements") and let `hypothesis` generate hundreds of randomized, adversarial inputs (null bytes, huge numbers, emojis) to find edge-case crashes.

#### Answer 10:
- **Statement Coverage:** Percentage of code lines executed by tests.
- **Branch Coverage:** Checks whether both branches (`True` and `False`) of every `if` statement and conditional were executed.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Testing an External Weather Client with Mocking

**Goal:** Write a complete test suite for `WeatherClient.get_temperature(city)` that mocks out the underlying network call.

<details>
<summary><b>Solution Code</b></summary>

```python
from unittest.mock import MagicMock
import pytest

class WeatherClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_temperature(self, city: str) -> float:
        response = self.api_client.fetch(f"/weather/{city}")
        if response.get("status") != 200:
            raise ValueError("City not found")
        return response["temp_c"]

def test_get_temperature_success():
    mock_api = MagicMock()
    mock_api.fetch.return_value = {"status": 200, "temp_c": 21.5}

    client = WeatherClient(mock_api)
    temp = client.get_temperature("Austin")

    assert temp == 21.5
    mock_api.fetch.assert_called_once_with("/weather/Austin")

def test_get_temperature_city_not_found():
    mock_api = MagicMock()
    mock_api.fetch.return_value = {"status": 404}

    client = WeatherClient(mock_api)
    with pytest.raises(ValueError):
        client.get_temperature("InvalidCity")
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Test order dependence

```python
CACHE: dict[str, int] = {}

def test_populates_cache() -> None:
    CACHE["a"] = 1
    assert len(CACHE) == 1

def test_cache_starts_empty() -> None:
    assert len(CACHE) == 0
```

**Observed symptom:** Both pass when run individually. Run together, the second fails. Run with `-p no:randomly` in the other order, both pass.

**(a)** What is the actual defect?

**(b)** Name two mechanisms pytest gives you to fix it.

**(c)** Why is a test suite that only passes in one order dangerous even if it is green?

<details>
<summary><b>Show the diagnosis</b></summary>

Module-level mutable state (`CACHE`) is shared across tests. Test one leaves it dirty; test two asserts on a clean slate.

**Fixes:** a `@pytest.fixture` with `autouse=True` that clears or rebuilds the state per test, or `monkeypatch` to install a fresh object. Best of all: don't use module-level mutable state — pass the cache in.

**Why it is dangerous:** the suite is asserting less than you think. Order-dependent tests hide real bugs, break unpredictably under `-x`, parallelisation (`pytest-xdist`) or randomisation, and mean a single test's failure can be caused by an unrelated one. Green is not the same as correct.

</details>

---

### D2. Assert on a tuple is always true

```python
def test_values() -> None:
    result = 2 + 2
    assert (result == 5, "arithmetic is broken")
```

**Observed symptom:** The test passes.

**(a)** Why does this pass despite `2 + 2 != 5`?

**(b)** What is the correct form?

**(c)** What does pytest do to help you catch this?

<details>
<summary><b>Show the diagnosis</b></summary>

`assert (expr, msg)` asserts a **two-element tuple**, which is always truthy. The comparison is evaluated and thrown away.

**Correct:** `assert result == 5, 'arithmetic is broken'` — comma outside the parentheses, no tuple.

**pytest helps:** it emits a warning for an assert on a non-empty tuple, and `ruff` flags it as `F631`. This course's CI runs `ruff`, so the linter catches it before review. That is the general lesson: a linter is a test for your tests.

</details>

---

### D3. Float equality in a test

```python
def test_total() -> None:
    prices = [0.1, 0.2]
    assert sum(prices) == 0.3
```

**Observed symptom:** Fails with `assert 0.30000000000000004 == 0.3`.

**(a)** Why is the sum not exactly 0.3?

**(b)** What should the assertion be?

**(c)** When is `Decimal` the right answer instead of a tolerance?

<details>
<summary><b>Show the diagnosis</b></summary>

Binary floating point cannot represent 0.1 or 0.2 exactly (IEEE 754), so the sum carries a representation error of ~4e-17. Module 01 introduces this; here it has consequences.

**Fix:** `assert sum(prices) == pytest.approx(0.3)`, or `pytest.approx(0.3, abs=1e-9)` when you want an explicit tolerance.

**Use `Decimal`** when the values are *money or any exact decimal quantity* and the rounding rules are part of the specification. A tolerance is right for physical measurement; exact decimal arithmetic is right for a ledger. Module 08's financial ledger project uses `Decimal` for precisely this reason.

</details>

---

### D4. Mock asserts nothing

```python
from unittest.mock import Mock

def notify(client, user_id: int) -> None:
    client.send(user_id)

def test_notify() -> None:
    client = Mock()
    notify(client, 42)
    client.send_notification.assert_called_once()
```

**Observed symptom:** The test passes, even though `notify` calls `send`, not `send_notification`.

**(a)** Why does asserting on the wrong method name still pass?

**(b)** What single argument to `Mock` prevents this whole class of bug?

**(c)** What is the more robust alternative to mocking here?

<details>
<summary><b>Show the diagnosis</b></summary>

A plain `Mock` auto-creates any attribute you touch. `client.send_notification` springs into existence as a new Mock, and `assert_called_once` on it... also auto-creates. Nothing is verified.

Wait — `assert_called_once` on a never-called mock *does* fail. The subtler bug is that `client.send_notification` exists at all: if you assert `assert_not_called()` or check `call_count == 0`, you get a false pass, and a typo in a method name is never caught.

**Fix:** `Mock(spec=RealClient)` or `autospec=True`, which raises `AttributeError` for any method the real class does not have.

**More robust:** inject a small hand-written fake that implements a `Protocol` (Module 23). It cannot drift from the interface, and the type checker verifies it.

</details>

---

### D5. Property-based test with a hidden assumption

```python
from hypothesis import given, strategies as st

def average(xs: list[float]) -> float:
    return sum(xs) / len(xs)

@given(st.lists(st.floats()))
def test_average_within_bounds(xs: list[float]) -> None:
    assert min(xs) <= average(xs) <= max(xs)
```

**Observed symptom:** Hypothesis reports a falsifying example of `[]`, then `[nan]`, then `[inf, -inf]`.

**(a)** Name the three distinct defects Hypothesis found.

**(b)** Which are bugs in `average` and which are bugs in the test?

**(c)** How do you express the constraints properly?

<details>
<summary><b>Show the diagnosis</b></summary>

**Three failures, three causes.** `[]` → `ZeroDivisionError`: a genuine bug in `average`, which has no defined behaviour for an empty list. `[nan]` → the comparison is `False` because any comparison with NaN is `False`: a bug in the *test's* assumption, since NaN has no ordering. `[inf, -inf]` → `inf + -inf` is NaN: again a real domain limit.

**Fix `average`:** raise `ValueError` on an empty list. **Fix the test:** constrain the strategy — `st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1)`.

This is exactly why property-based testing earns its place: three edge cases you would not have written by hand, found in one run. Module 08's ledger suite uses the same technique.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
