import React, { useState } from 'react';
import { BookOpen, Clock, ArrowRight, Play, CheckCircle2, Flame, Bookmark, Sparkles, Compass } from 'lucide-react';
import { CourseSummary, ProgressPayload } from '../types';
import { soundService } from '../services/sound';

interface CourseCatalogProps {
  courses: CourseSummary[];
  progress: ProgressPayload;
  onSelectCourse: (courseId: string) => void;
  onResumeLastPosition?: () => void;
  onOpenFlashcards?: () => void;
  onOpenPortfolio?: () => void;
}

export const CourseCatalog: React.FC<CourseCatalogProps> = ({
  courses,
  progress,
  onSelectCourse,
  onResumeLastPosition,
  onOpenFlashcards,
  onOpenPortfolio,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const categories = ['All', ...Array.from(new Set(courses.map((c) => c.category)))];

  const filteredCourses = selectedCategory === 'All'
    ? courses
    : courses.filter((c) => c.category === selectedCategory);

  const totalLessonsDone = progress.completed_lessons.length;
  const currentCourse = courses.find((c) => c.id === progress.current_course) || courses[0];
  const lastPos = progress.last_position;

  // Compute total curriculum words and labs
  const totalCurriculumWords = React.useMemo(() => {
    return courses.reduce((acc, c) => acc + (c.total_words || 0), 0);
  }, [courses]);

  const totalCurriculumLabs = React.useMemo(() => {
    return courses.reduce((acc, c) => acc + (c.debug_lab_count || 0), 0);
  }, [courses]);

  // Compute Spaced Repetition (SRS) cards due today
  const dueCardsCount = React.useMemo(() => {
    const customCards = progress.srs_custom_cards || [];
    const totalCardIds = [
      ...customCards.map((c) => c.id),
      ...Array.from({ length: 22 }, (_, i) => `srs-${(i + 1).toString().padStart(2, '0')}`),
    ];
    return totalCardIds.filter((id) => {
      const rev = progress.srs_card_reviews?.[id];
      return !rev || rev.next_review_epoch <= Date.now();
    }).length;
  }, [progress.srs_custom_cards, progress.srs_card_reviews]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      {/* Editorial Overview Header */}
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800/90 p-8 sm:p-10 shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-100 dark:border-zinc-800/80 pb-6">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span className="text-xs font-mono text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
              12 High-Performance Systems Tracks
            </span>
          </div>

          <div className="text-xs font-mono text-zinc-500 dark:text-zinc-400 space-x-2">
            <span>{totalCurriculumWords > 0 ? `~${Math.round(totalCurriculumWords / 1000)}k WORDS` : '1,018k WORDS'}</span>
            <span className="text-zinc-300 dark:text-zinc-700">/</span>
            <span>{totalCurriculumLabs > 0 ? `${totalCurriculumLabs} BUG LABS` : '171 BUG LABS'}</span>
            <span className="text-zinc-300 dark:text-zinc-700">/</span>
            <span>1,609 VERIFIED TESTS</span>
          </div>
        </div>

        <div className="max-w-4xl space-y-3">
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            AI Systems Mastery
          </h1>

          <p className="text-sm sm:text-base text-zinc-600 dark:text-zinc-400 leading-relaxed font-normal">
            From bare-metal CPython memory layout, cache-line B-Trees, and Raft consensus engines up to Triton FP8 kernels, Megatron 3D parallelism, vLLM PagedAttention, and multi-agent cognitive swarms.
          </p>

          <p className="text-xs sm:text-sm text-zinc-500 dark:text-zinc-400 font-normal leading-relaxed pt-1">
            <strong className="text-zinc-900 dark:text-zinc-200 font-semibold">Built for all types of learners:</strong> This curriculum is curated for everyone who is interested—from beginners taking their first steps with interactive playgrounds to senior practitioners and research engineers mastering complex distributed systems.
          </p>
        </div>

        <div className="pt-2 flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-3">
            {currentCourse && (
              <button
                onClick={() => {
                  soundService.playClick();
                  onSelectCourse(currentCourse.id);
                }}
                className="px-5 py-2.5 rounded-lg font-medium text-xs bg-blue-600 hover:bg-blue-500 text-white transition-colors flex items-center gap-2 shadow-sm"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                Resume Curriculum ({currentCourse.title.split(' ')[0]})
              </button>
            )}

            <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800/70 border border-zinc-200/70 dark:border-zinc-700/60 text-xs text-zinc-700 dark:text-zinc-300 font-medium">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
              <span>{totalLessonsDone} Completed</span>
            </div>

            {onOpenFlashcards && (
              <button
                onClick={() => {
                  soundService.playClick();
                  onOpenFlashcards();
                }}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-200/70 dark:border-amber-800/60 text-xs text-amber-700 dark:text-amber-300 font-medium hover:bg-amber-100 transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                <span>Flashcards (SRS)</span>
                {dueCardsCount > 0 && (
                  <span className="px-1.5 py-0.5 rounded-full bg-amber-500 text-zinc-950 font-bold text-xs">
                    {dueCardsCount}
                  </span>
                )}
              </button>
            )}

            {onOpenPortfolio && (
              <button
                onClick={() => {
                  soundService.playClick();
                  onOpenPortfolio();
                }}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200/70 dark:border-indigo-800/60 text-xs text-indigo-700 dark:text-indigo-300 font-medium hover:bg-indigo-100 transition-colors"
              >
                <Compass className="w-3.5 h-3.5 text-indigo-500" />
                <span>Transcript</span>
              </button>
            )}
          </div>

          <div className="text-xs text-zinc-400 font-mono">
            Local sync active · Auto-saving to .study_progress.json
          </div>
        </div>
      </div>

      {/* Spaced Repetition Due Today Hero Card */}
      {onOpenFlashcards && dueCardsCount > 0 && (
        <div className="rounded-2xl bg-gradient-to-r from-amber-500/10 via-orange-500/10 to-amber-500/5 border border-amber-500/30 p-6 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-xl bg-amber-500/20 text-amber-500 border border-amber-500/30 shrink-0">
              <Sparkles className="w-6 h-6" />
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono uppercase tracking-wider text-amber-600 dark:text-amber-400 font-bold">
                  Daily Review · SuperMemo SM-2
                </span>
                <span className="px-2 py-0.5 rounded-full text-xs font-mono bg-amber-500/20 text-amber-600 dark:text-amber-400 font-bold">
                  {dueCardsCount} Due Today
                </span>
              </div>
              <h3 className="text-base sm:text-lg font-bold text-zinc-900 dark:text-zinc-100">
                You have {dueCardsCount} flashcard{dueCardsCount > 1 ? 's' : ''} scheduled for review today
              </h3>
              <p className="text-xs text-zinc-500 dark:text-zinc-400">
                Reinforce consensus protocols, storage engine internals, and recently missed quiz questions with active recall.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <button
              onClick={() => {
                soundService.playClick();
                onOpenFlashcards();
              }}
              className="px-5 py-2.5 rounded-xl font-bold text-xs bg-amber-500 hover:bg-amber-400 text-zinc-950 transition-all shadow-md flex items-center gap-2 active:scale-95"
            >
              <Sparkles className="w-4 h-4 fill-current" />
              <span>Start Daily Review ({dueCardsCount})</span>
            </button>
          </div>
        </div>
      )}

      {/* Jump Back In Hero Card */}
      {lastPos && (
        <div className="rounded-2xl bg-gradient-to-r from-emerald-500/10 via-teal-500/10 to-blue-500/10 border border-emerald-500/30 p-6 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
              <span className="text-xs font-mono uppercase tracking-wider text-emerald-600 dark:text-emerald-400 font-bold">
                Jump Back In · Active Session
              </span>
            </div>
            <h3 className="text-base sm:text-lg font-bold text-zinc-900 dark:text-zinc-100">
              {lastPos.lesson_title || 'Resume Active Lesson'}
            </h3>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              Course: <span className="font-medium text-zinc-700 dark:text-zinc-300">{lastPos.course_title || lastPos.course_id}</span>
              {lastPos.module_title && ` • Module: ${lastPos.module_title}`}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                soundService.playSuccess();
                if (onResumeLastPosition) {
                  onResumeLastPosition();
                } else {
                  onSelectCourse(lastPos.course_id);
                }
              }}
              className="px-5 py-2.5 rounded-xl font-bold text-xs bg-emerald-600 hover:bg-emerald-500 text-white transition-all shadow-md flex items-center gap-2 active:scale-95"
            >
              <Play className="w-4 h-4 fill-current" />
              Resume Where You Left Off
            </button>
          </div>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider font-mono">
            Curriculum Catalog <span className="text-zinc-400 font-normal">({filteredCourses.length})</span>
          </h2>
        </div>

        <div className="inline-flex flex-wrap gap-1 p-1 rounded-lg bg-zinc-100 dark:bg-zinc-800/50 border border-zinc-200/70 dark:border-zinc-800">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-md text-xs transition-colors font-medium ${
                selectedCategory === cat
                  ? 'bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100 shadow-[0_1px_2px_rgba(0,0,0,0.05)] font-semibold'
                  : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Courses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredCourses.map((course) => {
          return (
            <div
              key={course.id}
              onClick={() => onSelectCourse(course.id)}
              className="group cursor-pointer rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 hover:border-zinc-400 dark:hover:border-zinc-700 p-6 transition-all flex flex-col justify-between shadow-[0_1px_3px_rgba(0,0,0,0.02)]"
            >
              <div className="space-y-3.5">
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800/80 text-zinc-700 dark:text-zinc-300 border border-zinc-200/60 dark:border-zinc-700/60">
                      Track {course.course_num.toString().padStart(2, '0')}
                    </span>
                    {course.depth_badge && (
                      <span className={`text-[11px] font-mono px-2 py-0.5 rounded-full border ${
                        course.depth_badge.includes('Comprehensive')
                          ? 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/30'
                          : course.depth_badge.includes('Deep')
                          ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/30'
                          : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
                      }`}>
                        {course.depth_badge}
                      </span>
                    )}
                  </div>
                  <span className="text-xs text-zinc-500 dark:text-zinc-400 font-medium">
                    {course.difficulty}
                  </span>
                </div>

                <h3 className="font-semibold text-base text-zinc-900 dark:text-zinc-100 group-hover:text-blue-600 transition-colors leading-snug">
                  {course.title}
                </h3>

                <p className="text-xs text-zinc-600 dark:text-zinc-400 line-clamp-3 leading-relaxed">
                  {course.description}
                </p>
              </div>

              <div className="pt-5 mt-6 border-t border-zinc-100 dark:border-zinc-800/70 flex items-center justify-between text-xs text-zinc-500">
                <div className="flex flex-wrap items-center gap-2.5">
                  <span className="flex items-center gap-1 font-mono text-xs" title={`${course.module_count} Modules across track`}>
                    <BookOpen className="w-3.5 h-3.5 text-zinc-400" />
                    {course.module_count} Mods
                  </span>
                  <span className="flex items-center gap-1 font-mono text-xs" title={`${course.reading_hours || 0}h reading + ${course.lab_hours || 0}h practical labs`}>
                    <Clock className="w-3.5 h-3.5 text-zinc-400" />
                    ~{course.estimated_hours}h
                  </span>
                  {course.total_words ? (
                    <span className="font-mono text-xs text-zinc-400">
                      ~{Math.round(course.total_words / 1000)}k words
                    </span>
                  ) : null}
                  {course.debug_lab_count !== undefined && course.debug_lab_count > 0 ? (
                    <span className="font-mono text-xs text-rose-500/90 dark:text-rose-400">
                      {course.debug_lab_count} labs
                    </span>
                  ) : null}
                </div>

                <span className="text-zinc-700 dark:text-zinc-300 group-hover:text-blue-600 font-medium flex items-center gap-1 transition-colors text-xs shrink-0">
                  View Syllabus <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
