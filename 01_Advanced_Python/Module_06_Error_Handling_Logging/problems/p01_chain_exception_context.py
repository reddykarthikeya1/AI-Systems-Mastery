"""Problem 01 — Contextual Exception Chaining

Target: Production-grade implementation

Example:
    >>> try:
    ...     try:
    ...         raise ValueError('inner failure')
    ...     except ValueError as err:
    ...         raise RuntimeError('outer failure') from err
    ... except RuntimeError as top:
    ...     format_exception_chain(top)
    ['RuntimeError: outer failure', 'ValueError: inner failure']

Hints:
    Hint 1: An exception can carry a link to the exception that caused it —
        walk that chain from the given exception back to its root cause,
        most recent first.
    Hint 2: Each exception object exposes both `__cause__` (an explicit
        `raise ... from ...`) and `__context__` (an exception that was
        already being handled when this one was raised); format each as
        `"TypeName: message"` and follow the chain to build the list.
    Hint 3: Prefer `__cause__` over `__context__` when both are set (explicit
        chaining wins over implicit), and stop once neither is present — an
        exception with no linked cause should just produce a one-element
        list.
"""

from __future__ import annotations


def format_exception_chain(exc: BaseException) -> list[str]:
    raise NotImplementedError('Implement format_exception_chain')
