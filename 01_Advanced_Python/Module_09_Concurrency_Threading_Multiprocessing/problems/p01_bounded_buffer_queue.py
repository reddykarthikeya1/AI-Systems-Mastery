"""Problem 01 — Thread-Safe Ring Buffer

Target: Production-grade implementation

Example:
    >>> q = BoundedQueue(2)
    >>> q.put('a')
    True
    >>> q.put('b')
    True
    >>> q.put('c')
    False
    >>> q.get()
    'a'
    >>> q.size()
    1

Hints:
    Hint 1: The queue's whole job is to reject writes once it is full and to
        return a sentinel rather than raise when a read finds it empty.
    Hint 2: Back it with a plain list acting as a FIFO: `put` appends to the
        end, `get` pops from the front (index 0), and `capacity` bounds the
        list's length.
    Hint 3: `put` must return `False` without mutating state when
        `len(items) >= capacity` (it doesn't overwrite the oldest entry), and
        `get` on an empty queue must return `None` instead of raising an
        `IndexError`.
"""

from __future__ import annotations


class BoundedQueue:
    def __init__(self, capacity: int):
        raise NotImplementedError('Implement BoundedQueue')
