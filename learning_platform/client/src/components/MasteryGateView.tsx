import React from 'react';
import { 
  ShieldCheck, ShieldAlert, CheckCircle2, XCircle, ArrowRight, 
  Award, Play, Bug, CheckSquare, Sparkles, BookOpen, RotateCcw,
  Clock, Hammer
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { ModuleItem, MasteryGateStatus } from '../types';
import { soundService } from '../services/sound';

interface MasteryGateViewProps {
  module: ModuleItem;
  courseTitle: string;
  gateStatus?: MasteryGateStatus;
  completedLessonsCount: number;
  totalLessonsCount: number;
  quizScore?: { score: number; total: number; passed: boolean };
  onLaunchQuiz: () => void;
  onLaunchLab: () => void;
  onLaunchLesson: (lessonId: string) => void;
  onClearGate: () => void;
  onNextModule?: () => void;
  onBackToSyllabus: () => void;
}

export const MasteryGateView: React.FC<MasteryGateViewProps> = ({
  module,
  courseTitle,
  gateStatus,
  completedLessonsCount,
  totalLessonsCount,
  quizScore,
  onLaunchQuiz,
  onLaunchLab,
  onLaunchLesson,
  onClearGate,
  onNextModule,
  onBackToSyllabus,
}) => {
  const hasQuiz = Boolean((module.quiz_question_count ?? 0) > 0 || module.lessons.some((l) => l.type === 'quiz'));
  const hasLab = Boolean(module.has_debug_lab || module.lessons.some((l) => l.type === 'troubleshooting'));
  const hasProject = Boolean(module.has_starter || module.has_solution || module.lessons.some((l) => l.type === 'project'));

  const lessonsDone = completedLessonsCount >= Math.max(1, totalLessonsCount);
  const quizDone = hasQuiz ? Boolean(quizScore?.passed || gateStatus?.quizPassed) : true;
  const labDone = hasLab ? Boolean(gateStatus?.labPassed) : true;
  const projectDone = hasProject ? Boolean(gateStatus?.projectPassed) : true;

  const allMet = lessonsDone && quizDone && labDone && projectDone;
  const isCleared = Boolean(gateStatus?.cleared);

  const isSrsDue = Boolean(
    isCleared &&
    gateStatus?.cleared_at &&
    Date.now() - gateStatus.cleared_at > 30 * 24 * 60 * 60 * 1000
  );

  const handleClaimMastery = () => {
    soundService.playFanfare();
    confetti({
      particleCount: 120,
      spread: 90,
      origin: { y: 0.6 },
    });
    onClearGate();
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-8 animate-fadeIn">
      {/* Top Banner */}
      <div className={`p-8 rounded-3xl border shadow-xl relative overflow-hidden transition-all ${
        isCleared 
          ? 'bg-gradient-to-br from-emerald-950/40 via-zinc-900 to-zinc-900 border-emerald-500/30' 
          : allMet
          ? 'bg-gradient-to-br from-blue-950/40 via-zinc-900 to-zinc-900 border-blue-500/30'
          : 'bg-zinc-900/60 border-zinc-800'
      }`}>
        <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div className="flex items-start gap-4">
            <div className={`p-4 rounded-2xl border ${
              isCleared 
                ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' 
                : allMet
                ? 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                : 'bg-zinc-800 text-zinc-400 border-zinc-700'
            }`}>
              {isCleared ? (
                <ShieldCheck className="w-10 h-10" />
              ) : (
                <ShieldAlert className="w-10 h-10" />
              )}
            </div>
            <div>
              <div className="text-xs font-mono uppercase tracking-wider text-zinc-400 flex items-center gap-2">
                <span>{courseTitle}</span>
                <span>•</span>
                <span>Module {module.module_num.toString().padStart(2, '0')}</span>
              </div>
              <h1 className="text-2xl font-bold text-zinc-100 mt-1">
                {isCleared ? 'Module Mastery Verified' : 'Module Mastery Gate'}
              </h1>
              <p className="text-sm text-zinc-400 mt-1 max-w-xl leading-relaxed">
                {isCleared
                  ? 'You have cleared this module mastery gate. All architectural concepts, assessments, and diagnostics are permanently recorded in your student record.'
                  : 'Progress requires verified mastery. Complete the lessons, score ≥ 70% on the conceptual assessment, and diagnose the hands-on lab to unlock progression.'}
              </p>
            </div>
          </div>

          <div className="self-stretch sm:self-center flex sm:flex-col items-center justify-center gap-2 shrink-0">
            {isCleared ? (
              <div className="flex flex-col items-center gap-2">
                <span className="px-4 py-1.5 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4" /> MASTERED
                </span>
                {onNextModule && (
                  <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-5 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-2 shadow-lg transition active:scale-95" onClick={onNextModule} >
                    <span>Next Module</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            ) : allMet ? (
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 w-full sm:w-auto px-6 py-3.5 rounded-2xl text-sm font-bold bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white flex items-center justify-center gap-2 shadow-xl transition-all active:scale-95 hover:shadow-blue-500/20" onClick={handleClaimMastery} >
                <Award className="w-5 h-5" />
                <span>Claim Module Mastery 🛡️</span>
              </button>
            ) : (
              <span className="px-4 py-2 rounded-xl text-xs font-mono text-zinc-400 bg-zinc-800/80 border border-zinc-700">
                Gate Locked (Requirements Pending)
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Spaced Repetition Due Banner */}
      {isSrsDue && (
        <div className="p-4 rounded-2xl border border-purple-500/30 bg-purple-950/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3 text-purple-300">
            <Clock className="w-5 h-5 text-purple-400 shrink-0" />
            <p className="text-xs sm:text-sm">
              <strong className="font-semibold">Spaced Repetition Review Due:</strong> This module was mastered over 30 days ago. Refresh your conceptual understanding with a quick review to reinforce retention.
            </p>
          </div>
          <button
            onClick={onLaunchQuiz}
            className="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-purple-600 hover:bg-purple-500 text-white whitespace-nowrap transition shadow shrink-0"
          >
            Review Assessment
          </button>
        </div>
      )}

      {/* Checklist Cards */}
      <div className="space-y-4">
        <h2 className="text-sm font-mono uppercase tracking-wider text-zinc-400 font-semibold px-1">
          Mastery Gate Requirements
        </h2>

        {/* 1. Core Lessons */}
        <div className={`p-6 rounded-2xl border transition-all ${
          lessonsDone ? 'bg-zinc-900/40 border-emerald-500/30' : 'bg-zinc-900/60 border-zinc-800'
        }`}>
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-xl ${
                lessonsDone ? 'bg-emerald-500/10 text-emerald-400' : 'bg-zinc-800 text-zinc-400'
              }`}>
                <BookOpen className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-semibold text-zinc-100">
                    Curriculum Lessons & Theory
                  </h3>
                  {lessonsDone ? (
                    <span className="px-2 py-0.5 rounded text-xs font-mono bg-emerald-500/20 text-emerald-400">
                      Completed
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 rounded text-xs font-mono bg-amber-500/20 text-amber-400">
                      Incomplete
                    </span>
                  )}
                </div>
                <p className="text-xs text-zinc-400 mt-0.5">
                  Review and mark all module reading lessons as completed.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="text-xs font-mono text-zinc-400">
                {completedLessonsCount} of {totalLessonsCount} lessons
              </span>
              {!lessonsDone && module.lessons.length > 0 && (
                <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 transition" onClick={() => onLaunchLesson(module.lessons[0].id)} >
                  Resume Reading
                </button>
              )}
            </div>
          </div>
        </div>

        {/* 2. MCQ Assessment */}
        {hasQuiz && (
          <div className={`p-6 rounded-2xl border transition-all ${
            quizDone ? 'bg-zinc-900/40 border-emerald-500/30' : 'bg-zinc-900/60 border-zinc-800'
          }`}>
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-xl ${
                  quizDone ? 'bg-emerald-500/10 text-emerald-400' : 'bg-zinc-800 text-zinc-400'
                }`}>
                  <CheckSquare className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-base font-semibold text-zinc-100">
                      Interactive Assessment (MCQ)
                    </h3>
                    {quizDone ? (
                      <span className="px-2 py-0.5 rounded text-xs font-mono bg-emerald-500/20 text-emerald-400">
                        Passed ({quizScore?.score ?? 100}%)
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-xs font-mono bg-rose-500/20 text-rose-400">
                        Score ≥ 70% Required
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-zinc-400 mt-0.5">
                    Demonstrate architectural understanding by answering module questions.
                  </p>
                </div>
              </div>

              <div>
                <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition ${
                    quizDone
                      ? 'bg-zinc-800 hover:bg-zinc-700 text-zinc-300'
                      : 'bg-amber-600 hover:bg-amber-500 text-white shadow-md'
                  }`} onClick={onLaunchQuiz} >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>{quizDone ? 'Retake Assessment' : 'Launch Assessment'}</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* 3. Hands-On Lab / Pytest */}
        {hasLab && (
          <div className={`p-6 rounded-2xl border transition-all ${
            labDone ? 'bg-zinc-900/40 border-emerald-500/30' : 'bg-zinc-900/60 border-zinc-800'
          }`}>
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-xl ${
                  labDone ? 'bg-emerald-500/10 text-emerald-400' : 'bg-zinc-800 text-zinc-400'
                }`}>
                  <Bug className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-base font-semibold text-zinc-100">
                      Bug Hunter Diagnostic Lab
                    </h3>
                    {labDone ? (
                      <span className="px-2 py-0.5 rounded text-xs font-mono bg-emerald-500/20 text-emerald-400">
                        Verified
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-xs font-mono bg-rose-500/20 text-rose-400">
                        Pending Diagnosis
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-zinc-400 mt-0.5">
                    Diagnose and resolve the production bugs planted in this module lab.
                  </p>
                </div>
              </div>

              <div>
                <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition ${
                    labDone
                      ? 'bg-zinc-800 hover:bg-zinc-700 text-zinc-300'
                      : 'bg-rose-600 hover:bg-rose-500 text-white shadow-md'
                  }`} onClick={onLaunchLab} >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>{labDone ? 'Review Bug Lab' : 'Launch Bug Lab'}</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* 4. Guided Hands-On Project */}
        {hasProject && (
          <div className={`p-6 rounded-2xl border transition-all ${
            projectDone ? 'bg-zinc-900/40 border-emerald-500/30' : 'bg-zinc-900/60 border-zinc-800'
          }`}>
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-xl ${
                  projectDone ? 'bg-emerald-500/10 text-emerald-400' : 'bg-zinc-800 text-zinc-400'
                }`}>
                  <Hammer className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-base font-semibold text-zinc-100">
                      Guided Project & Pytest Suite
                    </h3>
                    {projectDone ? (
                      <span className="px-2 py-0.5 rounded text-xs font-mono bg-emerald-500/20 text-emerald-400">
                        Suite Green
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-xs font-mono bg-amber-500/20 text-amber-400">
                        Pending Tests
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-zinc-400 mt-0.5">
                    Implement the project module starter and pass all test assertions.
                  </p>
                </div>
              </div>

              <div>
                <button
                  className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition ${
                    projectDone
                      ? 'bg-zinc-800 hover:bg-zinc-700 text-zinc-300'
                      : 'bg-purple-600 hover:bg-purple-500 text-white shadow-md'
                  }`}
                  onClick={() => {
                    const projLesson = module.lessons.find(l => l.type === 'project');
                    if (projLesson) onLaunchLesson(projLesson.id);
                  }}
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>{projectDone ? 'Review Project' : 'Launch Project IDE'}</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-6 border-t border-zinc-800">
        <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 rounded-xl border border-zinc-700 text-xs font-medium text-zinc-300 hover:bg-zinc-800 transition" onClick={onBackToSyllabus} >
          ← Return to Syllabus
        </button>

        {isCleared && onNextModule && (
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-5 py-2 rounded-xl text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white flex items-center gap-2 shadow transition" onClick={onNextModule} >
            <span>Advance to Next Module</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
};
