from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class ContextualChunk:
    chunk_id: str
    original_text: str
    context_header: str
    augmented_text: str


class ContextualAugmenter:
    @staticmethod
    def generate_context_header(doc_title: str, section_name: str, key_entities: list[str]) -> str:
        raise NotImplementedError("Implement generate_context_header")

    @classmethod
    def augment_chunk(
        cls,
        chunk_id: str,
        text: str,
        doc_title: str,
        section_name: str,
        key_entities: list[str],
    ) -> ContextualChunk:
        raise NotImplementedError("Implement augment_chunk")
