import React from 'react';
import { 
  ArrowLeft, CheckCircle2, Bookmark, Terminal, PanelLeftClose, PanelLeftOpen, ChevronRight
} from 'lucide-react';
import { LessonItem } from '../../types';

export interface ReaderSettings {
  fontSize: 'sm' | 'md' | 'lg' | 'xl';
  fontFamily: 'sans' | 'serif' | 'mono';
  measure: 'narrow' | 'normal' | 'wide' | 'full';
}

interface ReaderToolbarProps {
  courseTitle: string;
  moduleNum: number;
  currentLesson: LessonItem;
  onBackToSyllabus: () => void;
  isSidebarOpen: boolean;
  onToggleSidebar: () => void;
  readingMinutes: number;
  complexityBadge: string;
  readerSettings: ReaderSettings;
  onUpdateReaderSettings: (settings: Partial<ReaderSettings>) => void;
  isBookmarked?: boolean;
  onToggleBookmark?: () => void;
  isScratchpadOpen: boolean;
  onToggleScratchpad: () => void;
  isCompleted: boolean;
  onToggleComplete: () => void;
}

export const ReaderToolbar: React.FC<ReaderToolbarProps> = ({
  courseTitle,
  moduleNum,
  currentLesson,
  onBackToSyllabus,
  isSidebarOpen,
  onToggleSidebar,
  readingMinutes,
  complexityBadge,
  readerSettings,
  onUpdateReaderSettings,
  isBookmarked,
  onToggleBookmark,
  isScratchpadOpen,
  onToggleScratchpad,
  isCompleted,
  onToggleComplete,
}) => {
  return (
    <header className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
      <div className="flex items-center gap-3">
        <button
          onClick={onBackToSyllabus}
          className="p-2 rounded-xl border border-border hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors text-fg-subtle"
          title="Back to Course Syllabus"
          aria-label="Back to Course Syllabus"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-xl border border-border hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors text-fg-subtle hidden lg:flex items-center justify-center"
          title={isSidebarOpen ? "Hide syllabus rail" : "Show syllabus rail"}
          aria-label={isSidebarOpen ? "Hide syllabus rail" : "Show syllabus rail"}
        >
          {isSidebarOpen ? <PanelLeftClose className="w-4 h-4" /> : <PanelLeftOpen className="w-4 h-4" />}
        </button>

        <div>
          <nav aria-label="Breadcrumb" className="text-xs font-mono text-fg-subtle uppercase tracking-wider flex items-center gap-1.5 flex-wrap">
            <button 
              onClick={onBackToSyllabus}
              className="hover:text-fg transition-colors underline-offset-2 hover:underline"
            >
              {courseTitle}
            </button>
            <ChevronRight className="w-3 h-3 text-fg-subtle" />
            <span>Module {moduleNum.toString().padStart(2, '0')}</span>
            <ChevronRight className="w-3 h-3 text-fg-subtle" />
            <span className="text-fg-muted font-medium truncate max-w-[200px] sm:max-w-xs">{currentLesson.title}</span>
          </nav>
          <h1 className="text-base sm:text-lg font-semibold text-fg line-clamp-1 mt-0.5">
            {currentLesson.title}
          </h1>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-fg-muted border border-border">
              ⏱️ ~{readingMinutes} min read
            </span>
            <span className={`text-xs font-mono px-2 py-0.5 rounded-full border ${
              complexityBadge === 'Advanced Systems'
                ? 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/30'
                : complexityBadge === 'Foundational'
                ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
                : 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30'
            }`}>
              ⚡ {complexityBadge}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2.5 self-stretch md:self-auto justify-end flex-wrap">
        {/* Reader Preferences Bar */}
        <div className="hidden sm:flex items-center gap-1.5 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-900 border border-border text-xs select-none" aria-label="Reader Controls">
          {/* Font Size */}
          <div className="flex items-center border-r border-border pr-1 gap-0.5">
            <button
              onClick={() => {
                const sizes: ('sm' | 'md' | 'lg' | 'xl')[] = ['sm', 'md', 'lg', 'xl'];
                const idx = sizes.indexOf(readerSettings.fontSize);
                if (idx > 0) onUpdateReaderSettings({ fontSize: sizes[idx - 1] });
              }}
              disabled={readerSettings.fontSize === 'sm'}
              className="px-1.5 py-0.5 rounded font-mono font-bold text-fg-muted hover:bg-surface disabled:opacity-30 transition-colors"
              title="Decrease reading font size"
              aria-label="Decrease font size"
            >
              A−
            </button>
            <span className="text-[11px] font-mono text-fg-subtle px-0.5">
              {readerSettings.fontSize.toUpperCase()}
            </span>
            <button
              onClick={() => {
                const sizes: ('sm' | 'md' | 'lg' | 'xl')[] = ['sm', 'md', 'lg', 'xl'];
                const idx = sizes.indexOf(readerSettings.fontSize);
                if (idx < sizes.length - 1) onUpdateReaderSettings({ fontSize: sizes[idx + 1] });
              }}
              disabled={readerSettings.fontSize === 'xl'}
              className="px-1.5 py-0.5 rounded font-mono font-bold text-fg-muted hover:bg-surface disabled:opacity-30 transition-colors"
              title="Increase reading font size"
              aria-label="Increase font size"
            >
              A+
            </button>
          </div>

          {/* Font Family */}
          <div className="flex items-center border-r border-border pr-1 gap-0.5">
            {(['sans', 'serif', 'mono'] as const).map((fam) => (
              <button
                key={fam}
                onClick={() => onUpdateReaderSettings({ fontFamily: fam })}
                className={`px-1.5 py-0.5 rounded text-[11px] transition-colors ${
                  readerSettings.fontFamily === fam
                    ? 'bg-surface text-fg font-semibold shadow-xs'
                    : 'text-fg-subtle hover:text-fg'
                }`}
                title={`Font: ${fam}`}
                aria-label={`Font family ${fam}`}
              >
                {fam === 'sans' ? 'Sans' : fam === 'serif' ? 'Serif' : 'Mono'}
              </button>
            ))}
          </div>

          {/* Reading Measure */}
          <div className="flex items-center gap-0.5">
            {(['narrow', 'normal', 'wide', 'full'] as const).map((measure) => (
              <button
                key={measure}
                onClick={() => onUpdateReaderSettings({ measure })}
                className={`px-1.5 py-0.5 rounded text-[11px] font-mono transition-colors ${
                  readerSettings.measure === measure
                    ? 'bg-surface text-fg font-semibold shadow-xs'
                    : 'text-fg-subtle hover:text-fg'
                }`}
                title={`Reading measure: ${measure === 'narrow' ? '64ch' : measure === 'normal' ? '76ch' : measure === 'wide' ? '90ch' : 'Full Page Width'}`}
                aria-label={`Reading width ${measure}`}
              >
                {measure === 'narrow' ? '64ch' : measure === 'normal' ? '76ch' : measure === 'wide' ? '90ch' : 'Full'}
              </button>
            ))}
          </div>
        </div>

        {/* Bookmark Toggle */}
        {onToggleBookmark && (
          <button
            onClick={onToggleBookmark}
            className={`p-2 rounded-lg border text-xs font-medium transition-colors flex items-center gap-1.5 ${
              isBookmarked
                ? 'bg-amber-50 dark:bg-amber-950/50 border-amber-300 dark:border-amber-800 text-amber-600 dark:text-amber-400'
                : 'bg-zinc-100 dark:bg-zinc-800 border-border text-fg-muted hover:text-fg'
            }`}
            title={isBookmarked ? 'Bookmarked' : 'Bookmark this lesson'}
            aria-label={isBookmarked ? 'Bookmarked' : 'Bookmark this lesson'}
          >
            <Bookmark className={`w-3.5 h-3.5 ${isBookmarked ? 'fill-current' : ''}`} />
            <span className="hidden sm:inline">{isBookmarked ? 'Bookmarked' : 'Bookmark'}</span>
          </button>
        )}

        {/* Live Side Runner Toggle */}
        <button
          onClick={onToggleScratchpad}
          className={`px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-2 transition-all shadow-sm ${
            isScratchpadOpen
              ? 'bg-emerald-50 dark:bg-emerald-950/60 border-emerald-300 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300'
              : 'bg-zinc-100 dark:bg-zinc-800 border-border text-fg-muted hover:bg-zinc-200 dark:hover:bg-zinc-700'
          }`}
          title="Toggle Page-Aware Interactive Runner (Python, PowerShell, Shell)"
          aria-label="Toggle Page-Aware Interactive Runner"
        >
          <Terminal className="w-3.5 h-3.5 text-emerald-500" />
          <span>Live Runner</span>
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        </button>

        {/* Mark Complete Toggle */}
        <button
          onClick={onToggleComplete}
          aria-label={isCompleted ? 'Completed' : 'Mark Complete'}
          className={`px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-1.5 transition-all shadow-sm ${
            isCompleted
              ? 'bg-emerald-50 dark:bg-emerald-950/50 border-emerald-300 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300'
              : 'bg-zinc-100 dark:bg-zinc-800 border-border text-fg-muted hover:bg-zinc-200 dark:hover:bg-zinc-700'
          }`}
        >
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
          {isCompleted ? 'Completed' : 'Mark Complete'}
        </button>
      </div>
    </header>
  );
};
