#!/usr/bin/env python3
"""Modular Text-Based RPG Game Engine - Main Application Loop.

Module 02 Turnkey Project Implementation.
"""

from __future__ import annotations

import sys

from game_engine.combat import roll_attack
from game_engine.state import create_player
from game_engine.utils import print_banner
from game_engine.world import DUNGEON_MAP


def run_combat(
    get_stats,
    modify_hp,
    modify_gold,
    enemy_data: dict[str, object],
) -> bool:
    """Run an interactive turn-based combat encounter.

    Returns:
        bool: True if player won, False if player was defeated or fled.
    """
    enemy_name = str(enemy_data["name"])
    enemy_hp = int(enemy_data["hp"])
    enemy_max_hp = int(enemy_data["max_hp"])
    enemy_attack = int(enemy_data["attack"])
    enemy_defense = int(enemy_data["defense"])
    enemy_gold = int(enemy_data["gold"])

    print_banner(f"BATTLE INITIATED: {enemy_name.upper()} APPEARS!", border_char="!")
    print(f"Enemy: {enemy_name} (HP: {enemy_hp}/{enemy_max_hp}, Attack: {enemy_attack}, Def: {enemy_defense})")

    while enemy_hp > 0:
        player = get_stats()
        if not player["is_alive"]:
            return False

        print(f"\n[Your HP: {player['hp']}/{player['max_hp']}] | [{enemy_name} HP: {enemy_hp}/{enemy_max_hp}]")
        print("  1. Attack with weapon")
        print("  2. Attempt to Flee")

        action = input("Choose combat action (1-2): ").strip()

        match action:
            case "1":
                # Player attack turn
                damage, is_crit = roll_attack(base_attack=12, defense=enemy_defense)
                enemy_hp = max(0, enemy_hp - damage)
                crit_text = " [CRITICAL STRIKE!]" if is_crit else ""
                print(f"  -> You strike {enemy_name} for {damage} damage!{crit_text}")

                if enemy_hp == 0:
                    print(f"\n[VICTORY] You have defeated {enemy_name}!")
                    modify_gold(enemy_gold)
                    print(f"  -> Looted +{enemy_gold} Gold! (Total Gold: {get_stats()['gold']})")
                    return True

                # Enemy counter-attack turn
                e_damage, e_crit = roll_attack(base_attack=enemy_attack, defense=3)
                modify_hp(-e_damage)
                e_crit_text = " [CRITICAL STRIKE!]" if e_crit else ""
                print(f"  <- {enemy_name} counter-attacks for {e_damage} damage!{e_crit_text}")

                if not get_stats()["is_alive"]:
                    print(f"\n[DEFEAT] You were struck down by {enemy_name}...")
                    return False

            case "2":
                print("  -> You scramble backward and escape from combat!")
                return False
            case _:
                print("Invalid action! Select 1 to attack or 2 to flee.")

    return True


def main() -> int:
    print_banner("DUNGEON CRAWLER: MODULAR RPG ENGINE", border_char="=")
    hero_name = input("Enter your Hero's name: ").strip() or "Adventurer"

    # Initialize closure-based player state
    get_stats, modify_hp, modify_gold, add_item, remove_item = create_player(hero_name, max_hp=100, starting_gold=25)

    current_room_key = "entrance"
    defeated_enemies: set[str] = set()
    collected_loot: set[str] = set()

    print(f"\nWelcome, {hero_name}! Your quest begins at the Dungeon Gates.")

    while True:
        player = get_stats()
        if not player["is_alive"]:
            print_banner("GAME OVER - YOU HAVE FALLEN", border_char="*")
            break

        room = DUNGEON_MAP[current_room_key]
        print(f"\n=== {room['title']} ===")
        print(f"{room['description']}")

        # Display exits
        exits = room["exits"]
        exit_list = ", ".join(f"'{k}'" for k in exits)
        print(f"Available Exits: {exit_list}")

        # Check for room loot
        loot_item = room.get("loot")
        if loot_item and current_room_key not in collected_loot:
            print(f"  [Discovery] You spot a chest containing: '{loot_item}'!")

        # Check for enemy
        enemy_data = room.get("enemy")
        if enemy_data and current_room_key not in defeated_enemies:
            print(f"  [Threat] A hostile {enemy_data['name']} blocks your path!")

        print("\nCommands: [go <direction>] | [look] | [take] | [fight] | [potion] | [stats] | [quit]")
        raw_cmd = input(f"[{hero_name} @ {current_room_key}] > ").strip().lower()

        match raw_cmd.split():
            case ["go", direction]:
                if direction in exits:
                    current_room_key = exits[direction]
                else:
                    print(f"  [Error] Cannot go '{direction}'. Valid exits are: {exit_list}")

            case ["look"]:
                # Re-displays room on next cycle
                pass

            case ["take"] | ["loot"]:
                if loot_item and current_room_key not in collected_loot:
                    add_item(loot_item)
                    collected_loot.add(current_room_key)
                    print(f"  -> Collected '{loot_item}' and placed in inventory!")
                else:
                    print("  -> There is nothing to take here.")

            case ["fight"] | ["attack"]:
                if enemy_data and current_room_key not in defeated_enemies:
                    won = run_combat(get_stats, modify_hp, modify_gold, enemy_data)
                    if won:
                        defeated_enemies.add(current_room_key)
                        if current_room_key == "dragon_lair":
                            print_banner("CONGRATULATIONS! YOU DEFEATED THE RED DRAGON AND SAVED THE REALM!", border_char="*")
                            break
                else:
                    print("  -> There are no enemies to fight in this room.")

            case ["potion"] | ["heal"]:
                if remove_item("Health Potion") or remove_item("Small Health Potion") or remove_item("Greater Health Potion"):
                    new_hp = modify_hp(40)
                    print(f"  -> Drank potion and restored 40 HP! (Current HP: {new_hp}/{player['max_hp']})")
                else:
                    print("  -> You have no health potions in your inventory!")

            case ["stats"] | ["inventory"]:
                p = get_stats()
                print("\n--- HERO STATUS ---")
                print(f"Name      : {p['name']}")
                print(f"Health    : {p['hp']}/{p['max_hp']}")
                print(f"Gold      : {p['gold']} Coins")
                print(f"Inventory : {', '.join(p['inventory'])}")
                print("-------------------")

            case ["quit"] | ["exit"]:
                print(f"\nThanks for playing, {hero_name}! Farewell.")
                break

            case _:
                print("Unrecognized command. Try 'go north', 'look', 'take', 'fight', 'potion', 'stats', or 'quit'.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
