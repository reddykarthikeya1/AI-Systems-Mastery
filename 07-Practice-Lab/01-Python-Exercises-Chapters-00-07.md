# Python Exercises: Chapters 00 to 07

> Each chapter has graded exercises with hidden tests: two coding exercises and one debugging exercise. Create your files with `python 01-Python-Mastery/exercises/run.py --init`, edit `exercises/chNN.py`, then run `python 01-Python-Mastery/exercises/run.py NN`. Hints are also available in the terminal with `--hints NN` and walkthroughs with `--explain NN`.

---

## Chapter 00: Mental model: names, objects, mutability

**The three exercises**

- same_object_groups: find which names point at the same object.
- snapshot: copy nested lists/dicts so later mutation of the original cannot leak in.
- add_tag (debugging): this function shares state between calls. Find out why and fix it.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 00 - Mental model: names, objects, mutability.

1. same_object_groups: find which names point at the same object.
2. snapshot: copy nested lists/dicts so later mutation of the original cannot leak in.
3. add_tag (debugging): this function shares state between calls. Find out why and fix it."""

def same_object_groups(objs):
    """Return a list of index lists, one per group of 2+ positions in `objs` holding the *same object* (identity, not equality).
Groups ordered by first index; indices ascending. [a, b, a] -> [[0, 2]] when a is not b."""
    raise NotImplementedError()

def snapshot(value):
    """Return a deep copy of nested lists, dicts and tuples without using the `copy` module. Other values are returned as is."""
    raise NotImplementedError()

def add_tag(tag, tags=[]):
    """Return a list containing `tag` appended to `tags` (a new list when `tags` is omitted)."""
    tags.append(tag)
    return tags
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Think about object identity (id()) versus value equality (==).
2. Group indices by id(o) using a dictionary mapping id to a list of indices.
3. Sort groups with len > 1 by their first index; sort the indices inside ascending.

**Exercise 2**

1. Recursion is your friend for deep structures.
2. Check for isinstance(val, (list, dict, tuple)) and recursively snapshot children.
3. Leave atomic/scalar objects (ints, strings, None) unchanged; rebuild new container instances.

**Exercise 3**

1. Look at the function signature's default argument: tags=[].
2. When is `tags=[]` evaluated? At function definition time in CPython!
3. Replace `tags=[]` with `tags=None` and initialize `tags = []` inside the function body.

</details>

<details>
<summary>What the hidden tests check</summary>

- `add_tag_no_shared_state`
- `same_object_groups_identity`
- `snapshot_is_independent`
- `snapshot_keeps_scalars`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
def same_object_groups(objs):
    """Return a list of index lists, one per group of 2+ positions in `objs` holding the *same object* (identity, not equality).
    Groups ordered by first index; indices ascending. [a, b, a] -> [[0, 2]] when a is not b."""
    seen = {}
    for i, o in enumerate(objs):
        seen.setdefault(id(o), []).append(i)
    return sorted((v for v in seen.values() if len(v) > 1), key=lambda v: v[0])

def snapshot(value):
    """Return a deep copy of nested lists, dicts and tuples without using the `copy` module. Other values are returned as is."""
    if isinstance(value, list):
        return [snapshot(v) for v in value]
    if isinstance(value, dict):
        return {k: snapshot(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return tuple(snapshot(v) for v in value)
    return value

def add_tag(tag, tags=None):
    """Return a list containing `tag` appended to `tags` (a new list when `tags` is omitted)."""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```

**1. same_object_groups**

*Approach.* Identity is id(obj), not ==. Walk the list once, bucket indices by id, keep buckets with two or more entries, order by first index.

*Complexity.* Time O(n), space O(n).

*Common wrong answers.*

- Using == groups equal-but-distinct lists such as [1] and [1].
- Using a set of objects fails because lists are unhashable; key by id().

**2. snapshot**

*Approach.* Recurse over lists, dicts and tuples, rebuilding each container and returning scalars unchanged. Containers are rebuilt, so later mutation of the original cannot leak in.

*Complexity.* Time and space O(total size).

*Common wrong answers.*

- Forgetting tuples that contain lists: a tuple is immutable but its contents may not be.
- Copying only the outer container (a shallow copy) leaves nested lists shared.

**3. add_tag (debug)**

*Approach.* A default value is evaluated once, when the def statement runs, so tags=[] is one shared list. Use None as the default and create the list inside the body.

*Complexity.* Time O(1) per call.

*Common wrong answers.*

- Writing tags = tags or [] also discards an empty list the caller passed in on purpose.
- Believing the default is rebuilt on each call: that is a common but wrong mental model.

</details>

---

## Chapter 01: Foundations: slicing, parsing, numbers

**The three exercises**

- chunk: split a sequence into fixed-size chunks.
- parse_kv: parse "a=1;b=two;c=" into a typed dict.
- total_cents (debugging): money arithmetic that is off by one cent sometimes.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 01 - Foundations: slicing, parsing, numbers.

1. chunk: split a sequence into fixed-size chunks.
2. parse_kv: parse "a=1;b=two;c=" into a typed dict.
3. total_cents (debugging): money arithmetic that is off by one cent sometimes."""

