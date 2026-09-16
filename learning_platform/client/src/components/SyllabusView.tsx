import React from 'react';
import { ArrowLeft, BookOpen, CheckCircle, Clock, ChevronRight, Play, Terminal } from 'lucide-react';
import { CourseSummary, ModuleItem, ProgressPayload } from '../types';

interface SyllabusViewProps {
  course: CourseSummary;
  modules: ModuleItem[];
  progress: ProgressPayload;
  onBack: () => void;
  onSelectLesson: (filePath: string, lessonId: string) => void;
  onRunCourseDemo?: () => void;
}

export const SyllabusView: React.FC<SyllabusViewProps> = ({
  course,
  modules,
  progress,
  onBack,
  onSelectLesson,
  onRunCourseDemo,
}) => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Navigation Header */}
      <button
        onClick={onBack}
        className="inline-flex items-center gap-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Catalog
      </button>

      {/* Course Banner */}
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 p-8 shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-4">
        <div className="flex flex-wrap items-center gap-2.5">
          <span className="text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-zinc-200 border border-zinc-200/80 dark:border-zinc-700">
            Track {course.course_num.toString().padStart(2, '0')}
          </span>
          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
            {course.category}
          </span>
          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
            {course.difficulty} Standard
          </span>
        </div>

        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
          {course.title}
        </h1>

        <p className="text-sm text-zinc-600 dark:text-zinc-400 max-w-4xl leading-relaxed">
          {course.description}
        </p>

        {course.quickstart_script && onRunCourseDemo && (
          <div className="pt-2">
            <button
              onClick={onRunCourseDemo}
              className="px-4 py-2 rounded-lg text-xs font-medium bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-white transition-colors flex items-center gap-2 shadow-sm"
            >
              <Terminal className="w-3.5 h-3.5" /> Run Interactive Track Benchmark
            </button>
          </div>
        )}
      </div>

      {/* Modules List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-mono font-semibold uppercase tracking-wider text-zinc-500 flex items-center gap-2">
            Curriculum Modules <span className="font-normal text-zinc-400">({modules.length} Modules)</span>
          </h2>
        </div>

        <div className="space-y-3">
          {modules.map((mod) => {
            const completedCount = mod.lessons.filter((l) => progress.completed_lessons.includes(l.id)).length;
            const isCompleted = mod.lessons.length > 0 && completedCount === mod.lessons.length;

            return (
              <div
                key={mod.id}
                className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 overflow-hidden transition-colors"
              >
                <div className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-zinc-100 dark:border-zinc-800/70">
                  <div className="flex items-start gap-3">
                    <div className={`mt-0.5 p-1 rounded-full ${isCompleted ? 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950/40' : 'text-zinc-400 bg-zinc-100 dark:bg-zinc-800'}`}>
                      <CheckCircle className="w-4 h-4" />
                    </div>
                    <div>
                      <span className="text-[11px] font-mono font-medium text-zinc-400">
                        Module {mod.module_num.toString().padStart(2, '0')}
                      </span>
                      <h3 className="font-semibold text-sm sm:text-base text-zinc-900 dark:text-zinc-100 mt-0.5">
                        {mod.title}
                      </h3>
                      <p className="text-[11px] text-zinc-500 mt-0.5 font-mono">
                        {completedCount} of {mod.lessons.length} lessons completed
                      </p>
                    </div>
                  </div>

                  {mod.lessons.length > 0 && (
                    <button
                      onClick={() => onSelectLesson(mod.lessons[0].file_path, mod.lessons[0].id)}
                      className="px-3.5 py-1.5 rounded-md text-xs font-medium bg-coursera-blue hover:bg-blue-700 text-white transition-colors flex items-center gap-1.5 self-start md:self-auto shadow-sm"
                    >
                      <Play className="w-3 h-3 fill-current" />
                      Start Module
                    </button>
                  )}
                </div>

                {/* Sub-lessons list */}
                <div className="divide-y divide-zinc-100 dark:divide-zinc-800/60 bg-zinc-50/40 dark:bg-zinc-900/30">
                  {mod.lessons.map((lesson) => {
                    const done = progress.completed_lessons.includes(lesson.id);
                    return (
                      <div
                        key={lesson.id}
                        onClick={() => onSelectLesson(lesson.file_path, lesson.id)}
                        className="px-5 py-3 flex items-center justify-between hover:bg-zinc-100/70 dark:hover:bg-zinc-800/50 cursor-pointer transition-colors"
                      >
                        <div className="flex items-center gap-2.5">
                          <div className={`w-1.5 h-1.5 rounded-full ${done ? 'bg-emerald-500' : 'bg-zinc-300 dark:bg-zinc-700'}`} />
                          <span className="text-xs font-normal text-zinc-700 dark:text-zinc-300">
                            {lesson.title}
                          </span>
                        </div>

                        <ChevronRight className="w-3.5 h-3.5 text-zinc-400" />
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
