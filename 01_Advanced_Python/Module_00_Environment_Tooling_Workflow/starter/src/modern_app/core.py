"""STARTER - Module 00: Environment Tooling Workflow

Core application logic and domain models.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_core.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/core.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


class TaskItem(BaseModel):
    """Domain model representing a single task item."""
    id: int
    title: str = Field(..., min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    status: Literal["pending", "in_progress", "completed"] = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def mark_completed(self) -> None:
        """Mark task as completed."""
        # [Tier 2] Algorithm: Implement TaskItem.mark_completed adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_add_task
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 00: implement TaskItem.mark_completed()")



class TaskManager:
    """Manages an in-memory collection of task items with filtering and
    CRUD operations.

    """

    def __init__(self) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_add_task
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 00: implement TaskManager.__init__()")


    def add_task(self, title: str, description: str = "") -> TaskItem:
        """Create and store a new task."""
        # [Tier 2] Algorithm: Implement TaskManager.add_task adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_add_task
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 00: implement TaskManager.add_task()")


    def get_task(self, task_id: int) -> TaskItem | None:
        """Retrieve a task by ID."""
        # [Tier 1] Algorithm: Implement TaskManager.get_task adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_get_task
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 00: implement TaskManager.get_task()")


    def list_tasks(self, status: str | None = None) -> list[TaskItem]:
        """List tasks, optionally filtered by status."""
        # [Tier 2] Algorithm: Implement TaskManager.list_tasks adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_list_tasks_filtered
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 00: implement TaskManager.list_tasks()")


    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed. Returns True if task existed."""
        # [Tier 2] Algorithm: Implement TaskManager.complete_task adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_complete_task
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 00: implement TaskManager.complete_task()")


    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted."""
        # [Tier 2] Algorithm: Implement TaskManager.delete_task adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_delete_task
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 00: implement TaskManager.delete_task()")


    def __len__(self) -> int:
        # [Tier 2] Algorithm: Implement TaskManager.__len__ adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_add_task
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 00: implement TaskManager.__len__()")
