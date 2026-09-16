import React from 'react';
import { BookOpen, Moon, Sun, Search, Award, CheckCircle } from 'lucide-react';
import { CourseSummary, ProgressPayload } from '../types';

interface HeaderProps {
  progress: ProgressPayload;
  courses: CourseSummary[];
  onToggleTheme: () => void;
  onOpenSearch: () => void;
  onNavigateHome: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  progress,
  courses,
  onToggleTheme,
  onOpenSearch,
  onNavigateHome,
}) => {
  const isDark = progress.theme === 'dark';
  const totalCompleted = progress.completed_lessons.length;

  return (
    <header className="sticky top-0 z-40 w-full border-b border-zinc-200/80 dark:border-zinc-800/80 bg-white/90 dark:bg-zinc-950/90 backdrop-blur-md transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-15 flex items-center justify-between gap-4">
        {/* Logo & Brand */}
        <div 
          onClick={onNavigateHome}
          className="flex items-center gap-3 cursor-pointer select-none group"
        >
          <img 
            src="/logo.svg" 
            alt="AI Systems Mastery" 
            className="w-8 h-8 rounded-lg shadow-sm group-hover:scale-105 transition-transform" 
          />
          <div>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-sm tracking-tight text-zinc-900 dark:text-zinc-50">
                AI Systems Mastery
              </span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700/60">
                12 Tracks
              </span>
            </div>
            <p className="text-[11px] text-zinc-500 font-normal">
              By <span className="text-zinc-700 dark:text-zinc-300 font-medium">Karthikeya Reddy</span>
            </p>
          </div>
        </div>

        {/* Global Search & Action Buttons */}
        <div className="flex items-center gap-2.5">
          <button
            onClick={onOpenSearch}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs text-zinc-500 bg-zinc-100/80 dark:bg-zinc-900/80 hover:bg-zinc-200/80 dark:hover:bg-zinc-800 border border-zinc-200 dark:border-zinc-800 transition-colors"
          >
            <Search className="w-3.5 h-3.5" />
            <span className="hidden sm:inline font-normal">Search curriculum...</span>
            <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-mono text-zinc-400 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded">
              ⌘K
            </kbd>
          </button>

          {/* Progress Pill */}
          <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300 text-xs font-mono">
            <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
            <span>{totalCompleted} Done</span>
          </div>

          {/* Theme Toggle */}
          <button
            onClick={onToggleTheme}
            className="p-2 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 border border-zinc-200 dark:border-zinc-800 transition-colors"
            title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
          >
            {isDark ? <Sun className="w-4 h-4 text-zinc-300" /> : <Moon className="w-4 h-4 text-zinc-600" />}
          </button>
        </div>
      </div>
    </header>
  );
};
