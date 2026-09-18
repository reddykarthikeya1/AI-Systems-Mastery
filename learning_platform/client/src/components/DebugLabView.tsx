import React, { useState, useEffect, useRef } from 'react';
import { Bug, Play, CheckCircle2, RotateCcw, HelpCircle, Terminal, Check, AlertTriangle, GitCompare, Code, CheckSquare } from 'lucide-react';
import { runInteractiveCode } from '../services/api';
import { TestResult } from '../types';
import confetti from 'canvas-confetti';
import { soundService } from '../services/sound';

interface DebugLabViewProps {
  moduleFolderPath: string;
  moduleTitle: string;
  onPassLab: () => void;
}

export const DebugLabView: React.FC<DebugLabViewProps> = ({
  moduleFolderPath,
  moduleTitle,
  onPassLab,
}) => {
  const [symptoms, setSymptoms] = useState<string>('');
  const [code, setCode] = useState<string>('');
  const [starterCode, setStarterCode] = useState<string>('');
  const [answers, setAnswers] = useState<string>('');
  const [showSolution, setShowSolution] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [result, setResult] = useState<TestResult | null>(null);
  const [copiedCmd, setCopiedCmd] = useState<string | null>(null);

  const handleCopyCmd = (cmd: string, id: string) => {
    navigator.clipboard.writeText(cmd);
    setCopiedCmd(id);
    soundService.playClick();
    setTimeout(() => setCopiedCmd(null), 2500);
  };
  const [isResolved, setIsResolved] = useState<boolean>(false);
  const [viewMode, setViewMode] = useState<'editor' | 'diff'>('editor');

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/debug-files?module_path=${encodeURIComponent(moduleFolderPath)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.has_debug_lab && data.files.length > 0) {
          setSymptoms(data.symptoms || 'A subtle production defect has been planted in this module. Diagnose and fix the issue.');
          const brokenFile = data.files.find((f: any) => f.filename.includes('broken_') || f.filename.endsWith('.py')) || data.files[0];
          const answersFile = data.files.find((f: any) => f.filename.toUpperCase() === 'ANSWERS.MD');
          if (brokenFile) {
            setCode(brokenFile.content);
            setStarterCode(brokenFile.content);
          }
          if (answersFile) {
            setAnswers(answersFile.content);
          }
        } else {
          setSymptoms('No planted defect file detected for this module.');
          setCode('# Clean module implementation.\nprint("No defects found.")\n');
        }
      })
      .catch(() => {
        setSymptoms('Failed to load debug lab.');
      })
      .finally(() => setLoading(false));
  }, [moduleFolderPath]);

  const handleRunDiagnosis = async () => {
    setIsRunning(true);
    setResult(null);
    try {
      const res = await runInteractiveCode(code, 'python', moduleFolderPath);
      setResult(res);
      if (res.exit_code === 0) {
        setIsResolved(true);
        confetti({
          particleCount: 90,
          spread: 70,
          origin: { y: 0.6 },
        });
        onPassLab();
      }
    } catch (err: any) {
      setResult({
        exit_code: -1,
        stdout: '',
        stderr: err.message || 'Diagnosis failed',
        duration_sec: 0,
        status: 'error',
      });
    } finally {
      setIsRunning(false);
    }
  };

  const handleReset = () => {
    setCode(starterCode);
    setResult(null);
    setIsResolved(false);
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && (e.key === 'Enter' || e.key.toLowerCase() === 's')) {
        e.preventDefault();
        handleRunDiagnosis();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [code, moduleFolderPath]);

  if (loading) {
    return <div className="p-8 text-center text-xs font-mono text-zinc-500">Loading Bug Hunter Lab...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="rounded-xl p-5 bg-gradient-to-r from-rose-500/10 via-zinc-50 to-zinc-50 dark:from-rose-950/30 dark:via-surface dark:to-surface border border-rose-500/30 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-xs font-mono font-semibold uppercase tracking-wider bg-rose-500/20 text-rose-500 border border-rose-500/30 flex items-center gap-1">
              <Bug className="w-3 h-3" /> Bug Hunter Laboratory
            </span>
            <span className="text-xs font-mono text-zinc-500 truncate">
              {moduleTitle}
            </span>
          </div>
          <h2 className="text-base sm:text-lg font-bold text-fg mt-1">
            Planted Production Defect & Triage Drill
          </h2>
          <p className="text-xs text-zinc-500 mt-0.5">
            Identify the subtle race condition, off-by-one, or memory leak, apply a patch, and verify against unit tests.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-lg text-xs font-medium border border-zinc-300 dark:border-zinc-700 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition flex items-center gap-1.5" onClick={handleReset}
            
            title="Reset to broken starter" >
            <RotateCcw className="w-3.5 h-3.5" /> Reset Broken Code
          </button>

          <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition ${
              isRunning ? 'bg-zinc-400 text-white cursor-not-allowed' : 'bg-rose-600 hover:bg-rose-500 text-white active:scale-95'
            }`} onClick={handleRunDiagnosis}
            disabled={isRunning} >
            <Play className={`w-3.5 h-3.5 ${isRunning ? 'animate-spin' : 'fill-current'}`} />
            <span>{isRunning ? 'Diagnosing...' : 'Test & Verify Patch'}</span>
          </button>
        </div>
      </div>

      {/* Success Resolution Banner */}
      {isResolved && (
        <div className="rounded-xl p-4 bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-between gap-3 text-emerald-400">
          <div className="flex items-center gap-2.5">
            <CheckCircle2 className="w-5 h-5 shrink-0" />
            <span className="text-xs font-medium">
              Defect successfully neutralized! All assertion tests passed cleanly with 0 errors.
            </span>
          </div>
          <span className="text-xs font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-500/20">
            ✓ Patch Verified
          </span>
        </div>
      )}

      {/* Dual-Mode IDE Workflow Bar */}
      <div className="rounded-xl border border-rose-200 dark:border-rose-900/60 bg-rose-50/60 dark:bg-rose-950/30 p-3.5 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="p-2 rounded-lg bg-rose-600 text-white shrink-0 shadow-xs">
            <Bug className="w-4 h-4" />
          </div>
          <div className="space-y-0.5 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-bold text-rose-900 dark:text-rose-100">Dual-Mode Debugging:</span>
              <span className="text-rose-700 dark:text-rose-300">Patch in-app or debug in VS Code with step-through breakpoints</span>
            </div>
            <p className="text-rose-600 dark:text-rose-400 font-mono text-[11px] truncate">
              Target: <span className="font-semibold text-fg px-1.5 py-0.2 rounded bg-surface border border-rose-200 dark:border-rose-900/60">{moduleFolderPath}/debug_lab</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0 flex-wrap">
          <button
            onClick={() => handleCopyCmd(`code "${moduleFolderPath}/debug_lab"`, 'code')}
            className="px-2.5 py-1.5 rounded-lg border border-rose-300 dark:border-rose-800 bg-surface text-rose-700 dark:text-rose-300 hover:bg-rose-100/60 dark:hover:bg-rose-900/50 font-mono text-[11px] font-semibold flex items-center gap-1.5 transition shadow-xs"
            title="Copy command to open this debug lab in VS Code"
          >
            {copiedCmd === 'code' ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Terminal className="w-3.5 h-3.5 text-rose-500" />}
            <span>{copiedCmd === 'code' ? 'Copied code command!' : 'Open in VS Code: code .'}</span>
          </button>
          <button
            onClick={() => handleCopyCmd(`pytest "${moduleFolderPath}/debug_lab" -v`, 'pytest')}
            className="px-2.5 py-1.5 rounded-lg border border-rose-300 dark:border-rose-800 bg-surface text-rose-700 dark:text-rose-300 hover:bg-rose-100/60 dark:hover:bg-rose-900/50 font-mono text-[11px] font-semibold flex items-center gap-1.5 transition shadow-xs"
            title="Copy pytest command to run in your local terminal"
          >
            {copiedCmd === 'pytest' ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <CheckSquare className="w-3.5 h-3.5 text-emerald-500" />}
            <span>{copiedCmd === 'pytest' ? 'Copied CLI pytest!' : 'Run in Terminal: pytest'}</span>
          </button>
        </div>
      </div>

      {/* Grid: Left Symptoms + Right Editor */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Symptoms Column (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="rounded-xl bg-surface border border-border/80 p-5 shadow-sm space-y-3">
            <div className="flex items-center gap-2 border-b border-border pb-2">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              <span className="text-xs font-mono font-semibold uppercase tracking-wider text-fg-muted">
                Observed Defect Symptoms
              </span>
            </div>
            <pre className="text-xs text-zinc-700 dark:text-zinc-300 font-mono whitespace-pre-wrap leading-relaxed">
              {symptoms}
            </pre>
          </div>

          {answers && (
            <div className="rounded-xl bg-surface border border-border/80 p-4 shadow-sm">
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 text-xs font-semibold text-blue-500 hover:text-blue-400 flex items-center gap-1.5" onClick={() => setShowSolution(!showSolution)} >
                <HelpCircle className="w-3.5 h-3.5" />
                <span>{showSolution ? 'Hide Triage Guide' : 'Reveal Triage Guide & Root Cause'}</span>
              </button>
              {showSolution && (
                <div className="mt-3 pt-3 border-t border-border text-xs font-mono text-fg-muted leading-relaxed whitespace-pre-wrap">
                  {answers}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Editor Column (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="rounded-xl overflow-hidden border border-border bg-surface shadow-xl">
            <div className="px-4 py-2 bg-surface-raised border-b border-border flex items-center justify-between text-xs font-mono text-fg-muted">
              <div className="flex items-center gap-3">
                <span className="text-rose-500 dark:text-rose-400 font-semibold flex items-center gap-1.5">
                  <Bug className="w-3.5 h-3.5" /> Defect Patch Editor
                </span>
                <div className="flex items-center p-0.5 rounded-lg bg-surface border border-border">
                  <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-2 py-0.5 rounded text-xs transition-colors flex items-center gap-1 ${
                      viewMode === 'editor'
                        ? 'bg-surface-raised text-fg font-semibold shadow-xs'
                        : 'text-fg-muted hover:text-fg'
                    }`} onClick={() => setViewMode('editor')} >
                    <Code className="w-3 h-3" />
                    <span>Editor</span>
                  </button>
                  <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-2 py-0.5 rounded text-xs transition-colors flex items-center gap-1 ${
                      viewMode === 'diff'
                        ? 'bg-surface-raised text-fg font-semibold shadow-xs'
                        : 'text-fg-muted hover:text-fg'
                    }`} onClick={() => setViewMode('diff')} >
                    <GitCompare className="w-3 h-3" />
                    <span>Diff View</span>
                  </button>
                </div>
              </div>
              <span className="hidden sm:inline text-zinc-500">Ctrl + Enter to test patch</span>
            </div>

            {viewMode === 'editor' ? (
              <textarea
                ref={textareaRef}
                value={code}
                onChange={(e) => setCode(e.target.value)}
                spellCheck={false}
                className="w-full h-80 p-4 font-mono text-xs text-fg bg-transparent resize-none focus:outline-none leading-relaxed selection:bg-rose-500/30"
              />
            ) : (
              <div className="p-4 bg-bg h-80 overflow-y-auto font-mono text-xs space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Left: Original Broken Starter */}
                  <div className="rounded-lg border border-zinc-800 bg-surface-raised/60 p-3 space-y-2">
                    <div className="text-xs font-semibold text-rose-400 pb-1.5 border-b border-zinc-800 flex items-center justify-between">
                      <span>Planted Broken Code</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">Base</span>
                    </div>
                    <div className="space-y-0.5 overflow-x-auto max-h-60 overflow-y-auto">
                      {starterCode.split('\n').map((line, i) => {
                        const isModified = !code.includes(line);
                        return (
                          <div key={i} className={`flex items-start gap-2 px-1 py-0.5 rounded ${isModified ? 'bg-rose-950/40 text-rose-300' : 'text-zinc-400'}`}>
                            <span className="text-zinc-600 select-none w-5 text-right shrink-0">{i + 1}</span>
                            <span className="whitespace-pre font-mono">{line || ' '}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Right: Student's Working Patch */}
                  <div className="rounded-lg border border-zinc-800 bg-surface-raised/60 p-3 space-y-2">
                    <div className="text-xs font-semibold text-emerald-400 pb-1.5 border-b border-zinc-800 flex items-center justify-between">
                      <span>Your Working Patch</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Patch</span>
                    </div>
                    <div className="space-y-0.5 overflow-x-auto max-h-60 overflow-y-auto">
                      {code.split('\n').map((line, i) => {
                        const isNew = !starterCode.includes(line);
                        return (
                          <div key={i} className={`flex items-start gap-2 px-1 py-0.5 rounded ${isNew ? 'bg-emerald-950/40 text-emerald-300 font-semibold' : 'text-zinc-300'}`}>
                            <span className="text-zinc-600 select-none w-5 text-right shrink-0">{i + 1}</span>
                            <span className="whitespace-pre font-mono">{line || ' '}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Test Diagnosis Output Terminal */}
          <div className="rounded-xl overflow-hidden border border-zinc-800 bg-bg text-xs font-mono">
            <div className="px-3.5 py-1.5 bg-surface-raised border-b border-zinc-800 flex items-center justify-between text-xs text-zinc-400">
              <span className="font-semibold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5 text-rose-400" />
                <span>Diagnostics Terminal</span>
              </span>
              {result && (
                <span
                  className={`px-2 py-0.5 rounded-full font-medium ${
                    result.status === 'passed' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'
                  }`}
                >
                  {result.status === 'passed' ? 'PASSED (ZERO DEFECTS)' : 'FAILED (DEFECT REPRODUCED)'}
                </span>
              )}
            </div>

            <div className="p-3.5 max-h-48 overflow-y-auto select-text leading-relaxed">
              {!result && !isRunning && (
                <p className="text-zinc-600 italic">
                  Click "Test & Verify Patch" to execute the broken code and observe the runtime failure.
                </p>
              )}

              {isRunning && (
                <div className="flex items-center gap-2 text-rose-400">
                  <span className="animate-spin text-sm">◷</span> Executing test harness against patched code...
                </div>
              )}

              {result && (
                <>
                  {result.stdout && <pre className="text-emerald-400 whitespace-pre-wrap">{result.stdout}</pre>}
                  {result.stderr && <pre className="text-red-400 whitespace-pre-wrap">{result.stderr}</pre>}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
