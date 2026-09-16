import React, { useEffect } from 'react';
import { Flame, Clock, CheckCircle2, Award, X, Zap, Target, BookOpen, Layers } from 'lucide-react';
import { ProgressPayload, CourseSummary } from '../types';

interface StudyStatsModalProps {
  isOpen: boolean;
  onClose: () => void;
  progress: ProgressPayload;
  courses: CourseSummary[];
}

export const StudyStatsModal: React.FC<StudyStatsModalProps> = ({
  isOpen,
  onClose,
  progress,
  courses,
}) => {
  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const streak = progress.study_streak_days || 1;
  const totalCompleted = progress.completed_lessons.length;
  const totalCurriculumLessons = 1296;
  const curriculumPercentage = Math.round((totalCompleted / totalCurriculumLessons) * 100);

  // Estimate hours: 18 mins per completed lesson
  const hoursSpent = Math.round((totalCompleted * 18) / 60);
  const totalCurriculumHours = 380;

  // Quizzes passed count
  const quizScores = progress.quiz_scores || {};
  const passedQuizzesCount = Object.values(quizScores).filter((q: any) => q.passed).length;

  const tiers = [
    {
      name: 'Tier 1: Software Craftsmanship & Distributed Systems',
      courses: 'Courses 01 – 04',
      courseIds: ['01_Advanced_Python', '02_Data_Structures_and_Algorithms', '03_Databases_and_Storage_Engines', '04_System_Design_and_Distributed_Systems'],
      color: 'bg-blue-500',
    },
    {
      name: 'Tier 2: Mathematical & Deep Learning Foundations',
      courses: 'Courses 05 – 06',
      courseIds: ['05_Mathematics_for_ML_and_AI', '06_Deep_Learning_and_AI_Foundations'],
      color: 'bg-emerald-500',
    },
    {
      name: 'Tier 3: GPU Kernels & Distributed Infrastructure',
      courses: 'Courses 07 – 09',
      courseIds: ['07_GPU_Programming_and_AI_Kernels', '08_Distributed_Training_and_GPU_Infrastructure', '09_Inference_Systems_and_Serving_Engines'],
      color: 'bg-amber-500',
    },
    {
      name: 'Tier 4: Applied Cognitive & Enterprise Architectures',
      courses: 'Courses 10 – 12',
      courseIds: ['10_Advanced_Retrieval_and_Context_Engineering', '11_Autonomous_Agents_and_Cognitive_Architectures', '12_LLM_Evaluation_Science_and_Guardrails'],
      color: 'bg-purple-500',
    },
  ];

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div 
        role="dialog"
        aria-modal="true"
        aria-labelledby="stats-modal-title"
        className="w-full max-w-2xl rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200 dark:border-zinc-800 shadow-2xl overflow-hidden p-6 sm:p-8 space-y-6 max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800 pb-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-500">
              <Flame className="w-5 h-5" />
            </div>
            <div>
              <h2 id="stats-modal-title" className="text-base sm:text-lg font-bold text-zinc-900 dark:text-zinc-100">
                Study Velocity & Learning Analytics
              </h2>
              <p className="text-xs text-zinc-500">
                AI & Systems Academy • Individual Progress Dashboard
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            aria-label="Close analytics modal"
            className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* 4 Stat Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-1">
            <div className="flex items-center gap-1.5 text-amber-500 text-xs font-mono font-semibold uppercase">
              <Flame className="w-3.5 h-3.5" /> Streak
            </div>
            <div className="text-2xl font-bold font-mono text-zinc-900 dark:text-zinc-100">
              {streak} <span className="text-xs font-normal text-zinc-500">Days</span>
            </div>
            <div className="text-xs text-zinc-500 font-mono">Active consistency</div>
          </div>

          <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 space-y-1">
            <div className="flex items-center gap-1.5 text-blue-500 text-xs font-mono font-semibold uppercase">
              <CheckCircle2 className="w-3.5 h-3.5" /> Completed
            </div>
            <div className="text-2xl font-bold font-mono text-zinc-900 dark:text-zinc-100">
              {totalCompleted} <span className="text-xs font-normal text-zinc-500">/ {totalCurriculumLessons}</span>
            </div>
            <div className="text-xs text-zinc-500 font-mono">{curriculumPercentage}% of curriculum</div>
          </div>

          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 space-y-1">
            <div className="flex items-center gap-1.5 text-emerald-500 text-xs font-mono font-semibold uppercase">
              <Clock className="w-3.5 h-3.5" /> Time
            </div>
            <div className="text-2xl font-bold font-mono text-zinc-900 dark:text-zinc-100">
              ~{hoursSpent} <span className="text-xs font-normal text-zinc-500">Hours</span>
            </div>
            <div className="text-xs text-zinc-500 font-mono">of 380 total hours</div>
          </div>

          <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20 space-y-1">
            <div className="flex items-center gap-1.5 text-purple-500 text-xs font-mono font-semibold uppercase">
              <Award className="w-3.5 h-3.5" /> Quizzes
            </div>
            <div className="text-2xl font-bold font-mono text-zinc-900 dark:text-zinc-100">
              {passedQuizzesCount} <span className="text-xs font-normal text-zinc-500">Passed</span>
            </div>
            <div className="text-xs text-zinc-500 font-mono">Mastery verified</div>
          </div>
        </div>

        {/* 4-Tier Breakdown */}
        <div className="space-y-3 pt-2">
          <h3 className="text-xs font-mono font-semibold uppercase tracking-wider text-zinc-400">
            Curriculum Tier Breakdown
          </h3>

          <div className="space-y-2.5">
            {tiers.map((t, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl border border-zinc-200/80 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-900/40 space-y-2"
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-zinc-800 dark:text-zinc-200">{t.name}</span>
                  <span className="text-xs font-mono text-zinc-500">{t.courses}</span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-zinc-200 dark:bg-zinc-800 overflow-hidden">
                  <div className={`h-full ${t.color} rounded-full`} style={{ width: `${Math.min(100, Math.max(5, (curriculumPercentage * (idx + 1) * 0.8)))}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="pt-2 border-t border-zinc-100 dark:border-zinc-800 text-xs text-zinc-500 font-mono flex items-center justify-between">
          <span>Synced locally to .study_progress.json</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg text-xs font-medium bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 hover:bg-zinc-800 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
