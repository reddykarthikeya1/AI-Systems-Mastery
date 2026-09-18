import React from 'react';
import { CheckCircle2 } from 'lucide-react';
import { LessonItem } from '../../types';

interface SyllabusRailProps {
  moduleNum: number;
  allLessons: LessonItem[];
  currentLessonId: string;
  completedLessons: string[];
  onSelectLesson: (filePath: string, lessonId: string) => void;
  getLessonBadge: (type: string) => React.ReactNode;
}

export const SyllabusRail: React.FC<SyllabusRailProps> = ({
  moduleNum,
  allLessons,
  currentLessonId,
  completedLessons,
  onSelectLesson,
  getLessonBadge,
}) => {
  const completedCount = allLessons.filter((l) => completedLessons.includes(l.id)).length;

  return (
    <aside aria-label="Module syllabus sidebar" className="w-72 2xl:w-80 shrink-0 rounded-2xl bg-surface border border-border p-4 shadow-card space-y-3 sticky top-20">
      <div className="flex items-center justify-between border-b border-border pb-2">
        <span className="text-xs font-mono font-semibold text-fg uppercase tracking-wider">
          Module {moduleNum.toString().padStart(2, '0')} Syllabus
        </span>
        <span className="text-xs font-mono text-fg-subtle">
          {completedCount}/{allLessons.length}
        </span>
      </div>

      <nav aria-label="Module Lessons" className="space-y-1 max-h-[75vh] overflow-y-auto">
        {allLessons.map((l, idx) => {
          const active = l.id === currentLessonId;
          const isDone = completedLessons.includes(l.id);

          return (
            <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 w-full text-left px-2.5 py-2 rounded-xl text-xs transition-all flex items-center justify-between gap-2 ${
                active
                  ? 'bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 font-semibold border border-blue-300/80 dark:border-blue-800/70 shadow-xs'
                  : 'text-fg-muted hover:text-fg hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
              }`} key={l.id}
              onClick={() => onSelectLesson(l.file_path, l.id)}
              title={l.title}
              aria-label={`Lesson ${idx + 1}: ${l.title} ${isDone ? '(completed)' : ''}`} >
              <span className="line-clamp-1 flex items-center gap-2">
                <span className="font-mono text-xs text-fg-subtle shrink-0">
                  {(idx + 1).toString().padStart(2, '0')}
                </span>
                <span className="truncate">{l.title}</span>
              </span>
              <div className="flex items-center gap-1.5 shrink-0">
                {getLessonBadge(l.type)}
                {isDone ? (
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                ) : (
                  <div className="w-1.5 h-1.5 rounded-full bg-zinc-300 dark:bg-zinc-600 shrink-0" />
                )}
              </div>
            </button>
          );
        })}
      </nav>
    </aside>
  );
};
