# Design Rationale: Resilient Parallel Thumbnail Processing Pipeline

## Architectural Overview
A dual-concurrency batch processing engine that pipelines I/O-bound disk fetching with CPU-bound image resizing and hashing using threads, processes, and IPC queues.

## Key Design Decisions
1. **Process Pools for CPU Work:** Image scaling and cryptographic hashing run inside `ProcessPoolExecutor`, bypassing the Global Interpreter Lock to achieve true multi-core parallel scaling.
2. **Bounded IPC Queues for Backpressure:** Inter-process queues enforce maximum capacities (`maxsize=100`), preventing memory saturation when producers outpace consumer workers.
3. **Strict Entrypoint Guarding:** Worker execution is strictly enclosed in `if __name__ == '__main__':`, preventing recursive Windows `spawn` fork-bomb loops.

## Rejected Alternatives
1. **Using `threading.Thread` for Image Resizing:**
   - *Reason for Rejection:* Because CPython's GIL serializes bytecode execution, 4 CPU threads achieve 1.0x scaling and actually run slower due to mutex contention.
2. **Unbounded Message Queues:**
   - *Reason for Rejection:* Ingesting 50,000 images without queue size limits buffers gigabytes of raw byte arrays into RAM, crashing the host OS.

## Invariants & Guarantees
- Multi-core CPU scaling scales linearly across available physical cores.
- Worker process crashes are caught and reported without stalling the pipeline.

## Verification
```bash
pytest test_pipeline.py -v
```
