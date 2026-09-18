import React, { useState } from 'react';
import { CourseSummary, ProgressPayload } from '../types';
import { soundService } from '../services/sound';
import { useFocusTrap } from '../hooks/useFocusTrap';

interface PortfolioModalProps {
  isOpen: boolean;
  onClose: () => void;
  courses: CourseSummary[];
  progress: ProgressPayload;
}

export const PortfolioModal: React.FC<PortfolioModalProps> = ({
  isOpen,
  onClose,
  courses,
  progress,
}) => {
  const [copied, setCopied] = useState<boolean>(false);
  const trapRef = useFocusTrap(isOpen, onClose);

  if (!isOpen) return null;

  const totalLessons = progress.completed_lessons.length;
  const totalModules = progress.completed_modules.length;
  const streak = progress.study_streak_days || 0;

  // Generate markdown transcript
  const generateMarkdown = () => {
    const lines: string[] = [];
    lines.push('# Systems Engineering & AI Academy — Official Student Transcript');
    lines.push(`**Generated:** ${new Date().toLocaleDateString()} | **Author:** Karthikeya Reddy`);
    lines.push('');
    lines.push('## Executive Summary');
    lines.push(`- **Total Lessons Completed:** ${totalLessons}`);
    lines.push(`- **Modules Mastered:** ${totalModules}`);
    lines.push(`- **Consecutive Study Streak:** ${streak} days`);
    lines.push(`- **Curriculum Architecture:** 12 Rigorous Production Engineering Courses`);
    lines.push('');
    lines.push('## Course Competencies & Mastery');
    lines.push('| # | Course Title | Category | Difficulty | Est. Hours | Status |');
    lines.push('|---|--------------|----------|------------|------------|--------|');

    courses.forEach((c) => {
      const isComplete = progress.completed_modules.some((m) => m.startsWith(c.folder_name));
      const status = isComplete ? '✅ In Progress / Mastered' : '🔄 Active Candidate';
      lines.push(`| ${c.course_num} | ${c.title} | ${c.category} | ${c.difficulty} | ${c.estimated_hours}h | ${status} |`);
    });

    lines.push('');
    lines.push('## Core Competency Matrix');
    lines.push('- **Core Python & Concurrency:** CPython bytecode, GIL internals, memory allocators, async event loops');
    lines.push('- **High-Performance Data Structures:** B-Trees, Segment Trees, Monotonic Stacks, Union-Find, Cache-friendly layout');
    lines.push('- **Database Internals & Storage Engines:** B+ Trees, WAL framing, ARIES crash recovery, MVCC, LSM-trees');
    lines.push('- **Distributed Systems:** Raft consensus, PACELC theorem, Vector clocks, Two-Phase Commit, Saga choreography');
    lines.push('- **Modern AI Architectures:** Transformer attention engines, KV Cache paging, LoRA fine-tuning, RAG semantic pipelines');
    lines.push('');
    lines.push('---');
    lines.push('*Verified by Systems Engineering Academy CLI & Native Studio Engine.*');
    return lines.join('\n');
  };

  const handleCopyMarkdown = () => {
    soundService.playSuccess();
    navigator.clipboard.writeText(generateMarkdown());
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const handlePrint = () => {
    soundService.playClick();
    window.print();
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div 
        role="dialog"
        aria-modal="true"
        aria-labelledby="portfolio-modal-title"
        className="flex flex-col w-full max-w-4xl max-h-[90vh] bg-surface border border-border rounded-2xl shadow-2xl overflow-hidden print:m-0 print:p-0 print:border-none print:shadow-none"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-surface/70 print:hidden">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-lg">
              🎓
            </div>
            <div>
              <h2 id="portfolio-modal-title" className="text-base font-semibold text-fg flex items-center gap-2">
                Engineering Portfolio & Academic Transcript
                <span className="px-2 py-0.5 text-xs rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-mono">
                  Verified Local Progress
                </span>
              </h2>
              <p className="text-xs text-fg-muted">
                Official record of lessons mastered, test suites passed, and systems architectures built.
              </p>
            </div>
          </div>
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-1.5 rounded-lg text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors" onClick={() => {
              soundService.playClick();
              onClose();
            }}
            aria-label="Close transcript modal" >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Portfolio Content */}
        <div className="flex-1 p-5 md:p-6 overflow-y-auto space-y-5">
          {/* Top Banner / Student Summary Card */}
          <div className="p-5 rounded-2xl bg-gradient-to-r from-blue-600/10 via-indigo-600/10 to-purple-600/10 border border-blue-500/20 flex flex-col md:flex-row md:items-center justify-between gap-5">
            <div className="space-y-1">
              <span className="text-xs font-mono uppercase tracking-wider text-blue-600 dark:text-blue-400 font-bold">
                Student Engineering Record
              </span>
              <h1 className="text-xl md:text-2xl font-bold text-fg">
                Systems & AI Engineering Mastery
              </h1>
              <p className="text-xs md:text-sm text-zinc-600 dark:text-zinc-400">
                Comprehensive 12-Course Software Architecture, Database Internals, and Distributed Infrastructure track.
              </p>
            </div>

            <div className="grid grid-cols-3 gap-2.5 shrink-0">
              <div className="px-4 py-2.5 bg-white dark:bg-zinc-800/90 rounded-xl border border-border text-center shadow-sm min-w-[76px]">
                <div className="text-lg font-extrabold text-blue-600 dark:text-blue-400 font-mono leading-tight">
                  {totalLessons}
                </div>
                <div className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider mt-0.5">Lessons</div>
              </div>
              <div className="px-4 py-2.5 bg-white dark:bg-zinc-800/90 rounded-xl border border-border text-center shadow-sm min-w-[76px]">
                <div className="text-lg font-extrabold text-emerald-600 dark:text-emerald-400 font-mono leading-tight">
                  {totalModules}
                </div>
                <div className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider mt-0.5">Modules</div>
              </div>
              <div className="px-4 py-2.5 bg-white dark:bg-zinc-800/90 rounded-xl border border-border text-center shadow-sm min-w-[76px]">
                <div className="text-lg font-extrabold text-amber-600 dark:text-amber-400 font-mono leading-tight">
                  {streak}🔥
                </div>
                <div className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider mt-0.5">Streak</div>
              </div>
            </div>
          </div>

          {/* Courses Progress Table */}
          <div className="space-y-2.5">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold font-mono text-fg uppercase tracking-wider">
                Curriculum Breakdown ({courses.length} Courses)
              </h3>
              <span className="text-xs font-mono text-zinc-500">100% Offline Verified</span>
            </div>

            <div className="border border-border rounded-xl overflow-hidden shadow-xs">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-zinc-50 dark:bg-zinc-900/80 text-zinc-600 dark:text-zinc-400 border-b border-border font-semibold">
                  <tr>
                    <th className="w-12 px-3.5 py-2.5 text-center">#</th>
                    <th className="px-3.5 py-2.5">Course Title</th>
                    <th className="px-3.5 py-2.5">Track / Domain</th>
                    <th className="w-28 px-3.5 py-2.5">Level</th>
                    <th className="w-24 px-3.5 py-2.5 text-right">Estimated</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {courses.map((c) => (
                    <tr key={c.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/40 transition-colors">
                      <td className="px-3.5 py-2.5 font-mono font-semibold text-zinc-400 text-center">{c.course_num.toString().padStart(2, '0')}</td>
                      <td className="px-3.5 py-2.5 font-sans font-medium text-fg">
                        {c.title}
                      </td>
                      <td className="px-3.5 py-2.5 font-sans">
                        <span className="inline-block px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xs border border-border">
                          {c.category}
                        </span>
                      </td>
                      <td className="px-3.5 py-2.5 text-zinc-500 font-sans">{c.difficulty}</td>
                      <td className="px-3.5 py-2.5 text-right font-mono text-zinc-500">{c.estimated_hours} hrs</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Note & footer attribution */}
            <div className="pt-2 flex items-center justify-between text-[11px] text-zinc-400">
              <span>© Karthikeya Reddy. All rights reserved.</span>
              <span>Issued by AI & Systems Engineering Platform</span>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="px-6 py-3.5 bg-surface border-t border-border flex items-center justify-between print:hidden">
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 text-xs font-medium rounded-lg border border-border bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors" onClick={() => {
              soundService.playClick();
              onClose();
            }} >
            Close
          </button>

          <div className="flex items-center gap-3">
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 flex items-center gap-1.5 px-4 py-2 text-xs font-semibold rounded-lg bg-white dark:bg-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-700 text-zinc-800 dark:text-zinc-200 border border-border shadow-sm transition-all" onClick={handleCopyMarkdown} >
              {copied ? '✓ Copied Markdown' : '📋 Copy Markdown Transcript'}
            </button>
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 flex items-center gap-1.5 px-4 py-2 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-500 text-white shadow transition-all" onClick={handlePrint} >
              🖨️ Print / Save PDF
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
