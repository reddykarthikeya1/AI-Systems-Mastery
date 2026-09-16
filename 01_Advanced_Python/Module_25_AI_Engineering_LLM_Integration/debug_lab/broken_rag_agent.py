#!/usr/bin/env python3
"""Broken RAG Pipeline demonstrating mid-sentence splitting and zero overlap boundary loss."""

def naive_chunk_text(text: str, chunk_size: int = 50) -> list[str]:
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i : i + chunk_size])
    return chunks

if __name__ == "__main__":
    document = (
        "Server Alpha security policy: The administrative master key is 9988-SECURE. "
        "Do not share this key with external contractors."
    )
    chunks = naive_chunk_text(document, chunk_size=40)
    for idx, c in enumerate(chunks):
        print(f"Chunk {idx}: '{c}'")
