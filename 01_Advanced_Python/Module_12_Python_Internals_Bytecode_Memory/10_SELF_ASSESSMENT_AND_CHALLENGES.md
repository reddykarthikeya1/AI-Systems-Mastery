# Module 12: Self-Assessment Quiz & Mastery Challenges

Test your understanding of CPython internals, bytecode, AST, and memory management before moving to **Module 12**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Compilation Stages:** List the 5 stages of CPython execution from raw Python text to physical machine execution.
2. **Object Anatomy:** In CPython's C source code, what two essential fields are present in every `PyObject` header?
3. **Primary Memory Management:** How does CPython's Reference Counter determine the exact instant an object's memory can be safely deallocated?
4. **Cyclic Memory:** Why does a circular reference (e.g. `a.partner = b` and `b.partner = a`) fail to be freed by standard reference counting alone?
5. **Generational GC:** What is the heuristic behind the 3 generations (`Gen 0`, `Gen 1`, `Gen 2`) in Python's cyclic garbage collector?
6. **RAM Optimization:** What is `__slots__`, and how does it reduce memory consumption for classes with millions of instances?
7. **`__slots__` Inheritance:** If class `Parent` defines `__slots__ = ('x',)` but class `Child(Parent)` does not declare `__slots__`, what happens to `Child` instances?
8. **Bytecode Inspection:** What standard library module allows you to disassemble Python functions into low-level Virtual Machine opcodes?
9. **AST Architecture:** What is an Abstract Syntax Tree (AST), and how do linters (like Ruff/Flake8) use it for static code analysis?
10. **Weak References:** How does `weakref.ref(obj)` allow referencing an object without increasing its `ob_refcnt`?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
1. **Source Code (.py)**
2. **Token Stream** (Tokenizer / Lexer)
3. **Abstract Syntax Tree (AST)** (Parser)
4. **Bytecode (.pyc / code objects)** (Compiler)
5. **CPython Virtual Machine (PVM / ceval.c)** (Evaluation Loop)

#### Answer 2:
- `ob_refcnt`: The integer reference count.
- `ob_type`: A pointer to the object's type descriptor struct (e.g. `&PyLong_Type`).

#### Answer 3:
Whenever a variable goes out of scope or is reassigned, `ob_refcnt` is decremented. The instant `ob_refcnt == 0`, CPython immediately frees the memory back to the memory allocator.

#### Answer 4:
Because each object still holds a reference to the other, both objects maintain an `ob_refcnt >= 1` even when all external variables pointing to them have been deleted.

#### Answer 5:
**The Generational Hypothesis:** "Most objects die young." Newly allocated objects are placed in Generation 0 (collected frequently). Surviving objects are promoted to Gen 1 and Gen 2 (collected progressively less frequently), optimizing performance.

#### Answer 6:
It eliminates the default dynamic dictionary (`__dict__`) from each instance, replacing it with a compact, fixed-size C array of pointers, saving ~50-60% of RAM per object.

#### Answer 7:
`Child` instances will have a dynamic `__dict__` created, completely negating the memory savings of the parent class.

#### Answer 8:
**`dis`** (Disassembler module).

#### Answer 9:
An AST is a tree representation of the syntactic structure of source code. Linters walk this tree with `ast.NodeVisitor` to detect banned patterns (like `eval()` calls or mutable default arguments) without executing code.

#### Answer 10:
`weakref` creates a non-owning pointer that does not increment `ob_refcnt`, allowing the target object to be collected immediately when all strong references disappear.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: AST Wildcard Import Detector

**Goal:** Write a function `detect_wildcard_imports(source_code: str) -> list[int]` that parses Python code and returns line numbers of all `from module import *` statements.

<details>
<summary><b>Solution Code</b></summary>

```python
import ast

def detect_wildcard_imports(source_code: str) -> list[int]:
    tree = ast.parse(source_code)
    wildcard_lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    wildcard_lines.append(node.lineno)
    return wildcard_lines

# Verification:
code = """
from math import sqrt
from os import *
import sys
from collections import *
"""
print("Detected wildcard imports at lines:", detect_wildcard_imports(code))
# Output: [3, 5]
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Reference cycle keeps objects alive

```python
import gc

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
print(len(gc.get_objects()))
```

**Observed symptom:** Memory grows steadily even though no `Node` is reachable after `build()` returns.

**(a)** Why does reference counting alone not free these?

**(b)** What does the cyclic garbage collector do, and why is it not instant?

**(c)** What is the fix that avoids the cycle entirely?

<details>
<summary><b>Show the diagnosis</b></summary>

`root` refers to `child` and `child` refers back to `root`, so both refcounts stay at 1 after the function returns. Refcounting can never collect a cycle — that is its one structural weakness.

**The cyclic GC** finds unreachable cycles by tracing, but it runs **generationally** on allocation thresholds, not immediately. Until it runs, the memory is held. `gc.collect()` forces it; `gc.set_threshold()` tunes it.

**Avoid the cycle:** make the back-reference weak — `self.parent = weakref.ref(root)`. Then the child does not keep the parent alive, refcounting frees everything promptly, and the GC never has to get involved. This is the standard fix for parent pointers, observer registries and caches.

</details>

---

### D2. getsizeof misread as deep size

```python
import sys

