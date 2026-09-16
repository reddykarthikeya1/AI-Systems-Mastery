"""Utility helper functions for formatting and dice rolling."""

from __future__ import annotations

import random


def print_banner(text: str, border_char: str = "=", width: int = 65) -> None:
    """Display centered title banner framed with border characters."""
    print("\n" + border_char * width)
    print(f"  {text.center(width - 4)}")
    print(border_char * width)


def roll_dice(count: int, sides: int) -> tuple[list[int], int]:
    """Roll a number of multi-sided dice and return (rolls, total)."""
    if count <= 0 or sides <= 0:
        raise ValueError("Dice count and sides must be positive integers.")
    rolls = [random.randint(1, sides) for _ in range(count)]
    return rolls, sum(rolls)
