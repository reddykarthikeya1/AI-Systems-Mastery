import React, { useState, useEffect } from 'react';
import { X, ArrowRight, GitFork, CheckCircle2, BookOpen, Layers, ShieldCheck, Cpu, Zap, Database, Network, ChevronRight } from 'lucide-react';
import { CourseSummary } from '../types';

interface PrerequisiteMapModalProps {
  isOpen: boolean;
  onClose: () => void;
  courses: CourseSummary[];
  currentCourseId?: string;
  onSelectCourse?: (courseId: string) => void;
}

interface TierInfo {
  tierNum: number;
  name: string;
  subtitle: string;
  color: string;
  bgGradient: string;
  borderColor: string;
  courses: {
    id: string;
    num: string;
    title: string;
    requires: string[];
    topics: string[];
    icon: React.ReactNode;
  }[];
}

const TIERS: TierInfo[] = [
  {
    tierNum: 1,
    name: 'Systems & Algorithmic Engineering',
    subtitle: 'High-performance computing, memory layout, storage engines & distributed systems',
    color: 'text-sky-500',
    bgGradient: 'from-sky-500/10 via-sky-500/5 to-transparent',
    borderColor: 'border-sky-500/30',
    courses: [
      {
        id: '01_Advanced_Python',
        num: 'Course 01',
        title: 'Advanced Python & Runtime Internals',
        requires: [],
        topics: ['CPython Bytecode', 'GIL & Concurrency', 'Memory Layout', 'Asyncio Event Loops'],
        icon: <Cpu className="w-4 h-4 text-sky-400" />,
      },
      {
        id: '02_Data_Structures_and_Algorithms',
        num: 'Course 02',
        title: 'High-Performance Algorithms & Structures',
        requires: ['C01'],
        topics: ['Segment Trees', 'Fenwick Trees', 'Dinic Max Flow', 'Tarjan SCC', 'Cache Locality'],
        icon: <GitFork className="w-4 h-4 text-sky-400" />,
      },
      {
        id: '03_Databases_and_Storage_Engines',
        num: 'Course 03',
        title: 'Database Internals & Storage Engines',
        requires: ['C01', 'C02'],
        topics: ['Slotted Pages', 'Buffer Pools', 'B+ Trees', 'LSM-Trees', '2PL & MVCC', 'WAL'],
        icon: <Database className="w-4 h-4 text-sky-400" />,
      },
      {
        id: '04_System_Design_and_Distributed_Systems',
        num: 'Course 04',
        title: 'Distributed Systems & Consensus',
        requires: ['C03'],
        topics: ['Raft Consensus', 'Vector Clocks', 'Consistent Hashing', 'Split-Brain Defense'],
        icon: <Layers className="w-4 h-4 text-sky-400" />,
      },
    ],
  },
  {
    tierNum: 2,
    name: 'Mathematical Foundations of AI',
    subtitle: 'Subspace geometry, spectral diagonalization, multivariate calculus & probability',
    color: 'text-amber-500',
    bgGradient: 'from-amber-500/10 via-amber-500/5 to-transparent',
    borderColor: 'border-amber-500/30',
    courses: [
      {
        id: '05_Mathematics_for_ML_and_AI',
        num: 'Course 05',
        title: 'Rigorous Mathematics for ML & AI',
        requires: ['C01'],
        topics: ['Subspace Projections', 'Eigenvectors & SVD', 'Lagrangian Optimization', 'Information Theory'],
        icon: <BookOpen className="w-4 h-4 text-amber-400" />,
      },
    ],
  },
  {
    tierNum: 3,
    name: 'Deep Learning & GPU Infrastructure',
    subtitle: 'CUDA kernels, shared memory bank conflicts, and multi-node training',
    color: 'text-violet-500',
    bgGradient: 'from-violet-500/10 via-violet-500/5 to-transparent',
    borderColor: 'border-violet-500/30',
    courses: [
      {
        id: '06_Deep_Learning_and_AI_Foundations',
        num: 'Course 06',
        title: 'Deep Learning & Neural Architectures',
        requires: ['C01', 'C05'],
        topics: ['Autograd Internals', 'Attention Mechanisms', 'Backpropagation', 'Loss Landscapes'],
        icon: <Cpu className="w-4 h-4 text-violet-400" />,
      },
      {
        id: '07_GPU_Programming_and_AI_Kernels',
        num: 'Course 07',
        title: 'GPU Programming & CUDA Kernels',
        requires: ['C02', 'C06'],
        topics: ['Warp Synchrony', 'SRAM Tiling', 'Bank Conflicts', 'Tensor Cores', 'FlashAttention'],
        icon: <Zap className="w-4 h-4 text-violet-400" />,
      },
      {
        id: '08_Distributed_Training_and_GPU_Infrastructure',
        num: 'Course 08',
        title: 'Distributed Training & Large Clusters',
        requires: ['C04', 'C07'],
        topics: ['ZeRO-1/2/3', 'FSDP', 'Tensor & Pipeline Parallelism', 'NCCL Ring AllReduce'],
        icon: <Layers className="w-4 h-4 text-violet-400" />,
      },
    ],
  },
  {
    tierNum: 4,
    name: 'Inference Engines, Agents & Safety',
    subtitle: 'PagedAttention, speculative decoding, multi-agent swarms & guardrails',
    color: 'text-emerald-500',
    bgGradient: 'from-emerald-500/10 via-emerald-500/5 to-transparent',
    borderColor: 'border-emerald-500/30',
    courses: [
      {
        id: '09_Inference_Systems_and_Serving_Engines',
        num: 'Course 09',
        title: 'Serving Engines & Low-Latency Inference',
        requires: ['C07', 'C08'],
        topics: ['PagedAttention', 'Continuous Batching', 'Speculative Decoding', 'FP8 Quantization'],
        icon: <Zap className="w-4 h-4 text-emerald-400" />,
      },
      {
        id: '10_Advanced_Retrieval_and_Context_Engineering',
        num: 'Course 10',
        title: 'Advanced Retrieval & Context Systems',
        requires: ['C03', 'C09'],
        topics: ['HNSW Vector Indexes', 'Hybrid Sparse/Dense Search', 'GraphRAG', 'Context Compression'],
        icon: <Database className="w-4 h-4 text-emerald-400" />,
      },
      {
        id: '11_Autonomous_Agents_and_Cognitive_Architectures',
        num: 'Course 11',
        title: 'Autonomous Cognitive Agents',
        requires: ['C01', 'C10'],
        topics: ['ReAct Loops', 'Tool Call Reflection', 'Plan-and-Solve', 'Multi-Agent Consensus'],
        icon: <Cpu className="w-4 h-4 text-emerald-400" />,
      },
      {
        id: '12_LLM_Evaluation_Science_and_Guardrails',
        num: 'Course 12',
        title: 'Evaluation Science & Production Guardrails',
        requires: ['C05', 'C11'],
        topics: ['LLM-as-a-Judge', 'Deterministic Rail Defense', 'Safety Sandboxing', 'Red-Teaming'],
        icon: <ShieldCheck className="w-4 h-4 text-emerald-400" />,
      },
    ],
  },
];

