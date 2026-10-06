# Chapter 03-B: Design Patterns Catalog, Part 2

> **Core Learning Objective:** Complete the pattern vocabulary you need in a low-level design interview: Singleton, Prototype, Decorator, Facade, Composite, Bridge, Flyweight, Template Method, Chain of Responsibility, Iterator, Mediator, Memento and Visitor. Every example below runs as written, ends with assertions, and says when Python makes the pattern unnecessary.

Part 1 (Chapter 03) covered Factory, Builder, Adapter, Proxy, Strategy, Observer, Command and State. Together the two chapters cover the patterns that actually appear in interviews and in real codebases; the remaining GoF patterns (Abstract Factory variants, Interpreter) are rarely asked and are covered by their names in the glossary at the end.

---

## 1. How to Use a Pattern Without Over-Engineering

A pattern is a named solution to a recurring force. Name the force first:

| Force you feel | Pattern family | Pattern |
| :--- | :--- | :--- |
| "I need exactly one of these" | Creational | Singleton (usually: just pass one instance in) |
| "Creating it is expensive; I want a copy with changes" | Creational | Prototype |
| "I want to add behaviour without subclass explosion" | Structural | Decorator |
| "Callers should not know the five subsystems behind this" | Structural | Facade |
| "Part and whole should be treated the same" | Structural | Composite |
| "Two dimensions vary independently" | Structural | Bridge |
| "Millions of tiny objects share most of their data" | Structural | Flyweight |
| "The steps are fixed, the details vary" | Behavioural | Template Method |
| "Several handlers might deal with it; sender should not know which" | Behavioural | Chain of Responsibility |
| "Walk a collection without exposing its structure" | Behavioural | Iterator |
| "Objects talk to each other in a tangle" | Behavioural | Mediator |
| "I need undo or a snapshot" | Behavioural | Memento |
| "New operations over a stable set of node types" | Behavioural | Visitor |

---

## 2. Creational Patterns

### Singleton: one instance, safely

```python
import threading

class Config:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:                 # fast path, no lock once built
            with cls._lock:
                if cls._instance is None:         # re-check inside the lock
                    inst = super().__new__(cls)
                    inst.values = {}
                    cls._instance = inst
        return cls._instance

assert Config() is Config()

ids = []
threads = [threading.Thread(target=lambda: ids.append(id(Config()))) for _ in range(20)]
for t in threads: t.start()
for t in threads: t.join()
assert len(set(ids)) == 1                         # 20 racing threads, one object
```

**Python note.** A module is imported once, so a module-level object (`settings = Settings()`) is already a singleton with no ceremony. The real objection to the pattern is not construction but **hidden global state**: tests cannot isolate it. Prefer creating one instance at start-up and passing it to whoever needs it.

### Prototype: clone and tweak

```python
import copy
from dataclasses import dataclass, field, replace

@dataclass
class ReportTemplate:
    name: str
    sections: list = field(default_factory=list)

base = ReportTemplate("quarterly", ["summary", "risks"])

deep = copy.deepcopy(base)
deep.sections.append("appendix")
assert base.sections == ["summary", "risks"]      # deep copy: independent

shallow = replace(base, name="monthly")           # dataclasses.replace copies fields shallowly
assert shallow.sections is base.sections          # shares the same list: a classic trap
```

**Pitfall.** `copy.copy` and `dataclasses.replace` copy references to mutable fields. Use `deepcopy` when the clone will mutate nested data, and remember it is slow for large graphs.

---

## 3. Structural Patterns

### Decorator: add behaviour by wrapping

```python
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> int: ...

class Espresso(Coffee):
    def cost(self) -> int:
        return 200

class AddOn(Coffee):
    price = 0
    def __init__(self, inner: Coffee):
        self.inner = inner
    def cost(self) -> int:
        return self.inner.cost() + self.price

class Milk(AddOn):
    price = 50

class Sugar(AddOn):
    price = 10

assert Sugar(Milk(Espresso())).cost() == 260
assert Milk(Milk(Espresso())).cost() == 300      # decorators stack in any order and any number
```

