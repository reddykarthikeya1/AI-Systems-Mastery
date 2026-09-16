"""STARTER - Module 02: Functions Scopes Closures

Modular Text-Based RPG Game Engine - Main Application Loop.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_main.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/main.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from pathlib import Path
import sys

_here = Path(__file__).parent.resolve()
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

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
    # [Tier 2] Algorithm: Coordinate execution pipeline, processing inputs and
    #   aggregating results.
    # HINTS:
    #  - Process items sequentially or in batches, applying transformations.
    #  - Track successes and errors separately for a clean summary.
    # GRADES: test_player_state_closures_isolation
    # WARNING: Ensure exceptions from individual items do not crash the entire
    #   batch.
    raise NotImplementedError("Module 02: implement run_combat()")


def main() -> int:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_player_state_closures_isolation
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 02: implement main()")


if __name__ == "__main__":
    sys.exit(main())
