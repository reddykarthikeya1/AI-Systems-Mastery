# Debug Lab Answers: Module 12

<details>
<summary>Bug 1: Reference cycles keeping objects alive</summary>

### Root Cause
Python's primary memory management is reference counting. In a circular reference (`a.link = b; b.link = a`), deleting names `a` and `b` decrements their reference counts from 2 to 1, never reaching 0. Only the cyclic garbage collector (`gc.collect()`) can detect and free isolated reference clusters.

### Fix
Use weak references (`weakref.ref` or `weakref.proxy`) to break circular ownership:
```python
import weakref

class Node:
    def __init__(self, name: str):
        self.name = name
        self._link = None

    @property
    def link(self):
        return self._link() if self._link else None

    @link.setter
    def link(self, target):
        self._link = weakref.ref(target) if target else None
```
</details>

<details>
<summary>Bug 2: sys.getsizeof is shallow</summary>

### Root Cause
`sys.getsizeof()` returns only the bytes allocated directly to the container object itself (its pointer array), not the memory consumed by the objects it points to.

### Fix
Implement a recursive deep `getsizeof` walker to compute actual memory consumption:
```python
def deep_getsizeof(obj, seen=None):
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(deep_getsizeof(v, seen) + deep_getsizeof(k, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(deep_getsizeof(i, seen) for i in obj)
    return size
```
</details>
