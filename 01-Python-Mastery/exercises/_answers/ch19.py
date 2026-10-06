"""Chapter 19 - C ABI, struct layout and the boundary with Rust/C extensions (stdlib only).

1. struct_layout: compute field offsets and total size the way a C compiler does (natural alignment + tail padding).
2. pack_record / unpack_record: a fixed binary wire format via `struct`.
3. read_u32_le (debugging): reads a little-endian integer incorrectly.
"""
import ctypes
import struct

BUGGY = {
    "read_u32_le": '''def read_u32_le(buf, offset=0):
    """Read an unsigned 32-bit little-endian integer from bytes `buf` at `offset`."""
    return int.from_bytes(buf[offset:offset + 4], "big")''',
}

_SIZES = {"char": 1, "short": 2, "int": 4, "float": 4, "long long": 8, "double": 8, "void*": ctypes.sizeof(ctypes.c_void_p)}


def struct_layout(fields):
    """`fields` is a list of (name, type) with type in char, short, int, float, long long, double, void*.
    Return ({name: offset}, total_size). Each field is aligned to its own size; the total size is rounded up to the
    largest alignment among the fields (an empty struct has size 0)."""
    offsets, pos, biggest = {}, 0, 1
    for name, typ in fields:
        size = _SIZES[typ]
        pos = (pos + size - 1) // size * size
        offsets[name] = pos
        pos += size
        biggest = max(biggest, size)
    return offsets, (pos + biggest - 1) // biggest * biggest if fields else 0


def pack_record(rec_id, price, name):
    """Little-endian, no padding: uint32 id, float64 price, 8-byte name (UTF-8, truncated to 8 bytes, NUL padded). Always 20 bytes."""
    return struct.pack("<Id8s", rec_id, price, name.encode("utf-8")[:8])


def unpack_record(data):
    """Inverse of pack_record: returns (id, price, name) with trailing NULs stripped. Wrong length raises ValueError."""
    if len(data) != 20:
        raise ValueError("record must be 20 bytes")
    rec_id, price, raw = struct.unpack("<Id8s", data)
    return rec_id, price, raw.rstrip(b"\x00").decode("utf-8", errors="ignore")


def read_u32_le(buf, offset=0):
    """Read an unsigned 32-bit little-endian integer from bytes `buf` at `offset`."""
    return int.from_bytes(buf[offset:offset + 4], "little")


def t_struct_layout_matches_ctypes(m):
    cases = [[("a", "char"), ("b", "int"), ("c", "char")],
             [("a", "char"), ("b", "double"), ("c", "short")],
             [("p", "void*"), ("x", "char")],
             [("a", "short"), ("b", "short"), ("c", "int"), ("d", "long long")]]
    ctype = {"char": ctypes.c_char, "short": ctypes.c_short, "int": ctypes.c_int, "float": ctypes.c_float,
             "long long": ctypes.c_longlong, "double": ctypes.c_double, "void*": ctypes.c_void_p}
    for fields in cases:
        class S(ctypes.Structure):
            _fields_ = [(n, ctype[t]) for n, t in fields]
        offsets, size = m.struct_layout(fields)
        assert size == ctypes.sizeof(S), (fields, size, ctypes.sizeof(S))
        assert all(offsets[n] == getattr(S, n).offset for n, _ in fields)


def t_struct_layout_empty_and_known(m):
    assert m.struct_layout([]) == ({}, 0)
    assert m.struct_layout([("a", "char"), ("b", "int"), ("c", "char")]) == ({"a": 0, "b": 4, "c": 8}, 12)


def t_record_roundtrip(m):
    data = m.pack_record(7, 2.5, "widget")
    assert len(data) == 20 and m.unpack_record(data) == (7, 2.5, "widget")
    assert m.unpack_record(m.pack_record(1, 0.0, "averyverylongname"))[2] == "averyver"
    assert m.unpack_record(m.pack_record(4_000_000_000, 1.0, ""))[0] == 4_000_000_000


def t_record_wrong_length(m):
    try:
        m.unpack_record(b"\x00" * 19)
    except ValueError:
        return
    raise AssertionError("must reject wrong length")


def t_read_u32_le(m):
    assert m.read_u32_le(b"\x01\x00\x00\x00") == 1
    assert m.read_u32_le(b"\xff\x78\x56\x34\x12", 1) == 0x12345678
