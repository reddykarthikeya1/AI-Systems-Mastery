"""Unit tests for the Modular Text-Based RPG Game Engine."""

from __future__ import annotations

import pytest
from game_engine.combat import calculate_damage
from game_engine.state import create_player
from game_engine.utils import roll_dice
from game_engine.world import DUNGEON_MAP


def test_player_state_closures_isolation() -> None:
    """Test that player state closures properly encapsulate and modify state."""
    get_stats, modify_hp, _modify_gold, _add_item, _remove_item = create_player("Hero", max_hp=100, starting_gold=50)

    stats = get_stats()
    assert stats["name"] == "Hero"
    assert stats["hp"] == 100
    assert stats["gold"] == 50
    assert stats["is_alive"] is True

    # Test damage modification
    new_hp = modify_hp(-30)
    assert new_hp == 70
    assert get_stats()["hp"] == 70

    # Test healing cannot exceed max_hp
    overheal = modify_hp(50)
    assert overheal == 100

    # Test death state and 0 HP floor
    modify_hp(-150)
    assert get_stats()["hp"] == 0
    assert get_stats()["is_alive"] is False


def test_player_gold_and_inventory() -> None:
    """Test inventory addition, removal, and gold boundaries."""
    get_stats, _, modify_gold, add_item, remove_item = create_player("Rogue", starting_gold=10)

    modify_gold(25)
    assert get_stats()["gold"] == 35

    modify_gold(-100)
    assert get_stats()["gold"] == 0  # Cannot go below zero

    add_item("Magic Scroll")
    assert "Magic Scroll" in get_stats()["inventory"]

    assert remove_item("Magic Scroll") is True
    assert remove_item("Nonexistent Item") is False


def test_calculate_damage_math() -> None:
    """Test damage calculation logic and minimum damage floor."""
    # Standard: 15 attack - 5 defense = 10 damage
    assert calculate_damage(15, 5, is_crit=False) == 10

    # Critical hit: (15 * 2) - 5 = 25 damage
    assert calculate_damage(15, 5, is_crit=True) == 25

    # High defense floor: 5 attack - 20 defense -> clamped to minimum 1 damage
    assert calculate_damage(5, 20, is_crit=False) == 1


def test_roll_dice_utility() -> None:
    """Test random dice rolling bounds and totals."""
    rolls, total = roll_dice(count=3, sides=6)
    assert len(rolls) == 3
    assert total == sum(rolls)
    for r in rolls:
        assert 1 <= r <= 6

    with pytest.raises(ValueError):
        roll_dice(0, 6)


def test_dungeon_map_integrity() -> None:
    """Verify all room exits lead to valid existing rooms."""
    for room_key, room_data in DUNGEON_MAP.items():
        exits = room_data["exits"]
        for direction, target_room in exits.items():
            assert target_room in DUNGEON_MAP, f"Room '{room_key}' has invalid exit '{direction}' to '{target_room}'"


def test_two_independent_player_instances() -> None:
    """Test that two player instances maintain isolated closures."""
    get_p1, mod_hp1, _, _, _ = create_player("Player 1", max_hp=100)
    get_p2, _, _, _, _ = create_player("Player 2", max_hp=80)

    mod_hp1(-40)
    assert get_p1()["hp"] == 60
    assert get_p2()["hp"] == 80  # Unaffected


def test_player_duplicate_inventory_items() -> None:
    """Test adding multiple items with the same name and removing one."""
    get_stats, _, _, add_item, remove_item = create_player("Collector")
    add_item("Potion")
    add_item("Potion")
    assert get_stats()["inventory"].count("Potion") == 2

    remove_item("Potion")
    assert get_stats()["inventory"].count("Potion") == 1


def test_calculate_damage_extreme_defense() -> None:
    """Test defense far higher than attack always yields at least 1 damage."""
    assert calculate_damage(1, 100, is_crit=False) == 1
    assert calculate_damage(1, 100, is_crit=True) == 1


def test_roll_dice_invalid_sides() -> None:
    """Test roll_dice raises ValueError when sides < 1."""
    with pytest.raises(ValueError):
        roll_dice(count=1, sides=0)


def test_dungeon_map_entrance_exists() -> None:
    """Test dungeon map contains the default entrance room."""
    assert "entrance" in DUNGEON_MAP
    assert "description" in DUNGEON_MAP["entrance"]
