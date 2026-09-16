# Project Guide: Building an OpenTelemetry AI Tracing & Cost Engine

In this capstone lab, you will implement an OpenTelemetry-compliant tracing library that tracks nested spans, calculates token usage and dollar costs, and records TTFT and TPOT.

---

## Three-Tier Implementation Path

### Tier 1: Span Lifecycle & Context Manager (Required)
- Implement `TraceSpan` with `__enter__` and `__exit__`.
- Record start time, end time, and attributes.

### Tier 2: Token Counting & Model Pricing Calculator
- Implement pricing tables for standard model families.
- Calculate exact cost per span and aggregate across parent trace.

### Tier 3: OTel JSON Exporter & Latency Breakdown
- Export traces as standard OpenTelemetry JSON spans.
- Compute TTFT, TPOT, and total duration.
