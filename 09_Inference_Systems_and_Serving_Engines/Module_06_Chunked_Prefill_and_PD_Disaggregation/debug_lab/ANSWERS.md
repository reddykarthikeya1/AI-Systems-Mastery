# Debug Lab Solution & Forensic Post-Mortem

## Incident: Decode Node Generates From a Truncated Prompt

---

### Forensic Root Cause Analysis
`prefill_worker_send()` maps each chunk to a transfer slot with
`chunk_id % NUM_TRANSFER_SLOTS` and then overwrites that slot's dict entry:

```python
for chunk_id, chunk in enumerate(chunks):
    slot = chunk_id % NUM_TRANSFER_SLOTS
    transfer_bus[slot] = (chunk_id, chunk)  # last write to a slot wins
```

With `NUM_TRANSFER_SLOTS = 2` and 4 chunks, chunk 0 and chunk 2 both hash to
slot 0, and chunk 1 and chunk 3 both hash to slot 1. Each later chunk's write
simply clobbers the earlier chunk that shared its slot -- there is no
"slot is still occupied, wait or drain first" check, no acknowledgment from
the decode side that it has consumed a slot before it gets reused, and no
buffering of more than one chunk per slot. By the time
`decode_worker_receive()` reads `transfer_bus`, chunks 0 and 1 have already
been overwritten by chunks 2 and 3, so the decode node reconstructs only the
tail of the prompt (`"dog near the river bank ."`) and silently generates a
completion as if that were the entire input.

---

### Production Corrective Action & Code Fix

```python
def prefill_worker_send(chunks, transfer_bus):
    for chunk_id, chunk in enumerate(chunks):
        # Every chunk gets a durable, unique key -- a transfer slot is
        # reclaimed only after the decode side has acknowledged consuming it,
        # never reused purely because chunk_id wrapped around.
        transfer_bus[chunk_id] = (chunk_id, chunk)
```

(In a real PD-disaggregated deployment, the double-buffering optimization
this lab models is legitimate -- a slot may be pipelined and reused -- but
only after the decode node acknowledges it has drained that slot's KV data.
Reusing a slot purely by `chunk_id % NUM_TRANSFER_SLOTS` with no
backpressure or ack is the defect.) With the fix, all 4 chunks land in
distinct entries and `decode_worker_receive()` reassembles the full 14-token
prompt in order.

---

### Production Prevention Invariants
1. **Never Reuse a Buffer Slot Without an Ack:** Any pipelined transfer
   (network, ring buffer, double buffer) must confirm the consumer has read
   a slot before a producer is allowed to overwrite it.
2. **Round-Trip Token Count Assertion:** The decode node should assert the
   number of tokens (or chunks) it reassembled equals what the prefill node
   reports having sent, and fail loudly on a mismatch instead of silently
   generating from a partial context.
3. **Test With Chunk Count Exceeding Slot Count:** PD-disaggregation tests
   must include prompts long enough to produce more chunks than transfer
   slots -- the bug is invisible whenever chunk count stays at or below the
   slot count.
