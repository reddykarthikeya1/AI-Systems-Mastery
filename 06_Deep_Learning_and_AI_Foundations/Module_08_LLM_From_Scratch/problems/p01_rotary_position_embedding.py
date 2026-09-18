"""Problem 01 — Rotary Position Embedding

Topic: 08 LLM From Scratch
Target: Production-grade implementation

Apply 2D rotary embedding (RoPE) rotation to vector pair (x0, x1) at token position m with frequency theta.

Example:
    >>> rotary_position_embedding(1.0, 0.0, 1)
    (0.5403, 0.8415)

Hints:
    Hint 1: RoPE encodes position by rotating the (x0, x1) pair around the
        origin by an angle that grows with the token position m — it never
        changes the pair's length, only its direction.
    Hint 2: Use the standard 2D rotation matrix with angle `phi = m` (for
        this single frequency band the `theta ** 0 == 1` denominator from
        the spec collapses the angle to exactly m):
        `x0_rot = x0*cos(phi) - x1*sin(phi)`, `x1_rot = x0*sin(phi) +
        x1*cos(phi)`.
    Hint 3: `theta` is accepted as a parameter (matching RoPE's general
        multi-frequency signature) but, per this simplified single-band
        spec, does not change the computed angle — don't let it factor into
        `phi`. At `m == 0` the rotation is the identity, leaving the input
        unchanged; round both outputs to 4 decimal places.
"""

from __future__ import annotations


def rotary_position_embedding(x0: float, x1: float, m: int, theta: float = 10000.0) -> tuple[float, float]:
    """Angle phi = m / (theta ** 0) = m.
    Rotate:
    x0_rot = x0 * cos(phi) - x1 * sin(phi)
    x1_rot = x0 * sin(phi) + x1 * cos(phi)
    Returns (x0_rot, x1_rot) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement rotary_position_embedding")
