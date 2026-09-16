"""Diagnostic quiz questions, batch A: Modules 04-12.

Each entry is (title, code, symptom, questions, answer). A diagnostic question
shows real code plus an observed symptom and asks for cause, fix, and which test
would have caught it. That last part matters most: it connects debugging to the
test suite the learner already has.
"""

from __future__ import annotations

DIAGNOSTICS: dict[str, list[tuple[str, str, str, list[str], str]]] = {
    "04": [
        (
            "Shared mutable class attribute",
            '''class Account:
    transactions = []          # class attribute

    def __init__(self, owner: str) -> None:
        self.owner = owner

    def deposit(self, amount: float) -> None:
        self.transactions.append(amount)

a, b = Account("ada"), Account("bob")
a.deposit(100)
print(b.transactions)''',
            "Prints `[100]` — Bob sees Ada's deposit.",
            [
                "Why does Bob's account contain Ada's transaction?",
                "What is the one-line fix?",
                "What would the same code do if `transactions` were an `int` instead of a `list`?",
            ],
            "`transactions = []` is a **class** attribute, created once when the class body "
            "executes, and shared by every instance. `self.transactions.append(...)` looks up "
            "the name on the instance, fails, falls back to the class, and mutates the shared "
            "list.\n\n**Fix:** move it into `__init__` — `self.transactions: list[float] = []` "
            "— or use `field(default_factory=list)` in a dataclass.\n\n**With an `int`:** the bug "
            "would *hide*. `self.count += 1` rebinds rather than mutates, creating a genuine "
            "instance attribute on first write. That is why this bug is associated with mutable "
            "defaults specifically — immutable ones mask it.",
        ),
        (
            "`__eq__` without `__hash__`",
            '''class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

seen = {Point(1, 2)}
print(Point(1, 2) in seen)''',
            "Raises `TypeError: unhashable type: 'Point'`.",
            [
                "Why did defining `__eq__` make the class unhashable?",
                "What are the two correct fixes, and when would you choose each?",
                "What breaks if you define `__hash__` but leave it inconsistent with `__eq__`?",
            ],
            "Defining `__eq__` sets `__hash__ = None` implicitly. Python enforces the invariant "
            "that equal objects must hash equally; since it cannot infer your equality semantics, "
            "it removes hashability rather than let you violate it silently.\n\n**Fix 1** — "
            "define `__hash__ = lambda self: hash((self.x, self.y))` (do it properly as a method) "
            "when the object is logically immutable. **Fix 2** — use `@dataclass(frozen=True)`, "
            "which generates both consistently.\n\n**Inconsistent hash:** two equal objects with "
            "different hashes land in different buckets, so `in` returns `False` for an object "
            "that *is* present, and a dict can hold two keys that compare equal. Corruption that "
            "surfaces far from the cause.",
        ),
        (
            "MRO and cooperative `super()`",
            '''class Base:
    def __init__(self) -> None:
        self.log = ["Base"]

class Audited(Base):
    def __init__(self) -> None:
        Base.__init__(self)
        self.log.append("Audited")

class Timed(Base):
    def __init__(self) -> None:
        Base.__init__(self)
        self.log.append("Timed")

class Service(Audited, Timed):
    def __init__(self) -> None:
        Audited.__init__(self)
        Timed.__init__(self)

print(Service().log)''',
            "Prints `['Base', 'Timed']` — the `Audited` entry vanished.",
            [
                "Why is `'Audited'` missing from the log?",
                "How does replacing the explicit calls with `super().__init__()` fix it?",
                "What is `Service.__mro__` here?",
            ],
            "`Timed.__init__` calls `Base.__init__`, which **reassigns** `self.log = ['Base']`, "
            "discarding the `'Audited'` entry appended moments earlier. Explicit parent calls "
            "run `Base.__init__` twice.\n\n**Fix:** cooperative inheritance — every class calls "
            "`super().__init__()` exactly once, and Python walks the MRO linearly so `Base` runs "
            "only once: `['Base', 'Timed', 'Audited']`.\n\n**MRO:** `Service -> Audited -> Timed "
            "-> Base -> object`. Check it with `Service.__mro__`. This is the entire reason "
            "`super()` exists and why calling parents by name in a diamond is a bug.",
        ),
        (
            "`__slots__` silently defeated",
            '''class Compact:
    __slots__ = ("x", "y")

class Sub(Compact):
    pass

s = Sub()
s.anything = 42
print(hasattr(s, "__dict__"))''',
            "Prints `True`, and the memory saving `__slots__` promised is gone.",
            [
                "Why does the subclass have a `__dict__`?",
                "What must `Sub` declare to keep the saving?",
                "How would you measure whether it worked?",
            ],
            "A subclass that does not declare its own `__slots__` gets a `__dict__` "
            "automatically, so instances of `Sub` carry both the slots *and* a dict — larger "
            "than a plain class.\n\n**Fix:** `class Sub(Compact): __slots__ = ()`. An empty tuple "
            "is the declaration that says 'no new attributes'.\n\n**Measure it** with "
            "`sys.getsizeof` plus `__sizeof__`, or `tracemalloc` over 100k instances. Module 21 "
            "adds a `@pytest.mark.perf` test for exactly this; a claim about memory that is not "
            "measured is not a claim.",
        ),
        (
            "Property that shadows its own setter",
            '''class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("below absolute zero")
        self.celsius = value        # <-- note this line

t = Temperature(20)''',
            "`RecursionError: maximum recursion depth exceeded`.",
            [
                "Trace the recursion. What calls what?",
                "What is the fix?",
                "Why did `__init__` not bypass the property?",
            ],
            "The setter assigns to `self.celsius`, which *is* the property, so the setter calls "
            "itself forever.\n\n**Fix:** assign to the backing attribute — `self._celsius = "
            "value`. The getter already reads `_celsius`, so the names must differ.\n\n"
            "`__init__` did not bypass it because attribute assignment always goes through the "
            "type's data descriptors. `self.celsius = celsius` in `__init__` is a *feature* here "
            "— it means construction gets the same validation as later writes.",
        ),
    ],
    "06": [
        (
            "Bare except swallows the interrupt",
            '''import time

def poll() -> None:
    while True:
        try:
            time.sleep(1)
            raise ConnectionError("upstream down")
        except:                      # noqa: E722
            print("retrying...")''',
            "Ctrl+C does not stop the program.",
            [
                "Why does Ctrl+C fail to terminate it?",
                "What is the minimal correct change?",
                "Which two other exceptions does a bare `except` catch that you almost never want?",
            ],
            "`except:` catches **`BaseException`**, which includes `KeyboardInterrupt`. Your "
            "handler prints 'retrying' and loops, so the interrupt is discarded.\n\n**Fix:** "
            "`except Exception:` — or better, `except ConnectionError:`, naming what you actually "
            "expect.\n\n**Also caught:** `SystemExit` (so `sys.exit()` stops working) and "
            "`GeneratorExit` (breaking generator cleanup). The rule: catch the narrowest "
            "exception that you can actually handle, and let everything else propagate.",
        ),
        (
            "Duplicate log lines",
            '''import logging

def get_logger() -> logging.Logger:
    logger = logging.getLogger("app")
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

for _ in range(3):
    get_logger().info("processing")''',
            "The first message prints once, the second twice, the third three times.",
            [
                "Why does the output multiply?",
                "Give two different fixes.",
                "What does `logger.propagate = False` change, and when is it the wrong fix?",
            ],
            "`logging.getLogger('app')` returns the **same** logger object every time — loggers "
            "are cached by name. Each call appends *another* handler, so the record is emitted "
            "once per handler.\n\n**Fix 1:** configure logging once at application start "
            "(`logging.basicConfig` or `dictConfig`) and only ever *get* loggers afterwards. "
            "**Fix 2:** guard with `if not logger.handlers:` before adding.\n\n"
            "`propagate = False` stops records reaching ancestor loggers. It fixes duplication "
            "caused by a handler on both the child *and* the root, but here the duplicate "
            "handlers are on the same logger, so it changes nothing. It is also a common "
            "over-correction that silently hides records from your central handler.",
        ),
        (
            "Lost exception context",
            '''def load_config(path: str) -> dict:
    try:
        import json
        return json.loads(open(path).read())
    except Exception:
        raise ValueError("bad config")''',
            "The traceback says only `ValueError: bad config` — you cannot tell whether the file "
            "was missing, unreadable, or malformed JSON.",
            [
                "What information was destroyed, and by what exactly?",
                "What two syntaxes preserve the cause, and how do they differ?",
                "When is discarding the original deliberately correct?",
            ],
            "Raising a new exception inside an `except` block does keep `__context__` "
            "implicitly, but the *message* discards the useful detail, and any `from None` "
            "would drop the chain entirely. The reader loses the filename and the original error "
            "type.\n\n**`raise ValueError('bad config') from exc`** sets `__cause__` — 'this was "
            "*caused by* that', printed as 'The above exception was the direct cause'. "
            "**Implicit chaining** (plain `raise`) sets `__context__` — 'this happened *while* "
            "handling that'. Prefer explicit `from exc`.\n\n**Discard deliberately** only at a "
            "trust boundary — e.g. an API handler that must not leak internal paths to a client. "
            "There you use `from None`, and you log the original before dropping it.",
        ),
        (
            "`finally` swallows the return value",
            '''def risky() -> int:
    try:
        raise RuntimeError("boom")
    finally:
        return 0

print(risky())''',
            "Prints `0`. The `RuntimeError` disappears entirely.",
            [
                "Why is the exception discarded?",
                "What is the rule this illustrates?",
                "What does a `return` inside `except` do to an exception raised in `try`?",
            ],
            "A `return` (or `break`, or `continue`) in a `finally` block **replaces** whatever "
            "was in flight — including an in-flight exception. The exception is discarded, not "
            "logged, not chained.\n\n**Rule:** `finally` is for cleanup only. Never return, "
            "break, or continue from it.\n\n**`return` in `except`** is different and legitimate: "
            "it handles the exception and returns a value. The danger is specifically `finally`, "
            "because it runs on *both* the success and failure paths, so the override is invisible "
            "when you read only the happy path.",
        ),
        (
            "Exception group from concurrent tasks",
            '''import asyncio

async def worker(n: int) -> int:
    if n == 2:
        raise ValueError("two is bad")
    if n == 3:
        raise KeyError("three is worse")
    return n

async def main() -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            for i in range(4):
                tg.create_task(worker(i))
    except ValueError as exc:
        print("caught:", exc)

asyncio.run(main())''',
            "`ExceptionGroup` propagates uncaught — the `except ValueError` never fires.",
            [
                "Why does `except ValueError` not match?",
                "What syntax handles this correctly?",
                "What happens to the `KeyError` if you only handle `ValueError`?",
            ],
            "`TaskGroup` collects every failure into a single **`ExceptionGroup`**, which is not "
            "a `ValueError`, so a plain `except ValueError` does not match it.\n\n**Fix:** "
            "`except* ValueError as eg:` — the `except*` syntax (PEP 654, Python 3.11+) matches "
            "*inside* the group and binds a sub-group containing only the matching "
            "exceptions.\n\n**The `KeyError`** is re-raised in a residual `ExceptionGroup` after "
            "your handler runs. That is the point: `except*` cannot accidentally swallow "
            "failures it did not address, unlike a broad `except Exception`.",
        ),
    ],
    "08": [
        (
            "Test order dependence",
            '''CACHE: dict[str, int] = {}

def test_populates_cache() -> None:
    CACHE["a"] = 1
    assert len(CACHE) == 1

def test_cache_starts_empty() -> None:
    assert len(CACHE) == 0''',
            "Both pass when run individually. Run together, the second fails. Run with "
            "`-p no:randomly` in the other order, both pass.",
            [
                "What is the actual defect?",
                "Name two mechanisms pytest gives you to fix it.",
                "Why is a test suite that only passes in one order dangerous even if it is green?",
            ],
            "Module-level mutable state (`CACHE`) is shared across tests. Test one leaves it "
            "dirty; test two asserts on a clean slate.\n\n**Fixes:** a `@pytest.fixture` with "
            "`autouse=True` that clears or rebuilds the state per test, or `monkeypatch` to "
            "install a fresh object. Best of all: don't use module-level mutable state — pass "
            "the cache in.\n\n**Why it is dangerous:** the suite is asserting less than you "
            "think. Order-dependent tests hide real bugs, break unpredictably under `-x`, "
            "parallelisation (`pytest-xdist`) or randomisation, and mean a single test's "
            "failure can be caused by an unrelated one. Green is not the same as correct.",
        ),
        (
            "Assert on a tuple is always true",
            '''def test_values() -> None:
    result = 2 + 2
    assert (result == 5, "arithmetic is broken")''',
            "The test passes.",
            [
                "Why does this pass despite `2 + 2 != 5`?",
                "What is the correct form?",
                "What does pytest do to help you catch this?",
            ],
            "`assert (expr, msg)` asserts a **two-element tuple**, which is always truthy. The "
            "comparison is evaluated and thrown away.\n\n**Correct:** `assert result == 5, "
            "'arithmetic is broken'` — comma outside the parentheses, no tuple.\n\n**pytest "
            "helps:** it emits a warning for an assert on a non-empty tuple, and `ruff` flags it "
            "as `F631`. This course's CI runs `ruff`, so the linter catches it before review. "
            "That is the general lesson: a linter is a test for your tests.",
        ),
        (
            "Float equality in a test",
            '''def test_total() -> None:
    prices = [0.1, 0.2]
    assert sum(prices) == 0.3''',
            "Fails with `assert 0.30000000000000004 == 0.3`.",
            [
                "Why is the sum not exactly 0.3?",
                "What should the assertion be?",
                "When is `Decimal` the right answer instead of a tolerance?",
            ],
            "Binary floating point cannot represent 0.1 or 0.2 exactly (IEEE 754), so the sum "
            "carries a representation error of ~4e-17. Module 01 introduces this; here it has "
            "consequences.\n\n**Fix:** `assert sum(prices) == pytest.approx(0.3)`, or "
            "`pytest.approx(0.3, abs=1e-9)` when you want an explicit tolerance.\n\n**Use "
            "`Decimal`** when the values are *money or any exact decimal quantity* and the "
            "rounding rules are part of the specification. A tolerance is right for physical "
            "measurement; exact decimal arithmetic is right for a ledger. Module 08's financial "
            "ledger project uses `Decimal` for precisely this reason.",
        ),
        (
            "Mock asserts nothing",
            '''from unittest.mock import Mock

def notify(client, user_id: int) -> None:
    client.send(user_id)

def test_notify() -> None:
    client = Mock()
    notify(client, 42)
    client.send_notification.assert_called_once()''',
            "The test passes, even though `notify` calls `send`, not `send_notification`.",
            [
                "Why does asserting on the wrong method name still pass?",
                "What single argument to `Mock` prevents this whole class of bug?",
                "What is the more robust alternative to mocking here?",
            ],
            "A plain `Mock` auto-creates any attribute you touch. `client.send_notification` "
            "springs into existence as a new Mock, and `assert_called_once` on it... also "
            "auto-creates. Nothing is verified.\n\nWait — `assert_called_once` on a never-called "
            "mock *does* fail. The subtler bug is that `client.send_notification` exists at all: "
            "if you assert `assert_not_called()` or check `call_count == 0`, you get a false "
            "pass, and a typo in a method name is never caught.\n\n**Fix:** "
            "`Mock(spec=RealClient)` or `autospec=True`, which raises `AttributeError` for any "
            "method the real class does not have.\n\n**More robust:** inject a small hand-written "
            "fake that implements a `Protocol` (Module 23). It cannot drift from the interface, "
            "and the type checker verifies it.",
        ),
        (
            "Property-based test with a hidden assumption",
            '''from hypothesis import given, strategies as st

def average(xs: list[float]) -> float:
    return sum(xs) / len(xs)

@given(st.lists(st.floats()))
def test_average_within_bounds(xs: list[float]) -> None:
    assert min(xs) <= average(xs) <= max(xs)''',
            "Hypothesis reports a falsifying example of `[]`, then `[nan]`, then `[inf, -inf]`.",
            [
                "Name the three distinct defects Hypothesis found.",
                "Which are bugs in `average` and which are bugs in the test?",
                "How do you express the constraints properly?",
            ],
            "**Three failures, three causes.** `[]` → `ZeroDivisionError`: a genuine bug in "
            "`average`, which has no defined behaviour for an empty list. `[nan]` → the "
            "comparison is `False` because any comparison with NaN is `False`: a bug in the "
            "*test's* assumption, since NaN has no ordering. `[inf, -inf]` → `inf + -inf` is NaN: "
            "again a real domain limit.\n\n**Fix `average`:** raise `ValueError` on an empty "
            "list. **Fix the test:** constrain the strategy — "
            "`st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1)`.\n\n"
            "This is exactly why property-based testing earns its place: three edge cases you "
            "would not have written by hand, found in one run. Module 08's ledger suite uses "
            "the same technique.",
        ),
    ],
    "09": [
        (
            "Unlocked shared counter",
            '''import threading

counter = 0

def increment() -> None:
    global counter
    for _ in range(100_000):
        counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)''',
            "Prints something less than 400000, and a different number each run.",
            [
                "The GIL exists — so why is this still a race?",
                "Give two fixes and state the cost of each.",
                "Would this be safe on a free-threaded (PEP 703) build?",
            ],
            "`counter += 1` is **not atomic**. It compiles to LOAD, ADD, STORE (check with "
            "`dis.dis`), and the interpreter can switch threads between those bytecodes. The GIL "
            "guarantees only that one bytecode runs at a time, never that a *statement* is "
            "indivisible.\n\n**Fix 1:** a `threading.Lock` around the update — correct, costs "
            "contention. **Fix 2:** `itertools.count()` or per-thread accumulators summed at the "
            "end — no lock, better scaling, more code.\n\n**Free-threaded build:** *less* safe, "
            "not more. Removing the GIL removes the accidental protection of coarse bytecode "
            "granularity, so unsynchronised code that happened to work now fails more often. "
            "Correct locking is required either way.",
        ),
        (
            "Deadlock from lock ordering",
            '''import threading, time

lock_a, lock_b = threading.Lock(), threading.Lock()

def task_one() -> None:
    with lock_a:
        time.sleep(0.01)
        with lock_b:
            pass

def task_two() -> None:
    with lock_b:
        time.sleep(0.01)
        with lock_a:
            pass

t1 = threading.Thread(target=task_one); t2 = threading.Thread(target=task_two)
t1.start(); t2.start(); t1.join(); t2.join()''',
            "The program hangs forever. Both threads are alive but idle.",
            [
                "Draw the wait-for cycle. Which thread holds what, and wants what?",
                "What is the standard prevention rule?",
                "Why does removing the `sleep` calls often make the bug *disappear*?",
            ],
            "`task_one` holds `lock_a` and waits for `lock_b`; `task_two` holds `lock_b` and "
            "waits for `lock_a`. A cycle in the wait-for graph, so neither can "
            "proceed.\n\n**Prevention:** impose a **global lock ordering** — every code path "
            "acquires locks in the same fixed order (say, always `a` before `b`). Alternatively "
            "use `acquire(timeout=...)` and back off, or restructure so only one lock is needed."
            "\n\n**Removing the sleeps** makes each critical section so short that one thread "
            "usually finishes before the other starts. The bug becomes rare, not absent — the "
            "worst possible state, because it will surface in production under load. The sleeps "
            "here are a deterministic reproduction of a real timing bug.",
        ),
        (
            "ProcessPool cannot pickle the worker",
            '''from concurrent.futures import ProcessPoolExecutor

def run() -> list[int]:
    def square(n: int) -> int:      # defined inside run()
        return n * n
    with ProcessPoolExecutor() as ex:
        return list(ex.map(square, range(4)))

print(run())''',
            "On Windows/macOS: `AttributeError: Can't pickle local object 'run.<locals>.square'`.",
            [
                "Why must the worker be picklable at all?",
                "What are the three ways to make this work?",
                "Why does the same code sometimes succeed on Linux?",
            ],
            "`ProcessPoolExecutor` sends the callable to a separate OS process. With the "
            "**spawn** start method (default on Windows, and macOS since 3.8) the callable is "
            "pickled **by qualified name** and re-imported in the child. A closure or a nested "
            "function has no importable name.\n\n**Three fixes:** (1) move `square` to module "
            "level — the normal answer; (2) use `functools.partial` over a module-level function; "
            "(3) switch to `ThreadPoolExecutor` if the work is actually I/O-bound.\n\n**On "
            "Linux** the default was historically **fork**, which copies the parent's memory "
            "wholesale, so the child already has the closure and no pickling is needed. Code "
            "that works on your Linux CI and fails on a colleague's Mac is almost always this. "
            "The Module 09 notebook demonstrates the fix with `nb_workers.py`.",
        ),
        (
            "Daemon thread killed mid-write",
            '''import threading, time

def writer() -> None:
    with open("out.txt", "w") as fh:
        for i in range(100_000):
            fh.write(f"line {i}\\n")

t = threading.Thread(target=writer, daemon=True)
t.start()
time.sleep(0.01)
print("main done")''',
            "`out.txt` is truncated mid-line, or empty, and no error is reported.",
            [
                "What does `daemon=True` actually change?",
                "Why is the file truncated rather than merely short?",
                "What is the correct pattern for background work that must finish?",
            ],
            "A daemon thread does not keep the interpreter alive. When the main thread exits, "
            "daemon threads are killed **abruptly** — no exception, no `finally`, no context "
            "manager `__exit__`.\n\n**Truncated, not short:** the file object's buffer is never "
            "flushed and `close()` never runs, so whatever sat in the 8 KB buffer is lost — "
            "often mid-line.\n\n**Correct pattern:** non-daemon thread plus an explicit "
            "`t.join()`, or a `threading.Event` for cooperative shutdown that the worker checks "
            "and responds to by cleaning up. Use daemon threads only for work that is genuinely "
            "safe to abandon, such as a metrics poller.",
        ),
        (
            "Threads for CPU work",
            '''import threading, time, math

def cpu() -> None:
    sum(math.sqrt(i) for i in range(3_000_000))

start = time.perf_counter()
cpu(); cpu()
print(f"sequential: {time.perf_counter() - start:.2f}s")

start = time.perf_counter()
ts = [threading.Thread(target=cpu) for _ in range(2)]
for t in ts: t.start()
for t in ts: t.join()
print(f"threaded:   {time.perf_counter() - start:.2f}s")''',
            "Threaded is the same speed or slightly *slower* than sequential, on a multi-core "
            "machine.",
            [
                "Why is there no speedup?",
                "What would you change to get real parallelism, and what does that cost?",
                "How would you decide, before writing code, which of the two to reach for?",
            ],
            "The work is pure CPU, so it holds the GIL throughout. Only one thread executes "
            "bytecode at a time; the extra threads add context-switching overhead and nothing "
            "else.\n\n**For real parallelism:** `ProcessPoolExecutor` — each process has its own "
            "interpreter and its own GIL. The cost is process startup (~50 ms), and every "
            "argument and result must be pickled, so it only pays off when the work per task "
            "clearly exceeds that overhead. A native extension that releases the GIL is the "
            "other route (Module 22 measures 3.21× thread scaling from Rust).\n\n**Decide "
            "up front:** if the thread would spend its time *waiting* (network, disk, "
            "subprocess), use threads or `asyncio` — waiting releases the GIL. If it would spend "
            "its time *computing*, use processes. That one question settles it.",
        ),
    ],
    "10": [
        (
            "Blocking call inside a coroutine",
            '''import asyncio, time

async def fetch(n: int) -> int:
    time.sleep(1)          # not asyncio.sleep
    return n

async def main() -> None:
    start = time.perf_counter()
    await asyncio.gather(*(fetch(i) for i in range(5)))
    print(f"{time.perf_counter() - start:.1f}s")

asyncio.run(main())''',
            "Takes 5 seconds. You expected about 1.",
            [
                "Why did `gather` not overlap the work?",
                "What is the fix for a genuinely blocking library you cannot change?",
                "How would you detect this class of bug automatically?",
            ],
            "`time.sleep` blocks the **event loop thread**. While it sleeps, no other coroutine "
            "can run — there is only one thread, and nothing yielded control. `await` is the only "
            "point at which the loop can switch.\n\n**Fix:** `await asyncio.sleep(1)` here. For a "
            "third-party blocking library, push it off the loop: `await asyncio.to_thread(func, "
            "*args)` (or `loop.run_in_executor`). For CPU-bound work use a "
            "`ProcessPoolExecutor`.\n\n**Detect it:** run with `asyncio.run(main(), debug=True)` "
            "or `PYTHONASYNCIODEBUG=1` — the loop logs any callback that takes longer than 100 ms. "
            "`aiodebug` and `blockbuster` do this more aggressively. In production, a rising "
            "event-loop-lag metric is the signal.",
        ),
        (
            "Coroutine never awaited",
            '''import asyncio

async def save(record: dict) -> None:
    await asyncio.sleep(0.01)
    print("saved", record)

async def main() -> None:
    for i in range(3):
        save({"id": i})        # no await
    print("done")

asyncio.run(main())''',
            "Prints only `done`, plus `RuntimeWarning: coroutine 'save' was never awaited`. "
            "Nothing is saved.",
            [
                "What does calling an `async def` function actually return?",
                "Give two correct ways to run all three concurrently.",
                "Why is this a warning rather than an error?",
            ],
            "Calling a coroutine function returns a **coroutine object**; it does not start "
            "executing. Discarding it means the body never runs.\n\n**Fix 1:** `await "
            "save(...)` in the loop — sequential. **Fix 2:** collect and gather — "
            "`await asyncio.gather(*(save({'id': i}) for i in range(3)))` — concurrent. In 3.11+ "
            "prefer `async with asyncio.TaskGroup() as tg: tg.create_task(...)`, which also "
            "cancels siblings on failure.\n\n**Only a warning** because Python cannot know at "
            "call time whether you intend to await later; it detects the mistake at garbage "
            "collection, by which point the call site is gone. Turn it into an error in CI with "
            "`-W error::RuntimeWarning`.",
        ),
        (
            "Task exception never retrieved",
            '''import asyncio

async def flaky() -> None:
    raise ValueError("failed")

async def main() -> None:
    asyncio.create_task(flaky())
    await asyncio.sleep(0.1)
    print("main finished normally")

asyncio.run(main())''',
            "Prints `main finished normally`, then `Task exception was never retrieved` on "
            "stderr. Exit code is 0.",
            [
                "Why did the `ValueError` not propagate?",
                "What are the two ways to make failures visible?",
                "Why is a zero exit code the dangerous part here?",
            ],
            "`create_task` schedules the coroutine and returns a `Task`. The exception is stored "
            "*on the task*; nobody awaited it, so nobody observed it. The event loop reports it "
            "only when the task is garbage collected.\n\n**Fix 1:** keep a reference and await "
            "it — `task = asyncio.create_task(...)`, then `await task`. **Fix 2 (better):** "
            "`asyncio.TaskGroup`, which propagates any child failure as an `ExceptionGroup` when "
            "the block exits, and cancels the remaining siblings.\n\n**The zero exit code** means "
            "CI passes, health checks pass, and your orchestrator believes the job succeeded. "
            "Silent failure with a success signal is worse than a crash. Also beware: a task "
            "with no strong reference can be garbage collected *mid-execution* — always keep the "
            "handle.",
        ),
        (
            "Unbounded concurrency",
            '''import asyncio, httpx

async def fetch(client: httpx.AsyncClient, url: str) -> int:
    r = await client.get(url)
    return r.status_code

async def main(urls: list[str]) -> None:
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*(fetch(client, u) for u in urls))''',
            "With 50,000 URLs: file-descriptor exhaustion, connection resets, and the target "
            "site rate-limits or bans you.",
            [
                "What did `gather` do that caused this?",
                "What is the idiomatic way to bound it?",
                "Why is a semaphore better than batching into chunks of N?",
            ],
            "`gather` starts **every** coroutine immediately. 50,000 concurrent connections "
            "exhausts local file descriptors and looks like an attack to the "
            "server.\n\n**Bound it** with a semaphore:\n\n```python\nsem = "
            "asyncio.Semaphore(20)\nasync def bounded(u):\n    async with sem:\n        return "
            "await fetch(client, u)\n```\n\n**Better than chunking** because a semaphore keeps "
            "the pipeline *full*: as soon as one request finishes, the next starts. Fixed batches "
            "of N wait for the slowest member of each batch before starting the next, so one slow "
            "URL idles 19 workers. Also set `httpx.Limits(max_connections=...)` and a per-request "
            "timeout — Module 10's scraper daemon does all three.",
        ),
        (
            "Async generator not closed",
            '''import asyncio

async def rows():
    conn = "opened"
    try:
        for i in range(1000):
            yield i
    finally:
        print("cleanup ran")

async def main() -> None:
    async for row in rows():
        if row > 2:
            break          # abandon the generator

asyncio.run(main())''',
            "`cleanup ran` prints late, at interpreter shutdown, or sometimes not at all — and "
            "in a real version the database connection leaks.",
            [
                "Why does `finally` not run at the `break`?",
                "What construct guarantees prompt cleanup?",
                "What does `asyncio.run` already do for you here, and why is it not enough?",
            ],
            "Breaking out of `async for` leaves the generator suspended at the `yield`. Its "
            "`finally` runs only when the generator is closed — which happens at garbage "
            "collection, at an unpredictable time, and requires a running event loop to await "
            "`aclose()`.\n\n**Fix:** `contextlib.aclosing` —\n\n```python\nasync with "
            "aclosing(rows()) as gen:\n    async for row in gen:\n        ...\n```\n\nThis "
            "guarantees `aclose()` on exit, so cleanup is prompt and deterministic.\n\n"
            "`asyncio.run` does call `loop.shutdown_asyncgens()` at the end, which is why the "
            "message appears *eventually*. That is not enough: the connection stayed open for the "
            "rest of the program, and in a long-lived service 'eventually' can mean hours and "
            "thousands of leaked handles.",
        ),
    ],
    "11": [
        (
            "Assuming one recv equals one message",
            '''import socket

def receive(sock: socket.socket) -> str:
    data = sock.recv(1024)
    return data.decode()''',
            "Sometimes returns half a message; sometimes two messages concatenated. Works fine "
            "on localhost, fails over the internet.",
            [
                "Why can one `recv` return partial or multiple messages?",
                "What are the two standard framing solutions?",
                "Why does localhost hide the bug?",
            ],
            "TCP is a **byte stream**, not a message protocol. It guarantees order and delivery, "
            "never that your logical message boundaries survive. The kernel coalesces small "
            "sends (Nagle) and splits large ones at the MTU.\n\n**Framing, two options:** "
            "(1) **length prefix** — send a fixed-width big-endian length, then read exactly that "
            "many bytes in a loop; (2) **delimiter** — terminate with `\\n` and buffer until you "
            "see one, which requires escaping the delimiter in payloads.\n\n**Localhost hides "
            "it** because there is no real MTU, no fragmentation, and near-zero latency, so a "
            "small message almost always arrives in one piece. The bug appears the moment there "
            "is a real network between the peers — that is, in production.",
        ),
        (
            "recv returns fewer bytes than requested",
            '''def read_exactly(sock, n: int) -> bytes:
    return sock.recv(n)''',
            "Occasionally returns short data and the caller misparses the record.",
            [
                "What does the `n` in `recv(n)` actually mean?",
                "Write the correct loop.",
                "What does an empty `bytes` return signify?",
            ],
            "`recv(n)` reads **at most** `n` bytes — whatever is available in the socket buffer "
            "right now. It is not a promise to fill your buffer.\n\n**Correct:**\n\n```python\n"
            "def read_exactly(sock, n):\n    buf = bytearray()\n    while len(buf) < n:\n"
            "        chunk = sock.recv(n - len(buf))\n        if not chunk:\n            raise "
            "ConnectionError('peer closed early')\n        buf += chunk\n    return "
            "bytes(buf)\n```\n\n**Empty bytes (`b''`)** means the peer performed an orderly "
            "shutdown — EOF. It is not an error and not 'no data yet'; a non-blocking socket "
            "with no data raises `BlockingIOError` instead. Conflating the two is how you get a "
            "busy-loop that pegs a core.",
        ),
        (
            "Address already in use",
            '''import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 8080))
server.listen()''',
            "After stopping and immediately restarting the server: "
            "`OSError: [Errno 98] Address already in use`.",
            [
                "Why is the port still held when the process has exited?",
                "What is the fix, and where must it go?",
                "When is that fix *unsafe*?",
            ],
            "The previous listening socket's connections are in **TIME_WAIT**, a mandatory 2×MSL "
            "wait (typically 30–120 s) that lets delayed duplicate packets drain before the "
            "4-tuple can be reused.\n\n**Fix:** `server.setsockopt(socket.SOL_SOCKET, "
            "socket.SO_REUSEADDR, 1)` — and it must be set **before** `bind()`, or it has no "
            "effect.\n\n**Unsafe when:** you actually have multiple processes racing to bind the "
            "same port and expect only one to win — `SO_REUSEADDR` can mask a real "
            "misconfiguration. `SO_REUSEPORT` is the deliberate load-balancing tool for that, and "
            "it has different semantics. For a dev server, `SO_REUSEADDR` is correct and "
            "standard.",
        ),
        (
            "No timeout on a socket",
            '''import socket

sock = socket.create_connection(("example.com", 80))
sock.sendall(b"GET / HTTP/1.0\\r\\n\\r\\n")
body = sock.recv(65536)''',
            "The process hangs indefinitely when the peer is unresponsive. No error, no log, no "
            "exit.",
            [
                "Which two distinct operations can block forever here?",
                "How do you bound each?",
                "Why is an application-level timeout still needed even with TCP keepalive?",
            ],
            "Both the **connect** and the **recv** can block without limit. A silently dropped "
            "packet stream produces no error at all — the socket simply never becomes "
            "readable.\n\n**Bound them:** `socket.create_connection(addr, timeout=5)` sets both "
            "the connect timeout and the default socket timeout; `sock.settimeout(10)` adjusts it "
            "afterwards. A timeout raises `socket.timeout` (an `OSError` subclass), which you "
            "must handle.\n\n**Keepalive is not enough:** TCP keepalive defaults to *two hours* "
            "of idle time before the first probe on Linux, and it detects a dead *connection*, "
            "not a slow or hung *application* that keeps the socket open and never replies. "
            "Always set an application-level deadline for the whole operation.",
        ),
        (
            "HTTP parsing by string splitting",
            '''def parse_status(raw: bytes) -> int:
    first_line = raw.split(b"\\n")[0]
    return int(first_line.split(b" ")[1])''',
            "Works against one server, raises `IndexError` or `ValueError` against another.",
            [
                "Name three ways a valid HTTP response breaks this parser.",
                "What should you use instead?",
                "What is the security risk of a hand-rolled parser here?",
            ],
            "**Three breakages:** (1) HTTP uses `\\r\\n`, so `first_line` retains a trailing "
            "`\\r` and the split shifts; (2) the reason phrase is optional, and multiple spaces "
            "are legal, so field positions vary; (3) the response may arrive across several "
            "`recv` calls, so `raw` may not contain a complete first line at all.\n\n**Use "
            "instead:** `h11` or `httptools` for a correct low-level parser, or `httpx`/"
            "`requests` at the application level. Writing HTTP by hand is a teaching exercise, "
            "not a production strategy.\n\n**Security risk:** inconsistent parsing between your "
            "code and an upstream proxy is the basis of **request smuggling** — the proxy and "
            "the server disagree about where one request ends and the next begins, letting an "
            "attacker inject a request into another user's connection. Header and length parsing "
            "is exactly where this happens.",
        ),
    ],
    "12": [
        (
            "Reference cycle keeps objects alive",
            '''import gc

class Node:
    def __init__(self) -> None:
        self.parent: "Node | None" = None
        self.children: list["Node"] = []

def build() -> None:
    root = Node()
    child = Node()
    root.children.append(child)
    child.parent = root          # cycle

for _ in range(100_000):
    build()
print(len(gc.get_objects()))''',
            "Memory grows steadily even though no `Node` is reachable after `build()` returns.",
            [
                "Why does reference counting alone not free these?",
                "What does the cyclic garbage collector do, and why is it not instant?",
                "What is the fix that avoids the cycle entirely?",
            ],
            "`root` refers to `child` and `child` refers back to `root`, so both refcounts stay "
            "at 1 after the function returns. Refcounting can never collect a cycle — that is "
            "its one structural weakness.\n\n**The cyclic GC** finds unreachable cycles by "
            "tracing, but it runs **generationally** on allocation thresholds, not immediately. "
            "Until it runs, the memory is held. `gc.collect()` forces it; "
            "`gc.set_threshold()` tunes it.\n\n**Avoid the cycle:** make the back-reference weak "
            "— `self.parent = weakref.ref(root)`. Then the child does not keep the parent alive, "
            "refcounting frees everything promptly, and the GC never has to get involved. This is "
            "the standard fix for parent pointers, observer registries and caches.",
        ),
        (
            "getsizeof misread as deep size",
            '''import sys

data = [list(range(1000)) for _ in range(1000)]
print(sys.getsizeof(data))''',
            "Reports about 8 KB for a structure holding a million integers.",
            [
                "What is `getsizeof` actually measuring?",
                "How do you get the real total?",
                "Why is even the 'real total' ambiguous for Python objects?",
            ],
            "`getsizeof` returns the size of **that object only** — here a list of 1000 "
            "*pointers*, 8 bytes each plus header. It does not follow references.\n\n**Real "
            "total:** walk it recursively (`pympler.asizeof`), or measure the process instead: "
            "`tracemalloc.start()` then `tracemalloc.get_traced_memory()`, which is what "
            "Module 12's profiler does.\n\n**Ambiguous because of sharing:** small ints "
            "(-5..256) are interned, so `range(1000)` shares 262 of its objects with everything "
            "else in the process. Strings may be interned too. Asking 'how big is this object' "
            "has no single answer when parts of it are shared globally — which is why "
            "process-level measurement before and after is the honest technique.",
        ),
        (
            "Bytecode reveals a hidden cost",
            '''def build_slow(items: list[str]) -> str:
    result = ""
    for item in items:
        result += item
    return result''',
            "Quadratic slowdown: 10× more items takes ~100× longer.",
            [
                "What does `dis.dis` show about the loop body that explains the cost?",
                "What is the linear alternative?",
                "Why does CPython sometimes make this look fast in a microbenchmark?",
            ],
            "`dis.dis` shows `BINARY_OP 13 (+=)` inside the loop. Strings are **immutable**, so "
            "each `+=` allocates a brand-new string and copies every character accumulated so "
            "far. Total work is 1+2+3+...+n = O(n²).\n\n**Linear fix:** `''.join(items)` — one "
            "pass to compute the total length, one allocation, one copy per "
            "character.\n\n**Microbenchmarks lie** because CPython has an in-place optimisation "
            "for `str +=` when the left operand's refcount is exactly 1: it can resize in place "
            "and avoid the copy. That applies in a tight local loop but silently stops applying "
            "the moment anything else holds a reference — so the same code is linear in your "
            "benchmark and quadratic in production. `join` is unconditionally correct.",
        ),
        (
            "Interning makes `is` unreliable",
            '''a = 256
b = 256
print(a is b)

x = 257
y = 257
print(x is y)

s1 = "hello world"
s2 = "hello world"
print(s1 is s2)''',
            "Prints `True`, then `False`, then `True` — inconsistently across Python versions "
            "and between the REPL and a script file.",
            [
                "Explain each of the three results.",
                "What is the rule for using `is`?",
                "Why does running the same lines in a REPL versus a file change the answer?",
            ],
            "**256** is in CPython's small-integer cache (-5 to 256), so both names point at the "
            "same preallocated object. **257** is outside it, so two separate objects are "
            "created. **`\"hello world\"`** is interned here because the compiler constant-folds "
            "identical literals within the same code object.\n\n**Rule:** use `is` **only** for "
            "singletons — `None`, `True`, `False`, and your own sentinels. For value comparison "
            "always use `==`. `ruff` flags `is` against a literal as `F632`.\n\n**REPL vs file:** "
            "in a file, both `257` literals live in one code object and may be folded into one "
            "constant; in the REPL each line is compiled separately, so they cannot be. This is "
            "an implementation detail that has changed between versions — which is precisely why "
            "you must not depend on it.",
        ),
        (
            "AST transform breaks on a rewritten node",
            '''import ast

class Doubler(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if isinstance(node.value, int):
            return ast.Constant(value=node.value * 2)
        return node

tree = ast.parse("x = 21")
new = Doubler().visit(tree)
exec(compile(new, "<ast>", "exec"))''',
            "`ValueError: field 'lineno' is required for Constant` — or a segfault on some "
            "versions.",
            [
                "What is missing from the newly created node?",
                "What is the one-line fix?",
                "Why does `ast.NodeTransformer` not do this for you?",
            ],
            "A hand-constructed AST node has no position attributes (`lineno`, `col_offset`, "
            "`end_lineno`, `end_col_offset`). `compile` requires them on every node to build "
            "tracebacks and to bounds-check.\n\n**Fix:** `ast.fix_missing_locations(new)` before "
            "compiling — it copies positions from parent nodes throughout the tree. "
            "`ast.copy_location(new_node, node)` is the per-node equivalent.\n\n**Why not "
            "automatic:** `NodeTransformer` cannot know whether your new node corresponds to the "
            "old one's source position or to something synthetic, and guessing would produce "
            "misleading tracebacks. The explicit call is the API telling you that source mapping "
            "is your decision. Module 12's security profiler calls it after every rewrite.",
        ),
    ],
}
