# Beginner Playground: OpenTelemetry Tracing & Cost Observability

Welcome to AI Observability! In production, an AI request is not a black box: you must track TTFT (Time-To-First-Token), prompt/completion token usage, monetary cost, and nested tool spans.

---

## 1. The Core Mental Model: OpenTelemetry GenAI Spans

Every interaction generates a hierarchical **Trace**:
```
 [ Root Span: User Query ]  (Duration: 1.2s, Total Cost: $0.004)
     |
     +--> [ Span 1: Vector Search ]  (Duration: 45ms)
     |
     +--> [ Span 2: Guardrail Pre-flight ]  (Duration: 12ms)
     |
     +--> [ Span 3: LLM Completion ]  (TTFT: 180ms, TPOT: 15ms, 120 Tokens)
```

---

## 2. Interactive Pure-Python Experiment: OpenTelemetry Span Tracer

```python
import time

class MiniSpan:
    def __init__(self, name: str):
        self.name = name
        self.start_time = 0.0
        self.end_time = 0.0
        self.attributes = {}

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()

    @property
    def duration_ms(self) -> float:
        return (self.end_time - self.start_time) * 1000.0

with MiniSpan("llm_inference") as span:
    time.sleep(0.05) # Simulated generation
    span.attributes["gen_ai.usage.prompt_tokens"] = 512
    span.attributes["gen_ai.usage.completion_tokens"] = 64

print(f"Span '{span.name}' completed in {span.duration_ms:.2f} ms")
print("Attributes:", span.attributes)
```
