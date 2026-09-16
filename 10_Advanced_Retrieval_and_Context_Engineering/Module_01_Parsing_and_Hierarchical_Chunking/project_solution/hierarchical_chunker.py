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
    children: list[ChildChunk] = dataclasses.field(default_factory=list)


class HierarchicalDocumentChunker:
    """Splits documents into Parent-Child hierarchical chunks with structural metadata."""

    def __init__(self, parent_size_words: int = 100, child_size_words: int = 30, overlap_words: int = 5):
        self.parent_size = parent_size_words
        self.child_size = child_size_words
        self.overlap = overlap_words

    def chunk_document(self, doc_id: str, title: str, text: str) -> list[ParentChunk]:
        words = text.split()
        if not words:
            return []

        parents = []
        p_idx = 0
        w_idx = 0

        while w_idx < len(words):
            parent_words = words[w_idx : w_idx + self.parent_size]
            parent_text = " ".join(parent_words)
            parent_id = f"{doc_id}_p{p_idx}"

            parent_chunk = ParentChunk(parent_id=parent_id, title=title, full_text=parent_text)

            # Split parent into children
            c_idx = 0
            c_w_idx = 0
            while c_w_idx < len(parent_words):
                child_slice = parent_words[c_w_idx : c_w_idx + self.child_size]
                child_text = " ".join(child_slice)
                child_id = f"{parent_id}_c{c_idx}"

                child_chunk = ChildChunk(
                    child_id=child_id,
                    parent_id=parent_id,
                    text=child_text,
                    token_count=len(child_slice),
                )
                parent_chunk.children.append(child_chunk)

                c_w_idx += self.child_size - self.overlap
                c_idx += 1

            parents.append(parent_chunk)
            w_idx += self.parent_size
            p_idx += 1

        return parents