from decimal import Decimal

def chunk(seq, n):
    """Split `seq` into consecutive lists of length `n` (the last may be shorter). Raise ValueError if n <= 0."""
    raise NotImplementedError()

def parse_kv(line):
    """Parse 'a=1;b=two;c=' into {'a': 1, 'b': 'two', 'c': None}.
Integer-looking values (optional leading '-') become int, empty values become None, everything else stays str.
Ignore empty segments such as a trailing ';'. Split each pair on the FIRST '=' only; a segment without '=' raises ValueError."""
    raise NotImplementedError()

def total_cents(prices):
    """Sum price strings like "19.99" and return the total as an integer number of cents."""
    return int(sum(float(p) for p in prices) * 100)
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Think about dividing a list into slices of size k.
2. Use range(0, len(items), k) to generate slice start points.
3. Slice items[i:i+k] and raise ValueError if k <= 0.

**Exercise 2**

1. Split string lines and partition key-value pairs.
2. Use s.split('=', 1) so values with '=' aren't truncated.
3. Typecast booleans, ints, floats and strip extraneous whitespace.

**Exercise 3**

1. Floating-point math in financial calculations introduces binary precision rounding errors.
2. Avoid float arithmetic; multiply dollar amounts by 100 or use Decimal/integer cents.
3. Store and compute monetary values as integer cents.

</details>

<details>
<summary>What the hidden tests check</summary>

