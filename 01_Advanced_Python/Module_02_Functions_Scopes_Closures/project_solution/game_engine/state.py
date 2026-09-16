"""Player state management using closures."""

from __future__ import annotations

from collections.abc import Callable


def create_player(
    name: str,
    max_hp: int = 100,
    starting_gold: int = 20,
) -> tuple[
    Callable[[], dict[str, object]],
    Callable[[int], int],
    Callable[[int], int],
    Callable[[str], None],
    Callable[[str], bool],
]:
    """Factory function that returns closure functions managing player state.

    Returns:
        tuple containing:
            1. get_stats() -> dict
            2. modify_hp(amount) -> current_hp
            3. modify_gold(amount) -> current_gold
            4. add_item(item_name) -> None
            5. remove_item(item_name) -> bool
    """
    current_hp: int = max_hp
    gold: int = starting_gold
    inventory: list[str] = ["Health Potion", "Rusty Dagger"]

    def get_stats() -> dict[str, object]:
        """Return a snapshot of player stats."""
        return {
            "name": name,
            "hp": current_hp,
            "max_hp": max_hp,
            "gold": gold,
            "inventory": list(inventory),
            "is_alive": current_hp > 0,
        }

    def modify_hp(amount: int) -> int:
        """Modify player HP, clamped between 0 and max_hp."""
        nonlocal current_hp
        current_hp = max(0, min(max_hp, current_hp + amount))
        return current_hp

    def modify_gold(amount: int) -> int:
        """Modify player gold, preventing negative balances."""
        nonlocal gold
        gold = max(0, gold + amount)
        return gold

    def add_item(item: str) -> None:
        """Add an item to the player's inventory."""
        inventory.append(item)

    def remove_item(item: str) -> bool:
        """Remove an item from inventory. Returns True if item was found."""
        if item in inventory:
            inventory.remove(item)
            return True
        return False

    return get_stats, modify_hp, modify_gold, add_item, remove_item
