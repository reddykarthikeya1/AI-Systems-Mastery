import React, { useState, useEffect } from 'react';
import { Code2, Copy, Check, Play, RotateCcw, X, Clock, Terminal, AlertCircle } from 'lucide-react';
import { LessonItem, RunnerMode, TestResult } from '../../types';
import { runInteractiveCode } from '../../services/api';
import { soundService } from '../../services/sound';

interface ScriptViewerProps {
  currentLesson: LessonItem;
  content: string;
  onOpenInRunner?: (code: string, mode: RunnerMode) => void;
}

export const ScriptViewer: React.FC<ScriptViewerProps> = ({
  currentLesson,
  content,
  onOpenInRunner,
}) => {
  const [copied, setCopied] = useState(false);
  const [copiedOutput, setCopiedOutput] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState<TestResult | null>(null);

  const runnerMode: RunnerMode = currentLesson.type === 'powershell' 
    ? 'powershell' 
    : currentLesson.type === 'shell' 
    ? 'shell' 
    : 'python';

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleRunInline = async () => {
    if (isRunning) return;
    setIsRunning(true);
    soundService.playClick();
    const startTime = performance.now();
    try {
      const res = await runInteractiveCode(content, runnerMode);
      const duration = ((performance.now() - startTime) / 1000).toFixed(2);
      setResult({ ...res, duration_sec: parseFloat(duration) });
      if (res.exit_code === 0) {
        soundService.playSuccess();
      } else {
        soundService.playError();
      }
    } catch (err: any) {
      setResult({
        exit_code: 1,
        stdout: '',
        stderr: err?.message || 'Failed to execute script',
        duration_sec: 0,
        status: 'error',
      });
      soundService.playError();
    } finally {
      setIsRunning(false);
    }
  };

  // Keyboard shortcut Ctrl+Enter to run inline
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        handleRunInline();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [content, runnerMode]);

  const handleCopyOutput = () => {
    if (!result) return;
    const text = [result.stdout, result.stderr].filter(Boolean).join('\n');
    navigator.clipboard.writeText(text);
    setCopiedOutput(true);
    setTimeout(() => setCopiedOutput(false), 2000);
  };

  return (
    <div className="rounded-2xl bg-surface border border-border overflow-hidden shadow-card space-y-0">
      {/* Script Header Bar */}
      <div className="p-5 border-b border-border flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-zinc-50/70 dark:bg-surface-raised">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
            <Code2 className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold uppercase ${
                currentLesson.type === 'powershell'
                  ? 'bg-sky-500/10 text-sky-600 dark:text-sky-400 border border-sky-500/30'
                  : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30'
              }`}>
                {currentLesson.type === 'powershell' ? 'PowerShell Automation' : currentLesson.type === 'shell' ? 'Bash Shell Script' : 'Python Script'}
              </span>
              <span className="text-xs font-mono text-fg-subtle truncate max-w-[360px]">{currentLesson.file_path}</span>
            </div>
            <h2 className="text-base font-bold text-fg mt-1">
              {currentLesson.title}
            </h2>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button 
            className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-xl border border-border text-xs font-mono flex items-center gap-1.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 text-fg-muted transition-colors" 
            onClick={handleCopy}
            aria-label="Copy script content"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          {onOpenInRunner && (
            <button 
              className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 hidden xl:flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-border text-xs font-mono text-fg-muted hover:text-fg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
              onClick={() => onOpenInRunner(content, runnerMode)}
              title="Open in Side Scratchpad"
            >
              <Terminal className="w-3.5 h-3.5" />
              <span>Scratchpad</span>
            </button>
          )}

          <button 
            className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-2 shadow-sm transition-all disabled:opacity-50 active:scale-95" 
            onClick={handleRunInline}
            disabled={isRunning}
            aria-label="Run Script Inline"
            title="Execute script inline (Ctrl + Enter)"
          >
            {isRunning ? (
              <RotateCcw className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Play className="w-3.5 h-3.5 fill-current" />
            )}
            <span>{isRunning ? 'Running...' : 'Run Script'}</span>
          </button>
        </div>
      </div>

      {/* Code Body */}
      <div className="p-6 bg-zinc-950 overflow-x-auto">
        <pre className="font-mono text-xs sm:text-sm text-zinc-100 leading-relaxed whitespace-pre-wrap">
          {content}
        </pre>
      </div>

      {/* Inline Execution Output Drawer */}
      {result && (
        <div className="border-t border-zinc-800 bg-zinc-950 text-zinc-200 animate-in fade-in duration-150">
          <div className="flex items-center justify-between px-5 py-2.5 bg-zinc-900/90 border-b border-zinc-800/80 text-xs font-mono">
            <div className="flex items-center gap-2.5">
              <span className={`px-2 py-0.5 rounded text-[11px] font-bold flex items-center gap-1 border ${
                result.exit_code === 0 
                  ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30' 
                  : 'bg-rose-500/15 text-rose-400 border-rose-500/30'
              }`}>
                {result.exit_code === 0 ? <Check className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                <span>Exit: {result.exit_code} {result.exit_code === 0 ? '(Success)' : '(Error)'}</span>
              </span>
              {result.duration_sec !== undefined && (
                <span className="text-zinc-400 flex items-center gap-1 text-[11px]">
                  <Clock className="w-3 h-3" /> {result.duration_sec}s
                </span>
              )}
            </div>

            <div className="flex items-center gap-2">
              <button 
                onClick={handleCopyOutput}
                className="px-2 py-1 rounded hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 transition-colors flex items-center gap-1 text-xs font-mono"
              >
                {copiedOutput ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copiedOutput ? 'Copied' : 'Copy'}</span>
              </button>
              <button 
                onClick={() => setResult(null)} 
                className="px-2 py-1 rounded hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 transition-colors flex items-center gap-1 text-xs font-mono"
                title="Clear Output"
              >
                <X className="w-3.5 h-3.5" />
                <span>Clear</span>
              </button>
            </div>
          </div>

          <div className="p-5 max-h-80 overflow-y-auto font-mono text-xs leading-relaxed space-y-2 select-text">
            {result.stdout && (
              <pre className="text-emerald-400 whitespace-pre-wrap selection:bg-emerald-900 selection:text-white font-mono">
                {result.stdout}
              </pre>
            )}
            {result.stderr && (
              <pre className="text-rose-400 whitespace-pre-wrap selection:bg-rose-900 selection:text-white font-mono">
                {result.stderr}
              </pre>
            )}
            {!result.stdout && !result.stderr && (
              <span className="text-zinc-500 italic">(Process completed with no standard output)</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
