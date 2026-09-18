"""Problem 01 — Sliding Window Flow Control

Topic: 02 Network Protocols Transport API Paradigms
Target: Production-grade implementation

Simulate TCP sliding window acknowledging in-order packet sequence numbers.

Example:
    >>> sliding_window_flow_control(4, [0, 2, 1])
    (3, [])
    >>> sliding_window_flow_control(4, [0, 2])
    (1, [2])

Hints:
    Hint 1: A packet only advances the window when it exactly matches the
        next expected sequence number -- everything else just waits, so
        track what has arrived separately from what has been delivered.
    Hint 2: Use a set to buffer out-of-order arrivals and a single running
        `expected` counter; after adding each packet, drain the set with a
        while loop for as long as `expected` is present in it.
    Hint 3: Anything outside `[expected, expected + window_size)` -- a
        stale duplicate already delivered, or a packet too far ahead --
        must be silently ignored, not buffered; only in-window packets
        get added before the drain loop runs.
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
