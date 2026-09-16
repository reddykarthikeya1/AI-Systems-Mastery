import React, { useEffect } from 'react';
import { Bookmark, X, ArrowRight, BookOpen, Trash2 } from 'lucide-react';
import { CourseSummary, ModuleItem } from '../types';

interface BookmarksModalProps {
  isOpen: boolean;
  onClose: () => void;
  bookmarks: string[];
  onSelectLesson: (filePath: string, lessonId: string) => void;
  onRemoveBookmark: (lessonId: string) => void;
  modules: ModuleItem[];
}

export const BookmarksModal: React.FC<BookmarksModalProps> = ({
  isOpen,
  onClose,
  bookmarks,
  onSelectLesson,
  onRemoveBookmark,
  modules,
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

  // Resolve bookmark details from loaded modules
  const allLessons = modules.flatMap((m) => m.lessons);

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div 
        role="dialog"
        aria-modal="true"
        aria-labelledby="bookmarks-modal-title"
        className="w-full max-w-lg rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200 dark:border-zinc-800 shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center gap-2">
            <Bookmark className="w-5 h-5 text-blue-500 fill-blue-500" />
            <h2 id="bookmarks-modal-title" className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
              Saved Bookmarks ({bookmarks.length})
            </h2>
          </div>
          <button
            onClick={onClose}
            aria-label="Close bookmarks modal"
            className="p-1 rounded-lg text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 max-h-96 overflow-y-auto space-y-2">
          {bookmarks.length === 0 ? (
            <div className="text-center py-8 text-zinc-400 space-y-2">
              <Bookmark className="w-8 h-8 mx-auto stroke-1 opacity-50" />
              <p className="text-xs">No bookmarked lessons yet.</p>
              <p className="text-xs text-zinc-500">
                Click the bookmark button in any lesson reader to save topics for rapid review.
              </p>
            </div>
          ) : (
            bookmarks.map((bId) => {
              const lesson = allLessons.find((l) => l.id === bId);
              const title = lesson ? lesson.title : bId.replace(/_/g, ' ');
              const filePath = lesson ? lesson.file_path : '';

              return (
                <div
                  key={bId}
                  className="p-3 rounded-xl border border-zinc-200/80 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-900/40 hover:bg-zinc-100/80 dark:hover:bg-zinc-800/60 transition-colors flex items-center justify-between gap-3 group"
                >
                  <div
                    onClick={() => {
                      if (filePath) {
                        onSelectLesson(filePath, bId);
                        onClose();
                      }
                    }}
                    className="flex-1 min-w-0 cursor-pointer"
                  >
                    <div className="text-xs font-medium text-zinc-900 dark:text-zinc-100 line-clamp-1 group-hover:text-blue-600 transition-colors">
                      {title}
                    </div>
                    {filePath && (
                      <div className="text-xs font-mono text-zinc-400 truncate mt-0.5">
                        {filePath}
                      </div>
                    )}
                  </div>

                  <button
                    onClick={() => onRemoveBookmark(bId)}
                    className="p-1.5 rounded-lg text-zinc-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors"
                    title="Remove bookmark"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-zinc-50 dark:bg-zinc-950/60 border-t border-zinc-100 dark:border-zinc-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg text-xs font-medium bg-zinc-200 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-300 dark:hover:bg-zinc-700 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
