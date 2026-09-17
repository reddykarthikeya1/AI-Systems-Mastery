import React, { useState, useEffect } from 'react';
import { ChevronRight, ChevronLeft, CheckCircle2, Activity } from 'lucide-react';
import { LessonItem } from '../../types';
import { LessonSkeleton } from '../LessonSkeleton';
import { MasteryChecklist } from '../MasteryChecklist';
import { AlgorithmTraceScrubber } from '../AlgorithmTraceScrubber';
import { fetchModuleTrace } from '../../services/api';

interface MarkdownViewerProps {
  isLoading: boolean;
  content: string;
  lessonId: string;
  measureClass: string;
  fontSizeClass: string;
  fontFamilyClass: string;
  renderMarkdownWithMath: (text: string) => string;
  confidenceRated: string | null;
  onConfidenceClick: (rating: number, message: string) => void;
  nextLesson?: LessonItem | null;
  prevLesson?: LessonItem | null;
  currentLessonIndex: number;
  allLessons: LessonItem[];
  moduleNum: number;
  isCompleted: boolean;
  onPrevLesson: () => void;
  onCompleteAndNext: () => void;
  onOpenMasteryGate?: () => void;
  getLessonBadge: (type: string) => React.ReactNode;
}

export const MarkdownViewer: React.FC<MarkdownViewerProps> = ({
  isLoading,
  content,
  lessonId,
  measureClass,
  fontSizeClass,
  fontFamilyClass,
  renderMarkdownWithMath,
  confidenceRated,
  onConfidenceClick,
  nextLesson,
  prevLesson,
  currentLessonIndex,
  allLessons,
  moduleNum,
  isCompleted,
  onPrevLesson,
  onCompleteAndNext,
  onOpenMasteryGate,
  getLessonBadge,
}) => {
  const [showScrubber, setShowScrubber] = useState<boolean>(false);
  const [moduleTrace, setModuleTrace] = useState<any | null>(null);

  const currentLesson = allLessons[currentLessonIndex];

  useEffect(() => {
    let active = true;
    if (currentLesson?.file_path) {
      const norm = currentLesson.file_path.replace(/\\/g, '/');
      const parts = norm.split('/');
      if (parts.length > 1) {
        const moduleDir = parts.slice(0, parts.length - 1).join('/');
        fetchModuleTrace(moduleDir).then((trace) => {
          if (active && trace) {
            setModuleTrace(trace);
          }
        });
      }
    }
    return () => {
      active = false;
    };
  }, [currentLesson?.file_path]);

  // Check for embedded trace block in markdown
  const traceMatch = content.match(/```(?:trace|algorithm-trace)\n([\s\S]*?)```/);
  let parsedTrace = null;
  if (traceMatch) {
    try {
      parsedTrace = JSON.parse(traceMatch[1]);
    } catch {
      parsedTrace = null;
    }
  }

  const activeTrace = parsedTrace || moduleTrace;

  const isAlgorithmic =
    Boolean(activeTrace) ||
    /binary search|two pointer|sliding window|quickselect|partition|dijkstra|bfs|dfs|fenwick/i.test(content) ||
    lessonId.toLowerCase().includes('algorithm') ||
    lessonId.toLowerCase().includes('dsa');

  return (
    <div className="rounded-2xl bg-surface border border-border p-8 sm:p-10 shadow-sm">
      {isLoading ? (
        <LessonSkeleton />
      ) : (
        <>
          {/* Interactive Algorithm Trace Scrubber Toolbar Toggle */}
          {isAlgorithmic && (
            <div className="mb-6 p-4 rounded-2xl bg-sky-500/10 border border-sky-500/20 flex items-center justify-between gap-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-sky-500/20 text-sky-500">
                  <Activity className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold font-mono text-fg">
                    Interactive Algorithm State Scrubber
                  </h4>
                  <p className="text-xs text-fg-muted">
                    Step frame-by-frame through pointer movements, array states, and loop invariants.
                  </p>
                </div>
              </div>
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-sky-500 hover:bg-sky-600 text-white transition-colors shadow-sm" onClick={() => setShowScrubber(!showScrubber)} >
                {showScrubber ? 'Hide Scrubber' : 'Open Scrubber'}
              </button>
            </div>
          )}

          {/* Scrubber component if active */}
          {(showScrubber || parsedTrace) && (
            <div className="mb-8">
              <AlgorithmTraceScrubber trace={activeTrace || undefined} />
            </div>
          )}

          <div
            className={`markdown-body text-fg mx-auto transition-all ${measureClass} ${fontSizeClass} ${fontFamilyClass}`}
            dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(content) }}
          />

          {/* Spaced Repetition Confidence Rating */}
          <div className="mt-12 p-5 rounded-2xl bg-zinc-50/70 dark:bg-zinc-900/40 border border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <h4 className="text-sm font-semibold text-fg">
                How confident do you feel with this lesson?
              </h4>
              <p className="text-xs text-fg-subtle mt-0.5">
                Rates retention in your SuperMemo SM-2 spaced repetition deck.
              </p>
              {confidenceRated && (
                <span className="inline-flex items-center gap-1 text-xs text-emerald-600 dark:text-emerald-400 font-mono mt-1">
                  ✓ {confidenceRated}
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-xl text-xs font-medium border border-emerald-300 dark:border-emerald-800/80 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100 dark:hover:bg-emerald-900/40 transition-colors flex items-center gap-1.5" onClick={() => onConfidenceClick(5, '🟢 Solid retention scheduled (5/5)')}
                
                title="Got it: high retention, intervals expand"
                aria-label="Got it (High confidence)" >
                <span>🟢 Got it</span>
              </button>
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-xl text-xs font-medium border border-amber-300 dark:border-amber-800/80 bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 hover:bg-amber-100 dark:hover:bg-amber-900/40 transition-colors flex items-center gap-1.5" onClick={() => onConfidenceClick(3, '🟡 Review scheduled for tomorrow (3/5)')}
                
                title="Shaky: review tomorrow to solidify"
                aria-label="Shaky (Medium confidence)" >
                <span>🟡 Shaky</span>
              </button>
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-xl text-xs font-medium border border-rose-300 dark:border-rose-800/80 bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 hover:bg-rose-100 dark:hover:bg-rose-900/40 transition-colors flex items-center gap-1.5" onClick={() => onConfidenceClick(1, '🔴 Reset for immediate review today (1/5)')}
                
                title="Lost: reset interval to 1 day"
                aria-label="Lost (Low confidence)" >
                <span>🔴 Lost</span>
              </button>
            </div>
          </div>

          {/* You should now be able to... Mastery Checklist */}
          <MasteryChecklist lessonId={lessonId} content={content} />

          {/* Up Next Preview Card */}
          {nextLesson ? (
            <div className="my-8 p-5 sm:p-6 rounded-2xl bg-zinc-50/80 dark:bg-zinc-900/50 border border-border shadow-xs transition-all hover:border-blue-500/40 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                    Up Next • Lesson {currentLessonIndex + 2} of {allLessons.length}
                  </span>
                  {getLessonBadge(nextLesson.type)}
                </div>
                <h3 className="text-base font-semibold text-fg">
                  {nextLesson.title}
                </h3>
              </div>
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white flex items-center gap-1.5 shadow-sm transition-all active:scale-95 shrink-0" onClick={onCompleteAndNext}
                
                aria-label="Continue to Next Lesson" >
                <span>Next Lesson</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="my-8 p-6 rounded-2xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200/80 dark:border-emerald-800/60 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
                    Module Complete
                  </span>
                </div>
                <h3 className="text-base font-semibold text-fg">
                  All lessons cleared for Module {moduleNum.toString().padStart(2, '0')}
                </h3>
                <p className="text-xs text-fg-subtle">
                  Ready to test your comprehension in the Module Mastery Gate?
                </p>
              </div>
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-2 shadow-sm transition-all active:scale-95 shrink-0" onClick={() => {
                  if (onOpenMasteryGate) onOpenMasteryGate();
                }}
                
                aria-label="Unlock Module Mastery Gate" >
                <span>Mastery Gate 🛡️</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </>
      )}

      {/* Bottom Lesson Navigation Dock */}
      <div className="mt-12 pt-6 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-4 sticky bottom-4 bg-surface/95 backdrop-blur-md p-4 rounded-2xl border border-border shadow-xl z-20">
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 flex-1 sm:flex-initial px-4 py-2.5 rounded-xl border border-border bg-surface hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30 disabled:pointer-events-none transition-colors text-xs font-medium text-fg-muted flex items-center gap-2 shadow-sm" onClick={onPrevLesson}
            disabled={!prevLesson} >
            <ChevronLeft className="w-4 h-4" />
            <span>Previous Lesson</span>
          </button>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono text-fg-subtle">
          <span>Lesson {currentLessonIndex + 1} of {allLessons.length}</span>
          <span className="text-zinc-300 dark:text-zinc-700">•</span>
          <span className={`inline-flex items-center gap-1 font-semibold ${isCompleted ? 'text-emerald-500' : 'text-zinc-400'}`}>
            <CheckCircle2 className="w-3.5 h-3.5" />
            {isCompleted ? 'Completed' : 'In Progress'}
          </span>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 flex-1 sm:flex-initial px-5 py-2.5 rounded-xl text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center gap-2 shadow-md transition-all active:scale-95" onClick={onCompleteAndNext} >
            <span>{nextLesson ? 'Mark Complete & Next' : 'Unlock Module Mastery Gate 🛡️'}</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
