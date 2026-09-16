"""Starter template for the claim verifier.

    cd starter
    python -m pytest ../project_solution -q      # must FAIL until you write this

Build order that works: `implies` and `iff` first (they are one line each and
everything else reads better once they exist), then the quantifiers, then
`check_universal` / `check_existential`, then the truth-table helpers.

The part that carries the lesson is the `UNSETTLED` verdict. A clean run over a
domain you have not exhausted has proved nothing, and the API is designed so
that you cannot report it as a proof by accident.
"""

from __future__ import annotations

import enum
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
        """Name the evidence, not just the verdict: a reader needs to know
        whether a PROVED came from exhausting the domain."""
        raise NotImplementedError("implement Result.__str__")


def implies(p: bool, q: bool) -> bool:
    """`p -> q`. False in exactly one case - work out which before writing it."""
    raise NotImplementedError("implement implies")


def iff(p: bool, q: bool) -> bool:
    raise NotImplementedError("implement iff")


def for_all(domain: Iterable, predicate: Callable[..., bool]) -> bool:
    """Return False on the first counterexample."""
    raise NotImplementedError("implement for_all")


def there_exists(domain: Iterable, predicate: Callable[..., bool]) -> bool:
    """Return True on the first witness."""
    raise NotImplementedError("implement there_exists")


def _as_args(item: Any) -> tuple:
    """Domain items may be bare values or tuples; predicates take positional args."""
    raise NotImplementedError("implement _as_args")


def check_universal(claim: str, domain: Iterable,
                    predicate: Callable[..., bool],
                    exhaustive: bool = True) -> Result:
    """Settle `for all x in domain: predicate(x)`.

    One counterexample REFUTES. A clean run PROVES only when `exhaustive` is
    True; otherwise the honest verdict is UNSETTLED.
    """
    raise NotImplementedError("implement check_universal")


def check_existential(claim: str, domain: Iterable,
                      predicate: Callable[..., bool],
                      exhaustive: bool = True) -> Result:
    """Settle `there exists x in domain: predicate(x)`. Mirror of the universal."""
    raise NotImplementedError("implement check_existential")


def truth_table(expression: Callable[..., bool], variables: int) -> dict:
    raise NotImplementedError("implement truth_table")


def classify(expression: Callable[..., bool], variables: int) -> str:
    """"tautology", "contradiction" or "contingency"."""
    raise NotImplementedError("implement classify")


def equivalent(left: Callable[..., bool], right: Callable[..., bool],
               variables: int) -> bool:
    """Agreement on EVERY assignment - not on a sample."""
    raise NotImplementedError("implement equivalent")


def negate_universal(predicate: Callable[..., bool]) -> Callable[..., bool]:
    raise NotImplementedError("implement negate_universal")


def counterexample_shape(hypothesis: Callable[..., bool],
                         conclusion: Callable[..., bool]) -> Callable[..., bool]:
    """What refutes `for all x: P(x) -> Q(x)`. The hypothesis must HOLD."""
    raise NotImplementedError("implement counterexample_shape")
