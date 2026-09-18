"""Broken memory store with memory leak and no scoring balance."""

class BrokenMemoryStore:
    def __init__(self):
        self.memories = []

    def add_memory(self, content):
        self.memories.append(content)

    def retrieve(self, query):
        return self.memories


def reproduce_defect():
    print("Simulating 501 conversation turns against BrokenMemoryStore...")
    store = BrokenMemoryStore()
    for i in range(500):
        store.add_memory(f"turn {i}: user made small talk about unrelated topic #{i}")
    store.add_memory("the user's favorite color is teal")

    results = store.retrieve("what is the user's favorite color?")
    relevant_index = results.index("the user's favorite color is teal")
    prompt_chars = sum(len(m) for m in results)

    print("Conversation turns so far: 501")
    print("Expected memories returned for a single-fact query: a small, ranked top-k shortlist")
    print(f"Actual memories held in the store: {len(store.memories)}")
    print(f"Actual memories returned by retrieve(): {len(results)}")
    print(f"Position of the actually-relevant memory in the returned list: {relevant_index} of {len(results) - 1}")
    print(f"Characters that would be stuffed into the next LLM prompt: {prompt_chars}")


if __name__ == "__main__":
    reproduce_defect()
