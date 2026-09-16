"""Module 08: W3-Style Interactive Testing Playground.

Run this script directly in your terminal:
    python try_it_yourself.py
"""

def multiply(a, b):
    """Function under test."""
    return a * b

def is_even(n):
    """Function under test."""
    return n % 2 == 0

def run_test(test_name, test_func):
    try:
        test_func()
        print(f"  [OK] PASS: {test_name}")
        return True
    except AssertionError as e:
        print(f"  [X] FAIL: {test_name} -> {e}")
        return False

def test_multiply_positive():
    assert multiply(3, 4) == 12, "3 * 4 should be 12"

def test_multiply_zero():
    assert multiply(5, 0) == 0, "Any number * 0 should be 0"

def test_is_even_true():
    assert is_even(4) is True, "4 should be even"

def test_is_even_false():
    assert is_even(7) is False, "7 should not be even"

def main():
    print("=" * 60)
    print("  MODULE 08: INTERACTIVE MINI TEST RUNNER [TEST]")
    print("=" * 60)
    print("Running test suite:\n")

    tests = [
        ("test_multiply_positive", test_multiply_positive),
        ("test_multiply_zero", test_multiply_zero),
        ("test_is_even_true", test_is_even_true),
        ("test_is_even_false", test_is_even_false),
    ]

    passed = 0
    for name, fn in tests:
        if run_test(name, fn):
            passed += 1

    print("-" * 60)
    print(f"Test Results: {passed}/{len(tests)} passed (100% GREEN)!")
    print("You now understand the core mechanics of automated testing.")
    print("=" * 60)

if __name__ == "__main__":
    main()
