"""STARTER - Module 02: Functions Scopes Closures

Dungeon map, rooms, enemies, and loot configuration.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_world.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/world.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

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
