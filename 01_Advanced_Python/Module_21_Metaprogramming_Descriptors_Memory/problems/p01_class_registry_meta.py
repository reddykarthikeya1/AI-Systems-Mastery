"""Problem 01 — Subclass Auto-Registration Metaclass

Target: Production-grade implementation

Example:
    >>> class Base(metaclass=RegistryMeta): pass
    >>> class Worker(Base): pass
    >>> class Server(Base): pass
    >>> sorted(RegistryMeta.registry)
    ['Server', 'Worker']

Hints:
    Hint 1: The metaclass's job is to intercept every class creation that
        uses it and record the ones that matter — but "every class" would
        also catch the base class defining the registry itself.
    Hint 2: Build the actual class first with `super().__new__(mcls, name,
        bases, attrs)`, then store it in the shared `registry` dict keyed by
        `name`, using `mcls.registry` so all subclasses share one dict.
    Hint 3: Only register a class when `bases` is non-empty — the root class
        that merely declares `metaclass=RegistryMeta` has an empty `bases`
        tuple and must NOT end up in `registry`, only its subclasses should.
"""

from __future__ import annotations


class RegistryMeta(type):
    registry = {}
    def __new__(mcls, name, bases, attrs):
        raise NotImplementedError('Implement RegistryMeta')
