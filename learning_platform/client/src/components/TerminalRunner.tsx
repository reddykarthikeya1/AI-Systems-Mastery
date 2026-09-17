import React from 'react';
import { Terminal as TerminalIcon, CheckCircle2, XCircle, Clock, RotateCw } from 'lucide-react';
import { TestResult } from '../types';

interface TerminalRunnerProps {
  result: TestResult | null;
  isRunning: boolean;
  onRunTest: () => void;
  onRunDemo?: () => void;
  hasDemo?: boolean;
}

export const TerminalRunner: React.FC<TerminalRunnerProps> = ({
  result,
  isRunning,
  onRunTest,
  onRunDemo,
  hasDemo,
}) => {
  return (
    <div className="rounded-xl border border-border bg-bg text-zinc-100 overflow-hidden shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
      {/* Terminal Title Bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-bg border-b border-zinc-800/80">
        <div className="flex items-center gap-3">
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-zinc-600/70" />
            <div className="w-2.5 h-2.5 rounded-full bg-zinc-600/70" />
            <div className="w-2.5 h-2.5 rounded-full bg-zinc-600/70" />
          </div>
          <span className="text-xs font-mono text-zinc-400 flex items-center gap-1.5">
            <TerminalIcon className="w-3.5 h-3.5" /> Pytest & Execution Console
          </span>
        </div>

        <div className="flex items-center gap-2">
          {hasDemo && onRunDemo && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 text-xs font-mono px-3 py-1 rounded-md bg-zinc-800 hover:bg-zinc-700 text-zinc-200 disabled:opacity-50 transition-colors flex items-center gap-1.5 border border-zinc-700/60" onClick={onRunDemo}
              disabled={isRunning} >
              {isRunning ? <RotateCw className="w-3 h-3 animate-spin" /> : '▶'} Quickstart Demo
            </button>
          )}

          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 text-xs font-mono px-3 py-1 rounded-md bg-blue-600 hover:bg-blue-500 text-white disabled:opacity-50 transition-colors flex items-center gap-1.5" onClick={onRunTest}
            disabled={isRunning} >
            {isRunning ? <RotateCw className="w-3 h-3 animate-spin" /> : '▶'} Run Pytest
          </button>
        </div>
      </div>

      {/* Terminal Output Body */}
      <div className="p-4 font-mono text-xs overflow-x-auto max-h-96 min-h-[160px] bg-bg text-zinc-300">
        {isRunning ? (
          <div className="flex items-center gap-2 text-zinc-400 py-8 justify-center">
            <RotateCw className="w-4 h-4 animate-spin text-blue-500" />
            <span>Executing automated test suite and measuring timings...</span>
          </div>
        ) : result ? (
          <div>
            <div className="flex items-center justify-between pb-2.5 mb-3 border-b border-zinc-800 text-xs font-mono">
              <div className="flex items-center gap-2">
                {result.status === 'passed' ? (
                  <span className="flex items-center gap-1 text-emerald-400 font-semibold">
                    <CheckCircle2 className="w-3.5 h-3.5" /> SUITE PASSED
                  </span>
                ) : (
                  <span className="flex items-center gap-1 text-rose-400 font-semibold">
                    <XCircle className="w-3.5 h-3.5" /> TEST FAILED
                  </span>
                )}
                <span className="text-zinc-500">| Exit: {result.exit_code}</span>
              </div>
              <span className="flex items-center gap-1 text-zinc-400">
                <Clock className="w-3.5 h-3.5" /> {result.duration_sec}s
              </span>
            </div>

            <pre className="whitespace-pre-wrap leading-relaxed text-zinc-300 text-xs">
              {result.stdout || result.stderr || "Process finished with no output."}
            </pre>
          </div>
        ) : (
          <div className="text-zinc-500 text-center py-10 font-mono text-xs">
            Select <strong className="text-zinc-300 font-semibold">"Run Pytest"</strong> or <strong className="text-zinc-300 font-semibold">"Quickstart Demo"</strong> above to execute live against Python test suites.
          </div>
        )}
      </div>
    </div>
  );
};
