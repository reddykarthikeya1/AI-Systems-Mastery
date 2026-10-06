"""Chapter 01 - Foundations: slicing, parsing, numbers.

1. chunk: split a sequence into fixed-size chunks.
2. parse_kv: parse "a=1;b=two;c=" into a typed dict.
3. total_cents (debugging): money arithmetic that is off by one cent sometimes.
"""
from decimal import Decimal

BUGGY = {
    "total_cents": '''def total_cents(prices):
    """Sum price strings like "19.99" and return the total as an integer number of cents."""
    return int(sum(float(p) for p in prices) * 100)''',
}


def chunk(seq, n):
    """Split `seq` into consecutive lists of length `n` (the last may be shorter). Raise ValueError if n <= 0."""
    if n <= 0:
        raise ValueError("n must be positive")
    return [list(seq[i:i + n]) for i in range(0, len(seq), n)]


def parse_kv(line):
    """Parse 'a=1;b=two;c=' into {'a': 1, 'b': 'two', 'c': None}.
    Integer-looking values (optional leading '-') become int, empty values become None, everything else stays str.
    Ignore empty segments such as a trailing ';'. Split each pair on the FIRST '=' only; a segment without '=' raises ValueError."""
    out = {}
    for seg in line.split(";"):
        if not seg.strip():
            continue
        if "=" not in seg:
            raise ValueError(f"bad segment: {seg!r}")
        k, v = seg.split("=", 1)
        v = v.strip()
        if v == "":
            out[k.strip()] = None
        elif v.lstrip("-").isdigit() and v.count("-") <= 1 and not v.endswith("-"):
            out[k.strip()] = int(v)
        else:
            out[k.strip()] = v
    return out


def total_cents(prices):
    """Sum price strings like "19.99" and return the total as an integer number of cents."""
    return int(sum(Decimal(p) for p in prices) * 100)


def t_chunk_basic(m):
    assert m.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert m.chunk("abcdef", 3) == [["a", "b", "c"], ["d", "e", "f"]]
    assert m.chunk([], 4) == []


def t_chunk_rejects_bad_size(m):
    for bad in (0, -1):
        try:
            m.chunk([1], bad)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")


def t_parse_kv_types(m):
    assert m.parse_kv("a=1;b=two;c=") == {"a": 1, "b": "two", "c": None}
    assert m.parse_kv("n=-42;") == {"n": -42}


def t_parse_kv_first_equals_and_errors(m):
    assert m.parse_kv("url=a=b;x=1") == {"url": "a=b", "x": 1}
    assert m.parse_kv("v=1-2") == {"v": "1-2"}
    try:
        m.parse_kv("novalue")
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def t_total_cents_exact(m):
    assert m.total_cents(["0.29"]) == 29
    assert m.total_cents(["0.57"]) == 57
    assert m.total_cents(["19.99", "0.01"]) == 2000
    assert m.total_cents([]) == 0
