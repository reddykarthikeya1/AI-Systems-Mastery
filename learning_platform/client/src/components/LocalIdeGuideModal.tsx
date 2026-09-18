import React, { useState } from 'react';
import { X, Terminal, Code2, Copy, Check, ExternalLink, Sparkles, Laptop, Play, CheckSquare, Layers, Cpu, ShieldCheck } from 'lucide-react';
import { soundService } from '../services/sound';

interface LocalIdeGuideModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface CliCommand {
  id: string;
  title: string;
  category: string;
  command: string;
  description: string;
}

const COMMANDS: CliCommand[] = [
  {
    id: 'open-code',
    title: 'Open Whole Academy in VS Code',
    category: 'IDE Setup',
    command: 'code .',
    description: 'Launches Visual Studio Code at the root of the academy repository with all courses, tests, and workspaces ready.',
  },
  {
    id: 'venv-win',
    title: 'Create & Activate Virtualenv (Windows PowerShell)',
    category: 'Environment',
    command: 'python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1',
    description: 'Sets up an isolated Python 3.11+ virtual environment on Windows.',
  },
  {
    id: 'venv-unix',
    title: 'Create & Activate Virtualenv (macOS / Linux / WSL)',
    category: 'Environment',
    command: 'python3 -m venv .venv && source .venv/bin/activate',
    description: 'Sets up an isolated Python virtual environment on UNIX and WSL.',
  },
  {
    id: 'pip-install',
    title: 'Install Test & Development Harness',
    category: 'Environment',
    command: 'pip install -r requirements.txt',
    description: 'Installs pytest, hypothesis, fastapi, uvicorn, and core curriculum testing tools.',
  },
  {
    id: 'run-pytest-all',
    title: 'Run All Acceptance Tests',
    category: 'Verification',
    command: 'pytest -v',
    description: 'Executes the full automated pytest suite across all courses and modules.',
  },
  {
    id: 'run-workspace-test',
    title: 'Run Tests for a Single Module',
    category: 'Verification',
    command: 'pytest "01_Advanced_Python/Module_01_Memory_Management/tests" -v',
    description: 'Runs targeted unit and property-based tests for a specific learning module.',
  },
  {
    id: 'torchrun-multi',
    title: 'Launch Multi-GPU Distributed Training',
    category: 'Hardware & GPU',
    command: 'torchrun --nproc_per_node=2 08_Distributed_Training_and_GPU_Infrastructure/Module_03_Distributed_Data_Parallel_DDP/02_ddp_training.py',
    description: 'Spawns multi-GPU processes with PyTorch DDP and NCCL communication rings.',
  },
];

