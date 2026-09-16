from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class ContextualChunk:
    chunk_id: str
    original_text: str
    context_header: str
    augmented_text: str


class ContextualAugmenter:
    """Simulates Anthropic Contextual Retrieval chunk augmentation."""

    @staticmethod
    def generate_context_header(doc_title: str, section_name: str, key_entities: list[str]) -> str:
        entities_str = ", ".join(key_entities) if key_entities else "General"
        return f"[Doc: {doc_title} | Section: {section_name} | Entities: {entities_str}]"

    @classmethod
    def augment_chunk(
        cls,
        chunk_id: str,
        text: str,
        doc_title: str,
        section_name: str,
        key_entities: list[str],
    ) -> ContextualChunk:
        header = cls.generate_context_header(doc_title, section_name, key_entities)
        augmented = f"{header}\n{text}"
        return ContextualChunk(
            chunk_id=chunk_id,
            original_text=text,
            context_header=header,
            augmented_text=augmented,
        )
