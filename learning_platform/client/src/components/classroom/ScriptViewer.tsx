import React, { useState } from 'react';
import { Code2, Copy, Check, Play } from 'lucide-react';
import { LessonItem, RunnerMode } from '../../types';

interface ScriptViewerProps {
  currentLesson: LessonItem;
  content: string;
  onOpenInRunner: (code: string, mode: RunnerMode) => void;
}

export const ScriptViewer: React.FC<ScriptViewerProps> = ({
  currentLesson,
  content,
  onOpenInRunner,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const runnerMode: RunnerMode = currentLesson.type === 'powershell' 
    ? 'powershell' 
    : currentLesson.type === 'shell' 
    ? 'shell' 
    : 'python';

  return (
    <div className="rounded-2xl bg-surface border border-border overflow-hidden shadow-sm space-y-0">
      {/* Script Header Bar */}
      <div className="p-5 border-b border-border flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-zinc-50/70 dark:bg-surface-raised">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
            <Code2 className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold uppercase ${
                currentLesson.type === 'powershell'
                  ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                  : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
              }`}>
                {currentLesson.type === 'powershell' ? 'PowerShell Automation' : currentLesson.type === 'shell' ? 'Bash Shell Script' : 'Python Script'}
              </span>
              <span className="text-xs font-mono text-fg-subtle">{currentLesson.file_path}</span>
            </div>
            <h2 className="text-base font-bold text-fg mt-1">
              {currentLesson.title}
            </h2>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-xl border border-border text-xs font-mono flex items-center gap-1.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 text-fg-muted" onClick={handleCopy}
            
            aria-label="Copy script content" >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-2 shadow-sm transition-all" onClick={() => onOpenInRunner(content, runnerMode)}
            
            aria-label="Run in Live Runner" >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Run in Live Runner</span>
          </button>
        </div>
      </div>

      {/* Code Body */}
      <div className="p-6 bg-bg overflow-x-auto">
        <pre className="font-mono text-xs sm:text-sm text-zinc-200 leading-relaxed whitespace-pre-wrap">
          {content}
        </pre>
      </div>
    </div>
  );
};
