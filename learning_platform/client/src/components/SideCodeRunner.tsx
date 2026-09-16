import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, RotateCcw, Trash2, X, Maximize2, Minimize2, Check, AlertCircle, 
  Clock, Terminal, ChevronDown, Folder, Code2, Sparkles, Copy, FileText, CheckCircle2 
} from 'lucide-react';
import { runInteractiveCode } from '../services/api';
import { TestResult, RunnerMode } from '../types';

export interface PageSnippet {
  id: string;
  title: string;
  code: string;
  lang: string;
}

interface SideCodeRunnerProps {
  initialCode?: string;
  initialMode?: RunnerMode;
  courseTitle: string;
  moduleTitle: string;
  moduleFolderPath: string;
  lessonTitle: string;
  lessonFilePath: string;
  pageSnippets?: PageSnippet[];
  onClose: () => void;
}

const PRESETS: Record<RunnerMode, { name: string; code: string }[]> = {
  python: [
    {
      name: 'GEMM FLOPs & Roofline Model',
      code: `# Roofline Model: Arithmetic Intensity & FLOPs
matrix_dim = 2048
flops = 2 * (matrix_dim ** 3)
bytes_transferred = 3 * (matrix_dim ** 2) * 2  # FP16 (2 bytes)
arithmetic_intensity = flops / bytes_transferred

print(f"Matrix Dimension:     {matrix_dim} x {matrix_dim}")
print(f"Total Computation:    {flops / 1e9:.2f} GFLOPs")
print(f"Memory Traffic:       {bytes_transferred / (1024**2):.2f} MB")
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
      code: `# Python Interactive Scratchpad
import sys
import os

print(f"Python Runtime: {sys.version.split()[0]}")
print(f"Working Directory: {os.getcwd()}")
`,
    },
  ],
  powershell: [
    {
      name: 'Inspect Module Directory',
      code: `# List files and structure of active module
Get-ChildItem -Path . | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
`,
    },
    {
      name: 'Run Pytest on Current Module',
      code: `# Run pytest on the current active module
python -m pytest -v --tb=short
`,
    },
    {
      name: 'System & Environment Audit',
      code: `# Inspect active Python and PowerShell environment
Write-Host "Active PowerShell Version: $($PSVersionTable.PSVersion)"
Write-Host "Python Location: $(Get-Command python | Select-Object -ExpandProperty Source)"
Write-Host "Current Directory: $PWD"
`,
    },
  ],
  shell: [
    {
      name: 'Run Pytest (Shell)',
      code: `python -m pytest -v --tb=short
`,
    },
    {
      name: 'Check Git Status',
      code: `git status -s
`,
    },
    {
      name: 'Directory Listing',
      code: `dir /b
`,
    },
  ],
};

export const SideCodeRunner: React.FC<SideCodeRunnerProps> = ({
  initialCode = '',
  initialMode = 'python',
  courseTitle,
  moduleTitle,
  moduleFolderPath,
  lessonTitle,
  lessonFilePath,
  pageSnippets = [],
  onClose,
}) => {
  const [mode, setMode] = useState<RunnerMode>(initialMode);
  const [code, setCode] = useState<string>(initialCode || PRESETS[initialMode][0].code);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [result, setResult] = useState<TestResult | null>(null);
  const [widthMode, setWidthMode] = useState<'standard' | 'wide'>('standard');
  const [showPresets, setShowPresets] = useState<boolean>(false);
  const [showSnippets, setShowSnippets] = useState<boolean>(false);
  const [copiedOutput, setCopiedOutput] = useState<boolean>(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Sync external code or mode changes (e.g. user clicked "Run" on a lesson code block)
  useEffect(() => {
    if (initialCode) {
      setCode(initialCode);
      if (initialMode) setMode(initialMode);
      handleRun(initialCode, initialMode || mode);
    }
  }, [initialCode, initialMode]);

  const handleModeChange = (newMode: RunnerMode) => {
    setMode(newMode);
    // Switch to first preset of the new mode if current code is standard preset
    const currentIsPreset = Object.values(PRESETS).some(list => list.some(p => p.code === code));
    if (currentIsPreset || !code.trim()) {
      setCode(PRESETS[newMode][0].code);
    }
  };

  const handleRun = async (overrideCode?: string, overrideMode?: RunnerMode) => {
    const targetCode = typeof overrideCode === 'string' ? overrideCode : code;
    const targetMode = overrideMode || mode;
    if (!targetCode.trim() || isRunning) return;

    setIsRunning(true);
    try {
      const res = await runInteractiveCode(targetCode, targetMode, moduleFolderPath);
      setResult(res);
    } catch (err: any) {
      setResult({
        exit_code: -1,
        stdout: '',
        stderr: err.message || 'Execution failed to dispatch',
        duration_sec: 0,
        status: 'error',
        cwd: moduleFolderPath,
        mode: targetMode,
      });
    } finally {
      setIsRunning(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRun();
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

  const copyConsoleOutput = () => {
    if (!result) return;
    const text = [result.stdout, result.stderr].filter(Boolean).join('\n');
    navigator.clipboard.writeText(text);
    setCopiedOutput(true);
    setTimeout(() => setCopiedOutput(false), 2000);
  };

  const getPromptPrefix = () => {
    if (mode === 'python') return '>>>';
    if (mode === 'powershell') return 'PS >';
    return '$';
  };

  return (
    <aside
      className={`h-full flex flex-col border-l border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0B0F17] transition-all duration-200 shadow-2xl z-20 ${
        widthMode === 'wide' ? 'w-[720px]' : 'w-[520px]'
      }`}
    >
      {/* Top Header: Page Context & Controls */}
      <div className="px-4 py-3 border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-[#111622] space-y-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-500">
              <Terminal className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 dark:text-zinc-100 flex items-center gap-1.5">
                <span>Page-Aware Live Runner</span>
              </h3>
              <div className="text-[10px] font-mono text-zinc-500 flex items-center gap-1 line-clamp-1" title={moduleFolderPath}>
                <Folder className="w-3 h-3 text-zinc-400 shrink-0" />
                <span className="truncate">{moduleFolderPath}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-1">
            {/* Snippets on This Page */}
            {pageSnippets.length > 0 && (
              <div className="relative">
                <button
                  onClick={() => { setShowSnippets(!showSnippets); setShowPresets(false); }}
                  className="px-2 py-1 text-xs rounded-md bg-blue-50 dark:bg-blue-950/50 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-900/60 hover:bg-blue-100 dark:hover:bg-blue-900/50 transition flex items-center gap-1 font-medium"
                  title="Load code block from current lesson"
                >
                  <FileText className="w-3 h-3" />
                  <span>Page Code ({pageSnippets.length})</span>
                  <ChevronDown className="w-3 h-3" />
                </button>
                {showSnippets && (
                  <div className="absolute right-0 top-full mt-1 w-80 max-h-72 overflow-y-auto bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-xl py-1 z-30">
                    <div className="px-3 py-1.5 text-[10px] font-mono uppercase tracking-wider text-zinc-400 border-b border-zinc-100 dark:border-zinc-800">
                      Code Snippets in {lessonTitle}
                    </div>
                    {pageSnippets.map((s, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          setCode(s.code);
                          if (s.lang === 'BASH' || s.lang === 'SH') setMode('shell');
                          else if (s.lang === 'POWERSHELL' || s.lang === 'PS1') setMode('powershell');
                          else setMode('python');
                          setShowSnippets(false);
                        }}
                        className="w-full text-left px-3 py-2 text-xs text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 transition flex items-center justify-between gap-2"
                      >
                        <span className="truncate font-medium">{s.title}</span>
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-zinc-200/70 dark:bg-zinc-800 text-zinc-500">
                          {s.lang}
                        </span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Presets */}
            <div className="relative">
              <button
                onClick={() => { setShowPresets(!showPresets); setShowSnippets(false); }}
                className="px-2 py-1 text-xs rounded-md bg-zinc-200/70 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-300 dark:hover:bg-zinc-700 transition flex items-center gap-1"
                title="Load runtime preset"
              >
                <span>Presets</span> <ChevronDown className="w-3 h-3" />
              </button>
              {showPresets && (
                <div className="absolute right-0 top-full mt-1 w-64 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-xl py-1 z-30">
                  <div className="px-3 py-1.5 text-[10px] font-mono uppercase tracking-wider text-zinc-400 border-b border-zinc-100 dark:border-zinc-800">
                    {mode.toUpperCase()} Presets
                  </div>
                  {PRESETS[mode].map((p, idx) => (
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

            {/* Width Toggle */}
            <button
              onClick={() => setWidthMode(widthMode === 'wide' ? 'standard' : 'wide')}
              className="p-1.5 rounded-md text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition"
              title={widthMode === 'wide' ? 'Standard Width (520px)' : 'Expand Width (720px)'}
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

        {/* Runtime Mode Selector Pills */}
        <div className="flex items-center gap-1.5 pt-1">
          <span className="text-[11px] font-mono text-zinc-400 mr-1 select-none">Runtime:</span>
          
          <button
            onClick={() => handleModeChange('python')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              mode === 'python'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'bg-zinc-200/60 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <span>🐍 Python 3</span>
          </button>

          <button
            onClick={() => handleModeChange('powershell')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              mode === 'powershell'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'bg-zinc-200/60 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <span>⚡ PowerShell</span>
          </button>

          <button
            onClick={() => handleModeChange('shell')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              mode === 'shell'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'bg-zinc-200/60 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <span>💻 Shell / CMD</span>
          </button>
        </div>
      </div>

      {/* Editor Section */}
      <div className="flex-1 flex flex-col min-h-0">
        <div className="px-4 py-1.5 bg-zinc-100 dark:bg-[#161B22] border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between text-[11px] font-mono text-zinc-500">
          <span className="flex items-center gap-1.5">
            <span className="font-semibold text-zinc-400">{getPromptPrefix()}</span>
            <span>{mode === 'python' ? 'Interactive Python Script' : mode === 'powershell' ? 'PowerShell Command / Script' : 'Command Prompt / Bash'}</span>
          </span>
          <span>Ctrl + Enter to run</span>
        </div>

        <div className="relative flex-1 bg-[#0D1117] overflow-hidden">
          <textarea
            ref={textareaRef}
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onKeyDown={handleKeyDown}
            spellCheck={false}
            placeholder={`# Enter ${mode} code or commands to execute in ${moduleFolderPath}...`}
            className="w-full h-full p-4 font-mono text-xs text-[#E6EDF3] bg-transparent resize-none focus:outline-none leading-relaxed selection:bg-blue-500/30"
          />
        </div>

        {/* Action Toolbar */}
        <div className="px-4 py-2.5 bg-zinc-50 dark:bg-[#111622] border-t border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleRun()}
              disabled={isRunning || !code.trim()}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition ${
                isRunning
                  ? 'bg-zinc-400 text-white cursor-not-allowed'
                  : mode === 'python'
                    ? 'bg-emerald-600 hover:bg-emerald-500 text-white active:scale-95'
                    : mode === 'powershell'
                      ? 'bg-blue-600 hover:bg-blue-500 text-white active:scale-95'
                      : 'bg-indigo-600 hover:bg-indigo-500 text-white active:scale-95'
              }`}
            >
              <Play className={`w-3.5 h-3.5 ${isRunning ? 'animate-spin' : 'fill-current'}`} />
              {isRunning ? 'Running...' : `Run ${mode === 'python' ? 'Code' : mode === 'powershell' ? 'Script' : 'Command'}`}
            </button>

            <button
              onClick={() => setCode('')}
              className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition"
              title="Clear Editor"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>

            <button
              onClick={() => {
                setMode('powershell');
                setCode('python -m pytest -v --tb=short');
                handleRun('python -m pytest -v --tb=short', 'powershell');
              }}
              className="px-2 py-1 rounded text-[11px] font-mono font-medium text-zinc-600 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition border border-zinc-300 dark:border-zinc-700"
              title="Quickly run pytest in this module"
            >
              ⚡ Test Module
            </button>
          </div>

          {result && (
            <div className="flex items-center gap-2 text-[11px] font-mono">
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
            <div className="flex items-center gap-2">
              <span className="font-semibold uppercase tracking-wider text-zinc-300">
                Console Output
              </span>
              {result?.cwd && (
                <span className="text-[10px] text-zinc-500 truncate max-w-[200px]">
                  in {result.cwd}
                </span>
              )}
            </div>

            <div className="flex items-center gap-1">
              {result && (
                <button
                  onClick={copyConsoleOutput}
                  className="hover:text-zinc-200 px-1.5 py-0.5 rounded hover:bg-zinc-800 transition text-[10px] flex items-center gap-1"
                  title="Copy Console Output"
                >
                  {copiedOutput ? <CheckCircle2 className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedOutput ? 'Copied' : 'Copy'}</span>
                </button>
              )}
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
          </div>

          <div className="flex-1 p-3 overflow-y-auto font-mono text-xs leading-relaxed select-text space-y-2">
            {!result && !isRunning && (
              <p className="text-zinc-600 italic">
                Press "Run" or Ctrl+Enter to execute in {moduleFolderPath}. Output will appear here.
              </p>
            )}

            {isRunning && (
              <div className="flex items-center gap-2 text-emerald-400">
                <span className="animate-spin text-sm">◷</span> Executing in {mode} subprocess...
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
                  <p className="text-zinc-500 italic">Command completed with exit code: {result.exit_code}</p>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </aside>
  );
};
