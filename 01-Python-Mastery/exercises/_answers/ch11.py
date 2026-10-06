"""Chapter 11 - Legacy refactoring and break-fix.

1. characterize: record what legacy code does today so a refactor can be compared against it.
2. shadow_compare: run old and new implementations side by side (strangler-fig migration).
3. sorted_names (debugging): a helper that silently reorders its caller's data.
"""

BUGGY = {
    "sorted_names": '''def sorted_names(users):
    """Return the 'name' of each user dict ordered by 'age' then 'name'. The caller's list must not be modified."""
    users.sort(key=lambda u: (u["age"], u["name"]))
    return [u["name"] for u in users]''',
}


def characterize(fn, inputs):
    """Call fn(*args) for each args tuple in `inputs`. Return a list of ('ok', result) or ('raises', 'ExceptionClassName'), in order."""
    out = []
    for args in inputs:
        try:
            out.append(("ok", fn(*args)))
        except Exception as e:
            out.append(("raises", type(e).__name__))
    return out


def shadow_compare(old, new, on_diff):
    """Return a function that calls old(*a, **kw) and ALSO new(*a, **kw), but always returns/raises exactly what old does.
    When new's result differs from old's, or new raises, or exactly one of them raises, call on_diff(args, kwargs, old_outcome, new_outcome)
    where an outcome is ('ok', value) or ('raises', 'ExceptionClassName'). A failure of new must never affect the caller."""
    def call(fn, a, kw):
        try:
            return ("ok", fn(*a, **kw)), None
        except Exception as e:
            return ("raises", type(e).__name__), e

    def wrapper(*a, **kw):
        old_out, old_exc = call(old, a, kw)
        new_out, _ = call(new, a, kw)
        if old_out != new_out:
            on_diff(a, kw, old_out, new_out)
        if old_exc is not None:
            raise old_exc
        return old_out[1]

    return wrapper


def sorted_names(users):
    """Return the 'name' of each user dict ordered by 'age' then 'name'. The caller's list must not be modified."""
    return [u["name"] for u in sorted(users, key=lambda u: (u["age"], u["name"]))]


def t_characterize_records_results_and_errors(m):
    assert m.characterize(lambda a, b: a // b, [(6, 3), (1, 0), ("x", 2)]) == [("ok", 2), ("raises", "ZeroDivisionError"), ("raises", "TypeError")]
    assert m.characterize(len, []) == []


def t_shadow_agrees_silently(m):
    diffs = []
    f = m.shadow_compare(lambda x: x * 2, lambda x: x + x, lambda *a: diffs.append(a))
    assert f(4) == 8 and diffs == []


def t_shadow_reports_diff_and_returns_old(m):
    diffs = []
    f = m.shadow_compare(lambda x: x * 2, lambda x: x * 3, lambda a, kw, o, n: diffs.append((a, kw, o, n)))
    assert f(4) == 8
    assert diffs == [((4,), {}, ("ok", 8), ("ok", 12))]


def t_shadow_new_failure_never_leaks(m):
    diffs = []

    def bad(x):
        raise KeyError("boom")

    f = m.shadow_compare(lambda x: x, bad, lambda a, kw, o, n: diffs.append((o, n)))
    assert f(1) == 1 and diffs == [(("ok", 1), ("raises", "KeyError"))]
    g = m.shadow_compare(bad, bad, lambda *a: diffs.append("unexpected"))
    try:
        g(1)
    except KeyError:
        assert "unexpected" not in diffs
        return
    raise AssertionError("old's exception must propagate")


def t_sorted_names_does_not_mutate(m):
    users = [{"name": "b", "age": 30}, {"name": "a", "age": 30}, {"name": "z", "age": 20}]
    before = [dict(u) for u in users]
    assert m.sorted_names(users) == ["z", "a", "b"] and users == before
