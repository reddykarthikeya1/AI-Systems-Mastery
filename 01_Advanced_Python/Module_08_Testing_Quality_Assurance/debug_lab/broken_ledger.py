#!/usr/bin/env python3
"""Broken Testing Suite demonstrating order dependence, tuple assert, and float tolerance traps."""

GLOBAL_TEST_STATE: list[str] = []

def test_step_one_mutates_state():
    GLOBAL_TEST_STATE.append("initialized")
    assert len(GLOBAL_TEST_STATE) == 1

def test_step_two_assumes_step_one_ran():
    assert "initialized" in GLOBAL_TEST_STATE, "State was not prepared by previous test!"

def test_broken_tuple_assertion():
    computed_val = 99
    expected_val = 100
    assert (computed_val == expected_val, "Values should match!")

def test_floating_point_equality_without_approx():
    val = 0.1 + 0.2
    assert val == 0.3

if __name__ == "__main__":
    print("Running test suite...")
    test_step_one_mutates_state()
    test_step_two_assumes_step_one_ran()
    print("Order-dependent tests passed when run sequentially.")

    test_broken_tuple_assertion()
    print("Broken tuple assert passed silently despite 99 != 100!")

    try:
        test_floating_point_equality_without_approx()
    except AssertionError:
        print("Floating point equality failed as expected!")