Four add-ons as subclasses would need up to 16 combinations; decorators need four classes. Do not confuse this with Python's `@decorator` syntax, which is a related idea applied to functions.

### Facade: one simple door to a messy subsystem

```python
class Inventory:
    def reserve(self, sku: str) -> bool:
        return sku != "OUT-OF-STOCK"

class Payments:
    def charge(self, cents: int) -> str:
        return f"receipt-{cents}"

class Shipping:
    def schedule(self, sku: str) -> str:
        return f"track-{sku}"

class OrderFacade:
    def __init__(self):
        self.inventory, self.payments, self.shipping = Inventory(), Payments(), Shipping()

    def place(self, sku: str, cents: int) -> dict:
        if not self.inventory.reserve(sku):
            return {"ok": False, "reason": "out of stock"}
        return {"ok": True, "receipt": self.payments.charge(cents), "tracking": self.shipping.schedule(sku)}

shop = OrderFacade()
assert shop.place("BOOK", 1500) == {"ok": True, "receipt": "receipt-1500", "tracking": "track-BOOK"}
assert shop.place("OUT-OF-STOCK", 1500)["ok"] is False
```

A facade does not hide the subsystems; power users can still reach them. It narrows the common path.

### Composite: treat a tree and a leaf the same

```python
from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def size(self) -> int: ...

class File(Node):
    def __init__(self, size: int):
        self._size = size
    def size(self) -> int:
        return self._size

class Folder(Node):
    def __init__(self, *children: Node):
        self.children = list(children)
    def size(self) -> int:
        return sum(c.size() for c in self.children)

tree = Folder(File(10), Folder(File(5), File(7)), Folder())
assert tree.size() == 22                          # folder sizes recurse, empty folders are 0
```

This is the pattern behind file systems, UI widget trees, menus and org charts. The In-Memory File System case study uses it.

### Bridge: two dimensions that vary independently

```python
from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def circle(self, r: float) -> str: ...

class TextRenderer(Renderer):
    def circle(self, r: float) -> str:
        return f"circle r={r}"

class SvgRenderer(Renderer):
    def circle(self, r: float) -> str:
        return f'<circle r="{r}"/>'

class Shape:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer

class Circle(Shape):
    def __init__(self, renderer: Renderer, r: float):
        super().__init__(renderer)
        self.r = r
    def draw(self) -> str:
        return self.renderer.circle(self.r)

assert Circle(TextRenderer(), 2).draw() == "circle r=2"
assert Circle(SvgRenderer(), 2).draw() == '<circle r="2"/>'
```

With 3 shapes and 3 renderers, plain inheritance needs 9 classes; a bridge needs 6 and any new renderer works with every shape. Bridge is Strategy applied to a whole hierarchy.

### Flyweight: share the immutable part

```python
class Glyph:
    __slots__ = ("char", "font")
    def __init__(self, char: str, font: str):
        self.char, self.font = char, font

class GlyphFactory:
    def __init__(self):
        self._pool = {}
    def get(self, char: str, font: str) -> Glyph:
        key = (char, font)
        if key not in self._pool:
            self._pool[key] = Glyph(char, font)
        return self._pool[key]

factory = GlyphFactory()
text = [factory.get(c, "Mono") for c in "hello world"]
assert len(text) == 11 and len(factory._pool) == 8     # h e l o space w r d
assert factory.get("l", "Mono") is factory.get("l", "Mono")
```

The shared (intrinsic) state lives in the flyweight; the per-use (extrinsic) state, such as position, stays outside it. Python's `sys.intern` and small-integer caching are built-in flyweights.

---

## 4. Behavioural Patterns

### Template Method: fixed skeleton, variable steps

