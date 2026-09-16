import React, { useState, useEffect, useRef } from 'react';
import { Play, RotateCcw, Trash2, X, Maximize2, Minimize2, Check, AlertCircle, Clock, Terminal, ChevronDown } from 'lucide-react';
import { runInteractiveCode } from '../services/api';
import { TestResult } from '../types';

interface SideCodeRunnerProps {
  initialCode?: string;
  onClose: () => void;
}

const PRESETS = [
  {
    name: 'GEMM FLOPs & Roofline Calc',
    code: `# Roofline Model: Arithmetic Intensity & FLOPs
matrix_dim = 2048
flops = 2 * (matrix_dim ** 3)
bytes_transferred = 3 * (matrix_dim ** 2) * 2  # FP16 (2 bytes)
arithmetic_intensity = flops / bytes_transferred

print(f"Matrix Dimension: {matrix_dim} x {matrix_dim}")
print(f"Total Computation: {flops / 1e9:.2f} GFLOPs")
print(f"Memory Traffic:    {bytes_transferred / (1024**2):.2f} MB")
print(f"Arithmetic Intensity: {arithmetic_intensity:.2f} FLOPs/byte")
`,
  },
  {
    name: 'KV-Cache Memory Estimator',
    code: `# KV-Cache Memory Calculation for LLM Inference
batch_size = 4
seq_len = 8192
num_layers = 32
num_heads = 32
head_dim = 128
bytes_per_elem = 2  # FP16

# 2 * layers * 2(K & V) * batch * heads * seq * head_dim * bytes
kv_cache_bytes = 2 * num_layers * batch_size * num_heads * seq_len * head_dim * bytes_per_elem
kv_cache_gb = kv_cache_bytes / (1024 ** 3)

print(f"Model Configuration: L={num_layers}, H={num_heads}, D={head_dim}")
print(f"Context: {seq_len} tokens across {batch_size} concurrent requests")
print(f"Total KV-Cache required: {kv_cache_gb:.3f} GB GPU VRAM")
`,
  },
  {
    name: 'Softmax & Scaled Dot-Product',
    code: `# Scaled Dot-Product Attention in Pure Python
import math

def softmax(scores):
    exp_s = [math.exp(s - max(scores)) for s in scores]
    s_sum = sum(exp_s)
    return [s / s_sum for s in exp_s]

q = [1.0, 0.0, 2.0]
k = [[1.0, 0.0, 1.0], [0.0, 2.0, 0.0], [1.0, 1.0, 0.0]]
d_k = len(q)

raw_scores = [sum(qi * ki for qi, ki in zip(q, k_vec)) / math.sqrt(d_k) for k_vec in k]
weights = softmax(raw_scores)

print("Attention Scores (Raw):", [round(s, 3) for s in raw_scores])
print("Attention Weights (Softmax):", [round(w, 4) for w in weights])
print("Sum of weights:", round(sum(weights), 6))
`,
  },
  {
    name: 'Scratchpad Blank',
    code: `# Python Scratchpad
import sys

print(f"Python {sys.version.split()[0]} runtime active.")
for i in range(1, 6):
    print(f"Step {i}: Compute value = {2**i}")
`,
  },
];

