"""Lab 4: measure the memory claims made in Chapter 5 on YOUR Python version.

Every number quoted in the chapter should come from a script like this one, not from memory.
Run: python 04_measure_memory_claims.py
"""
import gc
import sys
import tracemalloc


class Standard:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Slotted:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


def bytes_per_instance(cls, n: int = 200_000) -> float:
    tracemalloc.start()
    objs = [cls(float(i), float(i) + 0.5) for i in range(n)]   # floats are distinct objects, counted in both cases
    current, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del objs
    return current / n


if __name__ == "__main__":
    std, slot = bytes_per_instance(Standard), bytes_per_instance(Slotted)
    reduction = 1 - slot / std
    print(f"Python {sys.version.split()[0]}")
    print(f"Standard instance incl. floats: {std:.0f} bytes")
    print(f"Slotted  instance incl. floats: {slot:.0f} bytes  ({reduction:.0%} smaller)")
    print("gc thresholds:", gc.get_threshold())
    print("free-threaded build:", getattr(sys, "_is_gil_enabled", lambda: True)() is False)
    # What the chapter may claim: slots help, by a version-dependent amount (tens of percent for small objects),
    # not a fixed 68%. Include the two float objects per instance (about 24 bytes each) in any honest comparison.
    assert slot < std, "slots should reduce memory"
    assert 0.05 < reduction < 0.75
    print("OK")