interface ModuleTrackNode {
  num: string;
  title: string;
  stage: 'Foundation' | 'Core' | 'Advanced' | 'Capstone';
  prereqs: string[];
  skills: string[];
}

const COURSE_MODULE_TRACKS: Record<string, ModuleTrackNode[]> = {
  '01_Advanced_Python': [
    { num: 'Mod 00', title: 'Environment & Tooling', stage: 'Foundation', prereqs: [], skills: ['Tooling', 'Virtualenvs', 'Ruff'] },
    { num: 'Mod 01', title: 'Python Fundamentals', stage: 'Foundation', prereqs: ['Mod 00'], skills: ['Type System', 'Memory Pointers'] },
    { num: 'Mod 02', title: 'Functions & Closures', stage: 'Core', prereqs: ['Mod 01'], skills: ['Scopes', 'Closures', 'LEGB Rule'] },
    { num: 'Mod 03', title: 'Data Structures', stage: 'Core', prereqs: ['Mod 01'], skills: ['Hash Tables', 'Collections', 'Layout'] },
    { num: 'Mod 04', title: 'Deep OOP', stage: 'Core', prereqs: ['Mod 02', 'Mod 03'], skills: ['MRO', 'Dunder Methods', 'Protocols'] },
    { num: 'Mod 05', title: 'Decorators & Generators', stage: 'Core', prereqs: ['Mod 02'], skills: ['Yield', 'Context Managers', 'Wrappers'] },
    { num: 'Mod 06', title: 'Error Handling', stage: 'Core', prereqs: ['Mod 04'], skills: ['Exception Trees', 'Structured Logging'] },
    { num: 'Mod 07', title: 'Files & Serialization', stage: 'Core', prereqs: ['Mod 03'], skills: ['Protobuf', 'Zero-Copy IO', 'JSON'] },
    { num: 'Mod 08', title: 'Testing & QA', stage: 'Core', prereqs: ['Mod 06'], skills: ['Pytest', 'Fixtures', 'Property Testing'] },
    { num: 'Mod 09', title: 'Threading & Multiprocessing', stage: 'Advanced', prereqs: ['Mod 04'], skills: ['GIL', 'IPC', 'Process Pools'] },
    { num: 'Mod 10', title: 'Asyncio Internals', stage: 'Advanced', prereqs: ['Mod 09'], skills: ['Event Loop', 'Coroutines', 'Tasks'] },
    { num: 'Mod 11', title: 'Sockets & HTTP', stage: 'Advanced', prereqs: ['Mod 10'], skills: ['TCP Sockets', 'HTTP/2', 'Transports'] },
    { num: 'Mod 12', title: 'Bytecode & Memory', stage: 'Advanced', prereqs: ['Mod 09'], skills: ['CPython Bytecode', 'GC Generations'] },
    { num: 'Mod 13', title: 'FastAPI Architecture', stage: 'Core', prereqs: ['Mod 10'], skills: ['ASGI Spec', 'Routing', 'Starlette'] },
    { num: 'Mod 14', title: 'Pydantic V2', stage: 'Core', prereqs: ['Mod 13'], skills: ['Rust Core', 'Schema Validation'] },
    { num: 'Mod 15', title: 'SQLAlchemy & Alembic', stage: 'Core', prereqs: ['Mod 13'], skills: ['Unit of Work', 'Async Session', 'Migrations'] },
    { num: 'Mod 16', title: 'Auth & Security', stage: 'Advanced', prereqs: ['Mod 13'], skills: ['OAuth2', 'JWT Signatures', 'RBAC'] },
    { num: 'Mod 17', title: 'WebSockets & DI', stage: 'Advanced', prereqs: ['Mod 13', 'Mod 16'], skills: ['Real-Time Frames', 'Dependency Tree'] },
    { num: 'Mod 18', title: 'Distributed Task Queues', stage: 'Advanced', prereqs: ['Mod 10', 'Mod 11'], skills: ['Celery', 'Redis Streams', 'Brokers'] },
    { num: 'Mod 19', title: 'Docker & CI/CD', stage: 'Core', prereqs: ['Mod 00'], skills: ['Multi-Stage', 'BuildKit', 'Pipelines'] },
    { num: 'Mod 20', title: 'Profiling & Caching', stage: 'Advanced', prereqs: ['Mod 12'], skills: ['cProfile', 'L1/L2 Cache', 'Flamegraphs'] },
    { num: 'Mod 21', title: 'Metaprogramming & Descriptors', stage: 'Advanced', prereqs: ['Mod 04', 'Mod 12'], skills: ['Descriptors', 'Metaclasses', '__slots__'] },
    { num: 'Mod 22', title: 'PyO3 Rust Extensions', stage: 'Advanced', prereqs: ['Mod 12', 'Mod 21'], skills: ['PyO3 FFI', 'Rust C-Ext', 'Zero-Cost'] },
    { num: 'Mod 23', title: 'Strict Typing & Packaging', stage: 'Advanced', prereqs: ['Mod 01'], skills: ['MyPy', 'PEP 561', 'Wheel Publishing'] },
    { num: 'Mod 24', title: 'Polars & Playwright', stage: 'Advanced', prereqs: ['Mod 10'], skills: ['Arrow IPC', 'Vectorized Query', 'Headless'] },
    { num: 'Mod 25', title: 'LLM Agent Integration', stage: 'Advanced', prereqs: ['Mod 10', 'Mod 13'], skills: ['Streaming Tokens', 'Function Calling'] },
    { num: 'Mod 26', title: 'Enterprise Capstone', stage: 'Capstone', prereqs: ['Mod 13', 'Mod 18', 'Mod 25'], skills: ['Production Gateway', 'Distributed State'] },
  ],
  '02_Data_Structures_and_Algorithms': [
    { num: 'Mod 01', title: 'Complexity & Memory Layout', stage: 'Foundation', prereqs: [], skills: ['Big-O', 'Cache Lines', 'Hardware Prefetch'] },
    { num: 'Mod 02', title: 'Arrays & Two Pointers', stage: 'Foundation', prereqs: ['Mod 01'], skills: ['Sliding Window', 'Two Pointers', 'Amortization'] },
    { num: 'Mod 03', title: 'Linked Lists & Pointers', stage: 'Foundation', prereqs: ['Mod 01'], skills: ['Floyd Cycle', 'Pointer Reversal', 'Sentinel'] },
    { num: 'Mod 04', title: 'Stacks, Queues & Monotonic', stage: 'Foundation', prereqs: ['Mod 02'], skills: ['Monotonic Stack', 'Deque Window'] },
    { num: 'Mod 05', title: 'Hash Tables & Collision', stage: 'Foundation', prereqs: ['Mod 02'], skills: ['Robin Hood Hash', 'Open Addressing', 'Chaining'] },
    { num: 'Mod 06', title: 'Binary Trees & BSTs', stage: 'Core', prereqs: ['Mod 03'], skills: ['AVL Rotation', 'Red-Black Invariants', 'Inorder'] },
    { num: 'Mod 07', title: 'Heaps & Priority Queues', stage: 'Core', prereqs: ['Mod 02'], skills: ['Binary Heap', 'Top-K Elements', 'K-Way Merge'] },
    { num: 'Mod 08', title: 'Graph Traversals & DAGs', stage: 'Core', prereqs: ['Mod 06'], skills: ['Tarjan SCC', 'Kahn Toposort', 'Bipartite'] },
    { num: 'Mod 09', title: 'Shortest Paths & MST', stage: 'Core', prereqs: ['Mod 07', 'Mod 08'], skills: ['Dijkstra', 'Bellman-Ford', 'Kruskal MST'] },
    { num: 'Mod 10', title: '1D Dynamic Programming', stage: 'Advanced', prereqs: ['Mod 02'], skills: ['Optimal Substructure', 'LIS', 'State Transition'] },
    { num: 'Mod 11', title: '2D DP & Knapsack', stage: 'Advanced', prereqs: ['Mod 10'], skills: ['0/1 Knapsack', 'Grid Paths', 'LCS Matrix'] },
    { num: 'Mod 12', title: 'Greedy & Intervals', stage: 'Core', prereqs: ['Mod 02'], skills: ['Interval Scheduling', 'Huffman Codes', 'Exchange'] },
    { num: 'Mod 13', title: 'Backtracking & Pruning', stage: 'Advanced', prereqs: ['Mod 08'], skills: ['N-Queens', 'Sudoku Bitmask', 'State Pruning'] },
    { num: 'Mod 14', title: 'Trie, Union-Find & Segment', stage: 'Advanced', prereqs: ['Mod 06'], skills: ['Segment Tree', 'Lazy Propagation', 'Disjoint Set'] },
    { num: 'Mod 15', title: 'SkipLists & Bloom Filters', stage: 'Advanced', prereqs: ['Mod 05'], skills: ['Probabilistic Layers', 'Counting Bloom', 'LRU'] },
    { num: 'Mod 16', title: 'String Matching & KMP', stage: 'Advanced', prereqs: ['Mod 02'], skills: ['KMP Table', 'Rabin-Karp Rolling Hash', 'Z-Algorithm'] },
    { num: 'Mod 17', title: 'Network Flow & Dinic', stage: 'Capstone', prereqs: ['Mod 08', 'Mod 09'], skills: ['Dinic Blocking Flow', 'Residual Graph', 'Bipartite'] },
  ],
  '03_Databases_and_Storage_Engines': [
    { num: 'Mod 01-05', title: 'Storage Engines & Relational Core', stage: 'Foundation', prereqs: [], skills: ['Slotted Pages', 'Buffer Pools', 'SQLite WAL', 'Postgres MVCC'] },
    { num: 'Mod 06-10', title: 'Enterprise Engines & Documents', stage: 'Core', prereqs: ['Mod 01-05'], skills: ['InnoDB Log', 'Oracle SGA', 'PL/SQL', '2PC', 'BSON Engine'] },
    { num: 'Mod 11-15', title: 'Sharding, Caching & Distributed LSM', stage: 'Core', prereqs: ['Mod 06-10'], skills: ['Shard Keys', 'Redis Ziplist', 'CRC16 Cluster', 'Cassandra Ring', 'LSM SSTables'] },
    { num: 'Mod 16-20', title: 'Specialized Engines & Vectors', stage: 'Advanced', prereqs: ['Mod 11-15'], skills: ['Cypher Graph', 'DuckDB Columnar', 'SCD-2 Pipelines', 'Lucene BM25', 'IVF Vector DB'] },
    { num: 'Mod 21-25', title: 'Internals, Concurrency & Capstone', stage: 'Capstone', prereqs: ['Mod 16-20'], skills: ['B+ Tree Splits', 'Cost-Based Optimizer', 'Strict 2PL', 'PITR Recovery', 'Polyglot CDC'] },
  ],
  '04_System_Design_and_Distributed_Systems': [
    { num: 'Mod 00-06', title: 'System Scalability Foundations', stage: 'Foundation', prereqs: [], skills: ['Capacity Math', 'Little\'s Law', 'Sliding Window', 'CDN Edge', 'Least-Conn', 'SOLID', 'Circuit Breakers'] },
    { num: 'Mod 07-13', title: 'Distributed Primitives & Streaming', stage: 'Core', prereqs: ['Mod 00-06'], skills: ['Elevator SCAN', 'Debt Simplification', 'Consistent Hashing', 'Snowflake IDs', 'XFetch', 'Count-Min', 'Consumer Groups'] },
    { num: 'Mod 14-20', title: 'High-Scale Industry Architectures', stage: 'Advanced', prereqs: ['Mod 07-13'], skills: ['TinyURL Base62', 'Discord Presence', 'Feed Fanout', 'Uber Geohash', 'HLS Slicing', 'SimHash Dedup', 'Flash Sale Inventory'] },
    { num: 'Mod 21-26', title: 'Consensus, Serving & Capstone', stage: 'Capstone', prereqs: ['Mod 14-20'], skills: ['HNSW SkipList', 'vLLM PagedAttention', 'Saga Rollback', 'Raft Election', 'W3C Traces', 'Idempotent Payment'] },
  ],
  '05_Mathematics_for_ML_and_AI': [
    { num: 'Mod 01-04', title: 'Set Theory & Linear Vector Spaces', stage: 'Foundation', prereqs: [], skills: ['Jaccard Similarity', '2-SAT Logic', 'Gaussian Elimination', 'Gram-Schmidt'] },
    { num: 'Mod 05-08', title: 'Spectral Geometry & Low-Rank SVD', stage: 'Core', prereqs: ['Mod 01-04'], skills: ['Power Iteration', 'Orthogonal Projections', 'Rank-1 SVD', 'Ridge Regression'] },
    { num: 'Mod 09-12', title: 'Calculus, Uncertainty & Estimation', stage: 'Advanced', prereqs: ['Mod 05-08'], skills: ['Armijo Line Search', 'Bayes Updates', 'Sample Covariance', 'Bootstrap CIs'] },
  ],
  '06_Deep_Learning_and_AI_Foundations': [
    { num: 'Mod 01-04', title: 'Foundational Tensors & Computational Graphs', stage: 'Foundation', prereqs: [], skills: ['Stable Softmax', 'BCE Loss', 'Strided Broadcasting', 'Graph Toposort'] },
    { num: 'Mod 05-08', title: 'Neural Architectures & Transformers', stage: 'Core', prereqs: ['Mod 01-04'], skills: ['2-Layer MLP Backprop', 'Causal Attention Mask', 'Bellman Q-Learning', 'RoPE Embeddings'] },
    { num: 'Mod 09-12', title: 'Empirical NLP, LoRA & Production MLOps', stage: 'Advanced', prereqs: ['Mod 05-08'], skills: ['BLEU Clipped Precision', 'LoRA Weight Merge', 'PSI Drift Detector', 'Beam Search'] },
  ],
  '07_GPU_Programming_and_AI_Kernels': [
    { num: 'Mod 01-04', title: 'SIMT Hardware, Indexing & Scans', stage: 'Foundation', prereqs: [], skills: ['Warp Divergence', 'Linear Grid Index', 'Coalesced Memory', 'Blelloch Scan'] },
    { num: 'Mod 05-08', title: 'Tiled SRAM GEMM & FlashAttention', stage: 'Core', prereqs: ['Mod 01-04'], skills: ['Shared Memory Tiling', 'Triton Block Masks', 'Fused LayerNorm', 'Online Softmax Rescaling'] },
    { num: 'Mod 09-11', title: 'Hopper TMA, Quantization & Roofline', stage: 'Advanced', prereqs: ['Mod 05-08'], skills: ['TMA Async Double Buffering', 'INT8 Quantization', 'Roofline Intensity'] },
  ],
  '08_Distributed_Training_and_GPU_Infrastructure': [
    { num: 'Mod 01-04', title: 'Interconnects, NCCL & ZeRO Sharding', stage: 'Foundation', prereqs: [], skills: ['NVLink Bandwidth', 'Ring AllReduce', 'DDP Bucketing', 'ZeRO-1/2/3 Footprint'] },
    { num: 'Mod 05-07', title: 'Megatron Tensor, Pipeline & Ring Parallelism', stage: 'Core', prereqs: ['Mod 01-04'], skills: ['Column-Row Parallel', '1F1B Schedule', 'RingAttention P2P'] },
    { num: 'Mod 08-10', title: '3D Parallelism, Checkpointing & Scaling Laws', stage: 'Capstone', prereqs: ['Mod 05-07'], skills: ['3D Rank Grid', 'DCP Shard Merge', 'Chinchilla Frontier'] },
  ],
  '09_Inference_Systems_and_Serving_Engines': [
    { num: 'Mod 01-03', title: 'Serving SLAs, KV Footprint & Paging', stage: 'Foundation', prereqs: [], skills: ['TTFT/TBT SLA', 'KV Cache Bytes', 'PagedAttention Block Table'] },
    { num: 'Mod 04-06', title: 'Radix Prefix & Continuous Batching', stage: 'Core', prereqs: ['Mod 01-03'], skills: ['Radix Common Prefix', 'Iteration Scheduler', 'Chunked Prefill Slicing'] },
    { num: 'Mod 07-09', title: 'Speculative Sampling, FP8 & Autoscaling', stage: 'Advanced', prereqs: ['Mod 04-06'], skills: ['Rejection Sampler', 'FP8 Scaled Dequant', 'Concurrency Queue HPA'] },
  ],
  '10_Advanced_Retrieval_and_Context_Engineering': [
    { num: 'Mod 01-03', title: 'Parsing, Contextual Chunks & Vectors', stage: 'Foundation', prereqs: [], skills: ['Recursive Splitting', 'Summary Prepending', 'Cosine Similarity'] },
    { num: 'Mod 04-06', title: 'Hybrid RRF, Cross-Encoders & ColBERT', stage: 'Core', prereqs: ['Mod 01-03'], skills: ['Reciprocal Rank Fusion', 'Reranker Thresholding', 'MaxSim Operator'] },
    { num: 'Mod 07-09', title: 'GraphRAG, HyDE & Needle-In-Haystack', stage: 'Advanced', prereqs: ['Mod 04-06'], skills: ['Entity Subgraph', 'HyDE Synthesis', 'NIAH Context Evaluation'] },
  ],
  '11_Autonomous_Agents_and_Cognitive_Architectures': [
    { num: 'Mod 01-03', title: 'ReAct Loops, LangGraph & Schema Tools', stage: 'Foundation', prereqs: [], skills: ['Thought-Action Parser', 'State Reducer', 'JSON Schema Validation'] },
    { num: 'Mod 04-06', title: 'Memory Buffers, Multi-Agent & Sandboxes', stage: 'Core', prereqs: ['Mod 01-03'], skills: ['Buffer Window Summary', 'Supervisor Swarm', 'AST Code Sandbox'] },
    { num: 'Mod 07-08', title: 'Time Travel Checkpoints & Trajectory Eval', stage: 'Capstone', prereqs: ['Mod 04-06'], skills: ['Checkpoint History Fork', 'Trajectory Accuracy Metric'] },
  ],
  '12_LLM_Evaluation_Science_and_Guardrails': [
    { num: 'Mod 01-03', title: 'Exact Match/F1, Judge Debiasing & MMLU', stage: 'Foundation', prereqs: [], skills: ['Exact Match & F1', 'Position Bias Swap', 'Multiple Choice Accuracy'] },
    { num: 'Mod 04-06', title: 'PII Redaction, Safety Policies & Injection', stage: 'Core', prereqs: ['Mod 01-03'], skills: ['Regex PII Redaction', 'Dialogue Policy Filter', 'Prompt Injection Detection'] },
    { num: 'Mod 07-08', title: 'Red-Teaming Fuzzing & OTel Observability', stage: 'Capstone', prereqs: ['Mod 04-06'], skills: ['Adversarial Mutation Fuzzer', 'OTel Span Duration Aggregator'] },
  ],
};

