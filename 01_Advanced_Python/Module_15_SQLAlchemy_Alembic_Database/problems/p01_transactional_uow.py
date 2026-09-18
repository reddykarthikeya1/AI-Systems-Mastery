"""Problem 01 — Unit of Work Transaction Manager

Target: Production-grade implementation

Example:
    >>> uow = UnitOfWork()
    >>> with uow:
    ...     pass
    >>> uow.state
    'committed'
    >>> uow.log
    ['commit']

Hints:
    Hint 1: Think of this as a context manager whose job is to record one
        outcome — commit or rollback — depending on whether the `with` block
        raised.
    Hint 2: Track state on the instance (e.g. `state` starting at `'idle'`
        and an append-only `log` list) and set both in `__enter__`/`__exit__`.
    Hint 3: `__exit__` receives `exc_type` — when it is not None you must log
        and switch to the rolled-back state AND return a falsy value so the
        original exception keeps propagating instead of being swallowed.
"""

from __future__ import annotations


class UnitOfWork:
    def __init__(self):
        raise NotImplementedError('Implement UnitOfWork')
