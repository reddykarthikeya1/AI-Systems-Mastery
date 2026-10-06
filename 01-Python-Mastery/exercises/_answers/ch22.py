"""Chapter 22 - Capstone Playbook: Metaclass plugin registries, chunked streaming aggregators, and generator cleanup.

1. PluginRegistryMeta: Metaclass that automatically registers and validates plugin classes.
2. chunked_stream_aggregator: Memory-bounded generator computing summary metrics across chunks.
3. managed_resource_stream (debugging): Fix generator resource handle leak on early break or exception.
"""
from typing import Dict, Any, Iterator, Tuple


class PluginRegistryMeta(type):
    """Metaclass that registers non-abstract plugins in a class-level dictionary."""
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        if not hasattr(cls, "_registry"):
            cls._registry = {}
        # Only register concrete subclasses (those that provide a plugin_name)
        plugin_name = namespace.get("plugin_name")
        if plugin_name:
            if not callable(namespace.get("execute")):
                raise TypeError(f"Plugin {name} must implement callable 'execute(self, payload)'")
            cls._registry[plugin_name] = cls
        return cls


def chunked_stream_aggregator(stream: Iterator[float], chunk_size: int) -> Iterator[Tuple[int, int, float, float, float]]:
    """Process `stream` in chunks of `chunk_size`.
    Yields (chunk_idx, count, mean, min_val, max_val) for each chunk.
    Never loads the entire stream into memory at once."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    chunk_idx = 0
    chunk = []
    for item in stream:
        chunk.append(float(item))
        if len(chunk) == chunk_size:
            yield (chunk_idx, len(chunk), sum(chunk) / len(chunk), min(chunk), max(chunk))
            chunk_idx += 1
            chunk = []
    if chunk:
        yield (chunk_idx, len(chunk), sum(chunk) / len(chunk), min(chunk), max(chunk))


class MockResource:
    def __init__(self):
        self.is_open = True

    def close(self):
        self.is_open = False


BUGGY = {
    "managed_resource_stream": '''def managed_resource_stream(resource, items):
    """Yield items while keeping resource open, closing it when done."""
    # BUG: If consumer breaks early or raises, resource.close() is never called!
    for item in items:
        yield item * 2
    resource.close()''',
}


def managed_resource_stream(resource, items):
    """Yield items from `items`, guaranteeing `resource.close()` is called even on early exit."""
    try:
        for item in items:
            yield item * 2
    finally:
        resource.close()


# --- Tests ---

def t_plugin_registry_meta(m):
    class BasePlugin(metaclass=m.PluginRegistryMeta):
        _registry = {}

    class JsonPlugin(BasePlugin):
        plugin_name = "json"
        def execute(self, payload):
            return {"format": "json", **payload}

    class CsvPlugin(BasePlugin):
        plugin_name = "csv"
        def execute(self, payload):
            return {"format": "csv", **payload}

    assert "json" in BasePlugin._registry
    assert "csv" in BasePlugin._registry
    assert BasePlugin._registry["json"] is JsonPlugin
    
    # Missing execute should raise TypeError
    try:
        class BrokenPlugin(BasePlugin):
            plugin_name = "broken"
        assert False, "Should raise TypeError for missing execute method"
    except TypeError:
        pass


def t_chunked_stream_aggregator(m):
    def data_gen():
        for x in [10.0, 20.0, 30.0, 40.0, 50.0]:
            yield x

    chunks = list(m.chunked_stream_aggregator(data_gen(), chunk_size=2))
    assert len(chunks) == 3
    # Chunk 0: [10, 20]
    assert chunks[0] == (0, 2, 15.0, 10.0, 20.0)
    # Chunk 1: [30, 40]
    assert chunks[1] == (1, 2, 35.0, 30.0, 40.0)
    # Chunk 2: [50] (remainder)
    assert chunks[2] == (2, 1, 50.0, 50.0, 50.0)


def t_managed_resource_stream_guaranteed_cleanup(m):
    res = m.MockResource()
    gen = m.managed_resource_stream(res, [1, 2, 3, 4, 5])
    assert next(gen) == 2
    assert res.is_open is True
    # Early break / close generator
    gen.close()
    assert res.is_open is False, "Resource was not closed after generator closed!"
