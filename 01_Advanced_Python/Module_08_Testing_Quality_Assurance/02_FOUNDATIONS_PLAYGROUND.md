# 🐣 Interactive Foundations Playground: Testing & Quality Assurance

> *"Untested code is broken by design; test suites provide the regression safety net."*

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
import unittest
```

---

## 1. TestCase Structure and Assertions

The `unittest` framework structures test suites with rich assertion methods.

```python
class MathTest(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(2 + 2, 4)
        self.assertTrue(10 > 5)
        self.assertIn("py", "python")

suite = unittest.TestLoader().loadTestsFromTestCase(MathTest)
result = unittest.TestResult()
suite.run(result)
assert result.wasSuccessful()
assert result.testsRun == 1
print(f"Executed test suite: {result.testsRun} test passed successfully.")
```

---

## 2. Verifying Exception Raising

Testing error paths with `assertRaises` guarantees invalid inputs fail safely.

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

case = unittest.TestCase()
with case.assertRaises(ZeroDivisionError):
    divide(10, 0)
assert divide(10, 2) == 5.0
print("Assertion verified ZeroDivisionError raised correctly.")
```

---

## 3. Subtest Isolation

Subtests allow parameterizing assertions across diverse test cases without halting early.

```python
cases = [(2, True), (3, False), (4, True), (5, False)]
passed_subtests = 0
for num, expected in cases:
    is_even = (num % 2 == 0)
    assert is_even == expected
    passed_subtests += 1

assert passed_subtests == 4
print(f"Validated {passed_subtests} parameterized subtest scenarios.")
```

---
