"""Tests for the claim verifier."""

from __future__ import annotations

from claim_verifier import (
    Verdict,
    check_existential,
    check_universal,
    classify,
    counterexample_shape,
    equivalent,
    for_all,
    iff,
    implies,
    negate_universal,
    there_exists,
    truth_table,
)


def test_implication_is_false_in_exactly_one_case():
    assert implies(True, True) is True
    assert implies(True, False) is False
    assert implies(False, True) is True
    assert implies(False, False) is True
    assert sum(1 for p in (True, False) for q in (True, False)
               if not implies(p, q)) == 1


def test_biconditional():
    assert iff(True, True) and iff(False, False)
    assert not iff(True, False)
    # It decomposes into two implications.
    for p in (True, False):
        for q in (True, False):
            assert iff(p, q) == (implies(p, q) and implies(q, p))


def test_quantifiers_over_an_empty_domain():
    assert for_all([], lambda x: False) is True
    assert there_exists([], lambda x: True) is False


def test_universal_is_refuted_by_one_counterexample():
    result = check_universal("all even", range(1, 6), lambda n: n % 2 == 0)
    assert result.verdict is Verdict.REFUTED
    assert result.counterexample == (1,)
    assert result.checked == 1, "it stops at the first failure"


def test_universal_proved_only_when_the_domain_is_exhausted():
    proved = check_universal("all positive", range(1, 6), lambda n: n > 0)
    assert proved.verdict is Verdict.PROVED
    assert proved.checked == 5

    sampled = check_universal("all positive", range(1, 6), lambda n: n > 0,
                              exhaustive=False)
    assert sampled.verdict is Verdict.UNSETTLED, (
        "a clean run over a sample proves nothing")


def test_existential_is_proved_by_one_witness():
    result = check_existential("some even", range(1, 6), lambda n: n % 2 == 0)
    assert result.verdict is Verdict.PROVED
    assert result.counterexample == (2,)


def test_existential_refuted_only_when_exhausted():
    refuted = check_existential("some above 10", range(1, 6), lambda n: n > 10)
    assert refuted.verdict is Verdict.REFUTED

    unsettled = check_existential("some above 10", range(1, 6), lambda n: n > 10,
                                  exhaustive=False)
    assert unsettled.verdict is Verdict.UNSETTLED


def test_the_n_squared_plus_n_plus_41_trap():
    """Forty confirming cases and the claim is still false."""
    from math import isqrt

    def prime(n):
        return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))

    small = check_universal("n^2+n+41 is prime", range(40),
                            lambda n: prime(n * n + n + 41), exhaustive=False)
    assert small.verdict is Verdict.UNSETTLED
    assert small.checked == 40

    wider = check_universal("n^2+n+41 is prime", range(45),
                            lambda n: prime(n * n + n + 41))
    assert wider.verdict is Verdict.REFUTED
    assert wider.counterexample == (40,)


def test_tuples_in_the_domain_are_unpacked():
    pairs = [(1, 2), (3, 4), (5, 5)]
    result = check_universal("a < b", pairs, lambda a, b: a < b)
    assert result.verdict is Verdict.REFUTED
    assert result.counterexample == (5, 5)


def test_classification():
    assert classify(lambda p: p or not p, 1) == "tautology"
    assert classify(lambda p: p and not p, 1) == "contradiction"
    assert classify(implies, 2) == "contingency"
    assert classify(lambda p, q: implies(p, q) or implies(q, p), 2) == "tautology"


def test_equivalence_requires_every_row():
    assert equivalent(lambda p, q: not (p and q),
                      lambda p, q: (not p) or (not q), 2)
    assert not equivalent(lambda p, q: not (p and q),
                          lambda p, q: (not p) and (not q), 2)
    # Contraposition holds; the converse does not.
    assert equivalent(lambda p, q: implies(p, q),
                      lambda p, q: implies(not q, not p), 2)
    assert not equivalent(lambda p, q: implies(p, q),
                          lambda p, q: implies(q, p), 2)


def test_truth_table_size():
    assert len(truth_table(lambda a, b, c: a and b and c, 3)) == 8


def test_negate_universal_gives_the_witness_predicate():
    positive = lambda n: n > 0
    witness = negate_universal(positive)
    assert witness(-1) is True
    assert witness(3) is False
    found = check_existential("some non-positive", range(-3, 4), witness)
    assert found.verdict is Verdict.PROVED


def test_counterexample_shape_requires_the_hypothesis_to_hold():
    """The error from Lesson 02.03: refuting with a case where P is false."""
    calibrated = lambda c, b: c
    good_brier = lambda c, b: b < 0.2
    shape = counterexample_shape(calibrated, good_brier)

    assert shape(True, 0.25) is True, "calibrated and bad: a real counterexample"
    assert shape(False, 0.25) is False, "uncalibrated and bad: refutes nothing"
    assert shape(True, 0.10) is False, "calibrated and good: supports the claim"

    models = [(True, 0.15), (False, 0.30), (True, 0.25)]
    found = check_existential("a calibrated model with Brier >= 0.2", models, shape)
    assert found.verdict is Verdict.PROVED
    assert found.counterexample == (True, 0.25)


def test_result_string_names_the_evidence():
    refuted = check_universal("all even", range(1, 4), lambda n: n % 2 == 0)
    assert "REFUTED" in str(refuted) and "counterexample" in str(refuted)

    unsettled = check_universal("all positive", range(1, 4), lambda n: n > 0,
                                exhaustive=False)
    assert "UNSETTLED" in str(unsettled)
    assert "not exhausted" in str(unsettled)


def test_equal_accuracy_does_not_imply_equal_predictions():
    """Lesson 02.19's worked counterexample, as a check."""
    labels = [1, 1, 0, 0]

    def accuracy(pred):
        return sum(p == t for p, t in zip(pred, labels, strict=True)) / len(labels)

    a, b = (1, 1, 1, 1), (0, 1, 0, 1)
    assert accuracy(a) == accuracy(b) == 0.5
    assert a != b

    import itertools
    same = [p for p in itertools.product([0, 1], repeat=4) if accuracy(p) == 0.5]
    assert len(same) == 6, "accuracy is not injective"
