"""Neural Named Entity Recognition (NER) Contextual Token Classifier Simulator."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class DetectedEntity:
    text: str
    entity_type: str  # PER, LOC, ORG, MEDICAL_ID
    start_pos: int
    end_pos: int


class NeuralNERPIIScanner:
    """Contextual token classification detecting unstructured PII entities."""

    HONORIFICS = {"dr", "mr", "mrs", "ms", "prof", "patient"}
    LOC_SUFFIXES = {"street", "avenue", "st", "ave", "road", "rd", "boulevard", "lane"}

    def scan_entities(self, text: str) -> List[DetectedEntity]:
        entities = []
        tokens = text.split()
        char_idx = 0

        for i, tok in enumerate(tokens):
            clean_tok = re.sub(r"[^a-zA-Z0-9]", "", tok)
            clean_lower = clean_tok.lower()
            start = text.find(tok, char_idx)
            end = start + len(tok)
            char_idx = end

            if i > 0:
                prev = re.sub(r"[^a-zA-Z0-9]", "", tokens[i - 1]).lower()
                if prev in self.HONORIFICS and clean_tok.istitle():
                    entities.append(DetectedEntity(text=tok, entity_type="PER", start_pos=start, end_pos=end))
                    continue

            if clean_lower in self.LOC_SUFFIXES and i > 0:
                entities.append(DetectedEntity(text=f"{tokens[i-1]} {tok}", entity_type="LOC", start_pos=start - len(tokens[i-1]) - 1, end_pos=end))

        return entities

    def mask_unstructured_pii(self, text: str) -> str:
        entities = self.scan_entities(text)
        result = text
        for ent in reversed(entities):
            result = result[:ent.start_pos] + f"[REDACTED_{ent.entity_type}]" + result[ent.end_pos:]
        return result
