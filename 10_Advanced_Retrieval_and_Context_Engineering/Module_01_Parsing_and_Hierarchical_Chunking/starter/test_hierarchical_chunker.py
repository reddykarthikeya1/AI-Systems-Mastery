from __future__ import annotations

from hierarchical_chunker import HierarchicalDocumentChunker


def test_hierarchical_chunking_parent_child_linkage():
    chunker = HierarchicalDocumentChunker(parent_size_words=50, child_size_words=20, overlap_words=5)
    text = "word " * 120  # 120 words total

    parents = chunker.chunk_document(doc_id="doc_1", title="Test Doc", text=text)

    # 120 words / 50 = 3 parents (50, 50, 20)
    assert len(parents) == 3
    assert parents[0].parent_id == "doc_1_p0"
    assert parents[1].parent_id == "doc_1_p1"

    # Verify children are linked to parent
    first_parent = parents[0]
    assert len(first_parent.children) > 1
    for child in first_parent.children:
        assert child.parent_id == first_parent.parent_id


def test_empty_document():
    chunker = HierarchicalDocumentChunker()
    assert chunker.chunk_document("doc_0", "Empty", "") == []
