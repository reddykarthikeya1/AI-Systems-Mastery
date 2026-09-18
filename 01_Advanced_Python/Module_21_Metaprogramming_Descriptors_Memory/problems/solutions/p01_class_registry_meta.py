"""Problem 01 — Subclass Auto-Registration Metaclass

Target: Production-grade implementation
"""

from __future__ import annotations


class RegistryMeta(type):
    registry = {}
    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)
        if bases:
            mcls.registry[name] = cls
        return cls
