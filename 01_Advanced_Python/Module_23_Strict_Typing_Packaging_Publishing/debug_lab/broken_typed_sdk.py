#!/usr/bin/env python3
"""Broken Typed SDK demonstrating Any escape hatch and dataclass mutable default traps."""

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T")

def transform_data(payload: Any) -> int:
    # Compiler assumes Any is compatible with int, masking runtime AttributeError or TypeError!
    return payload.non_existent_field()

# In regular classes or dataclasses without field(default_factory=...), shared list trap occurs!
@dataclass
class UserConfig:
    username: str
    roles: list[str] = None  # type: ignore

if __name__ == "__main__":
    try:
        val = transform_data("simple string")
    except AttributeError as err:
        print(f"Any escape hatch crashed at runtime: {err}")
