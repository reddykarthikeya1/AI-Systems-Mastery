from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class ChildChunk:
    child_id: str
    parent_id: str
    text: str
    token_count: int


@dataclasses.dataclass
class ParentChunk:
    parent_id: str
    title: str
    full_text: str
    children: list[ChildChunk]


class HierarchicalDocumentChunker:
    def __init__(self, parent_size_words: int = 100, child_size_words: int = 30, overlap_words: int = 5):
        raise NotImplementedError("Implement HierarchicalDocumentChunker")

    def chunk_document(self, doc_id: str, title: str, text: str) -> list[ParentChunk]:
        raise NotImplementedError("Implement chunk_document")
