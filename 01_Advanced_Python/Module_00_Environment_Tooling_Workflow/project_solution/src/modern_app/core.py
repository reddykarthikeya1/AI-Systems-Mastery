"""Core application logic and domain models."""

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
        self.status = "completed"


class TaskManager:
    """Manages an in-memory collection of task items with filtering and
    CRUD operations.
    """

    def __init__(self) -> None:
        self._tasks: dict[int, TaskItem] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> TaskItem:
        """Create and store a new task."""
        task = TaskItem(
            id=self._next_id,
            title=title,
            description=description,
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> TaskItem | None:
        """Retrieve a task by ID."""
        return self._tasks.get(task_id)

    def list_tasks(self, status: str | None = None) -> list[TaskItem]:
        """List tasks, optionally filtered by status."""
        if status is None:
            return list(self._tasks.values())
        return [t for t in self._tasks.values() if t.status == status]

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed. Returns True if task existed."""
        task = self._tasks.get(task_id)
        if task:
            task.mark_completed()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted."""
        return self._tasks.pop(task_id, None) is not None

    def __len__(self) -> int:
        return len(self._tasks)
