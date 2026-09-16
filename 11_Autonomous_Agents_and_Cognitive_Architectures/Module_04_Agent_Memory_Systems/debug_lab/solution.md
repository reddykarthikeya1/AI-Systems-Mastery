# Debug Lab Solution: Memory Bloat Bug

### The Defect
`BrokenMemoryStore` appends all past events to a flat list without bounding working memory or scoring memories by relevance and recency.

### The Fix
Implement bounded working memory and multi-factor episodic retrieval as shown in `project_solution/agent_memory_manager.py`.
