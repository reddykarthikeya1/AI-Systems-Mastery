"""Tests for Triton Pointer Offset Math."""
from __future__ import annotations

import pytest
from p01_triton_pointer_offset_math import triton_pointer_offset_math


def test_triton_pointer_offset_math():
    offs, masks = triton_pointer_offset_math(1, 4, 6)
    # pid 1 with block 4 -> offsets [4, 5, 6, 7]. For n=6, masks = [True, True, False, False]
    assert offs == [4, 5, 6, 7]
    assert masks == [True, True, False, False]
