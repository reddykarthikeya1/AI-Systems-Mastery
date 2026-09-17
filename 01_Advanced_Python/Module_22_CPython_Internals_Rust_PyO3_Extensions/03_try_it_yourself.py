"""Beginner playground for Module 22 - CPython Internals & Extensions.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import struct

# -------------------------------------------- 1. Binary Struct Packing and Unpacking
# Pack: int32, float32, char[4]
fmt = "=if4s"
packed = struct.pack(fmt, 42, 3.14, b"TEST")
assert len(packed) == 12

i_val, f_val, s_val = struct.unpack(fmt, packed)
assert i_val == 42
assert abs(f_val - 3.14) < 1e-4
assert s_val == b"TEST"
print(f"Binary struct packed to {len(packed)} bytes and unpacked accurately.")

# -------------------------------------------- 2. Zero-Copy Memoryviews on Byte Arrays
data = bytearray(b"0123456789ABCDEF")
view = memoryview(data)
slice_view = view[4:8]
assert slice_view.tobytes() == b"4567"

# Modify through view:
slice_view[0] = ord("X")
assert data[4:8] == b"X567"
print(f"Zero-copy in-place buffer mutation verified: {bytes(data[:8])}")

# -------------------------------------------- 3. Little-Endian vs Big-Endian Integer Representation
val = 0x12345678
le = struct.pack("<I", val)
be = struct.pack(">I", val)
assert le != be
assert le == bytes([0x78, 0x56, 0x34, 0x12])
assert be == bytes([0x12, 0x34, 0x56, 0x78])
print("Endianness byte ordering validated.")

print()
print("All checks passed.")
