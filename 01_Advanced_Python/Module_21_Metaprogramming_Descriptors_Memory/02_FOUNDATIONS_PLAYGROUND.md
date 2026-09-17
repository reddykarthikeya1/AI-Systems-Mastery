# 🐣 Interactive Foundations Playground: Metaprogramming & Descriptors

> *"Descriptors manage attribute access behind the scenes, powering properties, methods, and ORMs."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python

```

---

## 1. Custom Descriptor Protocol (__get__ and __set__)

The descriptor protocol intercepts attribute lookup, assignment, and deletion.

```python
class NonNegative:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, 0)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name} cannot be negative")
        instance.__dict__[self.name] = value

class Account:
    balance = NonNegative("balance")

acc = Account()
acc.balance = 500
assert acc.balance == 500
try:
    acc.balance = -50
except ValueError:
    pass
assert acc.balance == 500
print(f"Descriptor verified non-negative balance constraint: {acc.balance}")
```

---

## 2. Subclass Registration with __init_subclass__

`__init_subclass__` provides a clean hook to register plugin classes without full metaclass boilerplate.

```python
registry = {}
class PluginBase:
    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            registry[plugin_name] = cls

class AudioPlugin(PluginBase, plugin_name="audio"):
    pass

class VideoPlugin(PluginBase, plugin_name="video"):
    pass

assert "audio" in registry
assert "video" in registry
assert registry["audio"] is AudioPlugin
print(f"Registered plugins via __init_subclass__: {list(registry.keys())}")
```

---

## 3. Dynamic Attribute Lookup with __getattr__

`__getattr__` intercepts lookups for attributes that are not found in the instance dictionary.

```python
class DynamicProxy:
    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"No attribute {name}")

proxy = DynamicProxy({"version": "2.4", "status": "active"})
assert proxy.version == "2.4"
assert proxy.status == "active"
print("Dynamic proxy resolved missing attributes from wrapped dictionary.")
```

---
