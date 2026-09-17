"""Beginner playground for Module 08 - Testing & Quality Assurance.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import unittest

# -------------------------------------------- 1. TestCase Structure and Assertions
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

# -------------------------------------------- 2. Verifying Exception Raising
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

case = unittest.TestCase()
with case.assertRaises(ZeroDivisionError):
    divide(10, 0)
assert divide(10, 2) == 5.0
print("Assertion verified ZeroDivisionError raised correctly.")

# -------------------------------------------- 3. Subtest Isolation
cases = [(2, True), (3, False), (4, True), (5, False)]
passed_subtests = 0
for num, expected in cases:
    is_even = (num % 2 == 0)
    assert is_even == expected
    passed_subtests += 1

assert passed_subtests == 4
print(f"Validated {passed_subtests} parameterized subtest scenarios.")

print()
print("All checks passed.")
