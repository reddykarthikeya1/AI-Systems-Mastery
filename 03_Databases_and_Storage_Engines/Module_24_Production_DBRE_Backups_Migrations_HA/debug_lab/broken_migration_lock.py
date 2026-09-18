"""DEBUG LAB: Exclusive Table Lock Starvation During Online Schema Migration

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class RequestQueue:
    def __init__(self) -> None:
        self.pending: list[str] = []

    def submit(self, request_id: str) -> None:
        self.pending.append(request_id)

def run_migration_no_timeout(
    slow_query_duration_ticks: int, queue: RequestQueue, incoming_requests: list[str]
) -> int:
    """ALTER TABLE ... ADD COLUMN with no lock_timeout: waits indefinitely for
    whatever already holds the table, queuing every request that piles up
    behind it in the meantime instead of backing off and retrying."""
    ticks_waited = 0
    while ticks_waited < slow_query_duration_ticks:
        if ticks_waited < len(incoming_requests):
            queue.submit(incoming_requests[ticks_waited])
        ticks_waited += 1
    return ticks_waited

def reproduce_defect() -> None:
    print("Running an ADD COLUMN migration behind a pre-existing slow report query...")
    queue = RequestQueue()
    incoming_requests = [f"req-{i}" for i in range(200)]
    slow_query_duration_ticks = 180  # the slow report already holds the table

    waited = run_migration_no_timeout(slow_query_duration_ticks, queue, incoming_requests)
    acceptable_queue_depth = 20  # a lock_timeout + retry loop keeps this bounded

    print(f"ALTER TABLE waited {waited} ticks with no lock_timeout configured.")
    print(f"Web requests queued behind the blocked migration: {len(queue.pending)}")
    print(f"SLA-acceptable queue depth: {acceptable_queue_depth}")
    if len(queue.pending) > acceptable_queue_depth:
        print(f"[DEFECT OBSERVED] {len(queue.pending)} requests are stuck waiting "
              f"because the migration never gave up its place in line.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
