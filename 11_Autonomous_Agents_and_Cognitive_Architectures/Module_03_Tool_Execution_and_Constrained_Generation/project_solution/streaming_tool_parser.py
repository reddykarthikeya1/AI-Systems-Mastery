"""Streaming Partial JSON Tool Call Parser."""

from __future__ import annotations

import json
import re
from typing import Any, Callable, Dict, Optional


class StreamingToolParser:
    """Parses tool call JSON incrementally as tokens arrive."""

    def __init__(self, on_field_ready: Optional[Callable[[str, Any], None]] = None) -> None:
        self.on_field_ready = on_field_ready
        self.buffer = ""
        self.parsed_fields: Dict[str, Any] = {}
        self._notified_fields: set[str] = set()

    def feed_token(self, token: str) -> Dict[str, Any]:
        """Ingests a new token chunk and extracts any completed parameters."""
        self.buffer += token
        self._extract_fields()
        return dict(self.parsed_fields)

    def _extract_fields(self) -> None:
        pattern = re.compile(r'"([A-Za-z0-9_]+)"\s*:\s*("(?:[^"\\]|\\.)*"|[0-9]+(?:\.[0-9]+)?|true|false|null)')
        matches = pattern.findall(self.buffer)

        for key, raw_val in matches:
            if key not in self._notified_fields:
                try:
                    parsed_val = json.loads(raw_val)
                    self.parsed_fields[key] = parsed_val
                    self._notified_fields.add(key)
                    if self.on_field_ready:
                        self.on_field_ready(key, parsed_val)
                except json.JSONDecodeError:
                    continue

    def get_final_payload(self) -> Dict[str, Any]:
        """Attempts full JSON load or returns extracted parsed fields."""
        try:
            return json.loads(self.buffer)
        except json.JSONDecodeError:
            return dict(self.parsed_fields)
