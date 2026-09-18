"""DEBUG LAB: Distributed Lock Race Condition Releases Another Worker's Lock

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class RedisLike:
    """A toy key-value store with SET NX EX semantics and an unconditional DEL."""

    def __init__(self) -> None:
        self.store: dict[str, tuple[str, int]] = {}  # key -> (owner_token, expire_tick)

    def set_nx_ex(self, key: str, token: str, ttl: int, now: int) -> bool:
        existing = self.store.get(key)
        if existing and existing[1] > now:
            return False
        self.store[key] = (token, now + ttl)
        return True

    def delete(self, key: str) -> None:
        self.store.pop(key, None)

def reproduce_defect() -> None:
    print("Worker 1 acquires a lock, runs long, and worker 2 takes over...")
    r = RedisLike()

    r.set_nx_ex("lock:job42", "worker-1", ttl=10, now=0)
    print("t=0:  worker 1 acquires lock:job42 (ttl=10)")

    acquired_by_2 = r.set_nx_ex("lock:job42", "worker-2", ttl=10, now=12)
    print(f"t=12: worker 1's TTL has expired; worker 2 acquires it too: {acquired_by_2}")

    r.delete("lock:job42")  # worker 1 finally finishes and releases "its" lock
    print("t=13: worker 1 finishes its (already-expired) work and calls DEL")

    still_locked = "lock:job42" in r.store
    print(f"Lock present after worker 1's cleanup DEL: {still_locked}")
    if not still_locked and acquired_by_2:
        print("[DEFECT OBSERVED] Worker 1's unconditional DEL removed worker 2's "
              "still-active lock -- both workers now believe they own job42.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
