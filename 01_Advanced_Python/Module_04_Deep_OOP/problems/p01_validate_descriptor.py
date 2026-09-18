"""Problem 01 — Data Descriptor Validation

Target: Production-grade implementation

Example:
    >>> class Person:
    ...     age = TypedField(int)
    >>> p = Person()
    >>> p.age = 25
    >>> p.age
    25
    >>> p.age = 'invalid'
    Traceback (most recent call last):
        ...
    TypeError: Expected int, got str

Hints:
    Hint 1: This is a data descriptor (it defines both `__get__` and
        `__set__`), so it lives on the class and every instance's value must
        be stored somewhere per-instance, not on the descriptor itself.
    Hint 2: `__set_name__` already gives you the attribute's name — store the
        expected type and use `instance.__dict__[self.name]` to hold each
        instance's actual value, keyed by that name.
    Hint 3: `__get__` is also called with `instance=None` when the attribute
        is accessed on the class itself (e.g. `Person.age`) — return `self`
        in that case instead of trying to look up an instance value; and
        `__set__` must validate with `isinstance` before storing, raising
        `TypeError` on a mismatch rather than silently storing the bad value.
"""

from __future__ import annotations


class TypedField:
    def __init__(self, expected_type: type):
        raise NotImplementedError('Implement TypedField')
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, instance, owner):
        raise NotImplementedError()
    def __set__(self, instance, value):
        raise NotImplementedError()
