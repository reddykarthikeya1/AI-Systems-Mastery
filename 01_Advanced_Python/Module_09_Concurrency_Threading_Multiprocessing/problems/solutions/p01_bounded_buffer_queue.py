"""Problem 01 — Thread-Safe Ring Buffer

Target: Production-grade implementation
"""

from __future__ import annotations


class BoundedQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items = []
    def put(self, item) -> bool:
        if len(self.items) >= self.capacity: return False
        self.items.append(item)
        return True
    def get(self):
        if not self.items: return None
        return self.items.pop(0)
    def size(self) -> int:
        return len(self.items)
