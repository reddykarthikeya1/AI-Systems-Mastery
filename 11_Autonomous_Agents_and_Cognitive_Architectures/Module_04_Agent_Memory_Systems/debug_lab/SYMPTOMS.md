# Debug Lab Incident Report: Agent Memory Store Grows Without Bound and Buries the One Relevant Fact at the End of the List

- **Severity:** P2 Context Window Exhaustion / Cost
- **Affected Subsystem:** Module_04_Agent_Memory_Systems
- **Reported Impact:** After a few hundred turns of an ongoing conversation, prompt construction started ballooning toward the model's context limit. Even when it fit, retrieval returned so much irrelevant history that the one fact the assistant actually needed was diluted among hundreds of unrelated entries instead of being surfaced first.

---

## 🚨 Observable Symptoms & Logs
```text
Conversation turns so far: 501
Memories held in the store: 501
Memories returned by retrieve() for a single-fact query: 501
Position of the actually-relevant memory in the returned list: 500 of 500
Characters that would be stuffed into the next LLM prompt: 28313
```
After 501 conversation turns, the store holds 501 memories -- one for every turn, with nothing ever pruned or summarized. Querying `retrieve()` for a specific fact ("what is the user's favorite color?") returns all 501 memories rather than a shortlist, and the one memory that actually answers the query sits at the very last position of the returned list, indistinguishable in priority from the 500 unrelated small-talk entries in front of it. Assembling a prompt from this output would require over 28,000 characters for a single-fact lookup.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_04_Agent_Memory_Systems/debug_lab
   ```
2. `broken_memory.py` only defines `BrokenMemoryStore`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_memory import BrokenMemoryStore

   store = BrokenMemoryStore()
   for i in range(500):
       store.add_memory(f"turn {i}: user made small talk about unrelated topic #{i}")
   store.add_memory("the user's favorite color is teal")

   results = store.retrieve("what is the user's favorite color?")
   relevant_index = results.index("the user's favorite color is teal")
   prompt_chars = sum(len(m) for m in results)

   print("Conversation turns so far: 501")
   print(f"Memories held in the store: {len(store.memories)}")
   print(f"Memories returned by retrieve() for a single-fact query: {len(results)}")
   print(f"Position of the actually-relevant memory in the returned list: {relevant_index} of {len(results) - 1}")
   print(f"Characters that would be stuffed into the next LLM prompt: {prompt_chars}")
   ```
3. Observe that the number of memories returned always equals the total number stored (nothing is filtered), and that the relevant memory's position in the list is determined purely by when it was added, not by its relevance to the query.

---

## 🎯 Your Objective
1. Inspect `add_memory()` -- is there any cap on how many memories can accumulate, or any eviction/summarization?
2. Inspect `retrieve()` -- does it filter or rank memories against `query` at all, or hand back everything unconditionally?
3. Formulate a hypothesis for what happens to prompt size and retrieval precision as a conversation grows to thousands of turns, then check `ANSWERS.md`.
