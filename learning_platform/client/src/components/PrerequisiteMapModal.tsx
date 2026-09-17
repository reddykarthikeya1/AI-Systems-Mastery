import React, { useEffect } from 'react';
import { X, ArrowRight, GitFork, CheckCircle2, BookOpen, Layers, ShieldCheck, Cpu, Zap, Database } from 'lucide-react';
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

export const PrerequisiteMapModal: React.FC<PrerequisiteMapModalProps> = ({
  isOpen,
  onClose,
  courses,
  currentCourseId,
  onSelectCourse,
}) => {
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

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200"
      role="dialog"
      aria-modal="true"
      aria-labelledby="prereq-map-title"
    >
      <div className="w-full max-w-5xl max-h-[90vh] flex flex-col rounded-3xl bg-zinc-900 border border-zinc-800 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="px-6 py-5 border-b border-zinc-800 flex items-center justify-between bg-zinc-900/90 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <GitFork className="w-5 h-5" />
            </div>
            <div>
              <h2 id="prereq-map-title" className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                <span>Curriculum Dependency Map</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-400 font-mono font-medium">
                  4 Tiers • 12 Courses
                </span>
              </h2>
              <p className="text-xs text-zinc-400">
                Architectural progression path from low-level systems engineering to autonomous cognitive models.
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-zinc-800 transition"
            aria-label="Close prerequisite roadmap"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body: 4 Tiers */}
        <div className="flex-1 overflow-y-auto p-6 space-y-8 select-text">
          {TIERS.map((tier) => (
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
          ))}
        </div>

        {/* Footer info */}
        <div className="px-6 py-3.5 border-t border-zinc-800 bg-zinc-900/90 flex items-center justify-between text-xs text-zinc-400">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>All courses verified with reproducible test suites and production debug labs.</span>
          </div>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white font-medium text-xs transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
