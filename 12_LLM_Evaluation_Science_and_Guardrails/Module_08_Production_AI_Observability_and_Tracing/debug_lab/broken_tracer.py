"""Broken tracer with negative duration and missing cost."""

class BrokenTracer:
    def record(self, model, tokens):
        return {"tokens": tokens}


def reproduce_defect():
    print("Recording a trace for an LLM call that took 2.4s, 0.6s TTFT, and billed $0.018...")
    tracer = BrokenTracer()

    # The real API call this trace is describing took 2.4s end-to-end, 0.6s to
    # first token, and billed $0.018 -- record() isn't given the chance to
    # capture any of that.
    trace = tracer.record(model="gpt-4o", tokens=1523)

    print(f"Trace object emitted for this LLM call: {trace}")
    print("Expected: the trace should capture latency, time-to-first-token, and cost")
    print(f"Actual:   Does the trace capture latency/duration? {'latency' in trace or 'duration' in trace}")
    print(f"Actual:   Does the trace capture time-to-first-token? {'ttft' in trace}")
    print(f"Actual:   Does the trace capture monetary cost? {'cost' in trace}")


if __name__ == "__main__":
    reproduce_defect()