```python
from abc import ABC, abstractmethod

class Importer(ABC):
    def run(self, raw: str) -> list:              # the template: order is fixed
        rows = self.parse(raw)
        good = [r for r in rows if self.valid(r)]
        self.save(good)
        return good

    @abstractmethod
    def parse(self, raw: str) -> list: ...
    def valid(self, row) -> bool:                  # hook with a default
        return True
    @abstractmethod
    def save(self, rows: list) -> None: ...

class CsvImporter(Importer):
    def __init__(self):
        self.saved = []
    def parse(self, raw):
        return [line.split(",") for line in raw.splitlines()]
    def valid(self, row):
        return len(row) == 2
    def save(self, rows):
        self.saved.extend(rows)

imp = CsvImporter()
assert imp.run("a,1\nbroken\nb,2") == [["a", "1"], ["b", "2"]]
assert imp.saved == [["a", "1"], ["b", "2"]]
```

Template Method uses inheritance; if the steps are small you can pass them as functions (Strategy) and avoid the subclass.

### Chain of Responsibility: pass it along until someone handles it

```python
class Approver:
    def __init__(self, name: str, limit: int, successor=None):
        self.name, self.limit, self.successor = name, limit, successor

    def approve(self, amount: int) -> str:
        if amount <= self.limit:
            return f"{self.name} approved {amount}"
        if self.successor is None:
            return f"rejected {amount}: nobody can approve it"
        return self.successor.approve(amount)

chain = Approver("manager", 1_000, Approver("director", 10_000, Approver("cfo", 100_000)))
assert chain.approve(500) == "manager approved 500"
assert chain.approve(5_000) == "director approved 5000"
assert chain.approve(500_000).startswith("rejected")
```

Web middleware (authentication, logging, rate limiting) is a chain of responsibility, with the twist that every link may also act before and after the next one.

### Iterator: walk without exposing structure

```python
from itertools import islice

class Countdown:                                  # the class-based protocol
    def __init__(self, start: int):
        self.n = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

def fibonacci():                                  # the Pythonic way: a generator
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

assert list(Countdown(3)) == [3, 2, 1]
assert list(islice(fibonacci(), 8)) == [0, 1, 1, 2, 3, 5, 8, 13]   # infinite and lazy
```

Python bakes the pattern into the language: any object with `__iter__` works in `for`, comprehensions and `list()`. Write a generator unless you need the iterator to carry extra methods.

### Mediator: replace many-to-many with many-to-one

```python
class ChatRoom:
    def __init__(self):
        self.users = {}
    def join(self, user):
        self.users[user.name] = user
        user.room = self
    def send(self, sender: str, text: str):
        for name, user in self.users.items():
            if name != sender:
                user.inbox.append(f"{sender}: {text}")

class User:
    def __init__(self, name: str):
        self.name, self.inbox, self.room = name, [], None
    def say(self, text: str):
        self.room.send(self.name, text)

room, ana, bo, cy = ChatRoom(), User("ana"), User("bo"), User("cy")
for u in (ana, bo, cy):
    room.join(u)
ana.say("hi")
assert bo.inbox == ["ana: hi"] and cy.inbox == ["ana: hi"] and ana.inbox == []
```

Users know only the room, never each other, so n users need n links instead of n squared. The risk is a mediator that grows into a god object: keep it to routing.

### Memento: snapshot and restore

```python
class Editor:
    def __init__(self):
        self.text = ""
        self._history = []
    def type(self, s: str):
        self._history.append(self.text)           # the memento is just an immutable snapshot
        self.text += s
    def undo(self):
        if self._history:
            self.text = self._history.pop()

e = Editor()
e.type("hello"); e.type(" world")
assert e.text == "hello world"
e.undo(); assert e.text == "hello"
e.undo(); e.undo(); assert e.text == ""           # undoing past the start is a no-op
```

Store snapshots of immutable data (strings, tuples) so they cannot be corrupted later. For large state, store diffs (the Command pattern with an `undo()` method) rather than full copies.

### Visitor: add operations without touching the node classes

