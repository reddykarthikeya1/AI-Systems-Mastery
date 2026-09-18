import React, { useState } from 'react';
import { X, Cpu, Layers, Terminal } from 'lucide-react';

interface HardwareTopologyModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface MemoryTier {
  id: string;
  name: string;
  capacity: string;
  latencyNs: number;
  bandwidth: string;
  description: string;
  usedIn: string;
  hardwareLevel: 'SM-Local' | 'On-Chip' | 'On-Device' | 'Interconnect' | 'Cluster';
}

const MEMORY_TIERS: MemoryTier[] = [
  {
    id: 'regs',
    name: 'Registers (RF)',
    capacity: '64 - 128 KB / SM',
    latencyNs: 0.5,
    bandwidth: '~30 TB/s aggregate',
    description: 'Ultra-fast per-thread private storage directly inside execution units.',
    usedIn: 'Warp execution, accumulator states, immediate operands.',
    hardwareLevel: 'SM-Local',
  },
  {
    id: 'smem',
    name: 'Shared Memory / L1 (SRAM)',
    capacity: '100 - 228 KB / SM',
    latencyNs: 1.5,
    bandwidth: '15 - 20 TB/s',
    description: 'Software-managed user-addressable SRAM scratchpad shared across threads in a thread block.',
    usedIn: 'FlashAttention tiling Q/K/V blocks, matrix multiply tiles (GEMM), block reductions.',
    hardwareLevel: 'SM-Local',
  },
  {
    id: 'l2',
    name: 'L2 Cache',
    capacity: '50 - 128 MB on-chip',
    latencyNs: 8.0,
    bandwidth: '5.5 - 12 TB/s',
    description: 'Crossbar-connected cache shared by all Streaming Multiprocessors across the die.',
    usedIn: 'Prefetching global weights, broadcasting KV cache heads, TMA asynchronous copies.',
    hardwareLevel: 'On-Chip',
  },
  {
    id: 'hbm',
    name: 'HBM3e / VRAM',
    capacity: '80 - 141 GB / GPU',
    latencyNs: 200,
    bandwidth: '3.35 - 4.8 TB/s',
    description: 'Stacked 3D High Bandwidth Memory packaging connected through a silicon interposer.',
    usedIn: 'Model weights (FP16/BF16/FP8), KV Cache, optimizer states (ZeRO), gradients.',
    hardwareLevel: 'On-Device',
  },
  {
    id: 'nvlink',
    name: 'NVLink 4/5 Interconnect',
    capacity: 'Up to 8 GPUs/Node',
    latencyNs: 90,
    bandwidth: '900 - 1800 GB/s bidirectional',
    description: 'High-speed chip-to-chip interconnect for multi-GPU intra-node communication.',
    usedIn: 'Tensor Parallelism (TP AllReduce), Megatron column/row parallel linear, ZeRO-3 parameter broadcast.',
    hardwareLevel: 'Interconnect',
  },
  {
    id: 'pcie',
    name: 'PCIe Gen 5 x16',
    capacity: 'Host <-> Device',
    latencyNs: 1200,
    bandwidth: '64 - 128 GB/s',
    description: 'Host CPU to GPU peripheral bus.',
    usedIn: 'CPU memory offloading, initial weight loading from SSD, inference prompt transfer.',
    hardwareLevel: 'Interconnect',
  },
  {
    id: 'ib',
    name: 'InfiniBand / RoCE v2',
    capacity: 'Cross-Node Cluster',
    latencyNs: 2500,
    bandwidth: '400 - 800 Gbps / NIC',
    description: 'Remote Direct Memory Access (RDMA) network fabric scaling clusters up to tens of thousands of GPUs.',
    usedIn: 'Pipeline Parallelism (1F1B P2P), Data Parallel Ring AllReduce, ZeRO-DP cross-node gradients.',
    hardwareLevel: 'Cluster',
  },
];

