/**
 * Curated Glossary of Fundamental AI, Systems Engineering, and Algorithmic Concepts.
 * Provides concise, precise, staff-level definitions displayed on first-occurrence tooltips.
 */

export interface GlossaryEntry {
  term: string;
  definition: string;
  category: 'Systems' | 'AI & ML' | 'Algorithms' | 'Distributed Systems' | 'Databases';
  aliases?: string[];
}

export const GLOSSARY: Record<string, GlossaryEntry> = {
  // --- DISTRIBUTED SYSTEMS & DATABASES ---
  wal: {
    term: 'Write-Ahead Logging (WAL)',
    definition:
      'A persistence pattern where mutation intents are append-logged to durable storage before modifying in-memory data structures. Guarantees Atomicity and Durability across system crashes.',
    category: 'Databases',
    aliases: ['write-ahead log', 'write ahead log', 'wal'],
  },
  linearizability: {
    term: 'Linearizability',
    definition:
      'The strongest single-object consistency model: every read operation returns the result of the most recent write in real-world wall-clock time, creating the illusion of a single centralized copy.',
    category: 'Distributed Systems',
    aliases: ['linearizable', 'linearizability'],
  },
  serializability: {
    term: 'Serializability',
    definition:
      'The highest multi-transaction isolation level: guarantees that concurrent transaction execution yields outcomes identical to some purely sequential execution order.',
    category: 'Databases',
    aliases: ['serializable', 'serializability'],
  },
  'two-phase locking': {
    term: 'Two-Phase Locking (2PL)',
    definition:
      'A concurrency control protocol with a growing phase (locks acquired) and shrinking phase (locks released). Guarantees serializability by preventing interleavings that cause serializability violations.',
    category: 'Databases',
    aliases: ['2pl', 'two-phase locking', '2-phase locking'],
  },
  'raft quorum': {
    term: 'Raft Quorum',
    definition:
      'A strict majority of cluster nodes (⌊N/2⌋ + 1) required to elect a leader and commit log entries. Guarantees that any two quorums overlap by at least one node, preventing split-brain.',
    category: 'Distributed Systems',
    aliases: ['quorum', 'raft quorum', 'majority quorum'],
  },
  'split-brain': {
    term: 'Split-Brain',
    definition:
      'A critical failure state in distributed systems where a network partition isolates sub-clusters, each erroneously believing itself to be the active leader and accepting mutually conflicting writes.',
    category: 'Distributed Systems',
    aliases: ['split brain', 'split-brain'],
  },
  'vector clock': {
    term: 'Vector Clock',
    definition:
      'An array of logical clocks maintained across distributed nodes to capture causal relationships between events without relying on synchronized wall-clock time.',
    category: 'Distributed Systems',
    aliases: ['vector clocks', 'vector clock'],
  },
  'consistent hashing': {
    term: 'Consistent Hashing',
    definition:
      'A partitioning scheme mapping keys and nodes onto a circular keyspace ring. Minimizes key re-allocation to K/N when nodes join or leave a cluster.',
    category: 'Distributed Systems',
    aliases: ['consistent hash', 'consistent hashing'],
  },
  'merkle tree': {
    term: 'Merkle Tree',
    definition:
      'A cryptographic hash tree where non-leaf nodes contain cryptographic hashes of child nodes. Enables efficient, secure verification of data structure synchronization in distributed replicas.',
    category: 'Distributed Systems',
    aliases: ['merkle trees', 'merkle tree'],
  },
  'circuit breaker': {
    term: 'Circuit Breaker',
    definition:
      'A design pattern that detects repeated service failures and temporarily trips open to reject requests immediately, shielding degraded downstream services from cascading collapse.',
    category: 'Distributed Systems',
    aliases: ['circuit breakers', 'circuit breaker'],
  },
  'buffer pool': {
    term: 'Buffer Pool',
    definition:
      'An in-memory cache of database disk pages managed via frame tables and eviction policies (e.g. 2Q, LRU-K). Bridges the latency gap between memory and persistent block storage.',
    category: 'Databases',
    aliases: ['buffer pool', 'buffer cache', 'buffer pool manager'],
  },
  'slotted page': {
    term: 'Slotted Page',
    definition:
      'A page layout format where slot pointers grow forward from the page header while tuple payloads grow backward from the page footer, maximizing storage efficiency for variable-length records.',
    category: 'Databases',
    aliases: ['slotted page', 'slotted pages'],
  },
  'lsm-tree': {
    term: 'Log-Structured Merge-tree (LSM)',
    definition:
      'A write-optimized storage architecture buffering writes sequentially in memory (memtable) and periodically flushing sorted immutables (SSTables) to disk, consolidated via background compaction.',
    category: 'Databases',
    aliases: ['lsm', 'lsm tree', 'lsm-tree', 'log-structured merge'],
  },
  compaction: {
    term: 'SSTable Compaction',
    definition:
      'The background merge-sort process in LSM-trees that consolidates overlapping immutable files, purges deleted tombstones, and bounds read amplification.',
    category: 'Databases',
    aliases: ['compaction', 'sstable compaction'],
  },

  // --- HARDWARE, MEMORY & SYSTEMS ARCHITECTURE ---
  'false sharing': {
    term: 'False Sharing',
    definition:
      'A multi-core performance degradation occurring when independent threads modify distinct variables located on the same CPU cache line (typically 64 bytes), triggering invalidation ping-pong.',
    category: 'Systems',
    aliases: ['false sharing'],
  },
  'cache line': {
    term: 'Cache Line',
    definition:
      'The fundamental unit of data transfer between main memory and CPU cache hierarchies, conventionally standardized to 64 contiguous bytes.',
    category: 'Systems',
    aliases: ['cache lines', 'cache line'],
  },
  simd: {
    term: 'Single Instruction, Multiple Data (SIMD)',
    definition:
      'A parallel computing capability executing a single instruction simultaneously across vector registers containing multiple packed data elements (e.g. AVX-512, NEON).',
    category: 'Systems',
    aliases: ['simd', 'vectorization'],
  },
  tlb: {
    term: 'Translation Lookaside Buffer (TLB)',
    definition:
      'A high-speed hardware cache on the CPU that stores recent virtual-to-physical memory address translations, minimizing page-table traversal penalties.',
    category: 'Systems',
    aliases: ['tlb', 'translation lookaside buffer'],
  },
  backpressure: {
    term: 'Backpressure',
    definition:
      'A reactive flow-control mechanism signaling an upstream producer to throttle production rate when downstream consumers cannot sustain processing throughput, preventing buffer overflows.',
    category: 'Systems',
    aliases: ['backpressure', 'back-pressure'],
  },

  // --- GPU, KERNELS & DISTRIBUTED TRAINING ---
  warp: {
    term: 'GPU Warp',
    definition:
      'The fundamental execution unit in NVIDIA GPU hardware consisting of 32 parallel threads executed synchronously in lock-step under SIMT (Single Instruction, Multiple Threads).',
    category: 'AI & ML',
    aliases: ['warp', 'gpu warp', 'warps'],
  },
  'shared memory': {
    term: 'GPU Shared Memory',
    definition:
      'On-chip scratchpad SRAM shared among threads in a CUDA thread block. Has 100x lower latency than global DRAM, enabling efficient inter-thread communication and kernel tiling.',
    category: 'AI & ML',
    aliases: ['shared memory', 'gpu shared memory', 'sram'],
  },
  'bank conflict': {
    term: 'Shared Memory Bank Conflict',
    definition:
      'A GPU hardware stall occurring when multiple threads within the same warp simultaneously request distinct memory addresses mapped to the identical shared memory bank (typically 32 banks).',
    category: 'AI & ML',
    aliases: ['bank conflict', 'bank conflicts'],
  },
  'tensor core': {
    term: 'Tensor Core',
    definition:
      'Specialized mixed-precision matrix multiply-accumulate hardware units on modern GPUs capable of executing 4x4 or 16x16 matrix math in a single clock cycle (e.g. FP16/BF16/FP8).',
    category: 'AI & ML',
    aliases: ['tensor core', 'tensor cores'],
  },
  flashattention: {
    term: 'FlashAttention',
    definition:
      'An IO-aware exact attention algorithm that tiles computation across fast on-chip SRAM to avoid materializing the massive $N \\times N$ intermediate attention matrix in slow GPU HBM.',
    category: 'AI & ML',
    aliases: ['flashattention', 'flash attention', 'flash-attention'],
  },
  'kv cache': {
    term: 'KV Cache',
    definition:
      'A memory-saving inference technique storing previous key and value attention tensors across autoregressive generation steps, avoiding redundant $O(N^2)$ recomputation for earlier tokens.',
    category: 'AI & ML',
    aliases: ['kv cache', 'key-value cache', 'kv caching'],
  },
  pagedattention: {
    term: 'PagedAttention',
    definition:
      'An attention memory management architecture inspired by virtual memory paging that allocates KV cache in non-contiguous physical memory blocks, eliminating internal and external fragmentation.',
    category: 'AI & ML',
    aliases: ['pagedattention', 'paged attention'],
  },
  'speculative decoding': {
    term: 'Speculative Decoding',
    definition:
      'An inference acceleration technique employing a lightweight draft model to speculate $K$ prospective tokens in parallel, validated in a single forward pass by the larger target model.',
    category: 'AI & ML',
    aliases: ['speculative decoding', 'speculative sampling'],
  },
  'continuous batching': {
    term: 'Continuous Batching (Iteration-Level)',
    definition:
      'A dynamic serving scheduler that inserts newly arrived requests and retires completed requests at every forward token step, eliminating idle bubbles caused by variable sequence lengths.',
    category: 'AI & ML',
    aliases: ['continuous batching', 'iteration-level batching'],
  },
  lora: {
    term: 'Low-Rank Adaptation (LoRA)',
    definition:
      'A parameter-efficient fine-tuning method that freezes base model weights $W_0$ and injects trainable low-rank decomposition matrices $\\Delta W = B \\cdot A$ (where rank $r \\ll d$).',
    category: 'AI & ML',
    aliases: ['lora', 'low-rank adaptation', 'peft'],
  },
  quantization: {
    term: 'Model Quantization',
    definition:
      'The mapping of continuous high-precision floating-point weights and activations (FP32/FP16) to low-bitwidth integers (INT8/INT4/FP8) to reduce memory footprint and memory bandwidth bottlenecks.',
    category: 'AI & ML',
    aliases: ['quantization', 'quantized', 'int8 quantization', 'int4'],
  },
  'gradient checkpointing': {
    term: 'Gradient Checkpointing (Activation Recomputation)',
    definition:
      'A memory-for-compute trade-off that drops intermediate activation tensors during the forward pass and recomputes them during backpropagation, reducing activation memory from $O(N)$ to $O(\\sqrt{N})$.',
    category: 'AI & ML',
    aliases: ['gradient checkpointing', 'activation checkpointing'],
  },
  zero: {
    term: 'ZeRO (Zero Redundancy Optimizer)',
    definition:
      'A memory optimization paradigm that shards optimizer states (ZeRO-1), gradients (ZeRO-2), and model parameters (ZeRO-3) across data-parallel ranks, eliminating duplicate redundant storage.',
    category: 'AI & ML',
    aliases: ['zero', 'zero-3', 'zero redundancy optimizer', 'fsdp'],
  },
  rope: {
    term: 'Rotary Position Embedding (RoPE)',
    definition:
      'A relative positional encoding method that rotates query and key representations in the complex plane, preserving relative distance dependencies naturally via inner products.',
    category: 'AI & ML',
    aliases: ['rope', 'rotary positional embedding', 'rotary embeddings'],
  },

  // --- DATA STRUCTURES & ADVANCED ALGORITHMS ---
  'fenwick tree': {
    term: 'Fenwick Tree (Binary Indexed Tree)',
    definition:
      'An implicit tree array data structure supporting $O(\\log n)$ prefix sum queries and point updates by isolating lowset set bits via $i \\ \\& \\ (-i)$ bitwise operations.',
    category: 'Algorithms',
    aliases: ['fenwick tree', 'fenwick', 'binary indexed tree', 'bit'],
  },
  'segment tree': {
    term: 'Segment Tree',
    definition:
      'A binary tree structure where each node stores aggregated associative metrics (sum, min, max, gcd) over a contiguous range, supporting range queries and updates in $O(\\log n)$ time.',
    category: 'Algorithms',
    aliases: ['segment tree', 'segment trees'],
  },
  'disjoint set union': {
    term: 'Disjoint Set Union (DSU / Union-Find)',
    definition:
      'A near-constant time $O(\\alpha(n))$ partition tracker combining path compression and union-by-rank to maintain connected component memberships across dynamic edge additions.',
    category: 'Algorithms',
    aliases: ['dsu', 'union find', 'union-find', 'disjoint set'],
  },
  'dinic algorithm': {
    term: 'Dinic’s Algorithm',
    definition:
      'A maximum flow algorithm running in $O(V^2 E)$ time by iteratively constructing a BFS level graph and routing blocking flows along admissible edges via DFS.',
    category: 'Algorithms',
    aliases: ['dinic', "dinic's", 'dinic algorithm'],
  },
  'residual graph': {
    term: 'Residual Graph',
    definition:
      'An auxiliary directed graph indicating remaining forward capacities and backward cancelable flows in a network, enabling flow augmentations without violating conservation invariants.',
    category: 'Algorithms',
    aliases: ['residual graph', 'residual network'],
  },
  'topological sort': {
    term: 'Topological Sort',
    definition:
      'A linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge $u \\to v$, vertex $u$ comes before $v$ in the ordering.',
    category: 'Algorithms',
    aliases: ['topological sort', 'topological ordering'],
  },
  'bloom filter': {
    term: 'Bloom Filter',
    definition:
      'A space-efficient probabilistic data structure that tests set membership with zero false negatives and tunable false positives using multiple hash functions over a compact bit array.',
    category: 'Algorithms',
    aliases: ['bloom filter', 'bloom filters'],
  },
};

/**
 * Finds known glossary terms occurring in plain text.
 */
export function findGlossaryTerms(text: string): { term: string; entry: GlossaryEntry }[] {
  const found: { term: string; entry: GlossaryEntry }[] = [];
  const lower = text.toLowerCase();

  for (const [key, entry] of Object.entries(GLOSSARY)) {
    const searchTerms = [entry.term.toLowerCase(), ...(entry.aliases || []).map((a) => a.toLowerCase())];
    for (const st of searchTerms) {
      if (lower.includes(st)) {
        found.push({ term: st, entry });
        break;
      }
    }
  }

  return found;
}
