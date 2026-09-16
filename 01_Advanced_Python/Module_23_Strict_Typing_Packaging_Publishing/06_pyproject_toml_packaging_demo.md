# Modern PEP 621 `pyproject.toml` Packaging Standard

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "enterprise-typed-sdk"
version = "1.0.0"
description = "Production-grade, fully typed Python SDK library"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [{ name = "Python Lead", email = "lead@enterprise.com" }]
dependencies = [
    "httpx>=0.27.0",
    "pydantic>=2.7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "mypy>=1.10.0",
    "ruff>=0.4.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/enterprise_typed_sdk"]
```

## The `py.typed` Marker

Always place an empty file named `py.typed` inside your package root directory:
```
src/enterprise_typed_sdk/
├── __init__.py
├── client.py
└── py.typed   <-- Tells Mypy/Pyright to inspect inline type hints!
```
