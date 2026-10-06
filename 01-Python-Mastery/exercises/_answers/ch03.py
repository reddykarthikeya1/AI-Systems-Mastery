"""Chapter 03 - Functions, closures, decorators.

1. memoize: a caching decorator that counts hits and misses.
2. compose: right-to-left function composition.
3. make_multipliers (debugging): every returned function multiplies by the same number.
"""
import functools

BUGGY = {
    "make_multipliers": '''def make_multipliers(n):
    """Return a list of n functions; the i-th function multiplies its argument by i."""
    return [lambda x: x * i for i in range(n)]''',
}


def memoize(fn):
    """Cache results by positional and keyword arguments (all hashable). The wrapper exposes
    `.hits` and `.misses` counters and keeps the wrapped function's __name__ and __doc__."""
    cache = {}

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            wrapper.hits += 1
            return cache[key]
        wrapper.misses += 1
        cache[key] = fn(*args, **kwargs)
        return cache[key]

    wrapper.hits = 0
    wrapper.misses = 0
    return wrapper


def compose(*fns):
    """compose(f, g, h)(x) == f(g(h(x))). compose() is the identity function."""
    def run(x):
        for fn in reversed(fns):
            x = fn(x)
        return x
    return run


def make_multipliers(n):
    """Return a list of n functions; the i-th function multiplies its argument by i."""
    return [lambda x, i=i: x * i for i in range(n)]


def t_memoize_counts(m):
    calls = []

    @m.memoize
    def add(a, b=0):
        calls.append((a, b))
        return a + b

    assert add(1, 2) == 3 and add(1, 2) == 3 and add(1, b=2) == 3
    assert len(calls) == 2 and add.hits == 1 and add.misses == 2


def t_memoize_metadata(m):
    @m.memoize
    def square(x):
        """Square x."""
        return x * x

    assert square.__name__ == "square" and square.__doc__ == "Square x."


def t_compose_order(m):
    inc, dbl = (lambda x: x + 1), (lambda x: x * 2)
    assert m.compose(inc, dbl)(5) == 11
    assert m.compose(dbl, inc)(5) == 12
    assert m.compose()(7) == 7


def t_make_multipliers_late_binding(m):
    fs = m.make_multipliers(4)
    assert [f(10) for f in fs] == [0, 10, 20, 30]
    assert m.make_multipliers(0) == []