```python
from functools import singledispatch

class Num:
    def __init__(self, v): self.v = v

class Add:
    def __init__(self, l, r): self.l, self.r = l, r

class Mul:
    def __init__(self, l, r): self.l, self.r = l, r

@singledispatch
def evaluate(node):
    raise TypeError(f"unknown node {type(node).__name__}")

@evaluate.register
def _(node: Num): return node.v
@evaluate.register
def _(node: Add): return evaluate(node.l) + evaluate(node.r)
@evaluate.register
def _(node: Mul): return evaluate(node.l) * evaluate(node.r)

@singledispatch
def show(node): raise TypeError
@show.register
def _(node: Num): return str(node.v)
@show.register
def _(node: Add): return f"({show(node.l)} + {show(node.r)})"
@show.register
def _(node: Mul): return f"{show(node.l)} * {show(node.r)}"

expr = Mul(Add(Num(2), Num(3)), Num(4))
assert evaluate(expr) == 20
assert show(expr) == "(2 + 3) * 4"
```

The classic GoF Visitor uses `accept()` and double dispatch; `functools.singledispatch` gives the same open set of operations in a few lines. Visitor pays off when the node types are stable and operations keep growing (compilers, linters); it hurts when new node types appear often, because every visitor must change.

---

## 5. Look-Alikes: Choosing Between Them

| Pair | Real difference |
| :--- | :--- |
| Decorator vs Proxy | Decorator adds behaviour and is usually stacked by the client; a proxy controls access (lazy load, cache, auth) to one real object |
| Decorator vs Adapter | Adapter changes the interface; decorator keeps it |
| Facade vs Adapter | Facade simplifies many interfaces into a new one; adapter makes one interface match an expected one |
| Strategy vs State | Strategy is chosen from outside; State changes itself as the object moves between states |
| Strategy vs Template Method | Strategy composes (a swapped object); Template Method inherits (a subclass overrides steps) |
| Observer vs Mediator | Observer broadcasts to unknown listeners; Mediator centralises two-way coordination between known colleagues |
| Composite vs Decorator | Both nest, but composite aggregates many children, decorator wraps exactly one |

## 6. Patterns the Language Already Gives You

| Pattern | Python replacement |
| :--- | :--- |
| Singleton | A module-level instance |
| Iterator | Generators and `__iter__` |
| Strategy | Pass a function |
| Command | Pass a callable or `functools.partial` |
| Factory | Classes are callable; pass the class itself |
| Visitor | `functools.singledispatch` |
| Decorator (function form) | The `@` syntax and `functools.wraps` |

Saying this in an interview shows judgment: use the pattern for the shared vocabulary, implement it with the lightest idiom.

## 7. Glossary of the Remaining Patterns

- **Abstract Factory:** a factory of factories producing families of related objects (for example one UI toolkit's button, menu and window together).
- **Interpreter:** represents a small language's grammar as classes and evaluates sentences; in practice you reach for a parser library.
- **Observer, Strategy, State, Command, Builder, Adapter, Proxy, Factory Method:** see Chapter 03.

---

## Further Reading

- [Refactoring Guru: Composite](https://refactoring.guru/design-patterns/composite)
- [Refactoring Guru: Visitor](https://refactoring.guru/design-patterns/visitor)
- [Python docs: functools.singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch)
- [Python docs: copy module](https://docs.python.org/3/library/copy.html)

---

## Check Yourself

Answer in your head or on paper first, then open each answer.

<details>
<summary><strong>1.</strong> Why is `dataclasses.replace` not a deep clone, and when does that bite?</summary>

It copies field references, so mutable fields (lists, dicts) are shared between the original and the copy; mutating one changes both. Use `copy.deepcopy` when the clone will modify nested data.

</details>

<details>
<summary><strong>2.</strong> Decorator or subclassing for toppings on a drink?</summary>

Decorators: toppings combine freely at runtime, so n toppings need n classes rather than up to 2 to the power n subclasses.

</details>

<details>
<summary><strong>3.</strong> When does Visitor become a bad fit?</summary>

When new node types are added often: every existing visitor must gain a case for each new node. It suits stable node sets with growing operations.

</details>

<details>
<summary><strong>4.</strong> Which of these does Python make mostly unnecessary, and why?</summary>

Singleton (a module-level instance is one object), Iterator (generators), Strategy and Command (functions are first-class), Visitor (`singledispatch`). The ideas remain useful as shared vocabulary even when the heavy class structure is not.

</details>