export const PrerequisiteMapModal: React.FC<PrerequisiteMapModalProps> = ({
  isOpen,
  onClose,
  courses,
  currentCourseId,
  onSelectCourse,
}) => {
  const [activeTab, setActiveTab] = useState<'curriculum' | 'modules'>('curriculum');
  const [selectedTrackCourse, setSelectedTrackCourse] = useState<string>(
    currentCourseId || '01_Advanced_Python'
  );

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const currentTrackNodes = COURSE_MODULE_TRACKS[selectedTrackCourse] || COURSE_MODULE_TRACKS['01_Advanced_Python'];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200"
      role="dialog"
      aria-modal="true"
      aria-labelledby="prereq-map-title"
    >
      <div className="w-full max-w-5xl max-h-[90vh] flex flex-col rounded-3xl bg-zinc-900 border border-zinc-800 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="px-6 py-4 border-b border-zinc-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-zinc-900/90 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <GitFork className="w-5 h-5" />
            </div>
            <div>
              <h2 id="prereq-map-title" className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                <span>Curriculum Dependency Map</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-400 font-mono font-medium">
                  4 Tiers • 12 Courses • 175 Modules
                </span>
              </h2>
              <p className="text-xs text-zinc-400">
                Architectural progression path from low-level systems engineering to autonomous cognitive models.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 self-end sm:self-auto">
            {/* View Mode Switcher */}
            <div className="flex items-center p-0.5 rounded-xl bg-zinc-800/90 border border-zinc-700/60 text-xs font-medium">
              <button
                onClick={() => setActiveTab('curriculum')}
                className={`px-3 py-1 rounded-lg transition ${
                  activeTab === 'curriculum'
                    ? 'bg-sky-500 text-white shadow-sm'
                    : 'text-zinc-400 hover:text-white'
                }`}
              >
                Course Roadmap
              </button>
              <button
                onClick={() => setActiveTab('modules')}
                className={`px-3 py-1 rounded-lg transition ${
                  activeTab === 'modules'
                    ? 'bg-sky-500 text-white shadow-sm'
                    : 'text-zinc-400 hover:text-white'
                }`}
              >
                Module Tracks
              </button>
            </div>

            <button
              className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-zinc-800 transition"
              onClick={onClose}
              aria-label="Close prerequisite roadmap"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-8 select-text">
          {activeTab === 'curriculum' ? (
            /* 4 Tiers Curriculum View */
            TIERS.map((tier) => (
              <div
                key={tier.tierNum}
                className={`rounded-2xl border ${tier.borderColor} bg-gradient-to-r ${tier.bgGradient} p-5 space-y-4`}
              >
                {/* Tier Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-zinc-800/80 pb-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-mono font-bold uppercase tracking-wider ${tier.color}`}>
                        Tier {tier.tierNum}
                      </span>
                      <span className="text-zinc-600 dark:text-zinc-400">•</span>
                      <h3 className="text-sm sm:text-base font-bold text-white">
                        {tier.name}
                      </h3>
                    </div>
                    <p className="text-xs text-zinc-400 mt-0.5">
                      {tier.subtitle}
                    </p>
                  </div>
                  <span className="text-[11px] font-mono text-zinc-400 shrink-0">
                    {tier.courses.length} Course{tier.courses.length > 1 ? 's' : ''}
                  </span>
                </div>

                {/* Course Nodes in this tier */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                  {tier.courses.map((c) => {
                    const isCurrent = currentCourseId === c.id;
                    const matchingCourse = courses.find((item) => item.id === c.id);
                    const moduleCount = matchingCourse ? matchingCourse.module_count : 12;

                    return (
                      <div
                        key={c.id}
                        onClick={() => {
                          if (onSelectCourse) {
                            onSelectCourse(c.id);
                            onClose();
                          }
                        }}
                        className={`group p-4 rounded-xl border transition-all cursor-pointer flex flex-col justify-between gap-3 ${
                          isCurrent
                            ? 'border-sky-500 bg-sky-500/10 shadow-lg shadow-sky-500/10 ring-1 ring-sky-500'
                            : 'border-zinc-800 bg-zinc-900/80 hover:border-zinc-700 hover:bg-zinc-800/60'
                        }`}
                      >
                        <div className="space-y-2">
                          {/* Course header */}
                          <div className="flex items-start justify-between gap-2">
                            <div className="flex items-center gap-2">
                              <div className="p-1.5 rounded-lg bg-zinc-800 group-hover:bg-zinc-700 transition">
                                {c.icon}
                              </div>
                              <span className="text-xs font-mono font-bold text-zinc-400">
                                {c.num}
                              </span>
                            </div>

                            {c.requires.length > 0 ? (
                              <div className="flex items-center gap-1 text-[10px] font-mono text-amber-400/90 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                                <span>Req:</span>
                                <span>{c.requires.join(', ')}</span>
                              </div>
                            ) : (
                              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                                Foundational Entry
                              </span>
                            )}
                          </div>

                          {/* Title */}
                          <h4 className="text-sm font-bold text-white group-hover:text-sky-400 transition">
                            {c.title}
                          </h4>

                          {/* Topics tags */}
                          <div className="flex flex-wrap gap-1.5 pt-1">
                            {c.topics.map((t) => (
                              <span
                                key={t}
                                className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-800/80 text-zinc-300 border border-zinc-700/50"
                              >
                                {t}
                              </span>
                            ))}
                          </div>
                        </div>

                        {/* Footer */}
                        <div className="pt-2 border-t border-zinc-800/60 flex items-center justify-between text-xs text-zinc-400">
                          <span className="font-mono text-[11px]">
                            {moduleCount} Modules
                          </span>
                          <span className="flex items-center gap-1 text-sky-400 font-medium group-hover:translate-x-1 transition-transform">
                            <span>{isCurrent ? 'Current' : 'Jump to Course'}</span>
                            <ArrowRight className="w-3.5 h-3.5" />
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))
          ) : (
            /* Module-by-Module Prerequisite Tracks View */
            <div className="space-y-6">
              {/* Course Selector Tabs */}
              <div className="flex flex-wrap gap-2 pb-2 border-b border-zinc-800">
                {Object.keys(COURSE_MODULE_TRACKS).map((cId) => {
                  const isSelected = selectedTrackCourse === cId;
                  const cTitle = cId.replace(/^\d+_/, '').replace(/_/g, ' ');
                  return (
                    <button
                      key={cId}
                      onClick={() => setSelectedTrackCourse(cId)}
                      className={`text-xs px-3 py-1.5 rounded-xl border transition ${
                        isSelected
                          ? 'bg-sky-500 text-white border-sky-400 font-semibold shadow-md shadow-sky-500/20'
                          : 'bg-zinc-800/70 border-zinc-700/60 text-zinc-400 hover:text-white hover:bg-zinc-800'
                      }`}
                    >
                      {cTitle}
                    </button>
                  );
                })}
              </div>

              {/* Course Track Header */}
              <div className="flex items-center justify-between bg-zinc-800/40 p-4 rounded-2xl border border-zinc-800">
                <div>
                  <h3 className="text-sm sm:text-base font-bold text-white flex items-center gap-2">
                    <span>{selectedTrackCourse.replace(/_/g, ' ')}</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20 font-mono">
                      {currentTrackNodes.length} Step Track
                    </span>
                  </h3>
                  <p className="text-xs text-zinc-400 mt-1">
                    Linear dependency progression from conceptual primitives to production-grade architecture.
                  </p>
                </div>
                <button
                  onClick={() => {
                    if (onSelectCourse) {
                      onSelectCourse(selectedTrackCourse);
                      onClose();
                    }
                  }}
                  className="px-4 py-2 rounded-xl bg-sky-500 hover:bg-sky-400 text-white font-medium text-xs flex items-center gap-1.5 transition"
                >
                  <span>Open Course</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Flowchart / Step-by-Step Module Nodes */}
              <div className="space-y-3">
                {currentTrackNodes.map((mod, idx) => {
                  const stageColors = {
                    Foundation: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
                    Core: 'text-sky-400 bg-sky-500/10 border-sky-500/20',
                    Advanced: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
                    Capstone: 'text-violet-400 bg-violet-500/10 border-violet-500/20',
                  }[mod.stage];

                  return (
                    <div
                      key={mod.num}
                      className="p-4 rounded-2xl bg-zinc-900 border border-zinc-800 hover:border-zinc-700 transition flex flex-col sm:flex-row sm:items-center justify-between gap-3 group"
                    >
                      <div className="flex items-start sm:items-center gap-3">
                        <div className="w-8 h-8 rounded-xl bg-zinc-800 border border-zinc-700/60 flex items-center justify-center font-mono text-xs font-bold text-zinc-300 shrink-0 group-hover:border-sky-500/50 group-hover:text-sky-400 transition">
                          {idx + 1}
                        </div>
                        <div>
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="font-mono text-xs font-bold text-sky-400">
                              {mod.num}
                            </span>
                            <span className="text-zinc-600 dark:text-zinc-400">•</span>
                            <h4 className="text-sm font-semibold text-white group-hover:text-sky-300 transition">
                              {mod.title}
                            </h4>
                            <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${stageColors}`}>
                              {mod.stage}
                            </span>
                          </div>

                          <div className="flex items-center gap-1.5 pt-1.5 flex-wrap">
                            {mod.skills.map((skill) => (
                              <span
                                key={skill}
                                className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-800/80 text-zinc-300 border border-zinc-700/50"
                              >
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0 self-start sm:self-auto">
                        {mod.prereqs.length > 0 ? (
                          <span className="text-[11px] font-mono text-amber-400/90 bg-amber-500/10 px-2 py-1 rounded border border-amber-500/20 flex items-center gap-1">
                            <span>Requires:</span>
                            <span className="font-semibold">{mod.prereqs.join(', ')}</span>
                          </span>
                        ) : (
                          <span className="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20">
                            Entry Module
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Footer info */}
        <div className="px-6 py-3.5 border-t border-zinc-800 bg-zinc-900/90 flex items-center justify-between text-xs text-zinc-400">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>All courses verified with reproducible test suites, algorithmic problem banks, and trace execution scrubbers.</span>
          </div>
          <button
            className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-1.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white font-medium text-xs transition"
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
