"""Reference Solution — Problem 01: Rotary Position Embedding

Topic: 08 LLM From Scratch
"""

from __future__ import annotations


def rotary_position_embedding(x0: float, x1: float, m: int, theta: float = 10000.0) -> tuple[float, float]:
    import math
    phi = float(m)
    x0_rot = x0 * math.cos(phi) - x1 * math.sin(phi)
    x1_rot = x0 * math.sin(phi) + x1 * math.cos(phi)
    return (round(x0_rot, 4), round(x1_rot, 4))
