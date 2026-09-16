"""Combat mechanics and turn-based battle resolution."""

from __future__ import annotations

import random


def calculate_damage(base_attack: int, defense: int, is_crit: bool = False) -> int:
    """Calculate effective damage with a minimum threshold of 1.

    Args:
        base_attack: Attacker's base attack power.
        defense: Defender's armor/defense value.
        is_crit: If True, applies a 2.0x critical damage multiplier.

    Returns:
        int: Damage dealt to the defender.
    """
    multiplier = 2.0 if is_crit else 1.0
    raw_damage = (base_attack * multiplier) - defense
    return max(1, int(raw_damage))


def roll_attack(base_attack: int, defense: int) -> tuple[int, bool]:
    """Simulate an attack turn with a 1-in-20 chance for a critical hit."""
    d20 = random.randint(1, 20)
    is_crit = (d20 == 20)
    damage = calculate_damage(base_attack, defense, is_crit=is_crit)
    return damage, is_crit
