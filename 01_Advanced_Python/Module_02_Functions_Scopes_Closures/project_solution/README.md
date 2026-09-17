# Design Rationale: Modular Turn-Based Combat Engine

## Architectural Overview
A multi-entity turn-based RPG combat simulation demonstrating functional decomposition, closure-based state encapsulation, keyword-only arguments, and clean package boundaries.

## Key Design Decisions
1. **Closure-Encapsulated Combat Modifiers:** Status effects (buffs, debuffs, shields) are modeled as stateful closures that close over duration and power, isolating modifier mutation from entity state.
2. **Pure Functional Damage Calculation:** Damage mitigation pipelines are pure functions receiving entity snapshots, ensuring deterministic combat outcomes given identical RNG seeds.
3. **Keyword-Only Parameters (`*`):** Combat invocation requires explicit keywords for ambiguous numeric modifiers (e.g. `crit_multiplier=1.5`), eliminating argument transposition bugs.

## Rejected Alternatives
1. **Global Game State (`global player_hp`):**
   - *Reason for Rejection:* Global variables make concurrent combat simulations impossible and cause irreversible state pollution across automated unit tests.
2. **Deep Inheritance Hierarchy for Modifiers:**
   - *Reason for Rejection:* Subclassing for every status effect (`class PoisonedEntity(BurnedEntity)`) leads to combinatorial explosion and fragile MRO diamond inheritance.

## Invariants & Guarantees
- Damage cannot reduce entity health below 0.
- State modifiers automatically decrement duration and expire cleanly.

## Verification
```bash
pytest test_game_engine.py -v
```

---

## 🗺️ Recommended Step-by-Step Project Study Path

Follow this sequence to analyze and master the project architecture:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Architecture Review** | Read the specification and design breakdown in this `README.md`. |
| **2** | **Examine Implementation** | Study modular design patterns and invariant safeguards across source files. |
| **3** | **Run Test Suite** | Execute `pytest tests/` to see all production test cases pass green. |
| **4** | **Independent Re-Build** | Re-implement the solution from scratch in `[../starter/](../starter/)` until all tests pass. |

