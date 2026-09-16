"""Broken memory store with memory leak and no scoring balance."""

class BrokenMemoryStore:
    def __init__(self):
        self.memories = []

    def add_memory(self, content):
        # BUG: Unlimited growth causing unbounded prompt explosion
        self.memories.append(content)

    def retrieve(self, query):
        # BUG: Returns entire memory array without relevance or recency ranking
        return self.memories
