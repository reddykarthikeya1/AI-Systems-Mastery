import React, { useRef } from 'react';
import { 
  ArrowLeft, BookOpen, CheckCircle, Clock, ChevronRight, ChevronDown, Play, Terminal, 
  Hammer, CheckSquare, Bug, Award, Sparkles, Layers, Zap, Brain, ShieldCheck 
} from 'lucide-react';
import { CourseSummary, ModuleItem, ProgressPayload, LessonItem } from '../types';
import { renderMarkdownWithMath } from '../services/markdown';
import { useMermaid } from '../hooks/useMermaid';
import { handleMarkdownLinkClick } from '../services/linkInterceptor';

interface SyllabusViewProps {
  course: CourseSummary;
  modules: ModuleItem[];
  progress: ProgressPayload;
  onBack: () => void;
  onSelectLesson: (filePath: string, lessonId: string, initialTab?: string) => void;
  onOpenMasteryGate?: (module: ModuleItem) => void;
  onRunCourseDemo?: () => void;
}

export const SyllabusView: React.FC<SyllabusViewProps> = ({
  course,
  modules,
  progress,
  onBack,
  onSelectLesson,
  onOpenMasteryGate,
  onRunCourseDemo,
}) => {
  const syllabusRef = useRef<HTMLDivElement>(null);
  useMermaid(syllabusRef, [course]);
  // Calculate aggregate course progress
  const allCourseLessons: LessonItem[] = modules.flatMap((m) => m.lessons);
  const totalLessons = allCourseLessons.length;
  const completedCourseLessons = allCourseLessons.filter((l) => progress.completed_lessons.includes(l.id)).length;
  const overallPercentage = totalLessons > 0 ? Math.round((completedCourseLessons / totalLessons) * 100) : 0;

  // Count interactive labs in this course
  const totalProjects = modules.filter((m) => m.has_starter || m.has_solution || m.lessons.some((l) => l.type === 'project')).length;
  const totalQuizzes = modules.filter((m) => (m.quiz_question_count ?? 0) > 0 || m.lessons.some((l) => l.type === 'quiz') || true).length;
  const totalDebugLabs = modules.filter((m) => m.has_debug_lab).length;

  // Track collapsed/expanded state for each module card
  // By default, expand the first incomplete module (or the first module if all are completed)
  const [expandedModules, setExpandedModules] = React.useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    if (modules.length > 0) {
      const firstIncomplete = modules.find((m) => {
        const completed = m.lessons.filter((l) => progress.completed_lessons.includes(l.id)).length;
        return m.lessons.length > 0 && completed < m.lessons.length;
      });
      const activeId = firstIncomplete ? firstIncomplete.id : modules[0].id;
      initial[activeId] = true;
    }
    return initial;
  });

  const toggleModule = (modId: string) => {
    setExpandedModules((prev) => ({
      ...prev,
      [modId]: !prev[modId],
    }));
  };

  const expandAll = () => {
    const all: Record<string, boolean> = {};
    modules.forEach((m) => {
      all[m.id] = true;
    });
    setExpandedModules(all);
  };

  const collapseAll = () => {
    setExpandedModules({});
  };

  const getLessonTypeBadge = (type: string) => {
    switch (type) {
      case 'project':
        return (
          <span className="px-2 py-0.5 rounded text-xs font-mono font-medium bg-purple-100 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800 flex items-center gap-1">
            <Hammer className="w-2.5 h-2.5" /> Project Studio
          </span>
        );
      case 'quiz':
        return (
          <span className="px-2 py-0.5 rounded text-xs font-mono font-medium bg-amber-100 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800 flex items-center gap-1">
            <CheckSquare className="w-2.5 h-2.5" /> Graded MCQ
          </span>
        );
      case 'playground':
        return (
          <span className="px-2 py-0.5 rounded text-xs font-mono font-medium bg-cyan-100 dark:bg-cyan-950/60 text-cyan-700 dark:text-cyan-300 border border-cyan-200 dark:border-cyan-800 flex items-center gap-1">
            <Sparkles className="w-2.5 h-2.5" /> Playground
          </span>
        );
      case 'troubleshooting':
        return (
          <span className="px-2 py-0.5 rounded text-xs font-mono font-medium bg-rose-100 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800 flex items-center gap-1">
            <Bug className="w-2.5 h-2.5" /> Forensics
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded text-xs font-mono font-medium bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-900/40 flex items-center gap-1">
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
    <div className="w-full max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 xl:px-10 py-8 space-y-8">
      {/* Navigation Header */}
      <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 inline-flex items-center gap-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200 transition-colors" onClick={onBack} >
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Catalog
      </button>

      {/* Course Banner */}
      <div className="rounded-xl bg-surface border border-border/80 p-8 shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-6">
        <div className="flex flex-wrap items-center gap-2.5">
          <span className="text-xs font-mono font-semibold px-2.5 py-1 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-zinc-200 border border-zinc-200/80 dark:border-zinc-700">
            Track {(course.course_num ?? 1).toString().padStart(2, '0')}
          </span>
          <span className="text-xs font-mono px-2.5 py-1 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
            {course.category}
          </span>
          <span className="text-xs font-mono px-2.5 py-1 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
            {course.difficulty} Standard
          </span>
          <span className="text-xs font-mono px-2.5 py-1 rounded bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60 flex items-center gap-1">
            <Clock className="w-3 h-3" /> ~{course.estimated_hours} Hours Total
          </span>
        </div>

        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            {course.title}
          </h1>
          <div
            ref={syllabusRef}
            onClick={(e) => handleMarkdownLinkClick(e, { courseId: course.id, onSelectLesson })}
            className="text-sm text-zinc-600 dark:text-zinc-400 max-w-4xl leading-relaxed mt-2 [&>p]:inline [&>p]:m-0"
            dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(course.description) }}
          />
        </div>

        {/* Course Progress & Interactive Features Overview Bar */}
        <div className="pt-4 border-t border-zinc-100 dark:border-zinc-800/80 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-3.5 rounded-lg bg-zinc-50 dark:bg-zinc-950/60 border border-zinc-200/70 dark:border-zinc-800">
            <div className="text-xs font-mono text-zinc-400 uppercase">Track Completion</div>
            <div className="flex items-center justify-between mt-1">
              <span className="text-base font-bold text-fg">{overallPercentage}%</span>
              <span className="text-xs font-mono text-zinc-500">{completedCourseLessons}/{totalLessons} Lessons</span>
            </div>
            <div className="w-full h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full mt-2 overflow-hidden">
              <div 
                className="h-full bg-blue-600 rounded-full transition-all duration-500" 
                style={{ width: `${overallPercentage}%` }} 
              />
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-zinc-50 dark:bg-zinc-950/60 border border-zinc-200/70 dark:border-zinc-800 flex items-center gap-3">
            <div className="p-2 rounded-md bg-purple-100 dark:bg-purple-950/60 text-purple-600 dark:text-purple-300">
              <Hammer className="w-4 h-4" />
            </div>
            <div>
              <div className="text-sm font-bold text-fg">{totalProjects} Studios</div>
              <div className="text-xs text-zinc-500">In-Browser IDE Builds</div>
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-zinc-50 dark:bg-zinc-950/60 border border-zinc-200/70 dark:border-zinc-800 flex items-center gap-3">
            <div className="p-2 rounded-md bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-300">
              <CheckSquare className="w-4 h-4" />
            </div>
            <div>
              <div className="text-sm font-bold text-fg">{totalQuizzes} Assessments</div>
              <div className="text-xs text-zinc-500">Staff Interview MCQs</div>
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-zinc-50 dark:bg-zinc-950/60 border border-zinc-200/70 dark:border-zinc-800 flex items-center gap-3">
            <div className="p-2 rounded-md bg-rose-100 dark:bg-rose-950/60 text-rose-600 dark:text-rose-300">
              <Bug className="w-4 h-4" />
            </div>
            <div>
              <div className="text-sm font-bold text-fg">{totalDebugLabs} Bug Labs</div>
              <div className="text-xs text-zinc-500">Planted Defect Triages</div>
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
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 rounded-lg text-xs font-medium bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-white transition-colors flex items-center gap-2 shadow-sm" onClick={onRunCourseDemo} >
              <Terminal className="w-3.5 h-3.5" /> Run Interactive Track Benchmark
            </button>
          </div>
        )}
      </div>

      {/* Modules List */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <h2 className="text-xs font-mono font-semibold uppercase tracking-wider text-zinc-500 flex items-center gap-2">
              Curriculum Modules <span className="font-normal text-zinc-400">({modules.length} Total)</span>
            </h2>
            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={expandAll}
                className="text-[11px] font-mono px-2.5 py-0.5 rounded-md border border-border bg-surface hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-300 transition-colors shadow-xs"
                title="Expand all module cards"
              >
                Expand All
              </button>
              <button
                type="button"
                onClick={collapseAll}
                className="text-[11px] font-mono px-2.5 py-0.5 rounded-md border border-border bg-surface hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-300 transition-colors shadow-xs"
                title="Collapse all module cards"
              >
                Collapse All
              </button>
            </div>
          </div>
          <span className="text-xs text-zinc-400 font-mono">
            {completedCourseLessons}/{totalLessons} Lessons Finished
          </span>
        </div>

        <div className="space-y-4">
          {modules.map((mod) => {
            const isExpanded = Boolean(expandedModules[mod.id]);
            const completedCount = mod.lessons.filter((l) => progress.completed_lessons.includes(l.id)).length;
            const isCompleted = mod.lessons.length > 0 && completedCount === mod.lessons.length;
            const modPercentage = mod.lessons.length > 0 ? Math.round((completedCount / mod.lessons.length) * 100) : 0;
            const estHours = Math.max(1, Math.round(mod.lessons.length * 0.5));

            // Module interactive feature flags
            const modHasProject = Boolean(mod.has_starter || mod.has_solution || mod.lessons.some((l) => l.type === 'project'));
            const modHasQuiz = Boolean((mod.quiz_question_count ?? 0) > 0 || mod.lessons.some((l) => l.type === 'quiz') || true);
            const modHasDebug = Boolean(mod.has_debug_lab);
            const leetcodeLesson = mod.lessons.find((l) => l.type === 'challenge' || l.title.toLowerCase().includes('leetcode') || l.file_path.toLowerCase().includes('leetcode'));
            const modHasLeetcode = Boolean(
              leetcodeLesson ||
              course.folder_name.includes('02_Data_Structures') ||
              mod.folder_path.includes('02_Data_Structures')
            );

            // Find specific entry points
            const firstLesson = mod.lessons[0];
            const projectLesson = mod.lessons.find((l) => l.type === 'project');
            const quizLesson = mod.lessons.find((l) => l.type === 'quiz');

            return (
              <div
                key={mod.id}
                className="rounded-xl bg-surface border border-border/80 overflow-hidden transition-all hover:border-zinc-300 dark:hover:border-zinc-700 shadow-sm"
              >
                {/* Module Header Card - Accordion Toggle */}
                <div 
                  onClick={() => toggleModule(mod.id)}
                  className={`p-5 sm:p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 cursor-pointer select-none transition-colors ${
                    isExpanded 
                      ? 'border-b border-zinc-100 dark:border-zinc-800/70 bg-gradient-to-r from-transparent via-transparent to-zinc-50/50 dark:to-zinc-950/30' 
                      : 'hover:bg-zinc-50/60 dark:hover:bg-zinc-900/30'
                  }`}
                >
                  <div className="space-y-2 max-w-2xl">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="p-1 rounded-md bg-zinc-100 dark:bg-zinc-800 text-zinc-500 mr-0.5 inline-flex items-center justify-center">
                        <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-200 ${isExpanded ? 'rotate-180 text-sky-500' : 'text-zinc-400'}`} />
                      </span>
                      <span className="text-xs font-mono font-semibold text-zinc-500 uppercase tracking-wider">
                        Module {mod.module_num.toString().padStart(2, '0')}
                      </span>
                      <span className="text-xs font-mono text-zinc-400">
                        {mod.reading_minutes ? `⏱️ ~${mod.reading_minutes}m read` : `~${estHours} hrs`}
                      </span>

                      {/* Interactive Feature Badges */}
                      {modHasLeetcode && (
                        <span className="px-1.5 py-0.5 rounded text-xs font-mono bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60 font-semibold">
                          🧠 LeetCode Arena
                        </span>
                      )}
                      {modHasProject && (
                        <span className="px-1.5 py-0.5 rounded text-xs font-mono bg-purple-50 dark:bg-purple-950/50 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800/60">
                          🛠️ Project Studio
                        </span>
                      )}
                      {modHasQuiz && (
                        <span className="px-1.5 py-0.5 rounded text-xs font-mono bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60">
                          📝 Graded Quiz {mod.quiz_question_count ? `(${mod.quiz_question_count} Qs)` : ''}
                        </span>
                      )}
                      {modHasDebug && (
                        <span className="px-1.5 py-0.5 rounded text-xs font-mono bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800/60">
                          🐛 Bug Lab
                        </span>
                      )}
                      {mod.quickstart_script && (
                        <span className="px-1.5 py-0.5 rounded text-xs font-mono bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60">
                          ⚡ Live Demo
                        </span>
                      )}
                      {Boolean(progress.mastery_gates?.[mod.id]?.cleared || progress.completed_modules?.includes(mod.id)) ? (
                        <span className="px-2 py-0.5 rounded text-xs font-mono bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold flex items-center gap-1">
                          <ShieldCheck className="w-3 h-3" /> Mastered
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded text-xs font-mono bg-zinc-100 dark:bg-zinc-800 text-zinc-500 border border-zinc-200 dark:border-zinc-700 flex items-center gap-1">
                          Gate Pending
                        </span>
                      )}
                    </div>

                    <h3 className="font-semibold text-base sm:text-lg text-fg">
                      {mod.title}
                    </h3>

                    <div className="flex items-center gap-3 pt-1">
                      <div className="w-36 h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-emerald-500 rounded-full transition-all" 
                          style={{ width: `${modPercentage}%` }} 
                        />
                      </div>
                      <span className="text-xs font-mono text-zinc-500">
                        {completedCount}/{mod.lessons.length} completed ({modPercentage}%)
                      </span>
                      <span className="text-xs font-mono text-sky-600 dark:text-sky-400 font-medium">
                        {isExpanded ? '• Collapse' : `• ${mod.lessons.length} Lessons`}
                      </span>
                    </div>
                  </div>

                  {/* Module Direct Action Launchers */}
                  <div className="flex flex-wrap items-center gap-2 self-start md:self-auto">
                    {modHasProject && (projectLesson || firstLesson) && (
                      <button 
                        className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-lg text-xs font-medium border border-purple-300 dark:border-purple-800 bg-purple-50 dark:bg-purple-950/50 text-purple-700 dark:text-purple-300 hover:bg-purple-100 dark:hover:bg-purple-900/60 transition-colors flex items-center gap-1.5" 
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectLesson((projectLesson || firstLesson).file_path, (projectLesson || firstLesson).id, 'project');
                        }}
                        title="Jump straight into Guided Project Studio" 
                      >
                        <Hammer className="w-3 h-3" />
                        <span>Studio</span>
                      </button>
                    )}

                    {modHasQuiz && firstLesson && (
                      <button 
                        className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-lg text-xs font-medium border border-amber-300 dark:border-amber-800 bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 hover:bg-amber-100 dark:hover:bg-amber-900/60 transition-colors flex items-center gap-1.5" 
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectLesson((quizLesson || firstLesson).file_path, (quizLesson || firstLesson).id, 'quiz');
                        }}
                        title="Take Graded MCQ Assessment" 
                      >
                        <CheckSquare className="w-3 h-3" />
                        <span>Quiz</span>
                      </button>
                    )}

                    {modHasDebug && firstLesson && (
                      <button 
                        className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-lg text-xs font-semibold border border-rose-300 dark:border-rose-800 bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 hover:bg-rose-100 dark:hover:bg-rose-900/60 transition-colors flex items-center gap-1.5" 
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectLesson(firstLesson.file_path, firstLesson.id, 'debug');
                        }}
                        title="Diagnose planted production defect in Bug Hunter Lab" 
                      >
                        <Bug className="w-3.5 h-3.5 text-rose-500" />
                        <span>Bug Lab</span>
                      </button>
                    )}

                    {modHasLeetcode && (leetcodeLesson || firstLesson) && (
                      <button 
                        className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-lg text-xs font-bold border border-amber-400/80 dark:border-amber-600 bg-amber-500/10 hover:bg-amber-500/20 text-amber-600 dark:text-amber-400 transition-colors flex items-center gap-1.5 shadow-sm" 
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectLesson((leetcodeLesson || firstLesson).file_path, (leetcodeLesson || firstLesson).id, 'arena');
                        }}
                        title="Solve LeetCode problems with hidden testcases" 
                      >
                        <Brain className="w-3.5 h-3.5" />
                        <span>Arena</span>
                      </button>
                    )}

                    {onOpenMasteryGate && (
                      <button 
                        className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-colors flex items-center gap-1.5 ${
                          Boolean(progress.mastery_gates?.[mod.id]?.cleared || progress.completed_modules?.includes(mod.id))
                            ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20'
                            : 'border-zinc-300 dark:border-zinc-700 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                        }`} 
                        onClick={(e) => {
                          e.stopPropagation();
                          onOpenMasteryGate(mod);
                        }}
                        title="View Module Mastery Gate Requirements" 
                      >
                        <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                        <span>Gate</span>
                      </button>
                    )}

                    {firstLesson && (
                      <button 
                        className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium bg-blue-600 hover:bg-blue-500 text-white transition-colors flex items-center gap-1.5 shadow-sm" 
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectLesson(firstLesson.file_path, firstLesson.id);
                        }} 
                      >
                        <Play className="w-3 h-3 fill-current" />
                        <span>{completedCount > 0 ? 'Continue' : 'Open Module'}</span>
                      </button>
                    )}

                    {/* Explicit Expand / Collapse Pill */}
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleModule(mod.id);
                      }}
                      className="px-2.5 py-1.5 rounded-lg text-xs font-medium border border-border bg-surface hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-300 transition flex items-center gap-1.5 shadow-xs"
                      title={isExpanded ? 'Collapse lessons' : 'Expand lessons'}
                    >
                      <span>{isExpanded ? 'Collapse' : `${mod.lessons.length} Lessons`}</span>
                      <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`} />
                    </button>
                  </div>
                </div>

                {/* Sub-lessons list with detailed type badges and durations */}
                {isExpanded && (
                  <div className="divide-y divide-border bg-slate-100/60 dark:bg-slate-900/60 border-t border-border animate-in fade-in duration-150">
                    {mod.lessons.map((lesson) => {
                      const done = progress.completed_lessons.includes(lesson.id);
                      return (
                        <div
                          key={lesson.id}
                          onClick={() => onSelectLesson(lesson.file_path, lesson.id)}
                          title={lesson.title}
                          className="px-5 sm:px-6 py-3.5 flex items-center justify-between hover:bg-white dark:hover:bg-slate-800/70 cursor-pointer transition-colors group"
                        >
                          <div className="flex items-center gap-3 min-w-0 pr-4">
                            <div className={`w-2.5 h-2.5 rounded-full shrink-0 ${done ? 'bg-emerald-500' : 'bg-slate-300 dark:bg-slate-600'}`} />
                            <span className="text-xs font-medium text-fg line-clamp-1 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                              {lesson.title}
                            </span>
                          </div>

                          <div className="flex items-center gap-3 shrink-0">
                            {getLessonTypeBadge(lesson.type)}
                            <span className="text-xs font-mono text-fg-subtle hidden sm:inline">
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
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