data = [list(range(1000)) for _ in range(1000)]
print(sys.getsizeof(data))
```

**Observed symptom:** Reports about 8 KB for a structure holding a million integers.

**(a)** What is `getsizeof` actually measuring?

**(b)** How do you get the real total?

**(c)** Why is even the 'real total' ambiguous for Python objects?

<details>
<summary><b>Show the diagnosis</b></summary>

`getsizeof` returns the size of **that object only** — here a list of 1000 *pointers*, 8 bytes each plus header. It does not follow references.

**Real total:** walk it recursively (`pympler.asizeof`), or measure the process instead: `tracemalloc.start()` then `tracemalloc.get_traced_memory()`, which is what Module 12's profiler does.

**Ambiguous because of sharing:** small ints (-5..256) are interned, so `range(1000)` shares 262 of its objects with everything else in the process. Strings may be interned too. Asking 'how big is this object' has no single answer when parts of it are shared globally — which is why process-level measurement before and after is the honest technique.

</details>

---

### D3. Bytecode reveals a hidden cost

```python
def build_slow(items: list[str]) -> str:
    result = ""
    for item in items:
        result += item
    return result
```

**Observed symptom:** Quadratic slowdown: 10× more items takes ~100× longer.

**(a)** What does `dis.dis` show about the loop body that explains the cost?

**(b)** What is the linear alternative?

**(c)** Why does CPython sometimes make this look fast in a microbenchmark?

<details>
<summary><b>Show the diagnosis</b></summary>

`dis.dis` shows `BINARY_OP 13 (+=)` inside the loop. Strings are **immutable**, so each `+=` allocates a brand-new string and copies every character accumulated so far. Total work is 1+2+3+...+n = O(n²).

**Linear fix:** `''.join(items)` — one pass to compute the total length, one allocation, one copy per character.

**Microbenchmarks lie** because CPython has an in-place optimisation for `str +=` when the left operand's refcount is exactly 1: it can resize in place and avoid the copy. That applies in a tight local loop but silently stops applying the moment anything else holds a reference — so the same code is linear in your benchmark and quadratic in production. `join` is unconditionally correct.

</details>

---

### D4. Interning makes `is` unreliable

```python
a = 256
b = 256
print(a is b)

x = 257
y = 257
print(x is y)

s1 = "hello world"
s2 = "hello world"
print(s1 is s2)
```

**Observed symptom:** Prints `True`, then `False`, then `True` — inconsistently across Python versions and between the REPL and a script file.

**(a)** Explain each of the three results.

**(b)** What is the rule for using `is`?

**(c)** Why does running the same lines in a REPL versus a file change the answer?

<details>
<summary><b>Show the diagnosis</b></summary>

**256** is in CPython's small-integer cache (-5 to 256), so both names point at the same preallocated object. **257** is outside it, so two separate objects are created. **`"hello world"`** is interned here because the compiler constant-folds identical literals within the same code object.

**Rule:** use `is` **only** for singletons — `None`, `True`, `False`, and your own sentinels. For value comparison always use `==`. `ruff` flags `is` against a literal as `F632`.

**REPL vs file:** in a file, both `257` literals live in one code object and may be folded into one constant; in the REPL each line is compiled separately, so they cannot be. This is an implementation detail that has changed between versions — which is precisely why you must not depend on it.

</details>

---

### D5. AST transform breaks on a rewritten node

```python
import ast

class Doubler(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if isinstance(node.value, int):
            return ast.Constant(value=node.value * 2)
        return node

tree = ast.parse("x = 21")
new = Doubler().visit(tree)
exec(compile(new, "<ast>", "exec"))
```

**Observed symptom:** `ValueError: field 'lineno' is required for Constant` — or a segfault on some versions.

**(a)** What is missing from the newly created node?

**(b)** What is the one-line fix?

**(c)** Why does `ast.NodeTransformer` not do this for you?

<details>
<summary><b>Show the diagnosis</b></summary>

A hand-constructed AST node has no position attributes (`lineno`, `col_offset`, `end_lineno`, `end_col_offset`). `compile` requires them on every node to build tracebacks and to bounds-check.

**Fix:** `ast.fix_missing_locations(new)` before compiling — it copies positions from parent nodes throughout the tree. `ast.copy_location(new_node, node)` is the per-node equivalent.

**Why not automatic:** `NodeTransformer` cannot know whether your new node corresponds to the old one's source position or to something synthetic, and guessing would produce misleading tracebacks. The explicit call is the API telling you that source mapping is your decision. Module 12's security profiler calls it after every rewrite.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
