# Debug Lab: Hierarchical Chunker Drops the Overlap Window at Boundaries
# Course 10 - Module 01 Parsing and Hierarchical Chunking

CHUNK_SIZE = 40   # characters per chunk
OVERLAP = 10      # characters of overlap carried into the next chunk


def chunk_document(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split `text` into overlapping fixed-size chunks. The overlap exists so
    a sentence or fact that straddles a chunk boundary still appears whole in
    at least one chunk, instead of being severed."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end  # advance to the next non-overlapping window
    return chunks


def contains_intact(chunks, phrase):
    return any(phrase in chunk for chunk in chunks)


if __name__ == "__main__":
    document = (
        "Section 1: Refunds are processed within five business days of the "
        "return being received. Section 2: Exchanges require the original "
        "receipt and must occur within thirty days of purchase."
    )

    chunks = chunk_document(document)

    boundary_phrase = "received. Section 2"

    print(f"Document length: {len(document)} chars, chunk_size={CHUNK_SIZE}, overlap={OVERLAP}")
    print("Chunks produced:")
    for i, c in enumerate(chunks):
        print(f"  [{i}] {c!r}")

    print(f"\nExpected: the boundary phrase {boundary_phrase!r} (which straddles a "
          f"chunk cut) should appear INTACT in at least one chunk, thanks to the "
          f"{OVERLAP}-char overlap.")
    print(f"Actual: phrase found intact in some chunk = {contains_intact(chunks, boundary_phrase)}")
