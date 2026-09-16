"""STARTER - Module 26: Final Capstone Project

Distributed Task Queue and DLQ Processor for Capstone Platform.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_tasks.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/tasks.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import uuid
from dataclasses import dataclass

@dataclass
class BackgroundTask:
    task_id: str
    task_name: str
    payload: dict
    status: str = "PENDING"  # PENDING, SUCCESS, DLQ
    retries_left: int = 2
    result: str | None = None


class CapstoneTaskBroker:

    def __init__(self) -> None:
        self.queue: list[BackgroundTask] = []
        self.dlq: list[BackgroundTask] = []
        self.completed: dict[str, BackgroundTask] = {}


    def enqueue(self, task_name: str, payload: dict) -> BackgroundTask:
        # [Tier 2] Algorithm: Implement CapstoneTaskBroker.enqueue adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_task_broker_enqueue
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 26: implement CapstoneTaskBroker.enqueue()")


    def process_all(self) -> int:
        # [Tier 2] Algorithm: Coordinate execution pipeline, processing inputs
        #   and aggregating results.
        # HINTS:
        #  - Process items sequentially or in batches, applying transformations.
        #  - Track successes and errors separately for a clean summary.
        # GRADES: test_task_broker_process_all_success
        # WARNING: Ensure exceptions from individual items do not crash the
        #   entire batch.
        raise NotImplementedError("Module 26: implement CapstoneTaskBroker.process_all()")
