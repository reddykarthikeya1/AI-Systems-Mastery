"""Broken tracer with negative duration and missing cost."""

class BrokenTracer:
    def record(self, model, tokens):
        # BUG: Ignores latency, TTFT, and monetary cost
        return {"tokens": tokens}
