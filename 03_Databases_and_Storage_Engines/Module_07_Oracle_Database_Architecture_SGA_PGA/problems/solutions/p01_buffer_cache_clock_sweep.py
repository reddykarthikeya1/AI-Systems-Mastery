"""Reference Solution — Problem 01: Buffer Cache Clock Sweep

Topic: 07 Oracle Database Architecture SGA PGA
"""

from __future__ import annotations


def buffer_cache_clock_sweep(frames: list[dict], hand: int) -> tuple[int, int]:
    n = len(frames)
    attempts = 0
    while attempts < 2 * n + 1:
        f = frames[hand]
        if f['ref_bit'] == 1:
            f['ref_bit'] = 0
            hand = (hand + 1) % n
            attempts += 1
        else:
            if not f['dirty']:
                evicted = hand
                new_hand = (hand + 1) % n
                return (evicted, new_hand)
            hand = (hand + 1) % n
            attempts += 1
    return (-1, hand)
