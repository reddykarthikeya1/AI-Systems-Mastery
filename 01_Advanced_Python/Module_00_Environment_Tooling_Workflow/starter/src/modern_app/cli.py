"""STARTER - Module 00: Environment Tooling Workflow

Command-line interface for modern_app using rich formatting.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_cli.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/cli.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.console import Console

from modern_app.core import TaskManager

console = Console()

def create_parser() -> argparse.ArgumentParser:
    """Configure and return the command-line argument parser."""
    # [Tier 1] Algorithm: Normalize raw input data structure into typed domain
    #   representation.
    # HINTS:
    #  - Handle missing optional keys with sensible defaults (.get() pattern).
    #  - Coerce primitive data types safely and strip surrounding whitespace.
    # GRADES: test_add_task
    # WARNING: Watch for unexpected null or None values in optional fields.
    raise NotImplementedError("Module 00: implement create_parser()")


def display_tasks(manager: TaskManager, status_filter: str | None = None) -> None:
    """Display tasks in a rich styled table."""
    # [Tier 2] Algorithm: Implement display_tasks adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_list_tasks_filtered
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 00: implement display_tasks()")


def run_demo() -> None:
    """Demonstrate the TaskManager functionality in a rich console."""
    # [Tier 2] Algorithm: Coordinate execution pipeline, processing inputs and
    #   aggregating results.
    # HINTS:
    #  - Process items sequentially or in batches, applying transformations.
    #  - Track successes and errors separately for a clean summary.
    # GRADES: test_add_task
    # WARNING: Ensure exceptions from individual items do not crash the entire
    #   batch.
    raise NotImplementedError("Module 00: implement run_demo()")


def main(argv: list[str] | None = None) -> int:
    """Main CLI entrypoint."""
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_add_task
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 00: implement main()")


if __name__ == "__main__":
    sys.exit(main())
