"""Reference Solution — Problem 01: Sliding Window Flow Control

Topic: 02 Network Protocols Transport API Paradigms
"""

from __future__ import annotations


def sliding_window_flow_control(window_size: int, incoming_packets: list[int]) -> tuple[int, list[int]]:
    expected = 0
    buffered = set()
    for pkt in incoming_packets:
        if expected <= pkt < expected + window_size:
            buffered.add(pkt)
        while expected in buffered:
            buffered.remove(expected)
            expected += 1
    return (expected, sorted(buffered))
