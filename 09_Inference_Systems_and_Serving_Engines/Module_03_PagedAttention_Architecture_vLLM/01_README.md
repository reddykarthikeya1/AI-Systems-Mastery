# Module 03: PagedAttention Architecture (vLLM)


## PagedAttention Virtual Memory Block Table (vLLM)

```mermaid
flowchart LR
    subgraph Logical["Logical KV Cache (Contiguous per Request)"]
        L0["Block 0 (Tokens 0-15)"]
        L1["Block 1 (Tokens 16-31)"]
        L2["Block 2 (Tokens 32-47)"]
    end

    subgraph Table["Block Table (Page Table)"]
        BT0["Logical 0 -> Physical 7"]
        BT1["Logical 1 -> Physical 3"]
        BT2["Logical 2 -> Physical 12"]
    end

    subgraph Physical["Physical GPU DRAM Pages (Non-Contiguous)"]
        P3["Physical Block 3"]
        P7["Physical Block 7"]
        P12["Physical Block 12"]
    end

    L0 --> BT0 --> P7
    L1 --> BT1 --> P3
    L2 --> BT2 --> P12
```

---

## 1. Systems Architecture of PagedAttention

PagedAttention (Kwon et al., SOSP 2023) partitions the KV cache into fixed-size physical blocks that are mapped dynamically to logical token sequences via per-sequence block tables.

### 1.1 Core Data Structures
1. **Physical Block**: A contiguous memory buffer capable of storing key and value vectors for $B$ tokens (typically $B=16$ or $B=32$):
   $$\text{Block Size (bytes)} = 2 \times P \times L \times H_{\text{kv}} \times d_{\text{head}} \times B$$
2. **Block Table**: An integer array for each active sequence mapping logical block index $\lfloor i / B \rfloor$ to physical block ID:
   $$\text{PhysicalBlockID} = \text{BlockTable}\left[\left\lfloor \frac{i}{B} \right\rfloor\right]$$
   $$\text{SlotOffset} = i \pmod B$$
3. **Free Block Manager**: A free-list tracking unallocated physical block indices on the GPU.

---

## 2. Copy-on-Write (CoW) Mechanics

For decoding strategies that branch (e.g. beam search, parallel sampling, tree-of-thought):
- Multiple sequence forks point to the same physical blocks for shared prefixes.
- Each physical block maintains a **reference count** (`ref_count`).
- When Sequence $A$ appends a new token to a shared block:
  - If `ref_count > 1`, a new physical block is allocated, the content is copied (**Copy-on-Write**), `ref_count` of the original block is decremented, and Sequence $A$'s block table is updated.
  - If `ref_count == 1`, write occurs in-place.

```
Initial Shared State:
Sequence A: -> [Physical Block 4 (ref=2)]
Sequence B: -> [Physical Block 4 (ref=2)]

After Sequence A Appends Divergent Token (Copy-on-Write):
Sequence A: -> [Physical Block 9 (ref=1)] (New private block)
Sequence B: -> [Physical Block 4 (ref=1)] (Original block retained)
```