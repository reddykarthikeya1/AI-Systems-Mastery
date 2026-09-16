"""STARTER - Module 02: Functions Scopes Closures

Utility helper functions for formatting and dice rolling.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_utils.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/utils.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import random

def print_banner(text: str, border_char: str = "=", width: int = 65) -> None:
    """Display centered title banner framed with border characters."""
    # [Tier 2] Algorithm: Implement print_banner adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_player_state_closures_isolation
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 02: implement print_banner()")


def roll_dice(count: int, sides: int) -> tuple[list[int], int]:
    """Roll a number of multi-sided dice and return (rolls, total)."""
    # [Tier 2] Algorithm: Implement roll_dice adhering to the contract defined
    #   in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_roll_dice_utility
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 02: implement roll_dice()")
