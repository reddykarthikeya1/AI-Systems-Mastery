"""STARTER - Module 02: Functions Scopes Closures

Player state management using closures.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_state.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/state.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

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
    # [Tier 2] Algorithm: Implement create_player adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_player_state_closures_isolation
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 02: implement create_player()")
