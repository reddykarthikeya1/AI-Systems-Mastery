import React from 'react';
import { Layers, Play } from 'lucide-react';
import { LessonItem } from '../../types';

interface NotebookCell {
  type: 'markdown' | 'code';
  source: string;
}

interface NotebookViewerProps {
  currentLesson: LessonItem;
  notebookCells: NotebookCell[];
  renderMarkdownWithMath: (text: string) => string;
  onRunCode: (code: string) => void;
}

export const NotebookViewer: React.FC<NotebookViewerProps> = ({
  currentLesson,
  notebookCells,
  renderMarkdownWithMath,
  onRunCode,
}) => {
  const handleRunAll = () => {
    const allCode = notebookCells
      .filter((c) => c.type === 'code')
      .map((c) => c.source)
      .join('\n\n');
    onRunCode(allCode);
  };

  return (
    <div className="rounded-2xl bg-surface border border-border p-8 shadow-sm space-y-6">
      <div className="flex items-center justify-between border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-orange-500/10 text-orange-500 border border-orange-500/20">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-orange-500/10 text-orange-500 border border-orange-500/20">
              Jupyter Visual Notebook
            </span>
            <h2 className="text-base font-bold text-fg mt-1">
              {currentLesson.title}
            </h2>
          </div>
        </div>

        <button
          onClick={handleRunAll}
          className="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-orange-600 hover:bg-orange-500 text-white flex items-center gap-2 shadow-sm transition-all"
        >
          <Play className="w-3.5 h-3.5 fill-current" />
          <span>Run All Cells</span>
        </button>
      </div>

      {/* Cells List */}
      <div className="space-y-6">
        {notebookCells.map((cell, cIdx) => (
          <div key={cIdx} className="space-y-2">
            {cell.type === 'markdown' ? (
              <div
                className="markdown-body text-fg text-sm leading-relaxed"
                dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(cell.source) }}
              />
            ) : (
              <div className="rounded-xl border border-zinc-800 bg-[#0D1117] overflow-hidden">
                <div className="flex items-center justify-between px-3 py-1.5 bg-[#161B22] border-b border-zinc-800 text-xs font-mono text-zinc-400">
                  <span>Python Cell [{cIdx + 1}]</span>
                  <button
                    onClick={() => onRunCode(cell.source)}
                    className="px-2 py-0.5 rounded hover:bg-emerald-950/60 text-emerald-400 flex items-center gap-1 border border-emerald-500/30"
                  >
                    <Play className="w-3 h-3 fill-current" />
                    <span>Run Cell</span>
                  </button>
                </div>
                <pre className="p-4 font-mono text-xs text-zinc-200 overflow-x-auto">
                  {cell.source}
                </pre>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
