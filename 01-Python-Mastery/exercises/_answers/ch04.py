"""Chapter 04 - OOP, dunder methods, metaprogramming.

1. Money: a value object with arithmetic and ordering dunders.
2. Plugin: subclasses register themselves by name via __init_subclass__.
3. Point (debugging): equal points cannot be used as dictionary keys.
"""

BUGGY = {
    "Point": '''class Point:
    """Immutable-ish 2D point: equal coordinates mean equal points, and points work as dict keys."""

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)''',
}


class Money:
    """Value object: Money(cents, currency='USD'). Supports + (same currency only, else ValueError),
    ==, <, hash (equal objects hash equal), and repr like Money(1050, 'USD'). Instances are immutable by convention."""

    def __init__(self, cents, currency="USD"):
        self.cents = cents
        self.currency = currency

    def _check(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if other.currency != self.currency:
            raise ValueError("currency mismatch")
        return other

    def __add__(self, other):
        o = self._check(other)
        return o if o is NotImplemented else Money(self.cents + o.cents, self.currency)

    def __eq__(self, other):
        return isinstance(other, Money) and (self.cents, self.currency) == (other.cents, other.currency)

    def __lt__(self, other):
        o = self._check(other)
        return o if o is NotImplemented else self.cents < o.cents

    def __hash__(self):
        return hash((self.cents, self.currency))

    def __repr__(self):
        return f"Money({self.cents}, {self.currency!r})"


class Plugin:
    """Base class. Every subclass that defines a class attribute `name` is registered under it.
    Plugin.create(name, *args) instantiates the registered subclass; unknown names raise KeyError.
    Two subclasses with the same name raise ValueError at class-definition time."""

    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.__dict__.get("name")
        if name is None:
            return
        if name in Plugin.registry:
            raise ValueError(f"duplicate plugin {name!r}")
        Plugin.registry[name] = cls

    @classmethod
    def create(cls, name, *args):
        return Plugin.registry[name](*args)


class Point:
    """Immutable-ish 2D point: equal coordinates mean equal points, and points work as dict keys."""

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))


def t_money_arithmetic(m):
    a, b = m.Money(150), m.Money(50)
    assert a + b == m.Money(200) and a > b and b < a
    assert repr(m.Money(1050)) == "Money(1050, 'USD')"
    try:
        a + m.Money(1, "EUR")
    except ValueError:
        return
    raise AssertionError("mixed currency must raise")


def t_money_hash_and_set(m):
    assert len({m.Money(5), m.Money(5), m.Money(6)}) == 2
    assert m.Money(5) != m.Money(5, "EUR") and m.Money(5) != 5


def t_plugin_registry(m):
    class Csv(m.Plugin):
        name = "csv-test"

        def __init__(self, sep=","):
            self.sep = sep

    assert isinstance(m.Plugin.create("csv-test", ";"), Csv) and m.Plugin.create("csv-test").sep == ","
    class Anonymous(m.Plugin):
        pass
    try:
        m.Plugin.create("missing")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown plugin must raise KeyError")


def t_plugin_duplicates(m):
    class A(m.Plugin):
        name = "dup-test"
    try:
        class B(m.Plugin):
            name = "dup-test"
    except ValueError:
        return
    raise AssertionError("duplicate name must raise ValueError")


def t_point_hashable(m):
    d = {m.Point(1, 2): "a"}
    assert d[m.Point(1, 2)] == "a" and m.Point(1, 2) != m.Point(2, 1)
    assert len({m.Point(0, 0), m.Point(0, 0)}) == 1
