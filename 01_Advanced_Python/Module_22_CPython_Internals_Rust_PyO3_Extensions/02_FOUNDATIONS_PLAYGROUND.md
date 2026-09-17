# 🐣 Interactive Foundations Playground: CPython Internals & Extensions

> *"Working with raw memory buffers and structs bridges Python to native C performance."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import struct
```

---

## 1. Binary Struct Packing and Unpacking

`struct` packs Python values into binary representations matching C struct layouts.

```python
# Pack: int32, float32, char[4]
fmt = "=if4s"
packed = struct.pack(fmt, 42, 3.14, b"TEST")
assert len(packed) == 12

i_val, f_val, s_val = struct.unpack(fmt, packed)
assert i_val == 42
assert abs(f_val - 3.14) < 1e-4
assert s_val == b"TEST"
print(f"Binary struct packed to {len(packed)} bytes and unpacked accurately.")
```

---

## 2. Zero-Copy Memoryviews on Byte Arrays

`memoryview` slices large binary buffers without copying bytes into new allocations.

```python
data = bytearray(b"0123456789ABCDEF")
view = memoryview(data)
slice_view = view[4:8]
assert slice_view.tobytes() == b"4567"

# Modify through view:
slice_view[0] = ord("X")
assert data[4:8] == b"X567"
print(f"Zero-copy in-place buffer mutation verified: {bytes(data[:8])}")
```

---

## 3. Little-Endian vs Big-Endian Integer Representation

Packing formats support explicit byte ordering to ensure portability across network protocols.

```python
val = 0x12345678
le = struct.pack("<I", val)
be = struct.pack(">I", val)
assert le != be
assert le == bytes([0x78, 0x56, 0x34, 0x12])
assert be == bytes([0x12, 0x34, 0x56, 0x78])
print("Endianness byte ordering validated.")
```

---
