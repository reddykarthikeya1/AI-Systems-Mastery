"""Problem 01 — Sliding Window Flow Control

Topic: 02 Network Protocols Transport API Paradigms
Target: Production-grade implementation

Simulate TCP sliding window acknowledging in-order packet sequence numbers.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def sliding_window_flow_control(window_size: int, incoming_packets: list[int]) -> tuple[int, list[int]]:
    """incoming_packets are sequence numbers arriving (possibly out of order or duplicates).
    Window starts expecting seq=0.
    Packets within [expected_seq, expected_seq + window_size) are buffered.
    Advance expected_seq as contiguous packets from expected_seq arrive.
    Returns (final_expected_seq, currently_buffered_packets).
    """
    raise NotImplementedError("Implement sliding_window_flow_control")