export const HardwareTopologyModal: React.FC<HardwareTopologyModalProps> = ({ isOpen, onClose }) => {
  const [selectedTier, setSelectedTier] = useState<MemoryTier>(MEMORY_TIERS[1]);
  const [activeCodeTab, setActiveCodeTab] = useState<'triton' | 'cuda' | 'python'>('triton');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/70 backdrop-blur-sm animate-in fade-in duration-150">
      <div 
        className="relative w-full max-w-5xl max-h-[90vh] flex flex-col rounded-2xl bg-zinc-950 border border-zinc-800 shadow-2xl text-zinc-100 overflow-hidden"
        role="dialog"
        aria-labelledby="topology-modal-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-800/80 bg-zinc-900/60">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-md">
              <Cpu className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 id="topology-modal-title" className="text-base font-semibold text-zinc-50 flex items-center gap-2">
                AI Systems Hardware & Memory Hierarchy
                <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-cyan-950/80 text-cyan-400 border border-cyan-800/60">
                  H100 / Blackwell Spec
                </span>
              </h2>
              <p className="text-xs text-zinc-400">
                Interactive latency landscape, bandwidth bounds, and kernel execution primitives
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Visual Memory Pyramid / Hierarchy Cards */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs font-mono uppercase tracking-wider text-zinc-400 flex items-center gap-2">
                <Layers className="w-4 h-4 text-cyan-400" />
                Memory Hierarchy (Latency: Fast to Slow)
              </h3>
              <span className="text-xs text-zinc-500 font-mono">
                Click tier to inspect architectural properties
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2.5">
              {MEMORY_TIERS.map((tier) => {
                const isSelected = selectedTier.id === tier.id;
                return (
                  <button
                    key={tier.id}
                    onClick={() => setSelectedTier(tier)}
                    className={`flex flex-col text-left p-3 rounded-xl border transition-all relative ${
                      isSelected
                        ? 'bg-zinc-800/90 border-cyan-500 shadow-lg shadow-cyan-500/10 scale-[1.02]'
                        : 'bg-zinc-900/60 border-zinc-800/80 hover:bg-zinc-850 hover:border-zinc-700'
                    }`}
                  >
                    <div className="text-[10px] font-mono text-zinc-400 uppercase">{tier.hardwareLevel}</div>
                    <div className="text-xs font-semibold text-zinc-100 mt-1 truncate">{tier.name}</div>
                    <div className="text-[11px] font-mono text-cyan-400 mt-1">{tier.latencyNs} ns</div>
                    <div className="text-[10px] text-zinc-400 truncate mt-0.5">{tier.bandwidth}</div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Selected Tier Deep Dive Panel */}
          <div className="p-5 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800/80 pb-3">
              <div>
                <span className="text-xs font-mono uppercase px-2 py-0.5 rounded bg-zinc-800 text-zinc-300">
                  Tier: {selectedTier.hardwareLevel}
                </span>
                <h4 className="text-base font-bold text-zinc-100 mt-1">{selectedTier.name}</h4>
              </div>
              <div className="flex items-center gap-4 text-xs font-mono">
                <div>
                  <span className="text-zinc-500">Capacity: </span>
                  <span className="text-zinc-200 font-semibold">{selectedTier.capacity}</span>
                </div>
                <div>
                  <span className="text-zinc-500">Latency: </span>
                  <span className="text-emerald-400 font-semibold">{selectedTier.latencyNs} ns</span>
                </div>
                <div>
                  <span className="text-zinc-500">Bandwidth: </span>
                  <span className="text-cyan-400 font-semibold">{selectedTier.bandwidth}</span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div>
                <span className="font-mono text-zinc-400 block mb-1">Architectural Role:</span>
                <p className="text-zinc-300 leading-relaxed">{selectedTier.description}</p>
              </div>
              <div>
                <span className="font-mono text-zinc-400 block mb-1">Production AI Applications:</span>
                <p className="text-zinc-300 leading-relaxed">{selectedTier.usedIn}</p>
              </div>
            </div>

            {/* Relative Latency Comparison Bar (Logarithmic Scale) */}
            <div className="pt-2">
              <div className="flex justify-between text-[11px] font-mono text-zinc-400 mb-1.5">
                <span>Relative Latency Multiplier (1x = Registers @ 0.5ns)</span>
                <span className="text-cyan-400">{Math.round(selectedTier.latencyNs / 0.5)}x Register Latency</span>
              </div>
              <div className="w-full h-3 rounded-full bg-zinc-800 overflow-hidden p-0.5">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-emerald-500 via-cyan-500 to-rose-500 transition-all duration-300"
                  style={{
                    width: `${Math.min(100, Math.max(4, (Math.log10(selectedTier.latencyNs * 2 + 1) / Math.log10(5000)) * 100))}%`,
                  }}
                />
              </div>
            </div>
          </div>

          {/* Comparative Kernel Implementation Blueprint */}
          <div className="rounded-2xl bg-zinc-900/60 border border-zinc-800 overflow-hidden">
            <div className="flex items-center justify-between px-4 py-2.5 border-b border-zinc-800 bg-zinc-900/90">
              <div className="flex items-center gap-2 text-xs font-mono text-zinc-300">
                <Terminal className="w-3.5 h-3.5 text-cyan-400" />
                Kernel Implementation Mapping (Shared Memory Tiling / FlashAttention)
              </div>
              <div className="flex items-center gap-1.5 bg-zinc-800/80 p-1 rounded-lg">
                <button
                  onClick={() => setActiveCodeTab('triton')}
                  className={`px-2.5 py-1 text-xs font-mono rounded ${
                    activeCodeTab === 'triton' ? 'bg-cyan-600 text-white' : 'text-zinc-400 hover:text-zinc-200'
                  }`}
                >
                  Triton
                </button>
                <button
                  onClick={() => setActiveCodeTab('cuda')}
                  className={`px-2.5 py-1 text-xs font-mono rounded ${
                    activeCodeTab === 'cuda' ? 'bg-indigo-600 text-white' : 'text-zinc-400 hover:text-zinc-200'
                  }`}
                >
                  CUDA C++
                </button>
                <button
                  onClick={() => setActiveCodeTab('python')}
                  className={`px-2.5 py-1 text-xs font-mono rounded ${
                    activeCodeTab === 'python' ? 'bg-emerald-600 text-white' : 'text-zinc-400 hover:text-zinc-200'
                  }`}
                >
                  Python Model
                </button>
              </div>
            </div>

            <div className="p-4 bg-zinc-950 font-mono text-xs overflow-x-auto text-zinc-300 leading-relaxed">
              {activeCodeTab === 'triton' && (
                <pre><code>{`# Triton Online Softmax Tile Accumulation (Course 07)
@triton.jit
def _fused_attention_kernel(
    Q, K, V, Out,
    sm_scale,
    BLOCK_M: tl.constexpr = 64,
    BLOCK_N: tl.constexpr = 64,
):
    # Tile loaded directly into Shared Memory / Registers without HBM roundtrip
    q = tl.load(q_ptrs, mask=offs_m[:, None] < seqlen_q, other=0.0)
    m_prev = tl.zeros([BLOCK_M], dtype=tl.float32) - float("inf")
    l_prev = tl.zeros([BLOCK_M], dtype=tl.float32)
    acc = tl.zeros([BLOCK_M, BLOCK_D], dtype=tl.float32)

    for start_n in range(0, seqlen_k, BLOCK_N):
        k = tl.load(k_ptrs)   # SRAM Tiling
        qk = tl.dot(q, k) * sm_scale
        m_curr = tl.maximum(m_prev, tl.max(qk, 1))
        # Numerically stable exponent update
        p = tl.exp(qk - m_curr[:, None])
        l_curr = tl.exp(m_prev - m_curr) * l_prev + tl.sum(p, 1)
        acc = acc * tl.exp(m_prev - m_curr)[:, None] + tl.dot(p, v)
        m_prev, l_prev = m_curr, l_curr`}</code></pre>
              )}

              {activeCodeTab === 'cuda' && (
                <pre><code>{`// CUDA C++ Asynchronous Shared Memory Copy (TMA / cp.async)
__global__ void __launch_bounds__(128) flash_fwd_kernel(
    const half* __restrict__ Q,
    const half* __restrict__ K,
    const half* __restrict__ V,
    half* __restrict__ Out,
    const int seqlen
) {
    // Dynamically allocated SRAM scratchpad
    extern __shared__ half smem[];
    half* s_q = smem;
    half* s_k = smem + (BLOCK_M * HEAD_DIM);
    half* s_v = s_k + (BLOCK_N * HEAD_DIM);

    // Asynchronous DMA copy directly from HBM3e into SMEM bypassing registers
    #pragma unroll
    for (int i = threadIdx.x; i < (BLOCK_M * HEAD_DIM); i += blockDim.x) {
        asm volatile("cp.async.ca.shared.global [%0], [%1], 16;\n"
                     : : "r"(__cvta_generic_to_shared(s_q + i)), "l"(Q + q_offset + i));
    }
    asm volatile("cp.async.commit_group;\n");
    asm volatile("cp.async.wait_group 0;\n");
    __syncthreads();
}`}</code></pre>
              )}

              {activeCodeTab === 'python' && (
                <pre><code>{`# Python Algorithmic Equivalent (Standard Library Simulator)
# Matches 1:1 math without requiring an NVIDIA GPU host runtime
def online_softmax_flash_step(q_block, k_block, v_block, m_prev, l_prev, acc, scale):
    import math
    scores = [[sum(q * k for q, k in zip(q_row, k_col)) * scale for k_col in zip(*k_block)] for q_row in q_block]
    m_curr = [max(m_p, max(row)) for m_p, row in zip(m_prev, scores)]
    alpha = [math.exp(m_p - m_c) for m_p, m_c in zip(m_prev, m_curr)]
    p = [[math.exp(val - m_c) for val in row] for row, m_c in zip(scores, m_curr)]
    l_curr = [a * l_p + sum(p_row) for a, l_p, p_row in zip(alpha, l_prev, p)]
    acc_next = [[a * val for val in acc_row] for a, acc_row in zip(alpha, acc)]
    return m_curr, l_curr, acc_next`}</code></pre>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-6 py-3 border-t border-zinc-800 bg-zinc-900/60">
          <span className="text-xs text-zinc-400 font-mono">
            Mastery Insight: HBM roundtrips cost 200ns; Shared Memory tiling reduces memory traffic by up to 10x.
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 text-xs font-medium rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 transition-colors"
          >
            Close Explorer
          </button>
        </div>
      </div>
    </div>
  );
};
