# Debug Lab: PD-Disaggregated KV Transfer Loses Chunks to Slot Collision
# Course 09 - Module 06 Chunked Prefill and PD Disaggregation

CHUNK_SIZE = 4
NUM_TRANSFER_SLOTS = 2  # double-buffered transfer slots between prefill and decode nodes


def chunk_prompt(tokens):
    """Chunked prefill: split the prompt into fixed-size chunks so the
    prefill worker can interleave prefill work with other requests' decode
    steps instead of running the whole prompt in one giant pass."""
    return [tokens[i:i + CHUNK_SIZE] for i in range(0, len(tokens), CHUNK_SIZE)]


def prefill_worker_send(chunks, transfer_bus):
    """Simulates the prefill (P) node streaming each chunk's KV cache across
    the network to the decode (D) node, using a small pool of transfer slots
    so chunks can be pipelined instead of allocating one slot per chunk."""
    for chunk_id, chunk in enumerate(chunks):
        slot = chunk_id % NUM_TRANSFER_SLOTS
        transfer_bus[slot] = (chunk_id, chunk)  # last write to a slot wins


def decode_worker_receive(transfer_bus, num_chunks):
    """The decode (D) node reads whatever currently occupies each slot to
    reassemble the full prefilled context before starting generation."""
    assembled = {}
    for slot in range(NUM_TRANSFER_SLOTS):
        if slot in transfer_bus:
            chunk_id, chunk = transfer_bus[slot]
            assembled[chunk_id] = chunk
    ordered_tokens = []
    for chunk_id in range(num_chunks):
        ordered_tokens.extend(assembled.get(chunk_id, []))
    return ordered_tokens


if __name__ == "__main__":
    prompt = ["The", "quick", "brown", "fox", "jumps", "over",
              "the", "lazy", "dog", "near", "the", "river", "bank", "."]

    chunks = chunk_prompt(prompt)
    transfer_bus = {}
    prefill_worker_send(chunks, transfer_bus)
    received = decode_worker_receive(transfer_bus, len(chunks))

    print(f"Original prompt ({len(prompt)} tokens): {' '.join(prompt)}")
    print(f"Chunked into {len(chunks)} chunks of size {CHUNK_SIZE}: {chunks}")
    print(f"Expected: decode worker reassembles all {len(prompt)} tokens in order "
          f"before generating.")
    print(f"Actual tokens received by decode worker ({len(received)} tokens): "
          f"{' '.join(received)}")
