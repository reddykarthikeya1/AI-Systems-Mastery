# 🐣 Interactive Foundations Playground: Tries & Union-Find

> *"A Trie is Google Search's autocomplete: as you type 'c', 'a', 't', it follows letters down a branch."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---


## Segment Tree Binary Range Decomposition

```mermaid
flowchart TD
    R["[0..7] Sum: 36"]
    R --> L1["[0..3] Sum: 16"]
    R --> R1["[4..7] Sum: 20"]

    L1 --> L2A["[0..1] Sum: 7"]
    L1 --> L2B["[2..3] Sum: 9"]
    R1 --> R2A["[4..5] Sum: 9"]
    R1 --> R2B["[6..7] Sum: 11"]

    L2A --> L3A["[0]: 3"]
    L2A --> L3B["[1]: 4"]
    L2B --> L3C["[2]: 2"]
    L2B --> L3D["[3]: 7"]
    R2A --> R3A["[4]: 1"]
    R2A --> R3B["[5]: 8"]
    R2B --> R3C["[6]: 5"]
    R2B --> R3D["[7]: 6"]
```

## 1. How Disjoint Sets (Union-Find) Work
Imagine islands in an ocean. Whenever someone builds a bridge between two islands, you merge their teams. If two islands are already in the same team and you build another bridge, **that bridge is redundant (creates a loop)!**