"""Beginner playground for Module 21 - Metaprogramming & Descriptors.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# -------------------------------------------- 1. Custom Descriptor Protocol (__get__ and __set__)
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

# -------------------------------------------- 2. Subclass Registration with __init_subclass__
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

# -------------------------------------------- 3. Dynamic Attribute Lookup with __getattr__
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

print()
print("All checks passed.")
