"""Chapter 05 - Memory, GIL, garbage collection.

1. WeakCache: a get-or-create cache that never keeps objects alive.
2. deep_size: recursive sys.getsizeof that counts shared objects once.
3. EventBus (debugging): subscribers are never freed.
"""
import sys
import weakref

BUGGY = {
    "EventBus": '''class EventBus:
    """Calls subscribed bound methods on publish. Must NOT keep subscribers alive: once the
    subscriber object is garbage collected it is dropped. len(bus) counts live subscribers."""

    def __init__(self):
        self._subs = []

    def subscribe(self, bound_method):
        self._subs.append(bound_method)

    def publish(self, event):
        for cb in list(self._subs):
            cb(event)
        return len(self._subs)

    def __len__(self):
        return len(self._subs)''',
}


class WeakCache:
    """get_or_create(key, factory) returns the cached object for key, calling factory() only when there is no live one.
    The cache holds values weakly: once nothing else references a value, it disappears (a later call recreates it)."""

    def __init__(self):
        self._d = weakref.WeakValueDictionary()

    def get_or_create(self, key, factory):
        obj = self._d.get(key)
        if obj is None:
            obj = factory()
            self._d[key] = obj
        return obj

    def __len__(self):
        return len(self._d)


def deep_size(obj, _seen=None):
    """Total sys.getsizeof of obj plus everything reachable through lists, tuples, sets, frozensets and dicts
    (keys and values), counting each distinct object (by id) once."""
    seen = _seen if _seen is not None else set()
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(deep_size(k, seen) + deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(deep_size(i, seen) for i in obj)
    return size


class EventBus:
    """Calls subscribed bound methods on publish. Must NOT keep subscribers alive: once the
    subscriber object is garbage collected it is dropped. len(bus) counts live subscribers."""

    def __init__(self):
        self._subs = []

    def subscribe(self, bound_method):
        self._subs.append(weakref.WeakMethod(bound_method))

    def _live(self):
        self._subs = [r for r in self._subs if r() is not None]
        return [r() for r in self._subs]

    def publish(self, event):
        cbs = self._live()
        for cb in cbs:
            cb(event)
        return len(cbs)

    def __len__(self):
        return len(self._live())


class _Thing:
    def __init__(self, n):
        self.n = n


def t_weakcache_reuses_live_object(m):
    c = m.WeakCache()
    calls = []

    def make():
        calls.append(1)
        return _Thing(1)

    a = c.get_or_create("k", make)
    assert c.get_or_create("k", make) is a and len(calls) == 1


def t_weakcache_does_not_keep_alive(m):
    import gc
    c = m.WeakCache()
    a = c.get_or_create("k", lambda: _Thing(1))
    del a
    gc.collect()
    assert len(c) == 0
    assert isinstance(c.get_or_create("k", lambda: _Thing(2)), _Thing)


def t_deep_size_counts_shared_once(m):
    inner = "x" * 100
    lst = [inner, inner]
    assert m.deep_size(lst) == sys.getsizeof(lst) + sys.getsizeof(inner)
    d = {"k": inner, "j": inner}
    assert m.deep_size(d) == sys.getsizeof(d) + sys.getsizeof("k") + sys.getsizeof("j") + sys.getsizeof(inner)


def t_deep_size_nested(m):
    leaf = [1000001, 1000002]
    outer = [leaf, (leaf,)]
    expected = sys.getsizeof(outer) + sys.getsizeof(leaf) + sys.getsizeof(1000001) + sys.getsizeof(1000002) + sys.getsizeof((leaf,))
    assert m.deep_size(outer) == expected


def t_eventbus_drops_dead_subscribers(m):
    import gc

    class Sub:
        def __init__(self):
            self.seen = []

        def on(self, ev):
            self.seen.append(ev)

    bus, s = m.EventBus(), Sub()
    bus.subscribe(s.on)
    assert bus.publish("a") == 1 and s.seen == ["a"] and len(bus) == 1
    del s
    gc.collect()
    assert len(bus) == 0 and bus.publish("b") == 0
