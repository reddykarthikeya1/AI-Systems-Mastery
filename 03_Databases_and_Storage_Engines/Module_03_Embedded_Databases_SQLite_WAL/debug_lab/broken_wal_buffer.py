"""DEBUG LAB: Database is Locked Exception on High Concurrent Ingestion

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class LockedError(Exception):
    pass

class MiniSQLiteConnection:
    """A toy single-writer connection. busy_timeout is never configured, so a
    writer that arrives while the database is locked fails immediately instead
    of waiting for the lock to clear."""

    busy_timeout_ticks = 0

    def write(self, writer_id: int, arrival_tick: int, lock_release_tick: int) -> bool:
        if arrival_tick + self.busy_timeout_ticks < lock_release_tick:
            raise LockedError(f"writer {writer_id}: database is locked")
        return True

def reproduce_defect() -> None:
    print("Simulating 6 writers ingesting while a background writer holds the lock...")
    conn = MiniSQLiteConnection()
    lock_release_tick = 4          # the background writer holds the lock through tick 4
    arrivals = [0, 1, 2, 3, 4, 5]  # 6 writers arrive during a burst of ingestion

    succeeded, failed = 0, 0
    for writer_id, arrival in enumerate(arrivals, start=1):
        try:
            conn.write(writer_id, arrival, lock_release_tick)
            succeeded += 1
        except LockedError:
            failed += 1

    print(f"Writers that succeeded: {succeeded}/{len(arrivals)}")
    print(f"Writers that crashed with 'database is locked': {failed}/{len(arrivals)}")
    if failed > 0:
        print("[DEFECT OBSERVED] Writers that arrived while the lock was briefly held "
              "aborted instantly instead of waiting a few ticks for it to clear.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
