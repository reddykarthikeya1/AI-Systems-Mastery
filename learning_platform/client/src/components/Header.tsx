import React from 'react';
import { BookOpen, Moon, Sun, Search, Award, CheckCircle, Flame, Bookmark, Volume2, VolumeX, Layers, GraduationCap, GitFork } from 'lucide-react';
import { CourseSummary, ProgressPayload } from '../types';

interface HeaderProps {
  progress: ProgressPayload;
  courses: CourseSummary[];
  onToggleTheme: () => void;
  onOpenSearch: () => void;
  onNavigateHome: () => void;
  onOpenStats?: () => void;
  onOpenBookmarks?: () => void;
  onOpenFlashcards?: () => void;
  onOpenPortfolio?: () => void;
  onOpenPrereqMap?: () => void;
  onToggleSound?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  progress,
  courses,
  onToggleTheme,
  onOpenSearch,
  onNavigateHome,
  onOpenStats,
  onOpenBookmarks,
  onOpenFlashcards,
  onOpenPortfolio,
  onOpenPrereqMap,
  onToggleSound,
}) => {
  const isDark = progress.theme === 'dark';
  const totalCompleted = progress.completed_lessons.length;
  const streakDays = progress.study_streak_days || 1;
  const bookmarkCount = progress.bookmarks?.length || 0;

  return (
    <header role="banner" className="sticky top-0 z-40 w-full border-b border-border/80 bg-white/90 dark:bg-zinc-950/90 backdrop-blur-md transition-colors">
      <div className="w-full max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 xl:px-10 h-15 flex items-center justify-between gap-4">
        {/* Logo & Brand */}
        <div 
          onClick={onNavigateHome}
          className="flex items-center gap-3 cursor-pointer select-none group shrink-0"
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
              <span className="text-xs font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700/60">
                12 Tracks
              </span>
            </div>
            <p className="text-xs text-zinc-500 font-normal">
              By <span className="text-zinc-700 dark:text-zinc-300 font-medium">Karthikeya Reddy</span>
            </p>
          </div>
        </div>

        {/* Global Search & Action Controls */}
        <nav aria-label="Global Controls" className="flex items-center gap-2 sm:gap-2.5">
          {/* Spotlight Search Trigger */}
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs text-zinc-500 bg-zinc-100/80 dark:bg-zinc-900/80 hover:bg-zinc-200/80 dark:hover:bg-zinc-800 border border-border transition-colors" onClick={onOpenSearch}
            
            title="Search curriculum (Ctrl + K)"
            aria-label="Search curriculum (Ctrl + K)" >
            <Search className="w-3.5 h-3.5" />
            <span className="hidden md:inline font-normal text-zinc-400">Search curriculum...</span>
            <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-xs font-mono text-zinc-400 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded shadow-xs">
              Ctrl K
            </kbd>
          </button>

          {/* Study Streak Pill */}
          {onOpenStats && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-200/80 dark:border-amber-800/60 text-amber-700 dark:text-amber-300 text-xs font-mono transition-colors hover:bg-amber-100 dark:hover:bg-amber-900/40" onClick={onOpenStats}
              
              title="Daily Study Streak & Analytics"
              aria-label={`Daily Study Streak: ${streakDays} days`} >
              <Flame className="w-3.5 h-3.5 text-amber-500 fill-amber-500 animate-pulse" />
              <span className="font-semibold">{streakDays}d Streak</span>
            </button>
          )}

          {/* Bookmarks Pill */}
          {onOpenBookmarks && bookmarkCount > 0 && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-blue-50 dark:bg-blue-950/40 border border-blue-200/80 dark:border-blue-800/60 text-blue-700 dark:text-blue-300 text-xs font-mono transition-colors hover:bg-blue-100 dark:hover:bg-blue-900/40" onClick={onOpenBookmarks}
              
              title="View Bookmarked Lessons"
              aria-label={`Bookmarked lessons: ${bookmarkCount} saved`} >
              <Bookmark className="w-3.5 h-3.5 fill-blue-500 text-blue-500" />
              <span>{bookmarkCount} Saved</span>
            </button>
          )}

          {/* Completed Lessons Pill */}
          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-900 border border-border text-zinc-700 dark:text-zinc-300 text-xs font-mono" aria-label={`Completed lessons: ${totalCompleted}`}>
            <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
            <span>{totalCompleted} Done</span>
          </div>

          {/* Sound FX Toggle */}
          {onToggleSound && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-2 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 border border-border transition-colors" onClick={onToggleSound}
              
              title={progress.sound_enabled !== false ? "Audio Haptics: ON (Click to Mute)" : "Audio Haptics: MUTED (Click to Unmute)"}
              aria-label={progress.sound_enabled !== false ? "Mute audio haptics" : "Unmute audio haptics"} >
              {progress.sound_enabled !== false ? (
                <Volume2 className="w-4 h-4 text-emerald-500" />
              ) : (
                <VolumeX className="w-4 h-4 text-zinc-400" />
              )}
            </button>
          )}

          {/* Flashcards SRS Button */}
          {onOpenFlashcards && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-200/80 dark:border-amber-800/60 text-amber-700 dark:text-amber-300 text-xs font-mono transition-colors hover:bg-amber-100 dark:hover:bg-amber-900/40" onClick={onOpenFlashcards}
              
              title="Spaced Repetition Flashcards Deck"
              aria-label="Spaced repetition flashcards deck" >
              <Layers className="w-3.5 h-3.5 text-amber-500" />
              <span>Flashcards</span>
            </button>
          )}

          {/* Portfolio & Transcript Button */}
          {onOpenPortfolio && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200/80 dark:border-indigo-800/60 text-indigo-700 dark:text-indigo-300 text-xs font-mono transition-colors hover:bg-indigo-100 dark:hover:bg-indigo-900/40" onClick={onOpenPortfolio}
              
              title="Engineering Portfolio & Transcript"
              aria-label="Engineering portfolio and academic transcript" >
              <GraduationCap className="w-3.5 h-3.5 text-indigo-500" />
              <span>Transcript</span>
            </button>
          )}

          {/* Curriculum Prerequisite Roadmap Button */}
          {onOpenPrereqMap && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-sky-50 dark:bg-sky-950/40 border border-sky-200/80 dark:border-sky-800/60 text-sky-700 dark:text-sky-300 text-xs font-mono transition-colors hover:bg-sky-100 dark:hover:bg-sky-900/40" onClick={onOpenPrereqMap}
              
              title="Curriculum Prerequisite Roadmap"
              aria-label="Curriculum prerequisite roadmap" >
              <GitFork className="w-3.5 h-3.5 text-sky-500" />
              <span>Roadmap</span>
            </button>
          )}

          {/* Theme Toggle */}
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-2 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 border border-border transition-colors" onClick={onToggleTheme}
            
            title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
            aria-label={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"} >
            {isDark ? <Sun className="w-4 h-4 text-zinc-300" /> : <Moon className="w-4 h-4 text-zinc-600" />}
          </button>
        </nav>
      </div>
    </header>
  );
};
