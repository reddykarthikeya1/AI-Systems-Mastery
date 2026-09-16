import React from 'react';
import { 
  ArrowLeft, BookOpen, CheckCircle, Clock, ChevronRight, Play, Terminal, 
  Hammer, CheckSquare, Bug, Award, Sparkles, Layers, Zap 
} from 'lucide-react';
import { CourseSummary, ModuleItem, ProgressPayload, LessonItem } from '../types';

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
  // Calculate aggregate course progress
  const allCourseLessons: LessonItem[] = modules.flatMap((m) => m.lessons);
  const totalLessons = allCourseLessons.length;
  const completedCourseLessons = allCourseLessons.filter((l) => progress.completed_lessons.includes(l.id)).length;
  const overallPercentage = totalLessons > 0 ? Math.round((completedCourseLessons / totalLessons) * 100) : 0;

  // Count interactive labs in this course
  const totalProjects = modules.filter((m) => m.has_starter || m.has_solution || m.lessons.some((l) => l.type === 'project')).length;
  const totalQuizzes = modules.filter((m) => m.lessons.some((l) => l.type === 'quiz')).length;
  const totalDebugLabs = modules.filter((m) => m.has_debug_lab).length;

  const getLessonTypeBadge = (type: string) => {
    switch (type) {
      case 'project':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-purple-100 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800 flex items-center gap-1">
            <Hammer className="w-2.5 h-2.5" /> Project Studio
          </span>
        );
      case 'quiz':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-amber-100 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800 flex items-center gap-1">
            <CheckSquare className="w-2.5 h-2.5" /> Graded MCQ
          </span>
        );
      case 'playground':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-cyan-100 dark:bg-cyan-950/60 text-cyan-700 dark:text-cyan-300 border border-cyan-200 dark:border-cyan-800 flex items-center gap-1">
            <Sparkles className="w-2.5 h-2.5" /> Playground
          </span>
        );
      case 'troubleshooting':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-rose-100 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800 flex items-center gap-1">
            <Bug className="w-2.5 h-2.5" /> Forensics
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-900/40 flex items-center gap-1">
            <BookOpen className="w-2.5 h-2.5" /> Theory & Specs
          </span>
        );
    }
  };

  const getEstimatedLessonTime = (type: string) => {
    switch (type) {
      case 'project':
        return '45 min build';
      case 'quiz':
        return '15 min quiz';
      case 'playground':
        return '10 min demo';
      case 'troubleshooting':
        return '20 min triage';
      default:
        return '18 min read';
    }
  };

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
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 p-8 shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-6">
        <div className="flex flex-wrap items-center gap-2.5">
          <span className="text-[11px] font-mono font-semibold px-2.5 py-1 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-zinc-200 border border-zinc-200/80 dark:border-zinc-700">
            Track {course.course_num.toString().padStart(2, '0')}
          </span>
          <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
            {course.category}
          </span>
          <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
            {course.difficulty} Standard
          </span>
          <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60 flex items-center gap-1">
            <Clock className="w-3 h-3" /> ~{course.estimated_hours} Hours Total
          </span>
        </div>

        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            {course.title}
          </h1>
          <p className="text-sm text-zinc-600 dark:text-zinc-400 max-w-4xl leading-relaxed mt-2">
            {course.description}
          </p>
        </div>

        {/* Course Progress & Interactive Features Overview Bar */}
        <div className="pt-4 border-t border-zinc-100 dark:border-zinc-800/80 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-3.5 rounded-lg bg-zinc-50 dark:bg-zinc-950/60 border border-zinc-200/70 dark:border-zinc-800">
            <div className="text-[11px] font-mono text-zinc-400 uppercase">Track Completion</div>
            <div className="flex items-center justify-between mt-1">
              <span className="text-base font-bold text-zinc-900 dark:text-zinc-100">{overallPercentage}%</span>
              <span className="text-xs font-mono text-zinc-500">{completedCourseLessons}/{totalLessons} Lessons</span>
            </div>
            <div className="w-full h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full mt-2 overflow-hidden">
              <div 
                className="h-full bg-coursera-blue rounded-full transition-all duration-500" 
                style={{ width: `${overallPercentage}%` }} 
              />
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-zinc-50 dark:bg-zinc-950/60 border border-zinc-200/70 dark:border-zinc-800 flex items-center gap-3">
            <div className="p-2 rounded-md bg-purple-100 dark:bg-purple-950/60 text-purple-600 dark:text-purple-300">
              <Hammer className="w-4 h-4" />
            </div>
            <div>
              <div className="text-sm font-bold text-zinc-900 dark:text-zinc-100">{totalProjects} Studios</div>
              <div className="text-[11px] text-zinc-500">In-Browser IDE Builds</div>
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-zinc-50 dark:bg-zinc-950/60 border border-zinc-200/70 dark:border-zinc-800 flex items-center gap-3">
            <div className="p-2 rounded-md bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-300">
              <CheckSquare className="w-4 h-4" />
            </div>
            <div>
              <div className="text-sm font-bold text-zinc-900 dark:text-zinc-100">{totalQuizzes} Assessments</div>
              <div className="text-[11px] text-zinc-500">Staff Interview MCQs</div>
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-zinc-50 dark:bg-zinc-950/60 border border-zinc-200/70 dark:border-zinc-800 flex items-center gap-3">
            <div className="p-2 rounded-md bg-rose-100 dark:bg-rose-950/60 text-rose-600 dark:text-rose-300">
              <Bug className="w-4 h-4" />
            </div>
            <div>
              <div className="text-sm font-bold text-zinc-900 dark:text-zinc-100">{totalDebugLabs} Bug Labs</div>
              <div className="text-[11px] text-zinc-500">Planted Defect Triages</div>
            </div>
          </div>
        </div>

        {/* Flexible Learning Pathways Callout */}
        <div className="p-4 rounded-xl bg-blue-50/60 dark:bg-blue-950/30 border border-blue-200/70 dark:border-blue-900/50 flex items-start gap-3 text-xs text-blue-900 dark:text-blue-200">
          <Sparkles className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <span className="font-semibold">Self-Paced Architecture Pathway:</span> You do not need to follow modules in strict numerical order. Feel free to jump directly into whatever matches your engineering priorities: explore hands-on <strong>In-Browser Project Studios</strong>, test your depth with <strong>Staff Interview MCQs</strong>, or diagnose production race conditions in <strong>Bug Hunter Labs</strong>.
          </div>
        </div>

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
            Curriculum Modules <span className="font-normal text-zinc-400">({modules.length} Total)</span>
          </h2>
          <span className="text-[11px] text-zinc-400 font-mono">
            {completedCourseLessons}/{totalLessons} Lessons Finished
          </span>
        </div>

        <div className="space-y-4">
          {modules.map((mod) => {
            const completedCount = mod.lessons.filter((l) => progress.completed_lessons.includes(l.id)).length;
            const isCompleted = mod.lessons.length > 0 && completedCount === mod.lessons.length;
            const modPercentage = mod.lessons.length > 0 ? Math.round((completedCount / mod.lessons.length) * 100) : 0;
            const estHours = Math.max(1, Math.round(mod.lessons.length * 0.5));

            // Module interactive feature flags
            const modHasProject = Boolean(mod.has_starter || mod.has_solution || mod.lessons.some((l) => l.type === 'project'));
            const modHasQuiz = Boolean(mod.lessons.some((l) => l.type === 'quiz'));
            const modHasDebug = Boolean(mod.has_debug_lab);

            // Find specific entry points
            const firstLesson = mod.lessons[0];
            const projectLesson = mod.lessons.find((l) => l.type === 'project');
            const quizLesson = mod.lessons.find((l) => l.type === 'quiz');

            return (
              <div
                key={mod.id}
                className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 overflow-hidden transition-all hover:border-zinc-300 dark:hover:border-zinc-700 shadow-sm"
              >
                {/* Module Header Card */}
                <div className="p-5 sm:p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-zinc-100 dark:border-zinc-800/70 bg-gradient-to-r from-transparent via-transparent to-zinc-50/50 dark:to-zinc-950/30">
                  <div className="space-y-2 max-w-2xl">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-[11px] font-mono font-semibold text-zinc-500 uppercase tracking-wider">
                        Module {mod.module_num.toString().padStart(2, '0')}
                      </span>
                      <span className="text-[11px] font-mono text-zinc-400">
                        ~{estHours} hrs
                      </span>

                      {/* Interactive Feature Badges */}
                      {modHasProject && (
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-purple-50 dark:bg-purple-950/50 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800/60">
                          🛠️ Project Studio
                        </span>
                      )}
                      {modHasQuiz && (
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60">
                          📝 Graded Quiz
                        </span>
                      )}
                      {modHasDebug && (
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800/60">
                          🐛 Bug Lab
                        </span>
                      )}
                      {mod.quickstart_script && (
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60">
                          ⚡ Live Demo
                        </span>
                      )}
                    </div>

                    <h3 className="font-semibold text-base sm:text-lg text-zinc-900 dark:text-zinc-100">
                      {mod.title}
                    </h3>

                    <div className="flex items-center gap-3 pt-1">
                      <div className="w-36 h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-emerald-500 rounded-full transition-all" 
                          style={{ width: `${modPercentage}%` }} 
                        />
                      </div>
                      <span className="text-[11px] font-mono text-zinc-500">
                        {completedCount}/{mod.lessons.length} completed ({modPercentage}%)
                      </span>
                    </div>
                  </div>

                  {/* Module Direct Action Launchers */}
                  <div className="flex flex-wrap items-center gap-2 self-start md:self-auto">
                    {modHasProject && projectLesson && (
                      <button
                        onClick={() => onSelectLesson(projectLesson.file_path, projectLesson.id)}
                        className="px-3 py-1.5 rounded-lg text-xs font-medium border border-purple-300 dark:border-purple-800 bg-purple-50 dark:bg-purple-950/50 text-purple-700 dark:text-purple-300 hover:bg-purple-100 dark:hover:bg-purple-900/60 transition-colors flex items-center gap-1.5"
                        title="Jump straight into Guided Project Studio"
                      >
                        <Hammer className="w-3 h-3" />
                        <span>Studio</span>
                      </button>
                    )}

                    {modHasQuiz && quizLesson && (
                      <button
                        onClick={() => onSelectLesson(quizLesson.file_path, quizLesson.id)}
                        className="px-3 py-1.5 rounded-lg text-xs font-medium border border-amber-300 dark:border-amber-800 bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 hover:bg-amber-100 dark:hover:bg-amber-900/60 transition-colors flex items-center gap-1.5"
                        title="Take Graded MCQ Assessment"
                      >
                        <CheckSquare className="w-3 h-3" />
                        <span>Quiz</span>
                      </button>
                    )}

                    {firstLesson && (
                      <button
                        onClick={() => onSelectLesson(firstLesson.file_path, firstLesson.id)}
                        className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-coursera-blue hover:bg-blue-700 text-white transition-colors flex items-center gap-1.5 shadow-sm"
                      >
                        <Play className="w-3 h-3 fill-current" />
                        <span>{completedCount > 0 ? 'Continue' : 'Open Module'}</span>
                      </button>
                    )}
                  </div>
                </div>

                {/* Sub-lessons list with detailed type badges and durations */}
                <div className="divide-y divide-zinc-100 dark:divide-zinc-800/60 bg-zinc-50/40 dark:bg-zinc-900/30">
                  {mod.lessons.map((lesson) => {
                    const done = progress.completed_lessons.includes(lesson.id);
                    return (
                      <div
                        key={lesson.id}
                        onClick={() => onSelectLesson(lesson.file_path, lesson.id)}
                        className="px-5 sm:px-6 py-3.5 flex items-center justify-between hover:bg-zinc-100/70 dark:hover:bg-zinc-800/50 cursor-pointer transition-colors group"
                      >
                        <div className="flex items-center gap-3 min-w-0 pr-4">
                          <div className={`w-2 h-2 rounded-full shrink-0 ${done ? 'bg-emerald-500' : 'bg-zinc-300 dark:bg-zinc-700'}`} />
                          <span className="text-xs font-medium text-zinc-800 dark:text-zinc-200 line-clamp-1 group-hover:text-coursera-blue transition-colors">
                            {lesson.title}
                          </span>
                        </div>

                        <div className="flex items-center gap-3 shrink-0">
                          {getLessonTypeBadge(lesson.type)}
                          <span className="text-[11px] font-mono text-zinc-400 hidden sm:inline">
                            {getEstimatedLessonTime(lesson.type)}
                          </span>
                          {done ? (
                            <CheckCircle className="w-4 h-4 text-emerald-500" />
                          ) : (
                            <ChevronRight className="w-3.5 h-3.5 text-zinc-400 group-hover:translate-x-0.5 transition-transform" />
                          )}
                        </div>
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
