#!/usr/bin/env python3
"""Module 19: Metaprogramming with __init_subclass__ Demonstration.

This script demonstrates using Python 3.6+ __init_subclass__ to build an
automatic plugin registry without complex metaclasses.
"""

from __future__ import annotations

from typing import ClassVar


class PluginBase:
    """Base class that automatically registers all subclasses into a registry."""
    registry: ClassVar[dict[str, type[PluginBase]]] = {}

    def __init_subclass__(cls, plugin_name: str | None = None, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__.lower()
        PluginBase.registry[name] = cls
        print(f"Registered Plugin: '{name}' -> {cls.__name__}")


class JSONExporter(PluginBase, plugin_name="json"):
    def export(self, data: dict) -> str:
        return f"JSON: {data}"


class CSVExporter(PluginBase, plugin_name="csv"):
    def export(self, data: dict) -> str:
        return f"CSV: {data}"


def main() -> None:
    print("=" * 60)
    print("  Automatic Plugin Registration via __init_subclass__")
    print("=" * 60)

    print("\nAll Active Registered Plugins:")
    for name, plugin_cls in PluginBase.registry.items():
        print(f"  - [{name}]: {plugin_cls}")


if __name__ == "__main__":
    main()
