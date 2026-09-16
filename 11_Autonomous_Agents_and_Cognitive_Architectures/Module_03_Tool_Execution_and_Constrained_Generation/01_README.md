# Module 03: Tool Execution and Constrained Generation

## 1. Architectural Foundations: Function Calling & Constrained Decoding

Modern agent architectures rely on tools to interact with APIs, databases, and operating systems. Ensuring that an LLM outputs syntactically and semantically valid tool arguments requires two complementary mechanisms:
1. **Logit-Level Constrained Generation**: Constraining next-token sampling to tokens that satisfy Context-Free Grammars (CFGs) or JSON Schema (e.g., Outlines, llama.cpp GBNF).
2. **Deterministic Schema Validation & Coercion**: A host-side dispatcher that validates parameters against Pydantic / JSON Schema contracts before execution.

---

## 2. Tool Schema Protocol & Execution Lifecycle

```mermaid
flowchart TD
    A[Python Function] -->|inspect.signature| B[JSON Schema Definition]
    B -->|Serialized System Prompt| C[LLM Inference Engine]
    C -->|Generates Tool Call JSON| D[Grammar / JSON Parser]
    D -->|Parsed Arguments| E[Type Coercion & Validation]
    E -->|Validation Success| F[Sandboxed Tool Execution]
    E -->|Validation Failure| G[Error Feedback Observation]
    F -->|Return Value| H[Observation Injected to Agent]
    G -->|Self-Correction Prompt| C
```

---

## 3. Sandboxing & Timeout Management

Tools often perform network I/O, database queries, or OS subprocess calls. Unbounded tool execution will deadlock agent worker threads.

Key production invariants:
- **Strict Wall-Clock Timeouts**: Every tool execution must run inside an isolated thread or subprocess bounded by a hard ceiling (e.g., 5.0 seconds).
- **Graceful Error Encapsulation**: A tool must never raise an unhandled exception to the main loop; exceptions must be caught, formatted as descriptive strings, and returned to the LLM as an observation so it can self-heal.
