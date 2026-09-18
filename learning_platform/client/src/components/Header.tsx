import React from 'react';
import { BookOpen, Moon, Sun, Search, Award, CheckCircle, Flame, Bookmark, Volume2, VolumeX, Layers, GraduationCap, GitFork, Cpu, Terminal } from 'lucide-react';
import { CourseSummary, ProgressPayload, EngineeringRank } from '../types';

interface HeaderProps {
  progress: ProgressPayload;
  courses: CourseSummary[];
  rankInfo?: { currentRank: EngineeringRank; nextRank: EngineeringRank | null; progressPercent: number };
  earnedXp?: number;
  onToggleTheme: () => void;
  onOpenSearch: () => void;
  onNavigateHome: () => void;
  onOpenStats?: () => void;
  onOpenBookmarks?: () => void;
  onOpenFlashcards?: () => void;
  onOpenPortfolio?: () => void;
  onOpenPrereqMap?: () => void;
  onOpenHardwareTopology?: () => void;
  onOpenIdeGuide?: () => void;
  onToggleSound?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  progress,
  courses,
  rankInfo,
  earnedXp,
  onToggleTheme,
  onOpenSearch,
  onNavigateHome,
  onOpenStats,
  onOpenBookmarks,
  onOpenFlashcards,
  onOpenPortfolio,
  onOpenPrereqMap,
  onOpenHardwareTopology,
  onOpenIdeGuide,
  onToggleSound,
}) => {
  const isDark = progress.theme === 'dark';
  const totalCompleted = progress.completed_lessons.length;
  const streakDays = progress.study_streak_days || 0;
  const bookmarkCount = progress.bookmarks?.length || 0;

  return (
    <header role="banner" className="sticky top-0 z-40 w-full border-b border-border bg-surface/95 backdrop-blur-md transition-colors shadow-xs">
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
              <span className="font-semibold text-sm tracking-tight text-fg">
                AI Systems Mastery
              </span>
              <span className="text-xs font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border border-border">
                12 Tracks
              </span>
            </div>
            <p className="text-xs text-fg-subtle font-normal">
              By <span className="text-fg font-medium">Karthikeya Reddy</span>
            </p>
          </div>
        </div>

        {/* Global Search & Action Controls */}
        <nav aria-label="Global Controls" className="flex items-center gap-2 sm:gap-2.5">
          {/* Spotlight Search Trigger */}
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs text-fg-muted bg-zinc-100 dark:bg-zinc-800/80 hover:bg-zinc-200/80 dark:hover:bg-zinc-700 border border-border transition-colors shadow-xs" onClick={onOpenSearch}
            title="Search curriculum (Ctrl + K)"
            aria-label="Search curriculum (Ctrl + K)" >
            <Search className="w-3.5 h-3.5 text-zinc-500 dark:text-zinc-400" />
            <span className="hidden md:inline font-normal text-zinc-500 dark:text-zinc-400">Search curriculum...</span>
            <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-xs font-mono text-zinc-600 dark:text-zinc-300 bg-white dark:bg-zinc-700 border border-border rounded shadow-xs">
              Ctrl K
            </kbd>
          </button>

          {/* Study Streak Pill */}
          {onOpenStats && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-300/80 dark:border-amber-800/70 text-amber-700 dark:text-amber-300 text-xs font-mono transition-colors hover:bg-amber-100 dark:hover:bg-amber-900/50 shadow-xs" onClick={onOpenStats}
              title="Daily Study Streak & Analytics"
              aria-label={streakDays > 0
                ? `Daily study streak: ${streakDays} days`
                : 'No study streak yet. Complete a lesson to start one.'} >
              <Flame className="w-3.5 h-3.5 text-amber-500 fill-amber-500 animate-pulse" />
              <span className="font-semibold">
                {streakDays > 0 ? `${streakDays}d Streak` : 'Start streak'}
              </span>
            </button>
          )}

          {/* Bookmarks Pill */}
          {onOpenBookmarks && bookmarkCount > 0 && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-blue-50 dark:bg-blue-950/40 border border-blue-300/80 dark:border-blue-800/70 text-blue-700 dark:text-blue-300 text-xs font-mono transition-colors hover:bg-blue-100 dark:hover:bg-blue-900/50 shadow-xs" onClick={onOpenBookmarks}
              title="View Bookmarked Lessons"
              aria-label={`Bookmarked lessons: ${bookmarkCount} saved`} >
              <Bookmark className="w-3.5 h-3.5 fill-blue-500 text-blue-500" />
              <span>{bookmarkCount} Saved</span>
            </button>
          )}

          {/* Completed Lessons Pill */}
          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800/90 border border-border text-zinc-700 dark:text-zinc-200 text-xs font-mono shadow-xs" aria-label={`Completed lessons: ${totalCompleted}`}>
            <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
            <span>{totalCompleted} Done</span>
          </div>

          {/* Sound FX Toggle */}
          {onToggleSound && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-2 rounded-lg text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 border border-border transition-colors shadow-xs" onClick={onToggleSound}
              title={progress.sound_enabled !== false ? "Audio Haptics: ON (Click to Mute)" : "Audio Haptics: MUTED (Click to Unmute)"}
              aria-label={progress.sound_enabled !== false ? "Mute audio haptics" : "Unmute audio haptics"} >
              {progress.sound_enabled !== false ? (
                <Volume2 className="w-4 h-4 text-emerald-500" />
              ) : (
                <VolumeX className="w-4 h-4 text-zinc-400" />
              )}
            </button>
          )}

          {/* Engineering Rank & XP Pill */}
          {rankInfo && (
            <div 
              className="hidden xl:flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800/90 border border-border text-xs font-mono shadow-xs"
              title={`${rankInfo.currentRank.title} (${earnedXp || 0} XP) - ${rankInfo.progressPercent}% to ${rankInfo.nextRank?.title || 'Max Level'}`}
            >
              <span className="text-sm">{rankInfo.currentRank.badge}</span>
              <div className="flex flex-col">
                <div className="flex items-center gap-1.5 leading-none">
                  <span className="font-semibold text-fg">Lvl {rankInfo.currentRank.level}</span>
                  <span className="text-fg-subtle font-normal whitespace-nowrap">{rankInfo.currentRank.title}</span>
                </div>
                <div className="w-20 h-1 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden mt-1">
                  <div 
                    className="h-full bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-full"
                    style={{ width: `${rankInfo.progressPercent}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Flashcards SRS Button */}
          {/* Flashcards SRS Button */}
          {onOpenFlashcards && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-300/90 dark:border-amber-800/80 text-amber-800 dark:text-amber-300 text-xs font-mono transition-colors hover:bg-amber-100 dark:hover:bg-amber-900/50 shadow-xs" onClick={onOpenFlashcards}
              title="Spaced Repetition Flashcards Deck"
              aria-label="Spaced repetition flashcards deck" >
              <Layers className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
              <span className="font-medium">Flashcards</span>
            </button>
          )}

          {/* AI Systems Hardware Topology Explorer */}
          {onOpenHardwareTopology && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500 hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-cyan-50 dark:bg-cyan-950/40 border border-cyan-300/90 dark:border-cyan-800/80 text-cyan-800 dark:text-cyan-300 text-xs font-mono transition-colors hover:bg-cyan-100 dark:hover:bg-cyan-900/50 shadow-xs" onClick={onOpenHardwareTopology}
              title="AI Systems Hardware & Memory Hierarchy"
              aria-label="Hardware topology and memory hierarchy" >
              <Cpu className="w-3.5 h-3.5 text-cyan-600 dark:text-cyan-400" />
              <span className="font-medium">Hardware</span>
            </button>
          )}

          {/* Portfolio & Transcript Button */}
          {onOpenPortfolio && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-300/90 dark:border-indigo-800/80 text-indigo-800 dark:text-indigo-300 text-xs font-mono transition-colors hover:bg-indigo-100 dark:hover:bg-indigo-900/50 shadow-xs" onClick={onOpenPortfolio}
              title="Engineering Portfolio & Transcript"
              aria-label="Engineering portfolio and academic transcript" >
              <GraduationCap className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
              <span className="font-medium">Transcript</span>
            </button>
          )}

          {/* Curriculum Prerequisite Roadmap Button */}
          {onOpenPrereqMap && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-sky-50 dark:bg-sky-950/40 border border-sky-300/90 dark:border-sky-800/80 text-sky-800 dark:text-sky-300 text-xs font-mono transition-colors hover:bg-sky-100 dark:hover:bg-sky-900/50 shadow-xs" onClick={onOpenPrereqMap}
              title="Curriculum Prerequisite Roadmap"
              aria-label="Curriculum prerequisite roadmap" >
              <GitFork className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
              <span className="font-medium">Roadmap</span>
            </button>
          )}

          {/* Local IDE Workflow Guide Button */}
          {onOpenIdeGuide && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300/90 dark:border-emerald-800/80 text-emerald-800 dark:text-emerald-300 text-xs font-mono transition-colors hover:bg-emerald-100 dark:hover:bg-emerald-900/50 shadow-xs" onClick={onOpenIdeGuide}
              title="VS Code & Local Terminal Setup Guide"
              aria-label="Local IDE setup guide" >
              <Terminal className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
              <span className="font-medium">Local IDE</span>
            </button>
          )}

          {/* Theme Toggle */}
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-2 rounded-lg text-zinc-600 hover:text-zinc-900 dark:text-zinc-300 dark:hover:text-zinc-100 hover:bg-zinc-100 dark:hover:bg-zinc-800 border border-border transition-colors shadow-xs" onClick={onToggleTheme}
            title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
            aria-label={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"} >
            {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-500" />}
          </button>
        </nav>
      </div>
    </header>
  );
};
