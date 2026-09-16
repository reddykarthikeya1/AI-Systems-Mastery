"""Starter stub for Production Guardrail Pipeline."""

from __future__ import annotations
from typing import Any, List, Optional


class ProductionGuardrailPipeline:
    def __init__(self, blocked_topics: Optional[List[str]] = None) -> None:
        raise NotImplementedError("ProductionGuardrailPipeline is not implemented yet.")

    def inspect_input_safety(self, text: str) -> Any:
        raise NotImplementedError
