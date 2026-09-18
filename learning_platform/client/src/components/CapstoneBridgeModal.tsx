import React, { useState } from 'react';
import { X, Layers, Compass, CheckCircle2, ArrowRight, BookOpen, Code2, ShieldAlert, Cpu } from 'lucide-react';
import { ModuleItem } from '../types';

interface CapstoneBridgeModalProps {
  isOpen: boolean;
  onClose: () => void;
  module?: ModuleItem | null;
  onNavigateToCapstone?: () => void;
}

export const CapstoneBridgeModal: React.FC<CapstoneBridgeModalProps> = ({
  isOpen,
  onClose,
  module,
  onNavigateToCapstone,
}) => {
  const [activeTab, setActiveTab] = useState<'delta' | 'manifest' | 'phases'>('delta');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/70 backdrop-blur-sm animate-in fade-in duration-150">
      <div 
        className="relative w-full max-w-4xl max-h-[90vh] flex flex-col rounded-2xl bg-zinc-950 border border-zinc-800 shadow-2xl text-zinc-100 overflow-hidden"
        role="dialog"
        aria-labelledby="capstone-bridge-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-800/80 bg-zinc-900/60">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-600 flex items-center justify-center shadow-md">
              <Compass className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 id="capstone-bridge-title" className="text-base font-semibold text-zinc-50 flex items-center gap-2">
                Capstone Architecture Blueprint & Bridge
                {module && (
                  <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-emerald-950/80 text-emerald-400 border border-emerald-800/60">
                    Module {module.module_num}
                  </span>
                )}
              </h2>
              <p className="text-xs text-zinc-400">
                Bridging the beginner playground mental model to production-grade architecture
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

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 px-6 py-2.5 border-b border-zinc-800/80 bg-zinc-900/30">
          <button
            onClick={() => setActiveTab('delta')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 ${
              activeTab === 'delta'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-850'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            Mental Model Delta
          </button>
          <button
            onClick={() => setActiveTab('manifest')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 ${
              activeTab === 'manifest'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-850'
            }`}
          >
            <Code2 className="w-3.5 h-3.5" />
            Repository Structure Tour
          </button>
          <button
            onClick={() => setActiveTab('phases')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 ${
              activeTab === 'phases'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-850'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            Implementation Phases
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {activeTab === 'delta' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-900/40 text-xs text-emerald-300 flex items-start gap-3">
                <Compass className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold block mb-0.5">The Pedagogical Bridge:</span>
                  The beginner playground simplifies external realities so you grasp the core mathematical invariant. The production capstone wraps that same invariant in real-world concurrency, durability, backpressure, and fault tolerance.
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Beginner Playground Side */}
                <div className="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-semibold text-amber-400 uppercase">
                      Beginner Playground (Mental Model)
                    </span>
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-950/80 text-amber-400 border border-amber-800/40">
                      Step 1
                    </span>
                  </div>
                  <ul className="space-y-2 text-xs text-zinc-300">
                    <li className="flex items-start gap-2">
                      <span className="text-amber-400">•</span>
                      <span><strong>In-Memory Dict / Lists:</strong> Direct data structures with no disk synchronization.</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-amber-400">•</span>
                      <span><strong>Synchronous Flow:</strong> Single-threaded step-by-step function calls.</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-amber-400">•</span>
                      <span><strong>Plain Assertions:</strong> Self-validating print blocks to observe intermediate state.</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-amber-400">•</span>
                      <span><strong>Zero Dependencies:</strong> Pure Python standard library with no external frameworks.</span>
                    </li>
                  </ul>
                </div>

                {/* Production Capstone Side */}
                <div className="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-semibold text-emerald-400 uppercase">
                      Production Capstone (System Reality)
                    </span>
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800/40">
                      Step 5
                    </span>
                  </div>
                  <ul className="space-y-2 text-xs text-zinc-300">
                    <li className="flex items-start gap-2">
                      <span className="text-emerald-400">•</span>
                      <span><strong>Durability & Storage:</strong> Write-Ahead Logs (WAL), fsync, memory-mapped I/O, binary serialization.</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-emerald-400">•</span>
                      <span><strong>Concurrency & Race Protection:</strong> Thread locks, async task supervisors, non-blocking channels.</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-emerald-400">•</span>
                      <span><strong>Rigor & Benchmarks:</strong> Property-based fuzz testing (Hypothesis), throughput benchmarks.</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-emerald-400">•</span>
                      <span><strong>Architecture Standards:</strong> Type annotations, Ruff linting, clean interface boundaries.</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'manifest' && (
            <div className="space-y-3 text-xs">
              <p className="text-zinc-400">
                Every module's capstone repository is structured with modular software engineering conventions:
              </p>

              <div className="space-y-2 font-mono">
                <div className="p-3 rounded-lg bg-zinc-900/80 border border-zinc-800/80">
                  <span className="text-emerald-400 font-semibold">modern_project_template/</span>
                  <p className="text-zinc-400 text-[11px] font-sans mt-0.5">
                    Starter template with interfaces, type stubs, unit test fixtures, and <code># TODO</code> checkpoints for self-guided implementation.
                  </p>
                </div>
                <div className="p-3 rounded-lg bg-zinc-900/80 border border-zinc-800/80">
                  <span className="text-cyan-400 font-semibold">project_solution/</span>
                  <p className="text-zinc-400 text-[11px] font-sans mt-0.5">
                    Production reference implementation passing 100% of unit, integration, and performance benchmarks.
                  </p>
                </div>
                <div className="p-3 rounded-lg bg-zinc-900/80 border border-zinc-800/80">
                  <span className="text-indigo-400 font-semibold">tests/test_*.py</span>
                  <p className="text-zinc-400 text-[11px] font-sans mt-0.5">
                    Pytest suite testing edge conditions, failure recovery, concurrency safety, and invariant preservation.
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'phases' && (
            <div className="space-y-3 text-xs">
              <div className="flex items-start gap-3 p-3 rounded-xl bg-zinc-900/50 border border-zinc-800">
                <span className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-mono font-bold shrink-0">1</span>
                <div>
                  <h4 className="font-semibold text-zinc-200">Inspect the Invariant in Beginner Playground</h4>
                  <p className="text-zinc-400 mt-0.5">Run <code>beginner/playground.py</code> first to see the algorithm work with raw prints and numbers.</p>
                </div>
              </div>

              <div className="flex items-start gap-3 p-3 rounded-xl bg-zinc-900/50 border border-zinc-800">
                <span className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-mono font-bold shrink-0">2</span>
                <div>
                  <h4 className="font-semibold text-zinc-200">Solve the Algorithmic Problem in Practice Arena</h4>
                  <p className="text-zinc-400 mt-0.5">Implement the core function stub in the Practice Arena tab and ensure all pytest cases pass.</p>
                </div>
              </div>

              <div className="flex items-start gap-3 p-3 rounded-xl bg-zinc-900/50 border border-zinc-800">
                <span className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-mono font-bold shrink-0">3</span>
                <div>
                  <h4 className="font-semibold text-zinc-200">Review the Capstone Project Solution</h4>
                  <p className="text-zinc-400 mt-0.5">Study how the tested function integrates with asynchronous workers, disk logging, and error handling.</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-6 py-3.5 border-t border-zinc-800 bg-zinc-900/60">
          <span className="text-xs text-zinc-400">
            {module ? `Ready to explore ${module.title}?` : 'Explore the full capstone repository.'}
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-3.5 py-1.5 text-xs font-medium rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 transition-colors"
            >
              Close
            </button>
            {onNavigateToCapstone && (
              <button
                onClick={() => {
                  onClose();
                  onNavigateToCapstone();
                }}
                className="px-4 py-1.5 text-xs font-medium rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1.5 shadow-sm transition-colors"
              >
                Go to Capstone
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
