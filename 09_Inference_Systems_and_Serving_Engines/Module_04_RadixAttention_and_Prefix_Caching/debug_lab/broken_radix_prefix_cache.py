# Debug Lab: RadixAttention Prefix Cache Never Hits on Shared System Prompts
# Course 09 - Module 04 RadixAttention and Prefix Caching

CACHE_KEY_LEN = 4  # how many tokens of the request are used to key the cache


class RadixPrefixCache:
    """A simplified stand-in for RadixAttention's radix-tree prefix cache:
    requests sharing a common prompt prefix should reuse the same cached KV
    blocks instead of recomputing them."""

    def __init__(self):
        self.store = {}  # cache_key -> "computed KV blocks" (just a counter here)
        self.compute_calls = 0

    def _cache_key(self, tokens):
        # The cache should key on the tokens the requests actually share --
        # the leading system-prompt tokens -- so that two requests with the
        # same prefix but different user turns land on the same cache entry.
        return tuple(tokens[-CACHE_KEY_LEN:])

    def get_or_compute(self, tokens):
        key = self._cache_key(tokens)
        if key in self.store:
            return self.store[key], True  # cache hit, no recompute
        self.compute_calls += 1
        kv_blocks = f"kv_blocks_for_call_{self.compute_calls}"
        self.store[key] = kv_blocks
        return kv_blocks, False


if __name__ == "__main__":
    system_prompt = ["You", "are", "a", "helpful", "assistant", "."]

    request_a = system_prompt + ["What", "is", "2+2?"]
    request_b = system_prompt + ["Summarize", "this", "doc."]
    request_c = system_prompt + ["Translate", "hello."]

    cache = RadixPrefixCache()
    results = []
    for name, tokens in [("request_a", request_a), ("request_b", request_b), ("request_c", request_c)]:
        _, hit = cache.get_or_compute(tokens)
        results.append((name, hit))

    print("All three requests share the same 6-token system prompt prefix:")
    print(f"  {' '.join(system_prompt)}")
    print("Expected: request_b and request_c should HIT the cache entry request_a "
          "populated for the shared system prompt (only 1 total KV compute).")
    for name, hit in results:
        print(f"  {name}: cache_hit={hit}")
    print(f"Actual total KV compute calls (should be 1 if the shared prefix were reused): "
          f"{cache.compute_calls}")