export const SideCodeRunner: React.FC<SideCodeRunnerProps> = ({
  initialCode = '',
  onClose,
}) => {
  const [code, setCode] = useState<string>(initialCode || PRESETS[0].code);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [result, setResult] = useState<TestResult | null>(null);
  const [widthMode, setWidthMode] = useState<'standard' | 'wide'>('standard');
  const [showPresets, setShowPresets] = useState<boolean>(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Update code if initialCode changes externally (e.g. from lesson snippet)
  useEffect(() => {
    if (initialCode) {
      setCode(initialCode);
      // Auto-run snippet sent from lesson
      handleRunCode(initialCode);
    }
  }, [initialCode]);

  const handleRunCode = async (codeToRun?: string) => {
    const targetCode = typeof codeToRun === 'string' ? codeToRun : code;
    if (!targetCode.trim() || isRunning) return;

    setIsRunning(true);
    try {
      const res = await runInteractiveCode(targetCode);
      setResult(res);
    } catch (err: any) {
      setResult({
        exit_code: -1,
        stdout: '',
        stderr: err.message || 'Execution failed',
        duration_sec: 0,
        status: 'error',
      });
    } finally {
      setIsRunning(false);
    }
  };

  // Keyboard shortcut: Ctrl+Enter / Cmd+Enter
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRunCode();
    } else if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (!textarea) return;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newCode = code.substring(0, start) + '    ' + code.substring(end);
      setCode(newCode);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 4;
      }, 0);
    }
  };

  return (
    <aside
      className={`h-full flex flex-col border-l border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0B0F17] transition-all duration-200 shadow-2xl z-20 ${
        widthMode === 'wide' ? 'w-[680px]' : 'w-[480px]'
      }`}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-[#111622]">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-500">
            <Terminal className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-800 dark:text-zinc-200">
              Live Python Runner
            </h3>
            <span className="text-[10px] text-zinc-500 dark:text-zinc-400">
              Isolated Execution Engine
            </span>
          </div>
        </div>

        <div className="flex items-center gap-1">
          {/* Preset Selector */}
          <div className="relative">
            <button
              onClick={() => setShowPresets(!showPresets)}
              className="px-2 py-1 text-xs rounded-md bg-zinc-200/70 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-300 dark:hover:bg-zinc-700 transition flex items-center gap-1"
              title="Load example preset"
            >
              Presets <ChevronDown className="w-3 h-3" />
            </button>
            {showPresets && (
              <div className="absolute right-0 top-full mt-1 w-64 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-xl py-1 z-30">
                {PRESETS.map((p, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setCode(p.code);
                      setShowPresets(false);
                    }}
                    className="w-full text-left px-3 py-2 text-xs text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 transition"
                  >
                    {p.name}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Width Mode */}
          <button
            onClick={() => setWidthMode(widthMode === 'wide' ? 'standard' : 'wide')}
            className="p-1.5 rounded-md text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition"
            title={widthMode === 'wide' ? 'Standard Width' : 'Expand Width'}
          >
            {widthMode === 'wide' ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>

          {/* Close */}
          <button
            onClick={onClose}
            className="p-1.5 rounded-md text-zinc-500 hover:text-red-500 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition"
            title="Close Runner"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Editor Section */}
      <div className="flex-1 flex flex-col min-h-0">
        <div className="px-4 py-2 bg-zinc-100 dark:bg-[#161B22] border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between text-[11px] font-mono text-zinc-500">
          <span>Python 3 Code Editor</span>
          <span>Ctrl + Enter to run</span>
        </div>

        <div className="relative flex-1 bg-[#0D1117] overflow-hidden">
          <textarea
            ref={textareaRef}
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onKeyDown={handleKeyDown}
            spellCheck={false}
            placeholder="# Write or paste Python code here..."
            className="w-full h-full p-4 font-mono text-xs text-[#E6EDF3] bg-transparent resize-none focus:outline-none leading-relaxed selection:bg-blue-500/30"
          />
        </div>

        {/* Action Toolbar */}
        <div className="px-4 py-2.5 bg-zinc-50 dark:bg-[#111622] border-t border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleRunCode()}
              disabled={isRunning || !code.trim()}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition ${
                isRunning
                  ? 'bg-zinc-400 text-white cursor-not-allowed'
                  : 'bg-emerald-600 hover:bg-emerald-500 text-white active:scale-95'
              }`}
            >
              <Play className={`w-3.5 h-3.5 ${isRunning ? 'animate-spin' : 'fill-current'}`} />
              {isRunning ? 'Running...' : 'Run Code'}
            </button>

            <button
              onClick={() => setCode('')}
              className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition"
              title="Clear Editor"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>

          {result && (
            <div className="flex items-center gap-3 text-[11px] font-mono">
              <span className="flex items-center gap-1 text-zinc-500">
                <Clock className="w-3 h-3" />
                {result.duration_sec}s
              </span>
              <span
                className={`px-2 py-0.5 rounded-full font-medium flex items-center gap-1 ${
                  result.status === 'passed'
                    ? 'bg-emerald-500/10 text-emerald-500'
                    : 'bg-red-500/10 text-red-500'
                }`}
              >
                {result.status === 'passed' ? (
                  <Check className="w-3 h-3" />
                ) : (
                  <AlertCircle className="w-3 h-3" />
                )}
                {result.status.toUpperCase()}
              </span>
            </div>
          )}
        </div>

        {/* Output Console Section */}
        <div className="h-56 flex flex-col bg-[#0A0D12] text-zinc-300 font-mono text-xs border-t border-zinc-800">
          <div className="flex items-center justify-between px-3 py-1.5 bg-[#161B22] border-b border-zinc-800 text-[11px] text-zinc-400">
            <span className="font-semibold uppercase tracking-wider text-zinc-300">
              Terminal Output
            </span>
            {result && (
              <button
                onClick={() => setResult(null)}
                className="hover:text-zinc-200 p-0.5 rounded hover:bg-zinc-800 transition"
                title="Clear Output"
              >
                <Trash2 className="w-3 h-3" />
              </button>
            )}
          </div>

          <div className="flex-1 p-3 overflow-y-auto font-mono text-xs leading-relaxed select-text space-y-2">
            {!result && !isRunning && (
              <p className="text-zinc-600 italic">
                Press "Run Code" or Ctrl+Enter to execute. Output will stream here.
              </p>
            )}

            {isRunning && (
              <div className="flex items-center gap-2 text-emerald-400">
                <span className="animate-spin text-sm">◷</span> Executing code in Python subprocess...
              </div>
            )}

            {result && (
              <>
                {result.stdout && (
                  <pre className="text-emerald-400 whitespace-pre-wrap break-all font-mono">
                    {result.stdout}
                  </pre>
                )}
                {result.stderr && (
                  <pre className="text-red-400 whitespace-pre-wrap break-all font-mono">
                    {result.stderr}
                  </pre>
                )}
                {!result.stdout && !result.stderr && (
                  <p className="text-zinc-500 italic">Process completed with no output (exit code: {result.exit_code})</p>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </aside>
  );
};
