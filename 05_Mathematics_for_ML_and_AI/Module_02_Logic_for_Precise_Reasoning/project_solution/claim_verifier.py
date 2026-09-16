"""A toolkit for stating a claim precisely and then settling it.

An **in-process model**, in the sense that every claim here is evaluated over a
finite domain supplied by the caller. That is the honest scope: exhaustive
checking settles a universal claim over a finite domain, and over an infinite
one it can only refute, never prove. The API keeps that distinction visible
instead of returning a bare boolean that hides it.

The three verdicts, from Lesson 02.19:

| Verdict | What was established | Evidence |
| :--- | :--- | :--- |
| `PROVED` | true over the whole stated domain | exhaustive check |
| `REFUTED` | false | one explicit counterexample |
| `UNSETTLED` | nothing, on this domain | the search found no witness |

`UNSETTLED` is the verdict people skip, and it is the one that keeps the tool
honest: a search that finds no counterexample in a bounded region has not proved
anything, and saying so is the whole point.
"""

from __future__ import annotations

import enum
import itertools
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any


class Verdict(enum.StrEnum):
    PROVED = "proved"
    REFUTED = "refuted"
    UNSETTLED = "unsettled"


@dataclass
class Result:
    verdict: Verdict
    claim: str
    counterexample: tuple | None = None
    checked: int = 0
    exhaustive: bool = False

    def __str__(self) -> str:
        if self.verdict is Verdict.REFUTED:
            return f"REFUTED: {self.claim} - counterexample {self.counterexample!r}"
        if self.verdict is Verdict.PROVED:
            return f"PROVED over {self.checked} cases: {self.claim}"
        return (f"UNSETTLED after {self.checked} cases: {self.claim} "
                f"(no counterexample found; the domain was not exhausted)")


def implies(p: bool, q: bool) -> bool:
    """`p -> q`. False in exactly one case: p true and q false."""
    return (not p) or q


def iff(p: bool, q: bool) -> bool:
    return p == q


def for_all(domain: Iterable, predicate: Callable[..., bool]) -> bool:
    """Returns False on the first counterexample."""
    return all(predicate(*_as_args(x)) for x in domain)


def there_exists(domain: Iterable, predicate: Callable[..., bool]) -> bool:
    """Returns True on the first witness."""
    return any(predicate(*_as_args(x)) for x in domain)


def _as_args(item: Any) -> tuple:
    return item if isinstance(item, tuple) else (item,)


def check_universal(claim: str, domain: Iterable,
                    predicate: Callable[..., bool],
                    exhaustive: bool = True) -> Result:
    """Settle `for all x in domain: predicate(x)`.

    `exhaustive` is the caller's assertion that `domain` IS the whole domain of
    the claim. When it is False, a clean run returns UNSETTLED rather than
    PROVED - because checking a sample proves nothing about the rest.
    """
    checked = 0
    for item in domain:
        checked += 1
        args = _as_args(item)
        if not predicate(*args):
            return Result(Verdict.REFUTED, claim, counterexample=args,
                          checked=checked, exhaustive=exhaustive)
    verdict = Verdict.PROVED if exhaustive else Verdict.UNSETTLED
    return Result(verdict, claim, checked=checked, exhaustive=exhaustive)


def check_existential(claim: str, domain: Iterable,
                      predicate: Callable[..., bool],
                      exhaustive: bool = True) -> Result:
    """Settle `there exists x in domain: predicate(x)`.

    Mirror image of the universal: one witness PROVES it, and only an exhausted
    domain can REFUTE it.
    """
    checked = 0
    for item in domain:
        checked += 1
        args = _as_args(item)
        if predicate(*args):
            return Result(Verdict.PROVED, claim, counterexample=args,
                          checked=checked, exhaustive=exhaustive)
    verdict = Verdict.REFUTED if exhaustive else Verdict.UNSETTLED
    return Result(verdict, claim, checked=checked, exhaustive=exhaustive)


def truth_table(expression: Callable[..., bool], variables: int) -> dict:
    return {vals: expression(*vals)
            for vals in itertools.product([True, False], repeat=variables)}


def classify(expression: Callable[..., bool], variables: int) -> str:
    values = list(truth_table(expression, variables).values())
    if all(values):
        return "tautology"
    if not any(values):
        return "contradiction"
    return "contingency"


def equivalent(left: Callable[..., bool], right: Callable[..., bool],
               variables: int) -> bool:
    """Logical equivalence: agreement on EVERY assignment, not on a sample."""
    return all(left(*v) == right(*v)
               for v in itertools.product([True, False], repeat=variables))


def negate_universal(predicate: Callable[..., bool]) -> Callable[..., bool]:
    """`not (for all x: P(x))` is `exists x: not P(x)` - so the witness
    predicate to search for is the negation of the body."""
    def negated(*args):
        return not predicate(*args)
    return negated


def counterexample_shape(hypothesis: Callable[..., bool],
                         conclusion: Callable[..., bool]) -> Callable[..., bool]:
    """What refutes `for all x: P(x) -> Q(x)`.

    By Lesson 02.09 that is `exists x: P(x) and not Q(x)` - the hypothesis must
    HOLD. Searching for `not P and not Q` is the commonest way to refute nothing.
    """
    def shape(*args):
        return hypothesis(*args) and not conclusion(*args)
    return shape
