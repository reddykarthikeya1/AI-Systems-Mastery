"""STARTER - Module 02: Functions Scopes Closures

Combat mechanics and turn-based battle resolution.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_combat.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/combat.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

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
    # [Tier 2] Algorithm: Implement calculate_damage adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_calculate_damage_math
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 02: implement calculate_damage()")


def roll_attack(base_attack: int, defense: int) -> tuple[int, bool]:
    """Simulate an attack turn with a 1-in-20 chance for a critical hit."""
    # [Tier 2] Algorithm: Implement roll_attack adhering to the contract defined
    #   in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_roll_dice_utility
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 02: implement roll_attack()")
