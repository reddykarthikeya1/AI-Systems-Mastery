"""Distributed Task Queue and DLQ Processor for Capstone Platform."""

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
        task_id = f"TASK-{str(uuid.uuid4())[:8]}"
        task = BackgroundTask(task_id=task_id, task_name=task_name, payload=payload)
        self.queue.append(task)
        return task

    def process_all(self) -> int:
        count = 0
        while self.queue:
            task = self.queue.pop(0)
            try:
                if task.payload.get("should_fail"):
                    raise RuntimeError("Simulated transient task failure")
                task.status = "SUCCESS"
                task.result = f"Completed {task.task_name} successfully."
                self.completed[task.task_id] = task
                count += 1
            except Exception as err:
                if task.retries_left > 0:
                    task.retries_left -= 1
                    self.queue.append(task)
                else:
                    task.status = "DLQ"
                    task.result = str(err)
                    self.dlq.append(task)
                count += 1
        return count
