"""Tests for Thread-Safe Ring Buffer."""
from __future__ import annotations

import pytest
from p01_bounded_buffer_queue import BoundedQueue


def test_bounded_buffer_queue():
    q = BoundedQueue(2)
    assert q.put('a') is True
    assert q.put('b') is True
    assert q.put('c') is False
    assert q.get() == 'a'
    assert q.put('c') is True
    assert q.size() == 2
