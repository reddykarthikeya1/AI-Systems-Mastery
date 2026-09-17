from __future__ import annotations

from contextual_retriever import ContextualAugmenter


def test_contextual_augmentation():
    c = ContextualAugmenter.augment_chunk(
        chunk_id="chunk_42",
        text="Operating margin dropped by 4.2%.",
        doc_title="Apple 2023 10-K",
        section_name="Financial Highlights",
        key_entities=["Apple", "2023"],
    )

    assert "Apple 2023 10-K" in c.context_header
    assert "Operating margin dropped by 4.2%." in c.augmented_text
    assert c.augmented_text.startswith("[Doc: Apple 2023 10-K")
