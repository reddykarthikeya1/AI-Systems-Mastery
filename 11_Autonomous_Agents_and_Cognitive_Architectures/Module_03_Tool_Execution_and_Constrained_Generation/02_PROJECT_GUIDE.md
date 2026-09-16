# Project Guide: Building an Enterprise Tool Dispatcher

In this project, you will build a production-grade tool registry and execution engine with automatic schema generation, strict argument validation, and timeout isolation.

---

## Three-Tier Implementation Path

### Tier 1: Schema Introspection & Basic Dispatch
- Write a decorator `@tool` that inspects function signatures, docstrings, and Python type hints to generate valid JSON Schema.
- Implement `ToolRegistry.register(fn)` and `ToolRegistry.get_schemas()`.

### Tier 2: Validation, Coercion, and Error Wrapping
- Validate incoming dictionary arguments against parameter types.
- Perform safe type casting (e.g. parsing integer strings to `int`).
- Catch all runtime exceptions and return structured error diagnostics.

### Tier 3: Timeout Guards & Sandboxed Dispatch
- Wrap function invocation in a `concurrent.futures.ThreadPoolExecutor` to enforce strict timeout ceilings.
