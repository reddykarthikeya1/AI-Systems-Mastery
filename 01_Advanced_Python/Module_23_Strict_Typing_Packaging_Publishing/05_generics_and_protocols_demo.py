#!/usr/bin/env python3
"""Module 21: Generics and Protocol Demonstration.

This script demonstrates Generic classes (Generic[T]) and Structural Subtyping
with typing.Protocol.
"""

from __future__ import annotations

from typing import Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


class GenericRepository(Generic[T]):
    """Type-safe generic in-memory repository."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get_all(self) -> list[T]:
        return list(self._items)


@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str:
        ...


class HTMLCard:
    def __init__(self, title: str) -> None:
        self.title = title

    def render(self) -> str:
        return f"<div class='card'>{self.title}</div>"


def display_component(comp: Renderable) -> None:
    if not isinstance(comp, Renderable):
        raise TypeError("Component must satisfy the Renderable protocol!")
    print("Rendered:", comp.render())


def main() -> None:
    print("=" * 60)
    print("  Generic Repositories & Protocol Subtyping Demo")
    print("=" * 60)

    repo = GenericRepository[str]()
    repo.add("Alpha")
    repo.add("Beta")
    print(f"Generic String Items: {repo.get_all()}")

    card = HTMLCard("Strict Typing in Python 3.11+")
    display_component(card)


if __name__ == "__main__":
    main()
