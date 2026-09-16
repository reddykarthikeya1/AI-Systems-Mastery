"""Starter stub for GenAI Telemetry Tracer."""

from __future__ import annotations
from typing import Any, Dict


class GenAITracer:
    def __init__(self, trace_id: str) -> None:
        raise NotImplementedError("GenAITracer is not implemented yet.")

    def export_otel_payload(self) -> Dict[str, Any]:
        raise NotImplementedError