- `chunk_basic`
- `chunk_rejects_bad_size`
- `parse_kv_first_equals_and_errors`
- `parse_kv_types`
- `total_cents_exact`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
from decimal import Decimal

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
```

**1. chunk**

*Approach.* Step a start index by n and slice. Slicing past the end is safe, so the last chunk is simply shorter. Validate n first.

*Complexity.* Time O(len), space O(len).

*Common wrong answers.*

- Computing the chunk count with // and dropping the remainder.
- Forgetting n <= 0 would loop forever or return nonsense.

**2. parse_kv**

*Approach.* Split on ';', skip blank segments, split each pair on the FIRST '=' only, then convert: empty to None, optional minus plus digits to int, else the string.

*Complexity.* Time O(len).

*Common wrong answers.*

- split('=') without maxsplit breaks values that contain '=' (URLs).
- str.isdigit() rejects negatives; strip one leading '-' before testing, and reject '1-2'.

**3. total_cents (debug)**

*Approach.* float cannot represent 0.29 exactly, so 0.29 * 100 is 28.999999999999996 and int() truncates to 28. Sum Decimal values and convert once.

*Complexity.* Time O(n).

*Common wrong answers.*

- round(x * 100) hides the problem for some inputs but keeps float error in the sum.
- Passing a float to Decimal(...) copies the binary error; construct from the string.

</details>

---

## Chapter 02: Data structures under the hood

**The three exercises**

- LRUCache: O(1) get/put with least-recently-used eviction.
- top_k_frequent: heap or counter based top-k with deterministic tie-breaking.
- dedupe_keep_order (debugging): removes duplicates but scrambles the order.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 02 - Data structures under the hood.

1. LRUCache: O(1) get/put with least-recently-used eviction.
2. top_k_frequent: heap or counter based top-k with deterministic tie-breaking.
3. dedupe_keep_order (debugging): removes duplicates but scrambles the order."""

import heapq
from collections import Counter, OrderedDict

class LRUCache:
    """Fixed-capacity cache. get(key) returns the value or None and marks the key most recently used.
    put(key, value) inserts or updates and evicts the least recently used key when over capacity.
    capacity must be >= 1 (ValueError otherwise). Both operations must be O(1)."""

    def __init__(self, capacity):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()

    def put(self, key, value):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

def top_k_frequent(words, k):
    """Return the k most frequent words, most frequent first; ties broken alphabetically.
Must run in O(n log k), not O(n log n). Return fewer than k if there are fewer distinct words."""
    raise NotImplementedError()

def dedupe_keep_order(items):
    """Remove duplicates from a list of hashable items, keeping the first occurrence of each in original order."""
    return list(set(items))
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Preserve first-seen order while filtering out duplicates in O(N).
2. Use a set to track seen elements while yielding or appending.
3. In Python 3.7+, dict.fromkeys() preserves insertion order and hashes in O(1).

**Exercise 2**

1. An LRU cache evicts the least recently used item when capacity is exceeded.
2. Use collections.OrderedDict or a doubly-linked list with hash map.
3. When accessing or updating a key, call move_to_end(key); popitem(last=False) when full.

**Exercise 3**

1. Finding top K frequent elements efficiently without sorting the full array in O(N log N).
2. Count frequencies with collections.Counter, then use a min-heap of size K via heapq.
3. heapq.nlargest(k, counter.items(), key=lambda x: (x[1], x[0])) gives O(N log K).

</details>

<details>
<summary>What the hidden tests check</summary>

- `dedupe_order`
- `lru_eviction_order`
- `lru_update_and_capacity`
- `top_k_scales`
- `top_k_ties_and_short`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import heapq
from collections import Counter, OrderedDict

class LRUCache:
    """Fixed-capacity cache. get(key) returns the value or None and marks the key most recently used.
    put(key, value) inserts or updates and evicts the least recently used key when over capacity.
    capacity must be >= 1 (ValueError otherwise). Both operations must be O(1)."""

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self._d = OrderedDict()

    def get(self, key):
        if key not in self._d:
            return None
        self._d.move_to_end(key)
        return self._d[key]

    def put(self, key, value):
        self._d[key] = value
        self._d.move_to_end(key)
        if len(self._d) > self.capacity:
            self._d.popitem(last=False)

    def __len__(self):
        return len(self._d)

def top_k_frequent(words, k):
    """Return the k most frequent words, most frequent first; ties broken alphabetically.
    Must run in O(n log k), not O(n log n). Return fewer than k if there are fewer distinct words."""
    counts = Counter(words)
    return [w for w, _ in heapq.nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))]

def dedupe_keep_order(items):
    """Remove duplicates from a list of hashable items, keeping the first occurrence of each in original order."""
    return list(dict.fromkeys(items))
```

**1. LRUCache**

*Approach.* OrderedDict keeps insertion order and move_to_end is O(1). get moves the key to the end; put inserts, moves it, and pops the oldest when over capacity.

*Complexity.* get and put O(1); space O(capacity).

*Common wrong answers.*

- A plain dict plus list scan makes each access O(n).
- Updating an existing key must also refresh its recency.

**2. top_k_frequent**

*Approach.* Count with Counter, then heapq.nsmallest(k, ...) keyed by (-count, word) keeps only k items in the heap and gives deterministic ties.

*Complexity.* Time O(n + m log k) for m distinct words; space O(m).

*Common wrong answers.*

- sorted(...)[:k] is O(m log m), which the speed test rejects at scale.
- Ties left to dict order are not deterministic across inputs.

**3. dedupe_keep_order (debug)**

*Approach.* set() throws away order. dict preserves insertion order and dict.fromkeys(items) keeps the first occurrence of each key.

*Complexity.* Time O(n), space O(n).

*Common wrong answers.*

- list(set(items)) looks right on small inputs and fails on order.
- Checking 'x in result' on a list makes the loop O(n squared).

</details>

---

## Chapter 03: Functions, closures, decorators

**The three exercises**

- memoize: a caching decorator that counts hits and misses.
- compose: right-to-left function composition.
- make_multipliers (debugging): every returned function multiplies by the same number.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 03 - Functions, closures, decorators.

1. memoize: a caching decorator that counts hits and misses.
2. compose: right-to-left function composition.
3. make_multipliers (debugging): every returned function multiplies by the same number."""

import functools

def memoize(fn):
    """Cache results by positional and keyword arguments (all hashable). The wrapper exposes
