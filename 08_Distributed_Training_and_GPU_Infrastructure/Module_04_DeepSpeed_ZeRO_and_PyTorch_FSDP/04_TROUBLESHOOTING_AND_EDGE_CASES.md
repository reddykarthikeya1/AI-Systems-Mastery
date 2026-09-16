# Module 04: Troubleshooting & Edge Cases

## 1. Top 5 Production Failure Modes in FSDP / ZeRO

### Bug 1: Deadlock from Conditional Modules / MoE Routing
- **Symptom**: Training hangs indefinitely at a specific forward layer without throwing an error. GPU utilization drops to 0%.
- **Root Cause**: In ZeRO-3/FSDP, every rank must execute the forward pass of every wrapped submodule in the exact same order to participate in the collective `All-Gather`. If an Expert module in a Mixture of Experts (MoE) network receives 0 tokens on Rank 3, Rank 3 skips that module while Ranks 0–2 execute it. Ranks 0–2 block waiting for Rank 3's NCCL contribution forever.
- **Fix**: Never wrap conditional or dynamically skipped submodules with individual FSDP wrappers. Wrap the parent router module, or ensure dummy inputs are routed to ensure collective consensus.

### Bug 2: `gradient_as_bucket_view=True` Corruption
- **Symptom**: Loss NaN or training diverges after 100 steps when using custom gradient clipping or optimizer hooks.
- **Root Cause**: When `gradient_as_bucket_view=True`, gradient tensors are non-owning views into the underlying communication bucket buffer. Modifying or reallocating gradients in an in-place fashion invalidates the bucket layout.
- **Fix**: Use standard PyTorch gradient clipping (`torch.nn.utils.clip_grad_norm_`) or pass `gradient_as_bucket_view=False` if custom gradient manipulations are required.

### Bug 3: Memory Spike from Missing `auto_wrap_policy`
- **Symptom**: Wrapping a model with `FSDP(model)` without an `auto_wrap_policy` yields no memory reduction compared to DDP.
- **Root Cause**: If no inner submodules are wrapped, FSDP treats the entire network as a single atomic unit. It shards the parameters at rest, but before the forward pass, it `All-Gather`s the ENTIRE model into memory at once!
- **Fix**: Always specify a transformer layer wrapping policy:
  ```python
  from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
  from my_model import TransformerBlock

  auto_wrap = functools.partial(
      transformer_auto_wrap_policy,
      transformer_layer_cls={TransformerBlock}
  )
  ```
