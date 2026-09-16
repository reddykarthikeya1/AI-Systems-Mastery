# Self-Assessment & Staff Interview Challenges: Distributed Data Parallel

## Architectural Interview Scenarios

### Question 1: Unused Parameters in DDP
**Scenario**: In a multi-modal model, an image encoder is skipped for text-only samples. When training with PyTorch DDP, the training run hangs indefinitely. Why?

**Staff-Level Solution**:
DDP expects every registered parameter to fire its backward autograd hook in each step.
A bucket only issues AllReduce when its parameter counter reaches 0.
If the image encoder was skipped in the forward pass, its parameters receive no gradient and their hooks never fire!
The bucket waits forever, causing a cluster-wide distributed deadlock!
**Fix**:
1. Set `find_unused_parameters=True` in `DistributedDataParallel` (traverses graph to mark unused params, small CPU overhead).
2. Or better: partition the model cleanly or wrap unused submodules with `torch.no_grad()`.
