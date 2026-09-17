"""Problem 01 — Dependency Inversion Container

Topic: 05 SOLID Principles Clean Architecture
Target: Production-grade implementation

Resolve dependency injection registrations with circular dependency detection.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def dependency_inversion_container(bindings: dict[str, list[str]]) -> list[str]:
    """bindings maps service_name -> list of dependency service names.
    Return valid instantiation order (topological sort).
    Raise ValueError("Circular dependency detected") if a cycle exists.
    """
    raise NotImplementedError("Implement dependency_inversion_container")
