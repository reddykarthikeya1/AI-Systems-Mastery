# 🐣 Interactive Foundations Playground: PagedAttention Architecture (vLLM)

> *"PagedAttention treats GPU memory like virtual memory pages: non-contiguous blocks eliminate memory waste."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Virtual Memory Block Mapping

PagedAttention groups tokens into fixed-size physical blocks (e.g. 16 tokens), mapping logical sequence positions to physical block IDs.

```python
block_size = 16
logical_token_index = 37

logical_block_num = logical_token_index // block_size
block_offset = logical_token_index % block_size

assert logical_block_num == 2  # Block 2
assert block_offset == 5       # 5th token in block 2
assert logical_block_num * block_size + block_offset == 37
print(f"Token {logical_token_index} maps to Block {logical_block_num}, Offset {block_offset}.")
```

---

## 2. Zero Internal Fragmentation Invariant

Standard static allocation reserves maximum sequence length (e.g. 4096), wasting 60-80% memory on short responses.

```python
max_seq_len = 4096
actual_tokens = 150
static_waste = (max_seq_len - actual_tokens) / max_seq_len
paged_blocks_used = math.ceil(actual_tokens / block_size)  # 10 blocks = 160 slots
paged_waste = (paged_blocks_used * block_size - actual_tokens) / (paged_blocks_used * block_size)

assert static_waste > 0.90
assert paged_waste < 0.10
print(f"Memory waste: Static reservation={static_waste:.1%}, PagedAttention={paged_waste:.1%}")
```

---

## 3. Copy-On-Write Fork for Parallel Sampling

When generating multiple samples from one prompt, child streams share prompt physical blocks with reference count > 1.

```python
block_ref_counts = {101: 1}
# Fork 2 sampling branches
block_ref_counts[101] += 2

assert block_ref_counts[101] == 3, "Prompt block shared by parent and 2 child streams"
print(f"Physical block 101 shared with ref_count={block_ref_counts[101]}; zero redundant prompt memory.")
```

---
