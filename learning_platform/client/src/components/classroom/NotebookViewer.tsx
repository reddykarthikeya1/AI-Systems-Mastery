import React, { useState } from 'react';
import { Layers, Play, RotateCcw, Check, X, Clock, Copy, AlertCircle } from 'lucide-react';
import { LessonItem, TestResult } from '../../types';
import { runInteractiveCode } from '../../services/api';
import { soundService } from '../../services/sound';

interface NotebookCell {
  type: 'markdown' | 'code';
  source: string;
}

interface NotebookViewerProps {
  currentLesson: LessonItem;
  notebookCells: NotebookCell[];
  renderMarkdownWithMath: (text: string) => string;
  onRunCode?: (code: string) => void;
}

export const NotebookViewer: React.FC<NotebookViewerProps> = ({
  currentLesson,
  notebookCells,
  renderMarkdownWithMath,
}) => {
  const [runningCells, setRunningCells] = useState<Record<number, boolean>>({});
  const [cellResults, setCellResults] = useState<Record<number, TestResult>>({});
  const [isRunningAll, setIsRunningAll] = useState(false);

  const runCellInline = async (cIdx: number, source: string) => {
    setRunningCells((prev) => ({ ...prev, [cIdx]: true }));
    soundService.playClick();
    const startTime = performance.now();
    try {
      const res = await runInteractiveCode(source, 'python');
      const duration = parseFloat(((performance.now() - startTime) / 1000).toFixed(2));
      setCellResults((prev) => ({ ...prev, [cIdx]: { ...res, duration_sec: duration } }));
      if (res.exit_code === 0) soundService.playSuccess();
      else soundService.playError();
    } catch (err: any) {
      setCellResults((prev) => ({
        ...prev,
        [cIdx]: { exit_code: 1, stdout: '', stderr: err?.message || 'Cell execution failed', duration_sec: 0, status: 'error' },
      }));
      soundService.playError();
    } finally {
      setRunningCells((prev) => ({ ...prev, [cIdx]: false }));
    }
  };

  const handleRunAll = async () => {
    if (isRunningAll) return;
    setIsRunningAll(true);
    for (let i = 0; i < notebookCells.length; i++) {
      const cell = notebookCells[i];
      if (cell.type === 'code') {
        await runCellInline(i, cell.source);
      }
    }
    setIsRunningAll(false);
  };

  return (
    <div className="rounded-2xl bg-surface border border-border p-6 sm:p-8 shadow-card space-y-6">
      <div className="flex items-center justify-between border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-orange-500/10 text-orange-600 dark:text-orange-400 border border-orange-500/20">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-orange-500/10 text-orange-600 dark:text-orange-400 border border-orange-500/20 font-bold">
              Jupyter Visual Notebook
            </span>
            <h2 className="text-base font-bold text-fg mt-1">
              {currentLesson.title}
            </h2>
          </div>
        </div>

        <button 
          className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-xl text-xs font-bold bg-orange-600 hover:bg-orange-500 text-white flex items-center gap-2 shadow-sm transition-all disabled:opacity-50" 
          onClick={handleRunAll}
          disabled={isRunningAll}
        >
          {isRunningAll ? <RotateCcw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
          <span>{isRunningAll ? 'Running Cells...' : 'Run All Cells'}</span>
        </button>
      </div>

      {/* Cells List */}
      <div className="space-y-6">
        {notebookCells.map((cell, cIdx) => {
          const isCellRunning = Boolean(runningCells[cIdx]);
          const result = cellResults[cIdx];

          return (
            <div key={cIdx} className="space-y-2">
              {cell.type === 'markdown' ? (
                <div
                  className="markdown-body text-fg text-sm leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(cell.source) }}
                />
              ) : (
                <div className="rounded-xl border border-border bg-surface overflow-hidden shadow-card">
                  <div className="flex items-center justify-between px-3.5 py-1.5 bg-zinc-100 dark:bg-zinc-800/90 border-b border-border text-xs font-mono text-fg-subtle">
                    <span>In [{cIdx + 1}]</span>
                    <button 
                      className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-2.5 py-1 rounded-lg hover:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5 border border-emerald-500/30 text-xs font-semibold disabled:opacity-50 transition-colors" 
                      onClick={() => runCellInline(cIdx, cell.source)}
                      disabled={isCellRunning}
                    >
                      {isCellRunning ? <RotateCcw className="w-3 h-3 animate-spin" /> : <Play className="w-3 h-3 fill-current" />}
                      <span>{isCellRunning ? 'Running...' : 'Run Cell'}</span>
                    </button>
                  </div>
                  <pre className="p-4 bg-zinc-950 font-mono text-xs text-zinc-100 overflow-x-auto whitespace-pre-wrap leading-relaxed">
                    {cell.source}
                  </pre>

                  {/* Inline Output Container */}
                  {result && (
                    <div className="border-t border-zinc-800 bg-zinc-950 text-zinc-200 animate-in fade-in duration-150">
                      <div className="flex items-center justify-between px-4 py-1.5 bg-zinc-900 border-b border-zinc-800 text-[11px] font-mono text-zinc-400 select-none">
                        <div className="flex items-center gap-2">
                          <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold flex items-center gap-1 border ${
                            result.exit_code === 0 
                              ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30' 
                              : 'bg-rose-500/15 text-rose-400 border-rose-500/30'
                          }`}>
                            {result.exit_code === 0 ? <Check className="w-2.5 h-2.5" /> : <AlertCircle className="w-2.5 h-2.5" />}
                            <span>Out [{cIdx + 1}]: Exit {result.exit_code}</span>
                          </span>
                          {result.duration_sec !== undefined && (
                            <span className="text-zinc-500 text-[10px]">
                              {result.duration_sec}s
                            </span>
                          )}
                        </div>

                        <div className="flex items-center gap-2">
                          <button 
                            onClick={() => {
                              const out = [result.stdout, result.stderr].filter(Boolean).join('\n');
                              navigator.clipboard.writeText(out);
                            }}
                            className="hover:text-white px-1.5 py-0.5 rounded hover:bg-zinc-800 transition-colors text-[11px]"
                            title="Copy Output"
                          >
                            <Copy className="w-3 h-3" />
                          </button>
                          <button 
                            onClick={() => {
                              setCellResults((prev) => {
                                const next = { ...prev };
                                delete next[cIdx];
                                return next;
                              });
                            }}
                            className="hover:text-rose-400 px-1.5 py-0.5 rounded hover:bg-zinc-800 transition-colors text-xs font-bold"
                            title="Clear Output"
                          >
                            <X className="w-3 h-3" />
                          </button>
                        </div>
                      </div>

                      <div className="p-4 max-h-60 overflow-y-auto font-mono text-xs leading-relaxed space-y-1.5 select-text">
                        {result.stdout && (
                          <pre className="text-emerald-400 whitespace-pre-wrap font-mono">
                            {result.stdout}
                          </pre>
                        )}
                        {result.stderr && (
                          <pre className="text-rose-400 whitespace-pre-wrap font-mono">
                            {result.stderr}
                          </pre>
                        )}
                        {!result.stdout && !result.stderr && (
                          <span className="text-zinc-500 italic text-xs">(Cell produced no output)</span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
