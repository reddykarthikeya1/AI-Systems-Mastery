"""Unit tests for modern_app.core TaskManager and TaskItem."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from modern_app.core import TaskItem, TaskManager


@pytest.fixture
def task_manager() -> TaskManager:
    """Fixture providing a fresh TaskManager instance."""
    return TaskManager()


def test_add_task(task_manager: TaskManager) -> None:
    """Test adding a task increases count and sets fields properly."""
    task = task_manager.add_task("Learn uv", "Explore fast package manager")
    assert task.id == 1
    assert task.title == "Learn uv"
    assert task.description == "Explore fast package manager"
    assert task.status == "pending"
    assert len(task_manager) == 1


def test_get_task(task_manager: TaskManager) -> None:
    """Test retrieving existing and non-existing tasks."""
    task = task_manager.add_task("Task 1")
    retrieved = task_manager.get_task(task.id)
    assert retrieved is not None
    assert retrieved.title == "Task 1"

    assert task_manager.get_task(999) is None


def test_complete_task(task_manager: TaskManager) -> None:
    """Test completing a task modifies its status."""
    task = task_manager.add_task("Task to complete")
    assert task_manager.complete_task(task.id) is True
    assert task.status == "completed"
    assert task_manager.complete_task(999) is False


def test_list_tasks_filtered(task_manager: TaskManager) -> None:
    """Test filtering task list by status."""
    t1 = task_manager.add_task("Pending task")
    t2 = task_manager.add_task("Completed task")
    task_manager.complete_task(t2.id)

    pending_tasks = task_manager.list_tasks(status="pending")
    completed_tasks = task_manager.list_tasks(status="completed")

    assert len(pending_tasks) == 1
    assert pending_tasks[0].id == t1.id
    assert len(completed_tasks) == 1
    assert completed_tasks[0].id == t2.id


def test_delete_task(task_manager: TaskManager) -> None:
    """Test task deletion."""
    task = task_manager.add_task("To delete")
    assert task_manager.delete_task(task.id) is True
    assert len(task_manager) == 0
    assert task_manager.delete_task(task.id) is False


def test_invalid_task_title_raises_validation_error() -> None:
    """Test Pydantic validation on empty title."""
    with pytest.raises(ValidationError):
        TaskItem(id=1, title="")