`.hits` and `.misses` counters and keeps the wrapped function's __name__ and __doc__."""
    raise NotImplementedError()

def compose(*fns):
    """compose(f, g, h)(x) == f(g(h(x))). compose() is the identity function."""
    raise NotImplementedError()

def make_multipliers(n):
    """Return a list of n functions; the i-th function multiplies its argument by i."""
    return [lambda x: x * i for i in range(n)]
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Function composition applies functions from right to left or left to right.
2. functools.reduce(lambda acc, f: f(acc), funcs, initial_value) simplifies chaining.
3. Return a closure taking *args, **kwargs and passing the intermediate result through funcs.

**Exercise 2**

1. Late binding in closures: loop variables bind by reference to the enclosing frame.
2. Default argument values freeze values at closure definition time: `def mul(x, i=i):`.
3. Alternatively, use a factory function `make_mul(i)` that creates an isolated scope.

**Exercise 3**

1. Decorators that replace functions lose original docstrings, __name__, and signatures.
2. functools.wraps(fn) copies __module__, __name__, __qualname__, __doc__, and __annotations__.
3. Ensure the wrapper function returns the decorated function result and maintains cache hits.

</details>

<details>
<summary>What the hidden tests check</summary>

- `compose_order`
- `make_multipliers_late_binding`
- `memoize_counts`
- `memoize_metadata`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import functools

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
```

**1. memoize**

*Approach.* Build a key from args and sorted kwargs, keep a dict, count hits and misses on the wrapper, and apply functools.wraps so the name and docstring survive.

*Complexity.* O(1) average per call; space O(distinct calls).

*Common wrong answers.*

- Keying on args only makes f(1, b=2) and f(1) collide.
- Without functools.wraps, __name__ becomes 'wrapper' and debugging gets harder.

**2. compose**

*Approach.* Apply the functions right to left: reversed(fns). With no functions return the identity.

*Complexity.* O(number of functions) per call.

*Common wrong answers.*

- Applying left to right reverses the meaning of compose(f, g).
- Forgetting the empty case.

**3. make_multipliers (debug)**

*Approach.* Closures capture the variable, not its value, so every lambda sees the final i. Bind the current value with a default argument (i=i).

*Complexity.* O(n) to build.

*Common wrong answers.*

- Wrapping in a list comprehension does not fix it; the comprehension variable is still shared.
- functools.partial also works; the default-argument trick is the idiom.

</details>

---

## Chapter 04: OOP, dunder methods, metaprogramming

**The three exercises**

- Money: a value object with arithmetic and ordering dunders.
- Plugin: subclasses register themselves by name via __init_subclass__.
- Point (debugging): equal points cannot be used as dictionary keys.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 04 - OOP, dunder methods, metaprogramming.

1. Money: a value object with arithmetic and ordering dunders.
2. Plugin: subclasses register themselves by name via __init_subclass__.
3. Point (debugging): equal points cannot be used as dictionary keys."""

class Money:
    """Value object: Money(cents, currency='USD'). Supports + (same currency only, else ValueError),
    ==, <, hash (equal objects hash equal), and repr like Money(1050, 'USD'). Instances are immutable by convention."""

    def __init__(self, cents, currency='USD'):
        raise NotImplementedError()

    def _check(self, other):
        raise NotImplementedError()

    def __add__(self, other):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def __lt__(self, other):
        raise NotImplementedError()

    def __hash__(self):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()

class Plugin:
    """Base class. Every subclass that defines a class attribute `name` is registered under it.
    Plugin.create(name, *args) instantiates the registered subclass; unknown names raise KeyError.
    Two subclasses with the same name raise ValueError at class-definition time."""
    registry = {}

    def __init_subclass__(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def create(cls, name, *args):
        raise NotImplementedError()

class Point:
    """Immutable-ish 2D point: equal coordinates mean equal points, and points work as dict keys."""

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Creating custom immutable value types that support arithmetic and hashing.
2. Implement __eq__, __hash__, and arithmetic dunder methods (__add__, __sub__).
3. Ensure objects with equal values produce identical __hash__ values for set/dict storage.

**Exercise 2**

1. Validating attribute assignment dynamically on classes.
2. Use the descriptor protocol (__set_name__, __get__, __set__) or __setattr__.
3. Store private state in instance.__dict__ with private prefixed keys to avoid recursion.

**Exercise 3**

1. Metaclass or __init_subclass__ registry duplicate handling.
2. When a subclass registers a duplicate name, validate before adding to the registry dict.
3. Raise ValueError with descriptive message if the key already exists.

</details>

<details>
<summary>What the hidden tests check</summary>

- `money_arithmetic`
- `money_hash_and_set`
- `plugin_duplicates`
- `plugin_registry`
- `point_hashable`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
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
```

