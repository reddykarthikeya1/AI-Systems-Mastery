# Module_02_Functions_Scopes_Closures: Project Implementation Guide

**Deliverable:** a text-based RPG game engine leveraging lexical closures for private player state, first-class combat functions, and dice utilities.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_game.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Dice Rolling Utility
Implement `roll_dice(count, sides)` in `game_engine/utils.py` returning individual rolls and their sum, raising `ValueError` on non-positive sides.

### Step 2 — Combat Damage Calculation
Implement `calculate_damage(attack, defense, is_crit)` in `game_engine/combat.py` with minimum damage floor of 1.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_game.py -k "basic or initial or health or create" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Player State Closures
Implement `create_player(name, max_hp, starting_gold)` in `game_engine/state.py` encapsulating HP, gold, and inventory in lexical scope without global state.

### Step 4 — World Map Traversal
Implement room navigation through `DUNGEON_MAP` verifying all exits lead to existing locations.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/game_engine/combat.py`, remove the `max(1, ...)` clamp in `calculate_damage`.
Run:
```bash
pytest ../project_solution/test_game.py -k test_calculate_damage_extreme_defense -v
```
Watch the test fail when attack is lower than defense, then restore the minimum damage floor.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_game.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Status Effect Closures:** Create closure-based status effects (Poison, Regeneration, Shield) ticking each turn.
2. **Combat Log Decorator:** Implement a decorator recording every attack and defense calculation with timestamps.
3. **Inventory Weight System:** Add weight limits to player closures with encumbrance penalties.
4. **Procedural Dungeon Generator:** Generate dynamic graph rooms using breadth-first search.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_player_state_closures_isolation` | Proves closures encapsulate private state across mutations |
| `test_player_gold_and_inventory` | Proves inventory operations and non-negative gold boundaries |
| `test_calculate_damage_math` | Proves combat formula and critical hit multipliers |
| `test_roll_dice_utility` | Proves dice utility rolls within valid bounds |
| `test_two_independent_player_instances` | Proves independent closures do not leak state |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain the LEGB scope lookup order in CPython
- [ ] Use closures to achieve state encapsulation without object-oriented boilerplate
- [ ] Avoid late-binding variable capture traps in loops
- [ ] Design first-class functions passed as callbacks and strategy handlers
- [ ] Implement factory functions returning specialized callable interfaces
- [ ] Explain how the nonlocal keyword alters closure variable rebinding
- [ ] Write isolated unit tests verifying closure state modifications