export const LocalIdeGuideModal: React.FC<LocalIdeGuideModalProps> = ({ isOpen, onClose }) => {
  const [copiedId, setCopiedId] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    soundService.playSuccess();
    setTimeout(() => setCopiedId(null), 2500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/70 backdrop-blur-sm animate-in fade-in duration-150">
      <div 
        className="relative w-full max-w-4xl max-h-[90vh] flex flex-col rounded-2xl bg-surface border border-border shadow-2xl text-fg overflow-hidden"
        role="dialog"
        aria-labelledby="ide-guide-modal-title"
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-surface-raised">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center shadow-md text-white">
              <Terminal className="w-5 h-5" />
            </div>
            <div>
              <h2 id="ide-guide-modal-title" className="text-base font-bold text-fg flex items-center gap-2">
                Local IDE & Terminal Workflow Guide
                <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/30">
                  Dual-Mode Freedom
                </span>
              </h2>
              <p className="text-xs text-fg-muted">
                You are never restricted to this web app. Use the Live Runner in-browser, or build natively in VS Code, PyCharm, or your local terminal.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-fg-muted hover:text-fg hover:bg-surface transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Dual-Mode Workflow Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl border border-blue-200 dark:border-blue-900/60 bg-blue-50/60 dark:bg-blue-950/30 space-y-2">
              <div className="flex items-center gap-2 text-blue-700 dark:text-blue-300 font-bold text-sm">
                <Laptop className="w-4 h-4" />
                <span>1. In-App Live Runner Mode</span>
              </div>
              <p className="text-xs text-blue-900/80 dark:text-blue-200/80 leading-relaxed">
                Whenever you want quick, zero-setup verification, click <strong>▶ Run</strong> or <strong>Test My Code (Ctrl+Enter)</strong> right inside the app. Scripts run inline in a local sandboxed subprocess with instant stdout/stderr output.
              </p>
            </div>

            <div className="p-4 rounded-xl border border-emerald-200 dark:border-emerald-900/60 bg-emerald-50/60 dark:bg-emerald-950/30 space-y-2">
              <div className="flex items-center gap-2 text-emerald-700 dark:text-emerald-300 font-bold text-sm">
                <Code2 className="w-4 h-4" />
                <span>2. Local VS Code & Terminal Mode</span>
              </div>
              <p className="text-xs text-emerald-900/80 dark:text-emerald-200/80 leading-relaxed">
                All files live directly on your machine in this repository. Edit in <strong>VS Code</strong>, <strong>Cursor</strong>, or <strong>PyCharm</strong> to enjoy your favorite linters, extensions, Git graphs, and interactive debuggers with breakpoints.
              </p>
            </div>
          </div>

          {/* Local Directory Structure */}
          <div className="p-4 rounded-xl bg-surface-raised border border-border space-y-2.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-fg-muted flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-blue-500" />
                Repository & Workspace Layout
              </span>
              <span className="text-[11px] font-mono text-fg-subtle">Automatic Disk Sync</span>
            </div>
            <div className="p-3 rounded-lg bg-slate-950 text-slate-200 font-mono text-xs leading-relaxed overflow-x-auto space-y-1">
              <div><span className="text-blue-400">01_Advanced_Python/</span> ... <span className="text-purple-400">12_LLM_Evaluation/</span> <span className="text-slate-500"># Curriculum courses & lessons</span></div>
              <div><span className="text-emerald-400">user_workspaces/</span> <span className="text-slate-500"># Your editable solution workspaces for Project Studio</span></div>
              <div><span className="text-amber-400">tests/</span> <span className="text-slate-500"># Full platform automated acceptance test suites</span></div>
              <div><span className="text-cyan-400">.study_progress.json</span> <span className="text-slate-500"># Local persistence for completed lessons, XP, and streak</span></div>
            </div>
            <p className="text-xs text-fg-muted">
              💡 <strong>Instant Sync:</strong> Edits you save in the browser automatically write to disk, and edits you save in VS Code appear immediately when you refresh or reload the app.
            </p>
          </div>

          {/* CLI Commands Cheatsheet */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-fg flex items-center gap-2">
                <Play className="w-4 h-4 text-emerald-500" />
                Quick Terminal Commands
              </h3>
              <span className="text-xs font-mono text-fg-muted">Click any command to copy</span>
            </div>

            <div className="grid grid-cols-1 gap-2.5">
              {COMMANDS.map((cmd) => {
                const isCopied = copiedId === cmd.id;
                return (
                  <div 
                    key={cmd.id}
                    className="p-3.5 rounded-xl bg-surface-raised border border-border hover:border-blue-300 dark:hover:border-blue-700 transition flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xs"
                  >
                    <div className="space-y-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-bold text-xs text-fg">{cmd.title}</span>
                        <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-surface border border-border text-fg-muted">
                          {cmd.category}
                        </span>
                      </div>
                      <p className="text-xs text-fg-muted">{cmd.description}</p>
                      <code className="text-xs font-mono text-blue-600 dark:text-blue-400 bg-surface px-2 py-1 rounded border border-border block overflow-x-auto">
                        {cmd.command}
                      </code>
                    </div>

                    <button
                      onClick={() => handleCopy(cmd.command, cmd.id)}
                      className="shrink-0 px-3 py-1.5 rounded-lg border border-border bg-surface hover:bg-surface-raised font-mono text-xs font-semibold flex items-center gap-1.5 transition text-fg-muted hover:text-fg shadow-xs"
                      title="Copy command to clipboard"
                    >
                      {isCopied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                      <span>{isCopied ? 'Copied!' : 'Copy'}</span>
                    </button>
                  </div>
                );
              })}
            </div>
          </div>

          {/* GPU / Distributed Training Pro-Tip */}
          <div className="p-4 rounded-xl border border-purple-200 dark:border-purple-900/60 bg-purple-50/60 dark:bg-purple-950/30 space-y-2">
            <div className="flex items-center gap-2 text-purple-700 dark:text-purple-300 font-bold text-xs">
              <Cpu className="w-4 h-4" />
              <span>Advanced Pro-Tip: GPU Kernels & Distributed Clusters</span>
            </div>
            <p className="text-xs text-purple-900/85 dark:text-purple-200/85 leading-relaxed">
              Courses 07 (GPU Kernels & Triton), 08 (Distributed Training & NCCL), and 09 (Inference Engines) cover heavy production architectures. While mock tests run inside the app, for maximum speed run full kernels on physical NVIDIA hardware or remote cloud GPU instances (Lambda, RunPod, AWS) using <strong>VS Code Remote - SSH</strong> or Docker containers!
            </p>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3.5 border-t border-border bg-surface-raised flex items-center justify-between text-xs font-mono text-fg-muted">
          <span>Dual-Mode Architecture &bull; Total Developer Freedom</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold transition shadow-xs"
          >
            Got it, Let's Code!
          </button>
        </div>
      </div>
    </div>
  );
};
