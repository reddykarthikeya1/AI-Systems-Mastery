# Debug Lab: Needle-in-a-Haystack Test Inserts at the Wrong Depth
# Course 10 - Module 09 Context Optimization and NIAH Testing

FILLER_SENTENCE = "The library was quiet this afternoon. "


def build_haystack(num_sentences):
    return FILLER_SENTENCE * num_sentences


def insert_needle_at_depth(haystack, needle, depth_percent):
    """Insert `needle` into `haystack` at `depth_percent` of the way through
    the document (0.0 = very start, 1.0 = very end), the way NIAH tests
    probe whether a model can retrieve facts planted at different positions
    in a long context."""
    insertion_index = len(haystack) - int(depth_percent * len(haystack))
    return haystack[:insertion_index] + needle + haystack[insertion_index:]


def measured_depth(document_with_needle, needle):
    """Recover where the needle actually ended up, as a fraction of the
    document's length, so the test harness can label results by true depth."""
    idx = document_with_needle.index(needle)
    return idx / len(document_with_needle)


if __name__ == "__main__":
    haystack = build_haystack(num_sentences=50)
    needle = " The secret password is 'kingfisher-42'. "

    requested_depth = 0.10  # "plant the needle near the very beginning"

    document = insert_needle_at_depth(haystack, needle, requested_depth)
    actual_depth = measured_depth(document, needle)

    print(f"Haystack length: {len(haystack)} chars, requested insertion depth: "
          f"{requested_depth:.0%} (near the start of the document).")
    print(f"Expected: the needle should land at roughly {requested_depth:.0%} "
          f"of the way through the document.")
    print(f"Actual measured depth after insertion: {actual_depth:.1%}")
    print(f"First 80 chars of the document: {document[:80]!r}")
    print(f"Last 80 chars of the document:  {document[-80:]!r}")
