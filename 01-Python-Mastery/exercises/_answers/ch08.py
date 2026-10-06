"""Chapter 08 - Environments, dependencies, packaging.

1. parse_requirement: parse a requirements.txt line.
2. satisfies: check a version against a specifier set such as ">=1.2,<2.0" or "~=1.4.2".
3. latest (debugging): picks the wrong "newest" version.
"""
import re

BUGGY = {
    "latest": '''def latest(versions):
    """Return the highest version string from a non-empty list of dotted numeric versions (1.10 is newer than 1.9)."""
    return max(versions)''',
}


def parse_requirement(line):
    """Parse 'Requests[security]>=2.0,<3  # comment' into ('requests', ['security'], [('>=', '2.0'), ('<', '3')]).
    The name is lowercased with runs of '-', '_' and '.' normalised to '-'. Blank lines and full-line comments return None.
    Extras are returned sorted; specifiers keep their written order."""
    line = line.split("#", 1)[0].strip()
    if not line:
        return None
    m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[([^\]]*)\])?\s*(.*)$", line)
    if not m:
        raise ValueError(f"bad requirement: {line!r}")
    name = re.sub(r"[-_.]+", "-", m.group(1)).lower()
    extras = sorted(e.strip() for e in (m.group(2) or "").split(",") if e.strip())
    specs = []
    for part in filter(None, (p.strip() for p in m.group(3).split(","))):
        sm = re.match(r"^(==|!=|>=|<=|~=|>|<)\s*([0-9][0-9A-Za-z.*]*)$", part)
        if not sm:
            raise ValueError(f"bad specifier: {part!r}")
        specs.append((sm.group(1), sm.group(2)))
    return name, extras, specs


def _vt(v):
    return tuple(int(p) for p in v.split("."))


def _pad(a, b):
    n = max(len(a), len(b))
    return a + (0,) * (n - len(a)), b + (0,) * (n - len(b))


def satisfies(version, spec):
    """True when `version` meets every comma-separated clause of `spec` (empty spec = always True).
    Supports ==, !=, >=, <=, >, < and the compatible-release operator: ~=1.4.2 means >=1.4.2,<1.5 and ~=1.4 means >=1.4,<2.
    Versions compare numerically per component, padding with zeros (1.0 == 1.0.0)."""
    v = _vt(version)
    for clause in filter(None, (c.strip() for c in spec.split(","))):
        op, rhs = re.match(r"^(==|!=|>=|<=|~=|>|<)\s*(.+)$", clause).groups()
        r = _vt(rhs)
        a, b = _pad(v, r)
        if op == "~=":
            prefix = r[:-1]
            upper = prefix[:-1] + (prefix[-1] + 1,)
            lo, hi = _pad(v, upper)
            ok = a >= b and lo < hi
        else:
            ok = {"==": a == b, "!=": a != b, ">=": a >= b, "<=": a <= b, ">": a > b, "<": a < b}[op]
        if not ok:
            return False
    return True


def latest(versions):
    """Return the highest version string from a non-empty list of dotted numeric versions (1.10 is newer than 1.9)."""
    return max(versions, key=_vt)


def t_parse_requirement_full(m):
    assert m.parse_requirement("Requests[security]>=2.0,<3  # comment") == ("requests", ["security"], [(">=", "2.0"), ("<", "3")])
    assert m.parse_requirement("My_Pkg.Name==1.0") == ("my-pkg-name", [], [("==", "1.0")])


def t_parse_requirement_edge(m):
    assert m.parse_requirement("") is None and m.parse_requirement("   # just a comment") is None
    assert m.parse_requirement("flask") == ("flask", [], [])
    assert m.parse_requirement("x[b, a]") == ("x", ["a", "b"], [])


def t_satisfies_basic(m):
    assert m.satisfies("1.5.0", ">=1.2,<2.0") and not m.satisfies("2.0", ">=1.2,<2.0")
    assert m.satisfies("1.0", "==1.0.0") and m.satisfies("1.10", ">1.9") and m.satisfies("3", "")
    assert not m.satisfies("1.2.3", "!=1.2.3")


def t_satisfies_compatible_release(m):
    assert m.satisfies("1.4.9", "~=1.4.2") and not m.satisfies("1.5.0", "~=1.4.2") and not m.satisfies("1.4.1", "~=1.4.2")
    assert m.satisfies("1.9", "~=1.4") and not m.satisfies("2.0", "~=1.4")


def t_latest_numeric(m):
    assert m.latest(["1.9", "1.10", "1.2"]) == "1.10"
    assert m.latest(["2.0.1", "2.0.10", "2.0.9"]) == "2.0.10"
