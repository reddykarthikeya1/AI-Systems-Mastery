"""Chapter 07 - Type system and modern Python architecture.

1. check_types: runtime validation of a dict against a {key: type} schema.
2. Version: a frozen, ordered dataclass parsed from "1.10.2".
3. first_word (debugging): what a type checker would flag: the Optional is not handled.
"""
from dataclasses import dataclass

BUGGY = {
    "first_word": '''def first_word(text: str | None) -> str:
    """Return the first whitespace-separated word of `text`, or '' when text is None or blank."""
    return text.split()[0]''',
}


def check_types(data, schema):
    """Return a sorted list of error strings, empty when valid. For each key in `schema` (name -> type):
    missing key -> 'name: missing'; wrong type -> 'name: expected int, got str'. A bool is NOT accepted for int.
    Keys not in the schema are ignored."""
    errors = []
    for key, typ in schema.items():
        if key not in data:
            errors.append(f"{key}: missing")
            continue
        v = data[key]
        if (typ is int and isinstance(v, bool)) or not isinstance(v, typ):
            errors.append(f"{key}: expected {typ.__name__}, got {type(v).__name__}")
    return sorted(errors)


@dataclass(frozen=True, order=True)
class Version:
    """Version(major, minor, patch) - immutable and ordered numerically.
    Version.parse('1.10.2') builds one; missing parts default to 0 ('2' -> 2.0.0); more than 3 parts or non-numeric raises ValueError.
    str(v) gives 'major.minor.patch'."""
    major: int
    minor: int = 0
    patch: int = 0

    @classmethod
    def parse(cls, text):
        parts = text.strip().split(".")
        if not 1 <= len(parts) <= 3 or not all(p.isdigit() for p in parts):
            raise ValueError(f"bad version: {text!r}")
        return cls(*(int(p) for p in parts))

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def first_word(text: str | None) -> str:
    """Return the first whitespace-separated word of `text`, or '' when text is None or blank."""
    words = (text or "").split()
    return words[0] if words else ""


def t_check_types_valid_and_missing(m):
    schema = {"name": str, "age": int}
    assert m.check_types({"name": "a", "age": 3, "extra": 1}, schema) == []
    assert m.check_types({"name": "a"}, schema) == ["age: missing"]


def t_check_types_wrong_and_bool(m):
    schema = {"name": str, "age": int}
    assert m.check_types({"name": 5, "age": True}, schema) == ["age: expected int, got bool", "name: expected str, got int"]


def t_version_order_and_parse(m):
    V = m.Version
    assert V.parse("1.10.0") > V.parse("1.2.0") and V.parse("2") == V(2, 0, 0)
    assert str(V.parse("3.4")) == "3.4.0"
    assert sorted([V.parse("1.2.10"), V.parse("1.2.9")])[0] == V(1, 2, 9)


def t_version_frozen_and_errors(m):
    v = m.Version(1, 2, 3)
    try:
        v.major = 9
    except Exception as e:
        assert type(e).__name__ == "FrozenInstanceError"
    else:
        raise AssertionError("Version must be frozen")
    for bad in ("1.2.3.4", "a.b", ""):
        try:
            m.Version.parse(bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} must raise ValueError")


def t_first_word_handles_none(m):
    assert m.first_word("  hello world") == "hello"
    assert m.first_word(None) == "" and m.first_word("   ") == "" and m.first_word("") == ""
