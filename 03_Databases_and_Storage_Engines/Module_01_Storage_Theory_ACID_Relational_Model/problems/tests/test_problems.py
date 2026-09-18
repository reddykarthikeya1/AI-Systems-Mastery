"""Tests for Slotted Page Insert."""
from __future__ import annotations

import pytest
from p01_slotted_page_insert import slotted_page_insert


def test_slotted_page_insert():
    page = {'capacity': 4096, 'slots': [], 'free_offset': 4096}
    s0 = slotted_page_insert(page, b"record_zero")
    assert s0 == 0
    assert page['slots'][0] == (4096 - 11, 11)
    s1 = slotted_page_insert(page, b"record_one")
    assert s1 == 1
    # Check out of space
    page['free_offset'] = 20
    page['slots'] = [(100, 10)]
    assert slotted_page_insert(page, b"way_too_long_payload_to_fit") == -1