**1. Money**

*Approach.* A value object defines __eq__ and __hash__ together over the same fields, orders with __lt__, and refuses to mix currencies with a ValueError. Return NotImplemented for foreign types.

*Complexity.* O(1) per operation.

*Common wrong answers.*

- Defining __eq__ without __hash__ makes instances unhashable.
- Raising TypeError instead of returning NotImplemented blocks reflected operations.

**2. Plugin registry**

*Approach.* __init_subclass__ runs when a subclass is created. Read cls.__dict__.get('name') so inherited names do not register twice, and reject duplicates there.

*Complexity.* O(1) per subclass.

*Common wrong answers.*

- Using getattr(cls, 'name') also finds the parent's name and mis-registers subclasses.
- A metaclass works but is heavier than the hook.

**3. Point (debug)**

*Approach.* Defining __eq__ sets __hash__ to None, so instances become unhashable. Define __hash__ over the same fields used by __eq__.

*Complexity.* O(1).

*Common wrong answers.*

- Hashing a mutable field lets the hash change while the object sits in a set.
- hash(id(self)) breaks the rule that equal objects hash equal.

</details>

---

## Chapter 05: Memory, GIL, garbage collection

**The three exercises**

- WeakCache: a get-or-create cache that never keeps objects alive.
- deep_size: recursive sys.getsizeof that counts shared objects once.
- EventBus (debugging): subscribers are never freed.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 05 - Memory, GIL, garbage collection.

1. WeakCache: a get-or-create cache that never keeps objects alive.
2. deep_size: recursive sys.getsizeof that counts shared objects once.
3. EventBus (debugging): subscribers are never freed."""

import sys
import weakref

class WeakCache:
    """get_or_create(key, factory) returns the cached object for key, calling factory() only when there is no live one.
    The cache holds values weakly: once nothing else references a value, it disappears (a later call recreates it)."""

    def __init__(self):
        raise NotImplementedError()

    def get_or_create(self, key, factory):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

def deep_size(obj, _seen=None):
    """Total sys.getsizeof of obj plus everything reachable through lists, tuples, sets, frozensets and dicts
(keys and values), counting each distinct object (by id) once."""
    raise NotImplementedError()

class EventBus:
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
        return len(self._subs)
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Calculating recursive deep memory size of complex nested objects.
2. sys.getsizeof() only reports the shallow pointer array container overhead.
3. Traverse nested containers recursively while maintaining a `seen` set of object ids.

**Exercise 2**

1. Avoid memory leaks from long-lived event listeners or caches.
2. Use weakref.ref, weakref.WeakSet, or weakref.WeakKeyDictionary.
3. When the target object is dereferenced externally, it is cleanly garbage collected.

**Exercise 3**

1. Circular reference leaks with __del__ methods in older CPython versions.
2. Break reference cycles explicitly or rely on weakref callbacks instead of __del__.
3. Call gc.collect() to reclaim cyclic graphs that cannot be freed by refcounts.

</details>

<details>
<summary>What the hidden tests check</summary>

- `deep_size_counts_shared_once`
- `deep_size_nested`
- `eventbus_drops_dead_subscribers`
- `weakcache_does_not_keep_alive`
- `weakcache_reuses_live_object`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import sys
import weakref

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
```

**1. WeakCache**

*Approach.* WeakValueDictionary drops an entry when its value has no other strong reference. get_or_create returns the live object or builds a new one.

*Complexity.* O(1) average.

*Common wrong answers.*

- A normal dict holds a strong reference and never frees the value.
- Values must support weak references; plain ints and strs do not.

**2. deep_size**

*Approach.* Recurse through containers adding sys.getsizeof, and track seen ids so a shared object is counted once. Count dict keys and values.

*Complexity.* Time O(objects), space O(objects).

*Common wrong answers.*

- Forgetting the seen-set double-counts shared objects and loops on cycles.
- sys.getsizeof is shallow: it ignores what a container points to.

**3. EventBus (debug)**

*Approach.* Bound methods hold a strong reference to their instance. Store weakref.WeakMethod, drop dead entries on every publish and when reporting length.

*Complexity.* Publish is O(subscribers).

*Common wrong answers.*

- weakref.ref on a bound method dies immediately because the method object is temporary; use WeakMethod.
- Not pruning dead references leaves len() wrong.

</details>

---

## Chapter 06: Concurrency: asyncio, threads

**The three exercises**

- run_bounded: run async tasks with a concurrency limit, results in input order.
- first_completed: return the result of whichever thread finishes first.
- fetch_all (debugging): ten "requests" take ten times as long as one. Why?

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 06 - Concurrency: asyncio, threads.

1. run_bounded: run async tasks with a concurrency limit, results in input order.
2. first_completed: return the result of whichever thread finishes first.
3. fetch_all (debugging): ten "requests" take ten times as long as one. Why?"""

