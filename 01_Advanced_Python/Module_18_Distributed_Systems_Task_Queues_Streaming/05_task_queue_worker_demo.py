#!/usr/bin/env python3
"""Module 16: Background Task Queue & Worker Demonstration.

This script demonstrates background task dispatching, execution, and polling.
"""

from __future__ import annotations

import time
import uuid


class SimpleTaskQueue:
    def __init__(self) -> None:
        self.jobs: dict[str, dict] = {}

    def submit_task(self, name: str, payload: dict) -> str:
        job_id = str(uuid.uuid4())[:8]
        self.jobs[job_id] = {
            "name": name,
            "payload": payload,
            "status": "QUEUED",
            "result": None,
        }
        return job_id

    def process_next_job(self) -> str | None:
        for job_id, job in self.jobs.items():
            if job["status"] == "QUEUED":
                job["status"] = "PROCESSING"
                # Simulate job computation
                time.sleep(0.05)
                job["result"] = f"Processed {job['name']} successfully"
                job["status"] = "COMPLETED"
                return job_id
        return None


def main() -> None:
    print("=" * 60)
    print("  Asynchronous Task Queue & Worker Execution Demo")
    print("=" * 60)

    queue = SimpleTaskQueue()
    job_1 = queue.submit_task("GeneratePDFReport", {"user_id": 42})
    job_2 = queue.submit_task("TranscodeVideo1080p", {"video_id": 101})

    print(f"Submitted Job 1: ID={job_1}, Status={queue.jobs[job_1]['status']}")
    print(f"Submitted Job 2: ID={job_2}, Status={queue.jobs[job_2]['status']}\n")

    print("Worker executing jobs from queue...")
    while queue.process_next_job():
        pass

    print(f"Job 1 Final Status: {queue.jobs[job_1]['status']} | Result: {queue.jobs[job_1]['result']}")
    print(f"Job 2 Final Status: {queue.jobs[job_2]['status']} | Result: {queue.jobs[job_2]['result']}")


if __name__ == "__main__":
    main()
