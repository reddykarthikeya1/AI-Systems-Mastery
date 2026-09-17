import React, { useState, useEffect } from 'react';
import { Search, X, BookOpen, ArrowRight } from 'lucide-react';
import { CourseSummary } from '../types';

interface SearchModalProps {
  isOpen: boolean;
  courses: CourseSummary[];
  onClose: () => void;
  onSelectCourse: (courseId: string) => void;
}

export const SearchModal: React.FC<SearchModalProps> = ({
  isOpen,
  courses,
  onClose,
  onSelectCourse,
}) => {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        onClose();
      }
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!isOpen) return null;

  const results = courses.filter((c) =>
    c.title.toLowerCase().includes(query.toLowerCase()) ||
    c.category.toLowerCase().includes(query.toLowerCase()) ||
    c.description.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/50 backdrop-blur-sm">
      <div className="w-full max-w-xl rounded-xl bg-surface border border-border shadow-xl overflow-hidden">
        <div className="flex items-center px-4 border-b border-border">
          <Search className="w-4 h-4 text-zinc-400 mr-2.5" />
          <input
            type="text"
            placeholder="Search tracks, modules, systems..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            className="w-full py-3.5 text-xs bg-transparent outline-none text-fg placeholder:text-zinc-400"
          />
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-1 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300" onClick={onClose} >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="max-h-80 overflow-y-auto p-1.5 divide-y divide-zinc-100 dark:divide-zinc-800/60">
          {results.length > 0 ? (
            results.map((c) => (
              <div
                key={c.id}
                onClick={() => {
                  onSelectCourse(c.id);
                  onClose();
                }}
                className="p-3 hover:bg-zinc-100 dark:hover:bg-zinc-800/70 rounded-lg cursor-pointer flex items-center justify-between group transition-colors"
              >
                <div className="space-y-0.5">
                  <span className="text-xs font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 font-medium">
                    Track {c.course_num.toString().padStart(2, '0')}
                  </span>
                  <h4 className="text-xs font-semibold text-fg group-hover:text-blue-600 transition-colors">
                    {c.title}
                  </h4>
                  <p className="text-xs text-zinc-500 line-clamp-1">{c.description}</p>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-zinc-400 group-hover:translate-x-0.5 transition-transform" />
              </div>
            ))
          ) : (
            <div className="p-6 text-center text-xs text-zinc-500 font-mono">
              No results found for "{query}".
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
