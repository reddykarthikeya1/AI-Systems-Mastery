# Beginner Playground - Distributed LLM Serving and PagedAttention

> *"A hotel that reserves a whole floor for every guest in case they bring forty friends. Most arrive alone, the hotel shows as full, and the rooms are empty."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 1. What the KV cache is, and why it dominates memory

Generating each token requires attending to every previous token. Recomputing that
each time would be quadratic, so the intermediate keys and values are cached - the
**KV cache**.

It grows with every token generated, and it is per request. On a busy server the
KV cache, not the model weights, is what you run out of.

```python
KV_BYTES_PER_TOKEN = 800_000          # a realistic figure for a mid-size model
MAX_CONTEXT = 2_048
GPU_MEMORY = 40_000_000_000           # 40 GB

full_reservation = MAX_CONTEXT * KV_BYTES_PER_TOKEN
print(f"reserving the full context costs {full_reservation / 1e9:.2f} GB per request")
assert full_reservation > 1e9
```

---

## 2. Reserve for the worst case and you waste the common case

The simple allocator gives every request its maximum possible context up front,
because the cache has to be contiguous and you cannot know how long the answer
will be.

Most requests use a fraction of it. The rest is reserved, untouchable, and idle.

```python
REQUEST_LENGTHS = [120, 200, 340, 150, 90, 600, 210, 180]

contiguous_slots = GPU_MEMORY // full_reservation
reserved = len(REQUEST_LENGTHS) * full_reservation
actually_used = sum(REQUEST_LENGTHS) * KV_BYTES_PER_TOKEN
waste = 1 - actually_used / reserved

print(f"concurrent requests that fit: {contiguous_slots}")
print(f"memory reserved: {reserved / 1e9:>6.2f} GB")
print(f"memory used:     {actually_used / 1e9:>6.2f} GB")
print(f"wasted:          {waste:.0%}")
assert waste > 0.8, "most of the most expensive memory in the building is idle"
```

---

## 3. Pages: allocate in small blocks, on demand

Stop reserving. Hand out fixed-size **blocks** of 16 tokens as the sequence
actually grows, and keep a table mapping the logical sequence to its scattered
physical blocks.

This is virtual memory, applied to a GPU. The blocks need not be adjacent, so the
only waste left is the unused part of the final block - at most 15 tokens instead
of nearly 2,000.

```python
BLOCK_TOKENS = 16


def blocks_for(tokens):
    return -(-tokens // BLOCK_TOKENS)      # ceiling division


paged_bytes = sum(blocks_for(n) * BLOCK_TOKENS for n in REQUEST_LENGTHS)
paged_bytes *= KV_BYTES_PER_TOKEN
paged_waste = 1 - actually_used / paged_bytes

print(f"paged allocation uses {paged_bytes / 1e9:.2f} GB for the same 8 requests")
print(f"wasted: {paged_waste:.1%} (only the tail of each last block)")
assert paged_waste < 0.05, "internal fragmentation is now under 5%"
assert paged_bytes < reserved / 8, "8x less memory for identical work"
```

---

## 4. The payoff: how many requests fit at once

Throughput on an LLM server is decided by how many sequences you can keep in
flight. Free the wasted memory and the batch size rises, which is a several-fold
throughput gain from an allocator change.

```python
average_tokens = sum(REQUEST_LENGTHS) / len(REQUEST_LENGTHS)
contiguous_capacity = GPU_MEMORY // full_reservation
paged_capacity = GPU_MEMORY // (blocks_for(average_tokens) * BLOCK_TOKENS
                                * KV_BYTES_PER_TOKEN)

print(f"contiguous allocation: {contiguous_capacity:>4} concurrent sequences")
print(f"paged allocation:      {paged_capacity:>4} concurrent sequences")
print(f"improvement: {paged_capacity / contiguous_capacity:.1f}x")
assert paged_capacity > contiguous_capacity * 5
print("Same GPU, same model, same weights. Different allocator.")
```

---

## 5. Continuous batching, the other half of the win

Static batching waits for every sequence in a batch to finish before starting the
next. One long generation holds up fifteen short ones.

**Continuous batching** evicts a sequence the moment it emits its stop token and
admits a waiting request into the free slot. Combined with paging, the GPU stops
idling on both memory and compute.

```python
batch = [5, 5, 5, 100]                      # tokens left to generate
waiting = [5, 5, 5]

static_steps = max(batch)
print(f"static batching: {static_steps} steps, "
      f"and 3 slots idle for {static_steps - 5} of them")

slots = list(batch)
queue = list(waiting)
steps = 0
while any(slots) or queue:
    steps += 1
    for i, remaining in enumerate(slots):
        if remaining > 0:
            slots[i] -= 1
        elif queue:
            slots[i] = queue.pop(0) - 1
    if not queue and not any(slots):
        break

static_for_everything = static_steps + max(waiting)
print(f"continuous batching: {steps} steps for all {len(batch) + len(waiting)} requests")
print(f"static batching would need {static_for_everything} steps for the same seven")
assert steps < static_for_everything, "the waiting requests fitted into the idle gaps"
```

---

## 6. Predict before you run

A model can hold 2,048 tokens of context. You reserve that much memory for
every request, but the average conversation is 200 tokens. What fraction of
your very expensive GPU memory is doing nothing?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

This is the observation behind vLLM. Treating GPU memory like operating
system virtual memory - small pages, allocated on demand - raised serving
throughput several-fold without touching the model at all.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