import asyncio
import concurrent.futures
import time

async def run_bounded(factories, limit):
    """`factories` is a list of zero-argument async callables. Run them with at most `limit` running at once and
return their results in input order. If one raises, the exception propagates. limit < 1 raises ValueError."""
    raise NotImplementedError()

def first_completed(funcs, timeout):
    """Run the zero-argument callables in separate threads and return the result of the first to finish.
Raise TimeoutError if none finishes within `timeout` seconds. Do not wait for the slower ones before returning."""
    raise NotImplementedError()

async def fetch_all(n):
    """Simulate n concurrent 50 ms requests and return their ids in order. Total time must stay near 50 ms, not n * 50 ms."""
    async def fetch(i):
        time.sleep(0.05)
        return i
    return await asyncio.gather(*(fetch(i) for i in range(n)))
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Running multiple asynchronous coroutines concurrently with bounded parallelism.
2. Use asyncio.Semaphore to gate concurrent tasks.
3. Wrap coroutines in asyncio.create_task and await asyncio.gather(*tasks).

**Exercise 2**

1. Returning the first completed result from multiple async requests.
2. asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED).
3. Cancel remaining pending tasks to avoid socket leaks and dangling coroutines.

**Exercise 3**

1. CPU-bound or blocking I/O calls freezing the single-threaded asyncio event loop.
2. Never call time.sleep(), requests.get(), or heavy math directly inside coroutines.
3. Offload synchronous blocking code using `await asyncio.to_thread(func, *args)`.

</details>

<details>
<summary>What the hidden tests check</summary>

- `fetch_all_is_concurrent`
- `first_completed_is_fast`
- `first_completed_timeout`
- `run_bounded_errors`
- `run_bounded_limits_concurrency`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import asyncio
import concurrent.futures
import time

async def run_bounded(factories, limit):
    """`factories` is a list of zero-argument async callables. Run them with at most `limit` running at once and
    return their results in input order. If one raises, the exception propagates. limit < 1 raises ValueError."""
    if limit < 1:
        raise ValueError("limit must be >= 1")
    sem = asyncio.Semaphore(limit)

    async def guarded(f):
        async with sem:
            return await f()

    return await asyncio.gather(*(guarded(f) for f in factories))

def first_completed(funcs, timeout):
    """Run the zero-argument callables in separate threads and return the result of the first to finish.
    Raise TimeoutError if none finishes within `timeout` seconds. Do not wait for the slower ones before returning."""
    ex = concurrent.futures.ThreadPoolExecutor(max_workers=max(1, len(funcs)))
    try:
        futs = [ex.submit(f) for f in funcs]
        done, _ = concurrent.futures.wait(futs, timeout=timeout, return_when=concurrent.futures.FIRST_COMPLETED)
        if not done:
            raise TimeoutError("no task finished in time")
        return next(iter(done)).result()
    finally:
        ex.shutdown(wait=False, cancel_futures=True)

async def fetch_all(n):
    """Simulate n concurrent 50 ms requests and return their ids in order. Total time must stay near 50 ms, not n * 50 ms."""
    async def fetch(i):
        await asyncio.sleep(0.05)
        return i
    return await asyncio.gather(*(fetch(i) for i in range(n)))
