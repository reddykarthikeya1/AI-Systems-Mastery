# Module 03: Beginner Playground - PagedAttention Architecture (vLLM)

Welcome to **PagedAttention**!
In 2023, researchers at UC Berkeley asked a simple question:
*"Operating systems solved memory fragmentation 50 years ago using virtual memory paging. Why are AI serving systems still allocating giant contiguous blocks like MS-DOS in 1982?"*

Their answer was **PagedAttention** (the core engine behind **vLLM**), and it transformed the AI industry overnight!

---

## 1. The OS Virtual Memory Metaphor

In modern operating systems:
- A program thinks it has a clean, continuous memory space ($0 \dots 4\text{ GB}$).
- In reality, physical RAM is chopped into tiny **4 KB Pages** scattered all over the motherboard!
- The CPU uses a **Page Table** to translate virtual addresses to physical pages.

```
Logical Request Tokens:
[ Token 0 - 15 ] [ Token 16 - 31 ] [ Token 32 - 47 ]
       |                 |                  |
       v                 v                  v
  (Block Table)     (Block Table)      (Block Table)
       |                 |                  |
       v                 v                  v
[Physical Block 9] [Physical Block 2] [Physical Block 14]
(Scattered anywhere in GPU HBM!)
```

---

## 2. Why PagedAttention is a Superpower

1. **Near-Zero Memory Waste (< 4%)**:
   Instead of pre-allocating for 8,192 tokens, we only allocate a new 16-token physical block **when the 17th token is generated**!
   The only waste is the unused slots in the final block!
2. **Copy-on-Write (Parallel Sampling & Beam Search)**:
   Suppose a user asks: *"Write 4 different poems based on this 2,000-word story."*
   In traditional serving, that 2,000-word prompt's KV cache is duplicated 4 times ($4\times$ memory)!
   In PagedAttention, all 4 responses **point to the exact same physical blocks for the prompt**!
   Only when they generate divergent tokens do they allocate their own private blocks!
