"""Tests for Sliding Window Flow Control."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_sliding_window_flow_control import sliding_window_flow_control
except ImportError:
    from p01_sliding_window_flow_control import sliding_window_flow_control


def test_sliding_window_flow_control():
    # Packets 0, 2 arrive. Expected becomes 1, 2 is buffered.
    # Packet 1 arrives -> both 1 and 2 deliver, expected becomes 3.
    exp, buf = sliding_window_flow_control(4, [0, 2, 1])
    assert exp == 3
    assert buf == []
    exp2, buf2 = sliding_window_flow_control(4, [0, 2])
    assert exp2 == 1
    assert buf2 == [2]