```

**1. run_bounded**

*Approach.* A Semaphore(limit) gates a coroutine wrapper; gather(...) preserves input order and propagates the first exception.

*Complexity.* Time about ceil(n / limit) rounds; space O(n).

*Common wrong answers.*

- create_task for every job without a gate ignores the limit.
- Validate limit < 1 first: Semaphore(0) would deadlock.

**2. first_completed**

*Approach.* Submit to a ThreadPoolExecutor, wait(..., FIRST_COMPLETED, timeout), return the first result, and shut down with wait=False so slow tasks do not block the return.

*Complexity.* Time min(task times) plus overhead.

*Common wrong answers.*

- Using the executor as a context manager waits for every task on exit.
- Python threads cannot be killed: slow tasks keep running in the background.

**3. fetch_all (debug)**

*Approach.* time.sleep blocks the whole event loop, so ten 'concurrent' requests run one after another. Use await asyncio.sleep (or an async client).

*Complexity.* Total about one request's latency instead of n.

*Common wrong answers.*

- Wrapping the call in asyncio.gather does not help while the call itself blocks.
- run_in_executor is the fix when you cannot make the call async.

</details>

---

## Chapter 07: Type system and modern Python architecture

**The three exercises**

- check_types: runtime validation of a dict against a {key: type} schema.
- Version: a frozen, ordered dataclass parsed from "1.10.2".
- first_word (debugging): what a type checker would flag: the Optional is not handled.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 07 - Type system and modern Python architecture.

1. check_types: runtime validation of a dict against a {key: type} schema.
2. Version: a frozen, ordered dataclass parsed from "1.10.2".
3. first_word (debugging): what a type checker would flag: the Optional is not handled."""

from dataclasses import dataclass

def check_types(data, schema):
    """Return a sorted list of error strings, empty when valid. For each key in `schema` (name -> type):
missing key -> 'name: missing'; wrong type -> 'name: expected int, got str'. A bool is NOT accepted for int.
Keys not in the schema are ignored."""
    raise NotImplementedError()

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
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

def first_word(text: str | None) -> str:
    """Return the first whitespace-separated word of `text`, or '' when text is None or blank."""
    return text.split()[0]
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Validating dictionary data at runtime against type annotations.
2. Inspect __annotations__ and use typing.get_origin / typing.get_args.
3. Handle Union types, Optional types, and check isinstance() accordingly.

**Exercise 2**

1. Immutable dataclass-like class versioning.
2. Freeze attributes by defining __setattr__ to disallow mutation after initialization.
3. Implement custom __lt__, __gt__, and __eq__ based on parsed semantic version tuples.

**Exercise 3**

1. TypeVar variance: Covariance (covariant=True) allows subtypes; contravariance allows supertypes.
2. Immutable sequences should be covariant; mutable containers must be invariant.
3. Use typing.Protocol for structural duck-typing without inheritance hierarchies.

</details>

<details>
<summary>What the hidden tests check</summary>

- `check_types_valid_and_missing`
- `check_types_wrong_and_bool`
- `first_word_handles_none`
- `version_frozen_and_errors`
- `version_order_and_parse`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
from dataclasses import dataclass

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
```

**1. check_types**

*Approach.* Loop over the schema; report missing keys and wrong types. Treat bool as not-an-int by checking it first, because bool subclasses int.

*Complexity.* O(schema size).

*Common wrong answers.*

- isinstance(True, int) is True, so a bare isinstance accepts booleans.
- Forgetting to sort the errors makes output order depend on dict order.

**2. Version**

*Approach.* A frozen, ordered dataclass compares fields in order, so tuple-style numeric comparison comes for free. Parse with split('.') and validate each part.

*Complexity.* O(parts).

*Common wrong answers.*

- Comparing version strings sorts '1.10' before '1.9'.
- Omitting frozen=True lets callers mutate keys that are used in sets.

**3. first_word (debug)**

*Approach.* None has no split, and an empty string yields an empty list. Normalise with (text or '').split() and check the list before indexing.

*Complexity.* O(len).

*Common wrong answers.*

- A type annotation does not change runtime behaviour; the code still crashes on None.
- text.split()[0] raises IndexError for blank strings, not only None.

</details>

