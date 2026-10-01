# Recommended Reading - Distributed Training and GPU Infrastructure

Written explainers (official docs, university notes, standard references, well-known engineering blogs) for every module concept.
Each page was fetched and its text read by a script that checks the page actually names the concepts listed under `Covers`.
Use these when a video is not enough or you prefer text; then do the module exercises.

### Module 01: GPU Cluster Hardware & Interconnects

- [NVIDIA Hopper Architecture In-Depth | NVIDIA Technical Blog](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/) | **developer.nvidia.com** | Covers: GPU Cluster Hardware, Interconnects
- [InfiniBand - Wikipedia](https://en.wikipedia.org/wiki/InfiniBand) | **en.wikipedia.org** | Covers: GPU Cluster Hardware, Interconnects
- [NVLink & NVLink Switch: Fastest HPC Data Center Platform | NVIDIA](https://www.nvidia.com/en-us/data-center/nvlink/) | **nvidia.com** | Covers: Interconnects
- [NVLink - Wikipedia](https://en.wikipedia.org/wiki/NVLink) | **en.wikipedia.org** | Covers: Interconnects

### Module 02: NCCL Collective Communication Primitives

- [Collective Operations — NCCL 2.32.3 documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html) | **docs.nvidia.com** | Covers: NCCL Collective Communication Primitives
- [NVIDIA Collective Communication Library (NCCL) Documentation — NCCL 2.32.3 documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html) | **docs.nvidia.com** | Covers: NCCL Collective Communication Primitives
- [NVIDIA Collective Communications Library (NCCL) | NVIDIA Developer](https://developer.nvidia.com/nccl) | **developer.nvidia.com** | Covers: NCCL Collective Communication Primitives
- [Distributed communication package - torch.distributed — PyTorch 2.14 documentation](https://docs.pytorch.org/docs/2.14/distributed.html) | **pytorch.org** | Covers: NCCL Collective Communication Primitives

### Module 03: PyTorch Distributed Data Parallel (DDP)

- [Getting Started with Distributed Data Parallel — PyTorch Tutorials 2.14.0+cu130 documentation](https://docs.pytorch.org/tutorials/intermediate/ddp_tutorial.html) | **pytorch.org** | Covers: PyTorch Distributed Data Parallel, DDP
- [Distributed Data Parallel — PyTorch 2.14 documentation](https://docs.pytorch.org/docs/2.14/notes/ddp.html) | **pytorch.org** | Covers: PyTorch Distributed Data Parallel, DDP
- [Distributed Data Parallel in PyTorch - Video Tutorials — PyTorch Tutorials 2.14.0+cu130 documentatio](https://docs.pytorch.org/tutorials/beginner/ddp_series_intro.html) | **pytorch.org** | Covers: PyTorch Distributed Data Parallel, DDP

### Module 04: DeepSpeed ZeRO & PyTorch FSDP

- [Zero Redundancy Optimizer - DeepSpeed](https://www.deepspeed.ai/tutorials/zero/) | **deepspeed.ai** | Covers: DeepSpeed ZeRO
- [Getting Started with Fully Sharded Data Parallel (FSDP2) — PyTorch Tutorials 2.14.0+cu130 documentat](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html) | **pytorch.org** | Covers: PyTorch FSDP
- [FSDP2 · Hugging Face](https://huggingface.co/docs/transformers/main/en/fsdp) | **huggingface.co** | Covers: DeepSpeed ZeRO

### Module 05: Tensor Parallelism (Megatron-LM)

- [The Technology Behind BLOOM Training](https://huggingface.co/blog/bloom-megatron-deepspeed) | **huggingface.co** | Covers: Tensor Parallelism, Megatron-LM
- [[1909.08053] Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism](https://arxiv.org/abs/1909.08053) | **arxiv.org** | Covers: Megatron-LM
- [Parallelism methods · Hugging Face](https://huggingface.co/docs/transformers/perf_train_gpu_many) | **huggingface.co** | Covers: Tensor Parallelism
- [Large Scale Transformer model training with Tensor Parallel (TP) — PyTorch Tutorials 2.14.0+cu130 do](https://docs.pytorch.org/tutorials/intermediate/TP_tutorial.html) | **pytorch.org** | Covers: Tensor Parallelism

### Module 06: Pipeline Parallelism (1F1B Schedules)

- [Pipeline Parallelism — PyTorch 2.14 documentation](https://docs.pytorch.org/docs/2.14/distributed.pipelining.html) | **pytorch.org** | Covers: Pipeline Parallelism, 1F1B Schedules
- [Pipeline-Parallelism: Distributed Training via Model Partitioning](https://siboehm.com/articles/22/pipeline-parallel-training) | **siboehm.com** | Covers: Pipeline Parallelism, 1F1B Schedules
- [Pipeline Parallel | Colossal-AI](https://colossalai.org/docs/features/pipeline_parallel/) | **colossalai.org** | Covers: Pipeline Parallelism, 1F1B Schedules
- [[1811.06965] GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism](https://arxiv.org/abs/1811.06965) | **arxiv.org** | Covers: Pipeline Parallelism
- [[2104.04473] Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM](https://arxiv.org/abs/2104.04473) | **arxiv.org** | Covers: Pipeline Parallelism

### Module 07: Sequence Parallelism & Ring Attention

- [Ring Attention Explained | Coconut Mode](https://coconut-mode.com/posts/ring-attention/) | **coconut-mode.com** | Covers: Sequence Parallelism, Ring Attention
- [[2310.01889] Ring Attention with Blockwise Transformers for Near-Infinite Context](https://arxiv.org/abs/2310.01889) | **arxiv.org** | Covers: Ring Attention

### Module 08: 3D Parallelism Integration & Orchestration

- [Parallelism methods · Hugging Face](https://huggingface.co/docs/transformers/perf_train_gpu_many) | **huggingface.co** | Covers: 3D Parallelism Integration

### Module 09: Distributed Checkpointing & Fault Tolerance

- [Getting Started with Distributed Checkpoint (DCP) — PyTorch Tutorials 2.14.0+cu130 documentation](https://docs.pytorch.org/tutorials/recipes/distributed_checkpoint_recipe.html) | **pytorch.org** | Covers: Distributed Checkpointing
- [torchrun (Elastic Launch) — PyTorch 2.14 documentation](https://docs.pytorch.org/docs/2.14/elastic/run.html) | **pytorch.org** | Covers: Fault Tolerance
- [Distributed Checkpoint - torch.distributed.checkpoint — PyTorch 2.14 documentation](https://docs.pytorch.org/docs/2.14/distributed.checkpoint.html) | **pytorch.org** | Covers: Distributed Checkpointing
- [Fault-tolerant Distributed Training with torchrun — PyTorch Tutorials 2.14.0+cu130 documentation](https://docs.pytorch.org/tutorials/beginner/ddp_series_fault_tolerance.html) | **docs.pytorch.org** | Covers: Fault Tolerance

### Module 10: Scaling Laws, Cluster Profiling & FinOps

- [[2001.08361] Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) | **arxiv.org** | Covers: Scaling Laws
- [FinOps Foundation - What is FinOps?](https://www.finops.org/introduction/what-is-finops/) | **finops.org** | Covers: FinOps
- [PyTorch Profiler — PyTorch Tutorials 2.14.0+cu130 documentation](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html) | **pytorch.org** | Covers: Cluster Profiling
