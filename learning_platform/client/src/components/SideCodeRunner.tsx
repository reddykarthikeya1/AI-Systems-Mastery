import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, RotateCcw, Trash2, X, Maximize2, Minimize2, Check, AlertCircle, 
  Clock, Terminal, ChevronDown, Folder, Code2, Sparkles, Copy, FileText, CheckCircle2, CornerDownLeft 
} from 'lucide-react';
import { runInteractiveCode, formatCode } from '../services/api';
import { TestResult, RunnerMode } from '../types';

export interface PageSnippet {
  id: string;
  title: string;
  code: string;
  lang: string;
}

interface CliEntry {
  id: string;
  command: string;
  stdout: string;
  stderr: string;
  exitCode: number;
  durationSec: number;
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
      name: 'Run Pytest',
      code: 'python -m pytest -v --tb=short',
    },
    {
      name: 'List Directory',
      code: 'Get-ChildItem -Path . | Format-Table -AutoSize',
    },
    {
      name: 'Environment Audit',
      code: 'python --version; python -c "import sys; print(sys.executable)"',
    },
  ],
  shell: [
    {
      name: 'Run Pytest',
      code: 'python -m pytest -v --tb=short',
    },
    {
      name: 'Check Git Status',
      code: 'git status -s',
    },
    {
      name: 'Directory Listing',
      code: 'dir /b',
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
  
  // Python Script Editor State
  const [pythonCode, setPythonCode] = useState<string>(
    initialMode === 'python' && initialCode ? initialCode : PRESETS.python[0].code
  );
  const [isPythonRunning, setIsPythonRunning] = useState<boolean>(false);
  const [pythonResult, setPythonResult] = useState<TestResult | null>(null);
  const [isFormatting, setIsFormatting] = useState<boolean>(false);

  // CLI (PowerShell / CMD) State
  const [cliInput, setCliInput] = useState<string>('');
  const [cliHistory, setCliHistory] = useState<string[]>([]);
  const [cliHistoryIdx, setCliHistoryIdx] = useState<number>(-1);
  const [isCliRunning, setIsCliRunning] = useState<boolean>(false);
  const [cliEntries, setCliEntries] = useState<CliEntry[]>([
    {
      id: 'init',
      command: '',
      stdout: `Windows PowerShell / Terminal\nHost: local\nLocation: ${moduleFolderPath}\nType commands below (e.g. "python -m pytest", "dir", "clear")`,
      stderr: '',
      exitCode: 0,
      durationSec: 0,
    },
  ]);

  const [widthMode, setWidthMode] = useState<'standard' | 'wide'>('standard');
  const [showPresets, setShowPresets] = useState<boolean>(false);
  const [showSnippets, setShowSnippets] = useState<boolean>(false);
  const [copiedOutput, setCopiedOutput] = useState<boolean>(false);

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const cliTerminalEndRef = useRef<HTMLDivElement>(null);
  const cliInputRef = useRef<HTMLInputElement>(null);

  // Sync external code or mode changes
  useEffect(() => {
    if (initialCode) {
      if (initialMode === 'python' || (!initialMode && mode === 'python')) {
        setPythonCode(initialCode);
        handleRunPython(initialCode);
      } else {
        setMode(initialMode || 'powershell');
        handleRunCliCommand(initialCode, initialMode || 'powershell');
      }
    }
  }, [initialCode, initialMode]);

  // Scroll to bottom of CLI terminal on new entry
  useEffect(() => {
    if (mode !== 'python') {
      cliTerminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [cliEntries, isCliRunning, mode]);

  const handleModeChange = (newMode: RunnerMode) => {
    setMode(newMode);
    if (newMode !== 'python') {
      setTimeout(() => cliInputRef.current?.focus(), 100);
    }
  };

  // --- Python Execution & Formatting ---
  const handleRunPython = async (overrideCode?: string) => {
    const targetCode = typeof overrideCode === 'string' ? overrideCode : pythonCode;
    if (!targetCode.trim() || isPythonRunning) return;

    setIsPythonRunning(true);
    try {
      const res = await runInteractiveCode(targetCode, 'python', moduleFolderPath);
      setPythonResult(res);
    } catch (err: any) {
      setPythonResult({
        exit_code: -1,
        stdout: '',
        stderr: err.message || 'Execution failed to dispatch',
        duration_sec: 0,
        status: 'error',
        cwd: moduleFolderPath,
        mode: 'python',
      });
    } finally {
      setIsPythonRunning(false);
    }
  };

  const handleFormatPython = async () => {
    if (!pythonCode.trim() || isFormatting) return;
    setIsFormatting(true);
    try {
      const res = await formatCode(pythonCode, 'python');
      if (res.formatted) {
        setPythonCode(res.formatted);
      }
    } catch (err) {
      console.warn('Format failed', err);
    } finally {
      setIsFormatting(false);
    }
  };

  // --- CLI Execution (PowerShell / CMD mimicking real terminal) ---
  const handleRunCliCommand = async (cmdToRun: string, runnerMode: RunnerMode = mode) => {
    const cmd = cmdToRun.trim();
    if (!cmd || isCliRunning) return;

    // Handle internal shell commands
    if (cmd.toLowerCase() === 'clear' || cmd.toLowerCase() === 'cls') {
      setCliEntries([]);
      setCliInput('');
      return;
    }

    setCliHistory((prev) => [...prev, cmd]);
    setCliHistoryIdx(-1);
    setIsCliRunning(true);
    setCliInput('');

    const entryId = `cli-${Date.now()}`;

    try {
      const res = await runInteractiveCode(cmd, runnerMode, moduleFolderPath);
      setCliEntries((prev) => [
        ...prev,
        {
          id: entryId,
          command: cmd,
          stdout: res.stdout,
          stderr: res.stderr,
          exitCode: res.exit_code,
          durationSec: res.duration_sec,
        },
      ]);
    } catch (err: any) {
      setCliEntries((prev) => [
        ...prev,
        {
          id: entryId,
          command: cmd,
          stdout: '',
          stderr: err.message || 'Command failed to dispatch',
          exitCode: -1,
          durationSec: 0,
        },
      ]);
    } finally {
      setIsCliRunning(false);
      setTimeout(() => cliInputRef.current?.focus(), 50);
    }
  };

  const handleCliKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleRunCliCommand(cliInput);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (cliHistory.length === 0) return;
      const nextIdx = cliHistoryIdx === -1 ? cliHistory.length - 1 : Math.max(0, cliHistoryIdx - 1);
      setCliHistoryIdx(nextIdx);
      setCliInput(cliHistory[nextIdx]);
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (cliHistoryIdx === -1) return;
      const nextIdx = cliHistoryIdx + 1;
      if (nextIdx >= cliHistory.length) {
        setCliHistoryIdx(-1);
        setCliInput('');
      } else {
        setCliHistoryIdx(nextIdx);
        setCliInput(cliHistory[nextIdx]);
      }
    }
  };

  const handlePythonKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRunPython();
    } else if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (!textarea) return;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newCode = pythonCode.substring(0, start) + '    ' + pythonCode.substring(end);
      setPythonCode(newCode);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 4;
      }, 0);
    }
  };

  const copyPythonOutput = () => {
    if (!pythonResult) return;
    const text = [pythonResult.stdout, pythonResult.stderr].filter(Boolean).join('\n');
    navigator.clipboard.writeText(text);
    setCopiedOutput(true);
    setTimeout(() => setCopiedOutput(false), 2000);
  };

  const getCliPrompt = () => {
    const base = moduleFolderPath.split(/[\\/]/).pop() || 'Subject';
    return mode === 'powershell' ? `PS ...\\${base}>` : `C:\\...\\${base}>`;
  };

  return (
    <aside
      className={`h-full flex flex-col border-l border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0B0F17] transition-all duration-200 shadow-2xl z-20 ${
        widthMode === 'wide' ? 'w-[760px]' : 'w-[560px]'
      }`}
    >
      {/* Top Header Bar */}
      <div className="px-4 py-3 border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-[#111622] space-y-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className={`p-1.5 rounded-lg ${
              mode === 'python' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-blue-500/10 text-blue-500'
            }`}>
              <Terminal className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 dark:text-zinc-100 flex items-center gap-1.5">
                <span>{mode === 'python' ? 'Python Script Runner' : 'Interactive CLI Terminal'}</span>
              </h3>
              <div className="text-xs font-mono text-zinc-500 flex items-center gap-1 line-clamp-1" title={moduleFolderPath}>
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
                  <span>Snippets ({pageSnippets.length})</span>
                  <ChevronDown className="w-3 h-3" />
                </button>
                {showSnippets && (
                  <div className="absolute right-0 top-full mt-1 w-80 max-h-72 overflow-y-auto bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-xl py-1 z-30">
                    <div className="px-3 py-1.5 text-xs font-mono uppercase tracking-wider text-zinc-400 border-b border-zinc-100 dark:border-zinc-800">
                      Code Snippets in {lessonTitle}
                    </div>
                    {pageSnippets.map((s, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          if (s.lang === 'BASH' || s.lang === 'SH') {
                            setMode('shell');
                            handleRunCliCommand(s.code, 'shell');
                          } else if (s.lang === 'POWERSHELL' || s.lang === 'PS1') {
                            setMode('powershell');
                            handleRunCliCommand(s.code, 'powershell');
                          } else {
                            setMode('python');
                            setPythonCode(s.code);
                          }
                          setShowSnippets(false);
                        }}
                        className="w-full text-left px-3 py-2 text-xs text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 transition flex items-center justify-between gap-2"
                      >
                        <span className="truncate font-medium">{s.title}</span>
                        <span className="px-1.5 py-0.5 rounded text-xs font-mono bg-zinc-200/70 dark:bg-zinc-800 text-zinc-500">
                          {s.lang}
                        </span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Presets */}
            {mode === 'python' && (
              <div className="relative">
                <button
                  onClick={() => { setShowPresets(!showPresets); setShowSnippets(false); }}
                  className="px-2 py-1 text-xs rounded-md bg-zinc-200/70 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-300 dark:hover:bg-zinc-700 transition flex items-center gap-1"
                  title="Load Python presets"
                >
                  <span>Presets</span> <ChevronDown className="w-3 h-3" />
                </button>
                {showPresets && (
                  <div className="absolute right-0 top-full mt-1 w-64 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-xl py-1 z-30">
                    <div className="px-3 py-1.5 text-xs font-mono uppercase tracking-wider text-zinc-400 border-b border-zinc-100 dark:border-zinc-800">
                      Python Presets
                    </div>
                    {PRESETS.python.map((p, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          setPythonCode(p.code);
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
            )}

            {/* Width Toggle */}
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

        {/* Runtime Mode Selector Pills */}
        <div className="flex items-center gap-1.5 pt-1">
          <span className="text-xs font-mono text-zinc-400 mr-1 select-none">Runtime:</span>
          
          <button
            onClick={() => handleModeChange('python')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              mode === 'python'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'bg-zinc-200/60 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <span>🐍 Python (Script + Results)</span>
          </button>

          <button
            onClick={() => handleModeChange('powershell')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              mode === 'powershell'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'bg-zinc-200/60 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <span>⚡ PowerShell CLI</span>
          </button>

          <button
            onClick={() => handleModeChange('shell')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              mode === 'shell'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'bg-zinc-200/60 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <span>💻 Command Prompt / CMD</span>
          </button>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* MODE 1: PYTHON SCRIPT RUNNER (Editor + Dedicated Results Box)             */}
      {/* ========================================================================= */}
      {mode === 'python' ? (
        <div className="flex-1 flex flex-col min-h-0">
          <div className="px-4 py-1.5 bg-zinc-100 dark:bg-[#161B22] border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between text-xs font-mono text-zinc-500">
            <span className="flex items-center gap-1.5">
              <span className="font-semibold text-emerald-500">&gt;&gt;&gt;</span>
              <span>Python Script Editor</span>
            </span>
            <span>Ctrl + Enter to run</span>
          </div>

          {/* Python Code Textarea */}
          <div className="relative flex-1 bg-[#0D1117] overflow-hidden min-h-[160px]">
            <textarea
              ref={textareaRef}
              value={pythonCode}
              onChange={(e) => setPythonCode(e.target.value)}
              onKeyDown={handlePythonKeyDown}
              spellCheck={false}
              placeholder="# Write Python code to execute against this module..."
              className="w-full h-full p-4 font-mono text-xs text-[#E6EDF3] bg-transparent resize-none focus:outline-none leading-relaxed selection:bg-emerald-500/30"
            />
          </div>

          {/* Action Toolbar */}
          <div className="px-4 py-2.5 bg-zinc-50 dark:bg-[#111622] border-t border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleRunPython()}
                disabled={isPythonRunning || !pythonCode.trim()}
                className="px-4 py-1.5 rounded-lg text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1.5 shadow-sm transition active:scale-95 disabled:opacity-40"
              >
                <Play className={`w-3.5 h-3.5 ${isPythonRunning ? 'animate-spin' : 'fill-current'}`} />
                <span>{isPythonRunning ? 'Running...' : 'Run Python'}</span>
              </button>

              <button
                onClick={handleFormatPython}
                disabled={isFormatting || !pythonCode.trim()}
                className="px-2.5 py-1.5 rounded-lg text-xs font-medium border border-zinc-300 dark:border-zinc-700 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition text-zinc-700 dark:text-zinc-300 flex items-center gap-1"
                title="Format Python code"
              >
                <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                <span>Format</span>
              </button>

              <button
                onClick={() => setPythonCode('')}
                className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition"
                title="Clear Script"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
            </div>

            {pythonResult && (
              <div className="flex items-center gap-2 text-xs font-mono">
                <span className="flex items-center gap-1 text-zinc-500">
                  <Clock className="w-3 h-3" />
                  {pythonResult.duration_sec}s
                </span>
                <span
                  className={`px-2 py-0.5 rounded-full font-semibold flex items-center gap-1 ${
                    pythonResult.status === 'passed'
                      ? 'bg-emerald-500/10 text-emerald-400'
                      : 'bg-red-500/10 text-red-400'
                  }`}
                >
                  {pythonResult.status === 'passed' ? (
                    <Check className="w-3 h-3" />
                  ) : (
                    <AlertCircle className="w-3 h-3" />
                  )}
                  {pythonResult.status.toUpperCase()}
                </span>
              </div>
            )}
          </div>

          {/* Dedicated Results Box */}
          <div className="h-64 flex flex-col bg-[#0A0D12] text-zinc-300 font-mono text-xs border-t border-zinc-800">
            <div className="flex items-center justify-between px-4 py-2 bg-[#161B22] border-b border-zinc-800 text-xs text-zinc-400">
              <div className="flex items-center gap-2">
                <span className="font-bold text-zinc-200 uppercase tracking-wider">
                  Python Results Box
                </span>
                {pythonResult && (
                  <span className="text-zinc-500">
                    Exit code: {pythonResult.exit_code}
                  </span>
                )}
              </div>

              <div className="flex items-center gap-1">
                {pythonResult && (
                  <button
                    onClick={copyPythonOutput}
                    className="hover:text-zinc-200 px-2 py-0.5 rounded hover:bg-zinc-800 transition text-xs flex items-center gap-1 text-zinc-400"
                    title="Copy Result Output"
                  >
                    {copiedOutput ? <CheckCircle2 className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                    <span>{copiedOutput ? 'Copied' : 'Copy Output'}</span>
                  </button>
                )}
                {pythonResult && (
                  <button
                    onClick={() => setPythonResult(null)}
                    className="hover:text-zinc-200 p-1 rounded hover:bg-zinc-800 transition text-zinc-400"
                    title="Clear Results"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            </div>

            <div className="flex-1 p-4 overflow-y-auto font-mono text-xs leading-relaxed select-text space-y-2">
              {!pythonResult && !isPythonRunning && (
                <div className="text-zinc-600 italic py-6 text-center">
                  Press <kbd className="px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-300 font-sans text-xs">Run Python</kbd> or <kbd className="px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-300 font-sans text-xs">Ctrl+Enter</kbd> to execute script. Output will render here.
                </div>
              )}

              {isPythonRunning && (
                <div className="flex items-center gap-2 text-emerald-400 py-4">
                  <span className="animate-spin text-sm">◷</span> Executing script in Python subprocess...
                </div>
              )}

              {pythonResult && (
                <>
                  {pythonResult.stdout && (
                    <pre className="text-emerald-400 whitespace-pre-wrap break-all font-mono">
                      {pythonResult.stdout}
                    </pre>
                  )}
                  {pythonResult.stderr && (
                    <pre className="text-red-400 whitespace-pre-wrap break-all font-mono">
                      {pythonResult.stderr}
                    </pre>
                  )}
                  {!pythonResult.stdout && !pythonResult.stderr && (
                    <p className="text-zinc-500 italic">Script completed with exit code: {pythonResult.exit_code} (No stdout returned)</p>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      ) : (
        /* ========================================================================= */
        /* MODE 2: CLI TERMINAL (Mimics real Windows PowerShell / CMD prompt)         */
        /* ========================================================================= */
        <div className="flex-1 flex flex-col min-h-0 bg-[#0C1017] text-zinc-200 font-mono text-xs select-text">
          {/* Quick Command Chips */}
          <div className="px-4 py-2 bg-[#141A24] border-b border-zinc-800 flex items-center gap-2 overflow-x-auto text-xs">
            <span className="text-zinc-500 text-xs shrink-0">Quick Cmds:</span>
            <button
              onClick={() => handleRunCliCommand('python -m pytest -v --tb=short')}
              className="px-2 py-0.5 rounded bg-zinc-800 hover:bg-blue-600 hover:text-white text-zinc-300 transition whitespace-nowrap border border-zinc-700/60"
            >
              pytest -v
            </button>
            <button
              onClick={() => handleRunCliCommand('Get-ChildItem -Path . | Format-Table -AutoSize')}
              className="px-2 py-0.5 rounded bg-zinc-800 hover:bg-blue-600 hover:text-white text-zinc-300 transition whitespace-nowrap border border-zinc-700/60"
            >
              dir / ls
            </button>
            <button
              onClick={() => handleRunCliCommand('git status -s')}
              className="px-2 py-0.5 rounded bg-zinc-800 hover:bg-blue-600 hover:text-white text-zinc-300 transition whitespace-nowrap border border-zinc-700/60"
            >
              git status
            </button>
            <button
              onClick={() => setCliEntries([])}
              className="px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-400 transition whitespace-nowrap ml-auto"
              title="Clear terminal screen"
            >
              cls
            </button>
          </div>

          {/* Continuous Terminal Scrollback Stream */}
          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {cliEntries.map((entry) => (
              <div key={entry.id} className="space-y-1">
                {entry.command && (
                  <div className="flex items-center gap-2 text-blue-400 font-semibold">
                    <span className="text-zinc-500 select-none">{getCliPrompt()}</span>
                    <span>{entry.command}</span>
                  </div>
                )}
                {entry.stdout && (
                  <pre className="text-zinc-200 whitespace-pre-wrap break-all leading-relaxed pl-2 border-l border-zinc-800/80">
                    {entry.stdout}
                  </pre>
                )}
                {entry.stderr && (
                  <pre className="text-rose-400 whitespace-pre-wrap break-all leading-relaxed pl-2 border-l border-rose-900/60">
                    {entry.stderr}
                  </pre>
                )}
                {entry.command && entry.exitCode !== 0 && (
                  <div className="text-rose-500 text-xs pl-2">
                    Command exited with error code {entry.exitCode}
                  </div>
                )}
              </div>
            ))}

            {isCliRunning && (
              <div className="flex items-center gap-2 text-blue-400 py-1">
                <span className="animate-spin">◷</span>
                <span>Executing command...</span>
              </div>
            )}

            <div ref={cliTerminalEndRef} />
          </div>

          {/* Active Terminal Prompt Input Line */}
          <div className="p-3 bg-[#090D13] border-t border-zinc-800/80 flex items-center gap-2">
            <span className="text-blue-400 font-bold shrink-0 select-none">
              {getCliPrompt()}
            </span>
            <input
              ref={cliInputRef}
              type="text"
              value={cliInput}
              onChange={(e) => setCliInput(e.target.value)}
              onKeyDown={handleCliKeyDown}
              disabled={isCliRunning}
              placeholder="Type command and press Enter (↑ ↓ for history)..."
              className="flex-1 bg-transparent border-none text-zinc-100 focus:outline-none font-mono text-xs"
              autoFocus
            />
            <button
              onClick={() => handleRunCliCommand(cliInput)}
              disabled={isCliRunning || !cliInput.trim()}
              className="p-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 disabled:opacity-30 text-white transition shrink-0"
              title="Execute command"
            >
              <CornerDownLeft className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </aside>
  );
};
