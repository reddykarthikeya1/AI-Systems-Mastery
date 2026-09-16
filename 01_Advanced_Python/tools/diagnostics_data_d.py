"""Diagnostic quiz questions, batch D: Modules 00-03, 05, 07.

These six modules already had *build* challenges ("write a rate limiter"), which
test construction. They lacked *diagnostic* questions, which test the different
and rarer skill of reading a symptom and finding its cause.
"""

from __future__ import annotations

DIAGNOSTICS: dict[str, list[tuple[str, str, str, list[str], str]]] = {
    "00": [
        (
            "Wrong interpreter",
            '''$ pip install polars
Successfully installed polars-1.12.0

$ python -c "import polars"
ModuleNotFoundError: No module named 'polars'
''',
            "The install succeeded, and the very next command cannot find the package.",
            [
                "What is almost certainly different between `pip` and `python` here?",
                "What two commands diagnose it in one line each?",
                "What invocation makes this impossible?",
            ],
            "`pip` and `python` are resolving to **different interpreters**. A bare `pip` is "
            "whichever one appears first on `PATH`, which is often not the `python` you just "
            "ran — a common outcome with multiple Pythons, an inactive virtualenv, or a "
            "user-site install.\n\n**Diagnose:**\n```bash\npython -c \"import sys; "
            "print(sys.executable)\"\npip --version        # prints the interpreter it belongs "
            "to\n```\nCompare the two paths.\n\n**Prevent it** by never invoking `pip` directly: "
            "`python -m pip install polars`. The `-m` form guarantees the package lands in the "
            "interpreter you are about to use. This single habit eliminates the entire class of "
            "bug, and it is why every command in this course is written as `python -m pip` and "
            "`python -m pytest`.",
        ),
        (
            "Ruff passes locally, fails in CI",
            '''$ ruff check .
All checks passed!

# ...but CI reports:
# tools/helper.py:14:1: I001 Import block is un-sorted
''',
            "Identical command, opposite result.",
            [
                "Name three reasons the same command can disagree between machines.",
                "How do you make the two environments agree?",
                "Why is pinning the linter version not optional?",
            ],
            "**Three reasons:** (1) **different ruff versions** — rules are added and defaults "
            "change between releases, so a newer CI ruff flags what your older local one did "
            "not; (2) **different working directory** — ruff discovers `pyproject.toml` by "
            "walking upward, so running from a subdirectory can pick up different config; "
            "(3) **files excluded locally** — an untracked file, or one matched by a local "
            "`.gitignore` that CI does not have.\n\n**Make them agree:** pin the version in "
            "`pyproject.toml`, install with `pip install -e \".[dev]\"` in both places, and run "
            "from the repository root in both. Better still, add a `pre-commit` hook so the "
            "same pinned binary runs before every commit.\n\n**Pinning is not optional** because "
            "an unpinned linter turns your CI into a moving target: a build that passed yesterday "
            "fails today with no change to your code. That trains people to ignore CI, which is "
            "far more expensive than the pin.",
        ),
        (
            "Editable install that does not update",
            '''$ pip install -e .
$ # edit src/mypkg/core.py, add a new function
$ python -c "from mypkg.core import new_function"
ImportError: cannot import name 'new_function'
''',
            "An editable install is supposed to pick up edits immediately.",
            [
                "Give two reasons the edit is not visible.",
                "How do you verify which file Python actually loaded?",
                "What does `src/` layout protect you from that a flat layout does not?",
            ],
            "**Two reasons:** (1) a **stale non-editable copy** shadows it — a previous "
            "`pip install .` left a real copy in `site-packages`, which wins over the editable "
            "path; (2) you are **importing a different package** — a directory named `mypkg` in "
            "your current working directory shadows the installed one, because `''` (the cwd) "
            "comes first on `sys.path`.\n\n**Verify:**\n```python\nimport mypkg.core; "
            "print(mypkg.core.__file__)\n```\nThat prints the file actually in use. It is the "
            "single most useful line in Python packaging debugging.\n\n**`src/` layout protects "
            "you** from exactly the second case: because the package is not at the repository "
            "root, you *cannot* accidentally import it from the cwd. Any successful import proves "
            "the install works — which means your tests exercise the installed package, the way "
            "your users will. That is why Module 00's template uses it.",
        ),
        (
            "pytest cannot find the module",
            '''$ pytest
ImportError while importing test module 'tests/test_core.py'
ModuleNotFoundError: No module named 'mypkg'
''',
            "The tests import the package, and pytest cannot see it.",
            [
                "Why does pytest not automatically see your package?",
                "Name the three standard fixes and which is best.",
                "What does adding an `__init__.py` to `tests/` change?",
            ],
            "pytest inserts the **rootdir of the test file** into `sys.path` (in the default "
            "`prepend` import mode), not your source directory. With a `src/` layout the package "
            "is nowhere on the path unless it is installed.\n\n**Three fixes, worst to best:** "
            "(1) `sys.path` manipulation in `conftest.py` — works, but now tests exercise the "
            "source tree rather than the installed artifact; (2) `pythonpath = [\"src\"]` in "
            "`pyproject.toml` — declarative and fine; (3) **`pip install -e .`** — best, because "
            "the tests then import exactly what a user would.\n\n**An `__init__.py` in `tests/`** "
            "makes the test directory a package, which changes module naming (`tests.test_core` "
            "instead of `test_core`). That prevents name collisions between same-named test files "
            "in different directories — a real problem in large suites — but it does not fix a "
            "missing package. The two issues are often confused.",
        ),
        (
            "Committed virtual environment",
            '''$ git status
Changes to be committed:
    new file:   .venv/lib/python3.11/site-packages/polars/...
    ... 14,203 more files
''',
            "A one-line code change produced a 14,000-file commit.",
            [
                "Why is committing `.venv/` harmful, beyond size?",
                "What is the correct way to make the environment reproducible?",
                "How do you fix it after it has already been committed?",
            ],
            "**Beyond size:** a virtualenv contains **absolute paths** baked into its scripts "
            "and `pyvenv.cfg`, so it does not work on any other machine or even in a different "
            "directory. It contains **compiled binaries** for one OS and CPU architecture. And it "
            "makes every dependency change an unreviewable diff, so a malicious or accidental "
            "package change is invisible in review.\n\n**Correct approach:** commit the *intent* "
            "(`pyproject.toml`) and the *resolution* (`uv.lock` or `requirements.txt` with "
            "hashes). Anyone can then rebuild an identical environment, on their own "
            "platform.\n\n**Fix after committing:** add `.venv/` to `.gitignore`, then "
            "`git rm -r --cached .venv` to untrack it while keeping the files on disk. Note the "
            "history still contains them — repository size is permanently affected unless you "
            "rewrite history, which is why the `.gitignore` should exist from the first commit.",
        ),
    ],
    "01": [
        (
            "Float equality in a loop condition",
            '''total = 0.0
while total != 1.0:
    total += 0.1
    print(total)''',
            "Infinite loop. The printed values pass 1.0 and keep going.",
            [
                "Why is `total` never exactly 1.0?",
                "Give two correct rewrites.",
                "What does `0.1 + 0.2 == 0.3` evaluate to, and why does that matter here?",
            ],
            "0.1 has no exact binary representation, so accumulating it ten times gives "
            "`0.9999999999999999`, then `1.0999999999999999`. The loop condition is never "
            "satisfied.\n\n**Two rewrites:** count integers and scale — "
            "`for i in range(10): total = i / 10` — or compare with a tolerance: "
            "`while abs(total - 1.0) > 1e-9`. The first is better: it removes the accumulation "
            "error entirely rather than tolerating it.\n\n**`0.1 + 0.2 == 0.3` is `False`** "
            "(the sum is `0.30000000000000004`). It matters because it is the same defect in "
            "miniature: never use `==` or `!=` on accumulated floats. For money, use `Decimal` "
            "— Module 08's ledger does, precisely to avoid this.",
        ),
        (
            "Mutable default argument",
            '''def add_item(item: str, basket: list[str] = []) -> list[str]:
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("bread"))''',
            "Prints `['apple']`, then `['apple', 'bread']` — the second call inherited the first "
            "call's basket.",
            [
                "When exactly is the default list created?",
                "What is the correct pattern?",
                "Which immutable defaults are safe, and why does that make this bug worse?",
            ],
            "**Once**, when the `def` statement executes — not per call. Every call that omits "
            "the argument shares that one list object, so mutations accumulate across "
            "calls.\n\n**Correct:**\n```python\ndef add_item(item: str, basket: list[str] | None = "
            "None) -> list[str]:\n    if basket is None:\n        basket = []\n    "
            "basket.append(item)\n    return basket\n```\n\n**Immutable defaults are safe** — "
            "`0`, `\"\"`, `None`, `(1, 2)` — because you cannot mutate them; rebinding creates a "
            "new object. That is what makes this bug worse: 95% of default arguments are "
            "immutable and behave intuitively, so the mutable case violates an expectation you "
            "have built up over hundreds of correct functions. `ruff` flags it as `B006`, and "
            "this course enables that rule.",
        ),
        (
            "`is` versus `==`",
            '''def is_target(n: int) -> bool:
    return n is 1000

print(is_target(1000))
print(is_target(int("1000")))''',
            "Prints `True`, then `False`.",
            [
                "Explain the difference between the two calls.",
                "When is `is` the correct operator?",
                "Why is the first call `True` at all?",
            ],
            "`is` compares **identity** — whether two names point at the same object. `==` "
            "compares **value**. `int(\"1000\")` constructs a new object, so it is a different "
            "object with an equal value.\n\n**`is` is correct only for singletons**: `None`, "
            "`True`, `False`, and sentinels you created yourself (`MISSING = object()`, as in "
            "Module 20's cache). Never for numbers, strings, or containers.\n\n**The first call "
            "is `True`** because CPython's compiler folds identical literal constants within one "
            "code object, so both `1000`s are the same object. That is an implementation detail "
            "that has changed between versions and differs in the REPL — which is exactly why "
            "you must not rely on it. Modern Python emits a `SyntaxWarning` for `is` against a "
            "literal, and `ruff` flags it as `F632`.",
        ),
        (
            "Off-by-one in a range",
            '''def sum_to(n: int) -> int:
    """Sum every integer from 1 to n inclusive."""
    return sum(range(1, n))

print(sum_to(10))''',
            "Prints `45`. The correct answer is 55.",
            [
                "What is `range(1, 10)` actually?",
                "What is the fix?",
                "What is the design reason Python's ranges exclude the stop value?",
            ],
            "`range(1, 10)` yields 1 through **9** — the stop value is exclusive. So the sum "
            "omits 10.\n\n**Fix:** `range(1, n + 1)`.\n\n**Why exclusive:** it makes `len(range(a, "
            "b))` equal `b - a`, makes adjacent ranges join cleanly "
            "(`range(0,3)` + `range(3,6)` covers 0–5 with no overlap and no gap), and matches "
            "zero-based indexing so `range(len(xs))` covers exactly the valid indices. Every one "
            "of those properties would break with an inclusive stop. The convention costs you "
            "one off-by-one bug early and saves a dozen later — which is why writing a test "
            "against a known value (`sum_to(10) == 55`) catches it immediately.",
        ),
        (
            "String immutability in a loop",
            '''def build_csv(rows: list[list[str]]) -> str:
    out = ""
    for row in rows:
        for cell in row:
            out += cell + ","
        out = out[:-1] + "\\n"
    return out''',
            "Correct output, but processing 100,000 rows takes minutes.",
            [
                "Why is this quadratic rather than linear?",
                "What is the linear rewrite?",
                "Which line is the worse offender, and why?",
            ],
            "Strings are **immutable**, so `out += cell` allocates a whole new string and copies "
            "everything accumulated so far. Over n appends the total work is O(n²).\n\n**Linear "
            "rewrite:**\n```python\nreturn \"\\n\".join(\",\".join(row) for row in rows) + "
            "\"\\n\"\n```\nOne pass, one allocation per join.\n\n**`out = out[:-1] + \"\\n\"` is "
            "worse** than the `+=`: slicing copies the entire accumulated string, *then* the "
            "concatenation copies it again — two full copies per row rather than one. It also "
            "hides a correctness bug: on an empty row it strips a character it did not add. "
            "Module 12's diagnostic on `dis.dis` shows the bytecode behind this, including why "
            "CPython's in-place `+=` optimisation makes the problem invisible in "
            "microbenchmarks.",
        ),
    ],
    "02": [
        (
            "Late-binding closure",
            '''callbacks = []
for i in range(3):
    callbacks.append(lambda: i)

print([cb() for cb in callbacks])''',
            "Prints `[2, 2, 2]`. You expected `[0, 1, 2]`.",
            [
                "What does each lambda actually capture?",
                "Give two fixes.",
                "Why is this behaviour correct rather than a bug in Python?",
            ],
            "Each lambda captures the **variable** `i`, not its value at creation time. By the "
            "time any of them runs, the loop has finished and `i` is 2.\n\n**Two fixes:** bind "
            "at definition with a default argument — `lambda i=i: i` (defaults *are* evaluated "
            "eagerly, which is the same mechanism as the mutable-default bug, used "
            "deliberately) — or use `functools.partial(lambda x: x, i)`.\n\n**It is correct "
            "because** closures capture bindings, which is what makes them useful: a counter "
            "closure must see the *current* value of its enclosed variable, not a snapshot from "
            "when it was defined. Module 02's rate limiter depends on exactly that. What bites "
            "here is creating closures in a loop, where you almost always want a snapshot — so "
            "the fix is to ask for one explicitly.",
        ),
        (
            "Missing `nonlocal`",
            '''def make_counter():
    count = 0
    def increment():
        count += 1
        return count
    return increment

counter = make_counter()
print(counter())''',
            "`UnboundLocalError: cannot access local variable 'count' where it is not associated "
            "with a value`.",
            [
                "Why does assigning to `count` make it local?",
                "What keyword fixes it, and what is the alternative?",
                "Why does a read-only closure work without any keyword?",
            ],
            "Any **assignment** to a name inside a function makes that name local to the "
            "function for its entire body — the compiler decides this statically, before the "
            "code runs. `count += 1` is an assignment, so `count` is local, and reading it "
            "before assignment raises.\n\n**Fix:** `nonlocal count`, which binds the name to the "
            "enclosing function scope. The alternative is to avoid rebinding entirely by mutating "
            "a container: `count = [0]` then `count[0] += 1` — mutation is not "
            "assignment.\n\n**Read-only closures work** because with no assignment the compiler "
            "classifies the name as free, and the LEGB lookup finds it in the enclosing scope "
            "naturally. That asymmetry — read is automatic, write needs a declaration — is the "
            "single most confusing thing about Python scoping, and `nonlocal` exists precisely "
            "to make the write case explicit.",
        ),
        (
            "Shadowed builtin",
            '''def summarize(values: list[float]) -> dict[str, float]:
    sum = 0.0
    for v in values:
        sum += v
    max = values[0]
    for v in values:
        if v > max:
            max = v
    return {"total": sum, "peak": max, "count": len(values), "mean": sum / len(values)}

def process(data: list[list[float]]) -> list[float]:
    return [sum(batch) for batch in data]''',
            "`summarize` works. `process`, called later in the same module, raises "
            "`TypeError: 'float' object is not callable`.",
            [
                "Why does `process` fail when the shadowing happened in a different function?",
                "What actually broke?",
                "What tool catches this before runtime?",
            ],
            "It does not — read the traceback carefully. `sum` inside `summarize` is **local** "
            "to `summarize` and cannot affect `process`. The real failure is that somewhere a "
            "**module-level** `sum = ...` was introduced (or `from x import sum`), which shadows "
            "the builtin for the whole module.\n\nThe lesson is the diagnostic one: local "
            "shadowing is harmless and ugly; *module-level* shadowing is action at a distance, "
            "breaking code that never mentioned the name.\n\n**What broke:** the builtin `sum` is "
            "resolved at call time via LEGB, and a module-global binding is found before "
            "builtins.\n\n**Caught by** `ruff`'s flake8-builtins rules (`A001`/`A002`), which "
            "flag any assignment shadowing a builtin. Even for the harmless local case, "
            "renaming to `total` and `peak` costs nothing and removes the whole question.",
        ),
        (
            "Argument unpacking order",
            '''def connect(host: str, port: int = 5432, *, timeout: float = 5.0) -> str:
    return f"{host}:{port} t={timeout}"

config = {"host": "db.internal", "timeout": 10.0}
print(connect(*config))''',
            "Prints `host:timeout t=5.0` — the keys were passed as positional values.",
            [
                "What did `*config` unpack?",
                "What is the correct operator?",
                "Why can `timeout` never be passed positionally here?",
            ],
            "Iterating a dict yields its **keys**, so `*config` passed the strings `\"host\"` "
            "and `\"timeout\"` as `host` and `port`.\n\n**Correct:** `connect(**config)` — the "
            "double star unpacks a mapping into keyword arguments.\n\n**`timeout` is "
            "keyword-only** because of the bare `*` in the signature: every parameter after it "
            "can only be supplied by name. That is a deliberate API design choice — it prevents "
            "`connect(\"db\", 5432, 10.0)`, where the reader cannot tell what `10.0` means, and "
            "it lets you reorder or insert keyword-only parameters later without breaking "
            "callers. Use it for any parameter whose meaning is not obvious from position.",
        ),
        (
            "Decorator applied at the wrong time",
            '''import functools

def cache_result(fn):
    @functools.wraps(fn)
    def wrapper(*args):
        if not hasattr(wrapper, "_value"):
            wrapper._value = fn(*args)
        return wrapper._value
    return wrapper

@cache_result
def get_config(env: str) -> dict:
    return {"env": env}

print(get_config("dev"))
print(get_config("prod"))''',
            "Prints `{'env': 'dev'}` twice.",
            [
                "Why does the second call return the first result?",
                "What is the minimal fix?",
                "What should you use instead of hand-rolling this?",
            ],
            "The cache is stored on the **wrapper function object**, which is a single object "
            "shared by all calls. It ignores the arguments entirely — the first result is "
            "returned for every input forever.\n\n**Minimal fix:** key the cache by the "
            "arguments:\n```python\nwrapper._cache = {}\nif args not in wrapper._cache:\n    "
            "wrapper._cache[args] = fn(*args)\nreturn wrapper._cache[args]\n```\n\n**Use "
            "instead:** `functools.lru_cache` (or `functools.cache`), which handles argument "
            "keying, keyword arguments, a size bound, thread safety and hit/miss statistics — "
            "all things this hand-rolled version gets wrong. Module 20 covers when `lru_cache` is "
            "*not* enough (TTLs, sharing across processes) and what to reach for then.",
        ),
    ],
    "03": [
        (
            "Shallow copy of nested data",
            '''template = {"tags": [], "meta": {"v": 1}}
a = template.copy()
b = template.copy()
a["tags"].append("x")
print(b["tags"])''',
            "Prints `['x']` — the two copies share their inner list.",
            [
                "What exactly did `.copy()` duplicate?",
                "What are the two correct approaches?",
                "Why is `deepcopy` not always the right answer?",
            ],
            "`.copy()` is **shallow**: it creates a new outer dict whose values are the *same "
            "objects*. Both copies hold a reference to one list.\n\n**Two approaches:** "
            "`copy.deepcopy(template)` recursively duplicates everything; or restructure so "
            "there is nothing to share — build a fresh dict per use, or make the template "
            "immutable (`\"tags\": ()`) so mutation is impossible.\n\n**`deepcopy` is not always "
            "right** because it is slow (it walks the whole graph and maintains a memo table for "
            "cycles), it copies things you may want shared (an open connection, a logger, a "
            "lock), and it fails on objects that are not copyable. Prefer designing the sharing "
            "away: a factory function or `field(default_factory=...)` beats copying after the "
            "fact.",
        ),
        (
            "Mutating a dict during iteration",
            '''counts = {"a": 0, "b": 3, "c": 0, "d": 5}
for key in counts:
    if counts[key] == 0:
        del counts[key]''',
            "`RuntimeError: dictionary changed size during iteration`.",
            [
                "Why does Python refuse this rather than coping?",
                "What are the two standard fixes?",
                "Does the same restriction apply to lists?",
            ],
            "The iterator holds a position into the dict's internal table. Deleting an entry can "
            "trigger a resize and rehash, which would make that position meaningless — the "
            "iterator could skip entries or return them twice. Python detects the size change "
            "and raises rather than yielding silently wrong results.\n\n**Two fixes:** iterate "
            "over a snapshot — `for key in list(counts):` — or build a new dict, which is "
            "cleaner: `counts = {k: v for k, v in counts.items() if v != "
            "0}`.\n\n**Lists are worse:** mutating a list during iteration does **not** raise. "
            "It silently skips elements, because the index advances while the list shrinks. "
            "`for x in xs: if bad(x): xs.remove(x)` quietly leaves bad items behind. A raised "
            "error is a gift; the list version is the genuinely dangerous one.",
        ),
        (
            "Unhashable key",
            '''index: dict[list[str], int] = {}
index[["a", "b"]] = 1''',
            "`TypeError: unhashable type: 'list'`.",
            [
                "Why can a list not be a dict key?",
                "What should you use instead?",
                "What makes a custom class usable as a key?",
            ],
            "A dict places a key in a bucket derived from its hash. If the key were mutable, "
            "changing it after insertion would change its hash, and the entry would become "
            "unfindable — present in the dict but unreachable. Python forbids the situation by "
            "making mutable builtins unhashable.\n\n**Use instead:** a `tuple` (`(\"a\", \"b\")`) "
            "for an ordered key, or `frozenset` when order should not matter.\n\n**A custom "
            "class** is hashable by default (identity-based), and stays valid as long as you do "
            "not define `__eq__`. If you do define `__eq__`, you must define a consistent "
            "`__hash__` over the *immutable* parts — or use `@dataclass(frozen=True)`, which "
            "generates both. Module 04's diagnostic D2 covers what goes wrong when they "
            "disagree.",
        ),
        (
            "defaultdict creates entries on read",
            '''from collections import defaultdict

scores = defaultdict(int)
scores["ada"] = 10

if scores["bob"] > 5:
    print("bob qualifies")

print(len(scores), dict(scores))''',
            "Prints `2 {'ada': 10, 'bob': 0}` — merely checking `bob` created the key.",
            [
                "Why did a read insert a key?",
                "How do you check membership without inserting?",
                "When does this cause a real bug rather than a curiosity?",
            ],
            "`defaultdict.__missing__` is called on a failed lookup and it **inserts** the "
            "default before returning it. Any `d[key]` on a `defaultdict` is potentially a "
            "write.\n\n**Check without inserting:** `scores.get(\"bob\", 0)` or "
            "`if \"bob\" in scores`. Neither goes through `__missing__`.\n\n**Real bugs:** "
            "iterating a `defaultdict` while reading unknown keys mutates it mid-iteration "
            "(see D2 above); serialising it to JSON emits phantom entries that a consumer treats "
            "as real data; and a memory leak in a long-lived process that probes many "
            "never-present keys. The behaviour is correct and documented — the mistake is "
            "reaching for `defaultdict` when you only wanted a default *value*, where `.get()` "
            "is the right tool.",
        ),
        (
            "Wrong container for the access pattern",
            '''seen: list[str] = []
for record in records:          # 100,000 records
    if record["id"] not in seen:
        seen.append(record["id"])''',
            "Correct output; takes 40 seconds and gets quadratically worse.",
            [
                "What is the complexity of `in` on a list versus a set?",
                "What is the rewrite?",
                "When is a list genuinely the right choice for membership testing?",
            ],
            "`x in list` is **O(n)** — a linear scan. Inside a loop over n records that is "
            "O(n²): 100,000 records means up to 5 billion comparisons.\n\n**Rewrite:** "
            "`seen: set[str] = set()` with `seen.add(...)`. Set membership is O(1) average, "
            "making the loop O(n) — the 40 seconds becomes milliseconds. If insertion order "
            "matters, `dict.fromkeys()` preserves it while keeping O(1) lookups.\n\n**A list is "
            "right** when it is tiny (under roughly 10 elements, where the constant factors "
            "favour a scan and hashing costs more than it saves), when the elements are "
            "unhashable, or when you need the sequence for something else anyway and membership "
            "is a rare operation. Choosing the container from the access pattern rather than from "
            "habit is the whole lesson of this module.",
        ),
    ],
    "05": [
        (
            "Decorator without functools.wraps",
            '''def timed(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper

@timed
def calculate(x: int) -> int:
    """Compute the answer."""
    return x * 2

print(calculate.__name__, calculate.__doc__)''',
            "Prints `wrapper None` — the function lost its identity.",
            [
                "What metadata was lost?",
                "What is the one-line fix?",
                "Name two tools that break because of this.",
            ],
            "`__name__`, `__doc__`, `__qualname__`, `__module__`, `__annotations__` and "
            "`__dict__` all now describe the wrapper, not the wrapped "
            "function.\n\n**Fix:** `@functools.wraps(fn)` on the wrapper. It copies all of the "
            "above and sets `__wrapped__` so introspection can find the original.\n\n**Two tools "
            "that break:** **pytest** — a decorated test function reports as `wrapper` in output "
            "and fixture resolution can fail; and **Sphinx / any documentation generator** — "
            "every decorated function documents as \"wrapper\" with no docstring. Also affected: "
            "`pickle` (which looks up by qualified name), and debuggers showing the wrong frame "
            "name. Note `wraps` still does not fix the *signature* — see Module 21's diagnostic "
            "D4 for why FastAPI needs more.",
        ),
        (
            "Generator consumed twice",
            '''def parse(path: str):
    for line in open(path):
        yield line.strip()

records = parse("data.txt")
print(f"count: {sum(1 for _ in records)}")
for record in records:
    print(record)''',
            "The count is correct. The loop prints nothing.",
            [
                "Why is the generator empty the second time?",
                "What are the two ways to fix it, and their trade-off?",
                "How would you detect this class of bug in review?",
            ],
            "A generator is a **one-shot iterator**. Once exhausted it stays exhausted; there is "
            "no rewind. The `sum` consumed every item.\n\n**Two fixes:** materialise it — "
            "`records = list(parse(path))` — which allows repeated iteration at the cost of "
            "holding everything in memory; or call the generator function again — "
            "`for record in parse(path)` — which re-reads the file, using no extra memory but "
            "doing the I/O twice. The trade-off is memory versus repeated work, and which is "
            "right depends on the file size.\n\n**Detect in review:** any variable holding a "
            "generator that appears more than once. A useful habit is naming them for their "
            "one-shot nature (`record_stream`, not `records`), and returning a `list` from "
            "public APIs unless streaming is the documented point — a caller cannot tell a "
            "generator from a list until it silently comes back empty.",
        ),
        (
            "Context manager swallowing exceptions",
            '''class Transaction:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            print(f"rolling back: {exc}")
        return True

with Transaction():
    raise ValueError("constraint violated")

print("execution continues")''',
            "Prints the rollback message, then `execution continues`. The `ValueError` vanishes.",
            [
                "What does returning `True` from `__exit__` mean?",
                "What should it return here?",
                "When is suppressing an exception legitimate?",
            ],
            "A truthy return from `__exit__` tells Python the exception has been **handled** and "
            "must be suppressed. The caller never learns the transaction failed.\n\n**It should "
            "return `False`** (or simply `None`, which is falsy) — do the rollback, then let the "
            "exception propagate so the caller can decide.\n\n**Legitimate suppression** is rare "
            "and always deliberate: `contextlib.suppress(FileNotFoundError)` is the canonical "
            "example, and its *name* announces the intent. A manager that silently eats "
            "exceptions is one of the hardest bugs to find, because the symptom appears far "
            "downstream where the data turns out to be missing. The rule: return `False` unless "
            "the class name says 'suppress'.",
        ),
        (
            "Generator with cleanup that never runs",
            '''def read_rows(path: str):
    fh = open(path)
    try:
        for line in fh:
            yield line
    finally:
        fh.close()
        print("closed")

for row in read_rows("data.txt"):
    if row.startswith("STOP"):
        break''',
            "`closed` prints at an unpredictable time, and under load the process runs out of "
            "file descriptors.",
            [
                "Why does `finally` not run at the `break`?",
                "What construct guarantees prompt cleanup?",
                "Why is the `try/finally` still worth keeping?",
            ],
            "Breaking out leaves the generator **suspended** at the `yield`. Its `finally` runs "
            "only when the generator is closed, which happens at garbage collection — "
            "unpredictably, and in a reference cycle possibly never.\n\n**Prompt cleanup:** "
            "`contextlib.closing`:\n```python\nwith closing(read_rows(path)) as rows:\n    for "
            "row in rows:\n        ...\n```\nThis calls `.close()` on exit, which throws "
            "`GeneratorExit` into the generator and runs the `finally` immediately.\n\n**Keep "
            "the `try/finally`** because it is what makes `close()` effective at all — without "
            "it, closing the generator would not release the file. The two work together: the "
            "`finally` defines the cleanup, and `closing` guarantees it is triggered on time. "
            "Better still, put the `with open(...)` *inside* the generator so the file is scoped "
            "to the iteration.",
        ),
        (
            "Decorator with arguments, one layer short",
            '''import functools

def retry(times: int):
    @functools.wraps(times)
    def wrapper(*args, **kwargs):
        for _ in range(times):
            try:
                return times(*args, **kwargs)
            except Exception:
                continue
    return wrapper

@retry(3)
def flaky() -> str:
    return "ok"''',
            "`TypeError: 'int' object is not callable`.",
            [
                "How many layers does a decorator with arguments need, and how many are here?",
                "Write the correct structure.",
                "How do you write a decorator that works both with and without arguments?",
            ],
            "It needs **three** levels: the argument-taking factory, the decorator that receives "
            "the function, and the wrapper. This has two, so `times` is being used where the "
            "function should be.\n\n**Correct:**\n```python\ndef retry(times: int):\n    def "
            "decorator(fn):\n        @functools.wraps(fn)\n        def wrapper(*args, **kwargs):"
            "\n            for attempt in range(times):\n                try:\n                    "
            "return fn(*args, **kwargs)\n                except Exception:\n                    "
            "if attempt == times - 1:\n                        raise\n        return wrapper\n    "
            "return decorator\n```\nNote the re-raise on the final attempt — the original also "
            "returned `None` silently after exhausting retries, which is a second bug.\n\n**Both "
            "forms:** accept the function as an optional first parameter — "
            "`def retry(fn=None, *, times=3)` — and if `fn is None`, return "
            "`functools.partial(retry, times=times)`. That is how `@dataclass` supports both "
            "`@dataclass` and `@dataclass(frozen=True)`.",
        ),
    ],
    "07": [
        (
            "Missing encoding",
            '''with open("config.json") as fh:
    data = fh.read()''',
            "Works on the author's Linux machine. On a colleague's Windows machine: "
            "`UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d`.",
            [
                "What encoding is used when you omit the parameter?",
                "What is the fix, and what is the belt-and-braces version?",
                "Why does the same file work on one machine and not another?",
            ],
            "`locale.getpreferredencoding(False)` — the **platform default**. On most Linux and "
            "macOS systems that is UTF-8; on Windows it has historically been a legacy code page "
            "such as cp1252.\n\n**Fix:** always pass it — `open(path, encoding=\"utf-8\")`. "
            "Belt-and-braces for files you did not produce: "
            "`encoding=\"utf-8\", errors=\"replace\"`, which substitutes a replacement character "
            "rather than raising — appropriate for logs, not for data you will "
            "write back.\n\n**Machine-dependent** because nothing about the file changed; the "
            "*decoder* changed. This is the single most common cross-platform Python bug. PEP "
            "686 makes UTF-8 the default in Python 3.15, and `PYTHONWARNDEFAULTENCODING=1` warns "
            "today — but explicit `encoding=` is correct on every version and should be "
            "unconditional.",
        ),
        (
            "JSON round-trip loses integer keys",
            '''import json

original = {1: "one", 2: "two"}
restored = json.loads(json.dumps(original))
print(restored)
print(original == restored)''',
            "Prints `{'1': 'one', '2': 'two'}` and `False`.",
            [
                "Why did the keys change type?",
                "What are the two ways to preserve them?",
                "Name two other types that do not survive a JSON round-trip.",
            ],
            "The JSON specification requires object keys to be **strings**. `json.dumps` "
            "coerces silently rather than raising, so the information is lost at serialisation, "
            "not at parse.\n\n**Two fixes:** convert back explicitly on load with "
            "`object_hook=lambda d: {int(k): v for k, v in d.items()}` (only safe if you know "
            "every key is an integer); or restructure to a list of "
            "`{\"id\": 1, \"value\": \"one\"}` objects, which is more portable and "
            "self-describing.\n\n**Two others:** `tuple` becomes `list` (so "
            "`(1, 2) != [1, 2]` after a round trip), and `datetime` is not serialisable at all "
            "without a custom encoder — and a naive datetime loses its intended timezone "
            "regardless. Also: `set` is unsupported, `Decimal` becomes `float` and loses "
            "precision, and `NaN`/`Infinity` are emitted as non-standard JSON that other "
            "parsers reject.",
        ),
        (
            "Non-atomic file write",
            '''import json

def save(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)''',
            "After a crash or a full disk, `config.json` exists but is truncated mid-object and "
            "will not parse. The previous good version is gone.",
            [
                "Name the two independent failure modes.",
                "What is the atomic-write pattern?",
                "Why is `os.replace` the critical call rather than `os.rename`?",
            ],
            "**Two failures.** (1) `open(path, \"w\")` **truncates immediately**, so the old "
            "content is destroyed before the new content is written — a crash leaves nothing "
            "usable. (2) A reader can observe the file mid-write and read a partial "
            "document.\n\n**Atomic write:** serialise to a temporary file *in the same "
            "directory*, `fh.flush()` then `os.fsync(fh.fileno())` to force it to disk, close it, "
            "then `os.replace(tmp, path)`. A reader sees either the complete old file or the "
            "complete new one, never a partial "
            "one.\n\n**`os.replace` rather than `os.rename`** because `replace` is guaranteed to "
            "overwrite an existing destination atomically on **all** platforms; `os.rename` "
            "raises `FileExistsError` on Windows if the target exists. Same directory matters "
            "too: a rename across filesystems is a copy-and-delete and therefore not atomic. "
            "Module 07's `config_migrator` implements exactly this, and its tests assert the "
            "temporary file is cleaned up.",
        ),
        (
            "Pickle from an untrusted source",
            '''import pickle, requests

payload = requests.get("https://api.partner.example/state").content
state = pickle.loads(payload)''',
            "No error. Reviewed and merged. Later, the partner's endpoint is compromised and the "
            "server executes arbitrary commands.",
            [
                "What does `pickle.loads` actually do?",
                "What should be used instead?",
                "When is pickle acceptable?",
            ],
            "Unpickling **executes** the byte stream: the format includes opcodes that call "
            "arbitrary callables via `__reduce__`. `pickle.loads` on untrusted input is remote "
            "code execution, full stop — not a hardening opportunity, not mitigable by "
            "validation afterwards, because the code has already run by then.\n\n**Instead:** "
            "JSON for plain data, or a schema-validated format — Pydantic (Module 14), "
            "MessagePack, Protobuf, or Arrow. Any of these parse into data without invoking "
            "code.\n\n**Pickle is acceptable** only for data you produced, that never crossed a "
            "trust boundary, and where you control both ends and the Python version — a local "
            "cache file, or `multiprocessing`'s internal transport. Even then note that pickle is "
            "not a stable format across versions. The rule is short: if you did not write the "
            "bytes, do not unpickle them. Module 20's `RedisBackend` defaults to JSON for this "
            "reason and documents the risk of its pickle option.",
        ),
        (
            "CSV without newline handling",
            '''import csv

with open("out.csv", "w") as fh:
    writer = csv.writer(fh)
    writer.writerows([["a", "b"], ["c", "d"]])''',
            "On Windows the file has a blank line between every row.",
            [
                "Why the extra blank lines?",
                "What is the exact fix?",
                "What is the equivalent trap when reading?",
            ],
            "The `csv` module writes `\\r\\n` itself as the line terminator. In text mode with "
            "default newline translation, Python then converts the `\\n` to `\\r\\n` again, "
            "producing `\\r\\r\\n` — which most readers render as an empty "
            "row.\n\n**Fix:** `open(path, \"w\", newline=\"\", encoding=\"utf-8\")`. The empty "
            "string disables newline translation and lets `csv` control line endings, which is "
            "exactly what the documentation "
            "requires.\n\n**When reading**, the same `newline=\"\"` is needed: without it, a "
            "quoted field containing an embedded newline gets translated, and the row is split "
            "in the wrong place — corrupting the data silently rather than visibly. So the rule "
            "is symmetric: **always** pass `newline=\"\"` to any file handed to the `csv` module, "
            "in either direction.",
        ),
    ],
}
