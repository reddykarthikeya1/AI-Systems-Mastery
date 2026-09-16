"""Reference solution — Problem 06: Min Stack (O(1) Minimum)

Pattern:    Stack with auxiliary state
Complexity: Time O(1) per operation, Space O(n)
"""

from __future__ import annotations


def simulate_min_stack(ops: list[tuple[str, int | None]]) -> list[int | None]:
    values: list[int] = []
    mins: list[int] = []        # mins[i] is the minimum of values[:i+1]
    out: list[int | None] = []

    for name, arg in ops:
        if name == "push":
            assert arg is not None
            values.append(arg)
            # Push unconditionally so pop can stay a simple paired pop.
            mins.append(arg if not mins else min(arg, mins[-1]))
        elif name == "pop":
            if values:
                values.pop()
                mins.pop()
        elif name == "top":
            out.append(values[-1] if values else None)
        elif name == "get_min":
            out.append(mins[-1] if mins else None)
        else:
            raise ValueError(f"unknown operation: {name!r}")

    return out
