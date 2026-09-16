"""Dungeon map, rooms, enemies, and loot configuration."""

from __future__ import annotations

DUNGEON_MAP: dict[str, dict[str, object]] = {
    "entrance": {
        "title": "Dungeon Entrance Archway",
        "description": "A damp stone archway lit by flickering wall torches. Cool air blows from the north.",
        "exits": {"north": "hallway", "east": "armory"},
        "enemy": None,
        "loot": "Wooden Torch",
    },
    "armory": {
        "title": "Abandoned Weapon Vault",
        "description": "Racks of ancient weapons line the walls. A skeleton guards the weapon chest!",
        "exits": {"west": "entrance"},
        "enemy": {
            "name": "Skeleton Guard",
            "hp": 25,
            "max_hp": 25,
            "attack": 8,
            "defense": 2,
            "gold": 25,
        },
        "loot": "Fine Steel Longsword",
    },
    "hallway": {
        "title": "Whispering Hallway",
        "description": "A dark corridor echoing with the chatter of subterranean goblins.",
        "exits": {"south": "entrance", "north": "dragon_lair"},
        "enemy": {
            "name": "Cave Goblin",
            "hp": 18,
            "max_hp": 18,
            "attack": 6,
            "defense": 1,
            "gold": 12,
        },
        "loot": "Greater Health Potion",
    },
    "dragon_lair": {
        "title": "The Ancient Dragon's Lair",
        "description": "A gigantic cavern of scorched granite. Mountains of gold surround an ancient Dragon!",
        "exits": {"south": "hallway"},
        "enemy": {
            "name": "Elder Wyrm",
            "hp": 65,
            "max_hp": 65,
            "attack": 14,
            "defense": 4,
            "gold": 500,
        },
        "loot": "Crown of Dragonkind",
    },
}
