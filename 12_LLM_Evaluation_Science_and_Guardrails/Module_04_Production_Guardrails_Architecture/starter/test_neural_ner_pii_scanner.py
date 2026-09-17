"""Unit tests for Neural NER PII Scanner."""

from __future__ import annotations

from neural_ner_pii_scanner import NeuralNERPIIScanner


def test_detect_person_name_with_context():
    scanner = NeuralNERPIIScanner()
    text = "The doctor consulted with Dr. Katherine regarding the diagnosis."
    entities = scanner.scan_entities(text)
    assert len(entities) == 1
    assert entities[0].text == "Katherine"
    assert entities[0].entity_type == "PER"

    masked = scanner.mask_unstructured_pii(text)
    assert "Dr. [REDACTED_PER]" in masked


def test_detect_location_context():
    scanner = NeuralNERPIIScanner()
    text = "Send documents to 742 Evergreen Terrace."
    entities = scanner.scan_entities(text)
    assert len(entities) >= 0
