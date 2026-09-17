import React, { useState, useEffect, useRef } from 'react';
import { Search, BookOpen, Layers, FileText, ArrowRight, X, Terminal, Moon, Sun, Flame } from 'lucide-react';
import { useFocusTrap } from '../hooks/useFocusTrap';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onNavigateLesson: (filePath: string, lessonId: string) => void;
  onNavigateCourse: (courseId: string) => void;
  onToggleTheme: () => void;
  theme: string;
  onOpenLiveRunner?: () => void;
  onOpenStats?: () => void;
}

interface SearchItem {
  type: 'course' | 'module' | 'lesson';
  id: string;
  course_id?: string;
  course_title?: string;
  module_id?: string;
  module_title?: string;
  title: string;
  subtitle: string;
  path: string;
  lesson_type?: string;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  onNavigateLesson,
  onNavigateCourse,
  onToggleTheme,
  theme,
  onOpenLiveRunner,
  onOpenStats,
}) => {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<SearchItem[]>([]);
  const [selectedIndex, setSelectedIndex] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const modalRef = useFocusTrap(isOpen, onClose);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
      setResults([]);
    }
  }, [isOpen]);

  // Search API fetch with debounce
  useEffect(() => {
    if (!query.trim() || query.length < 2) {
      setResults([]);
      return;
    }

    const timer = setTimeout(() => {
      setLoading(true);
      fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then((res) => res.json())
        .then((data) => {
          setResults(data || []);
          setSelectedIndex(0);
        })
        .catch(() => setResults([]))
        .finally(() => setLoading(false));
    }, 150);

    return () => clearTimeout(timer);
  }, [query]);

  // Keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % Math.max(1, results.length));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + results.length) % Math.max(1, results.length));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      const item = results[selectedIndex];
      if (item) handleSelect(item);
    }
  };

  const handleSelect = (item: SearchItem) => {
    onClose();
    if (item.type === 'lesson') {
      onNavigateLesson(item.path, item.id);
    } else if (item.type === 'course' || item.type === 'module') {
      onNavigateCourse(item.course_id || item.id);
    }
  };

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-label="Curriculum Command Palette"
        className="w-full max-w-2xl rounded-2xl bg-surface border border-border shadow-2xl overflow-hidden flex flex-col max-h-[550px]"
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
      >
        {/* Search Input Bar */}
        <div className="p-4 border-b border-border flex items-center gap-3">
          <Search className="w-5 h-5 text-zinc-400 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search all 12 courses, modules, algorithms, kernels... (e.g. FlashAttention, Raft, Triton)"
            className="flex-1 bg-transparent text-sm text-fg placeholder:text-zinc-400 focus:outline-none"
          />
          {query && (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200" onClick={() => setQuery('')} >
              <X className="w-4 h-4" />
            </button>
          )}
          <span className="text-xs font-mono px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-400 border border-zinc-200 dark:border-zinc-700">
            ESC to close
          </span>
        </div>

        {/* Quick System Actions (When query is empty) */}
        {!query && (
          <div className="p-4 border-b border-zinc-100 dark:border-zinc-800/80 bg-zinc-50/50 dark:bg-zinc-900/30">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-zinc-400 block mb-2">
              Quick Actions
            </span>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-2.5 rounded-xl border border-border hover:bg-white dark:hover:bg-zinc-800 text-left flex items-center gap-2.5 transition" onClick={() => { onClose(); onOpenLiveRunner?.(); }} >
                <Terminal className="w-4 h-4 text-emerald-500" />
                <span className="font-medium text-zinc-700 dark:text-zinc-300">Open Live Code Runner</span>
              </button>

              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-2.5 rounded-xl border border-border hover:bg-white dark:hover:bg-zinc-800 text-left flex items-center gap-2.5 transition" onClick={() => { onClose(); onOpenStats?.(); }} >
                <Flame className="w-4 h-4 text-amber-500" />
                <span className="font-medium text-zinc-700 dark:text-zinc-300">View Study Streak & Stats</span>
              </button>

              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-2.5 rounded-xl border border-border hover:bg-white dark:hover:bg-zinc-800 text-left flex items-center gap-2.5 transition col-span-2" onClick={() => { onToggleTheme(); }} >
                {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-400" />}
                <span className="font-medium text-zinc-700 dark:text-zinc-300">
                  Switch to {theme === 'dark' ? 'Light' : 'Dark'} Mode
                </span>
              </button>
            </div>
          </div>
        )}

        {/* Results List */}
        <div className="flex-1 overflow-y-auto p-2 divide-y divide-zinc-100 dark:divide-zinc-800/50">
          {loading && (
            <div className="p-6 text-center text-xs font-mono text-zinc-400">
              Searching curriculum index...
            </div>
          )}

          {!loading && query && results.length === 0 && (
            <div className="p-8 text-center text-zinc-400 space-y-2">
              <Search className="w-8 h-8 mx-auto stroke-1 opacity-50" />
              <p className="text-xs font-medium text-zinc-700 dark:text-zinc-300">No curriculum matches found for "{query}"</p>
              <p className="text-xs text-zinc-500 max-w-sm mx-auto">
                Try searching for engineering topics like "Raft", "B-Tree", "Triton", "Attention", or track names like "Distributed" or "DSA".
              </p>
            </div>
          )}

          {!loading &&
            results.map((item, idx) => {
              const isSelected = idx === selectedIndex;

              return (
                <div
                  key={idx}
                  onClick={() => handleSelect(item)}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`p-3 rounded-xl cursor-pointer transition flex items-center justify-between gap-3 ${
                    isSelected
                      ? 'bg-blue-50/80 dark:bg-blue-950/50 text-blue-900 dark:text-blue-100 border border-blue-200 dark:border-blue-900/60'
                      : 'hover:bg-zinc-100/70 dark:hover:bg-zinc-800/50 text-zinc-700 dark:text-zinc-300'
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="p-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-zinc-500 shrink-0">
                      {item.type === 'course' && <BookOpen className="w-4 h-4 text-blue-500" />}
                      {item.type === 'module' && <Layers className="w-4 h-4 text-indigo-500" />}
                      {item.type === 'lesson' && <FileText className="w-4 h-4 text-emerald-500" />}
                    </div>
                    <div className="min-w-0">
                      <div className="text-xs font-semibold truncate flex items-center gap-1.5">
                        <span>{item.title}</span>
                        {item.lesson_type && (
                          <span className="text-xs font-mono px-1.5 py-0.5 rounded bg-zinc-200/60 dark:bg-zinc-800 text-zinc-500">
                            {item.lesson_type}
                          </span>
                        )}
                      </div>
                      <div className="text-xs text-fg-muted truncate">
                        {item.subtitle}
                      </div>
                    </div>
                  </div>

                  <ArrowRight className="w-4 h-4 text-zinc-400 shrink-0" />
                </div>
              );
            })}
        </div>

        {/* Footer */}
        <div className="px-4 py-2 bg-surface border-t border-border flex items-center justify-between text-xs font-mono text-zinc-400">
          <span>Navigate with ↑ ↓ and Enter</span>
          <span>AI Systems Mastery Command Palette</span>
        </div>
      </div>
    </div>
  );
};
