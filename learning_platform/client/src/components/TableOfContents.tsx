import React, { useMemo, useEffect, useState } from 'react';
import { List, Clock, Bookmark, BookOpen, ChevronRight } from 'lucide-react';

interface TableOfContentsProps {
  content: string;
  isBookmarked?: boolean;
  onToggleBookmark?: () => void;
}

export const TableOfContents: React.FC<TableOfContentsProps> = ({
  content,
  isBookmarked,
  onToggleBookmark,
}) => {
  const [activeHeadingId, setActiveHeadingId] = useState<string>('');

  // Extract H2 and H3 headings
  const headings = useMemo(() => {
    if (!content) return [];
    const items: { id: string; text: string; level: number }[] = [];
    const lines = content.split('\n');

    lines.forEach((line) => {
      const match = line.match(/^(#{2,3})\s+(.+)/);
      if (match) {
        const level = match[1].length;
        const rawText = match[2].trim().replace(/[*`_]/g, '');
        const id = rawText.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        items.push({ id, text: rawText, level });
      }
    });

    return items;
  }, [content]);

  // Estimated reading time
  const readingTime = useMemo(() => {
    if (!content) return 1;
    const words = content.trim().split(/\s+/).length;
    return Math.max(1, Math.ceil(words / 180));
  }, [content]);

  // IntersectionObserver scroll-spy to highlight current reading section
  useEffect(() => {
    const timer = setTimeout(() => {
      const container = document.querySelector('.markdown-body');
      if (!container) return;

      const headingEls = container.querySelectorAll('h2, h3');
      if (headingEls.length === 0) return;

      const observer = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) {
              const raw = entry.target.textContent || '';
              const match = headings.find((h) =>
                raw.toLowerCase().includes(h.text.toLowerCase().slice(0, 15))
              );
              if (match) {
                setActiveHeadingId(match.text);
              }
            }
          }
        },
        { rootMargin: '-60px 0px -60% 0px', threshold: 0.1 }
      );

      headingEls.forEach((el) => observer.observe(el));
      return () => observer.disconnect();
    }, 400);

    return () => clearTimeout(timer);
  }, [headings]);

  const scrollToHeading = (text: string) => {
    // Find heading element by text content in .markdown-body
    const container = document.querySelector('.markdown-body');
    if (!container) return;

    const headingEls = container.querySelectorAll('h1, h2, h3');
    for (const el of Array.from(headingEls)) {
      if (el.textContent?.toLowerCase().includes(text.toLowerCase().slice(0, 20))) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setActiveHeadingId(text);
        break;
      }
    }
  };

  if (headings.length < 2) return null;

  return (
    <div className="rounded-xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-4 shadow-sm space-y-3 sticky top-20">
      {/* Top Meta Bar */}
      <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800 pb-2.5">
        <div className="flex items-center gap-1.5 text-zinc-500 text-xs font-mono">
          <Clock className="w-3.5 h-3.5" />
          <span>{readingTime} min read</span>
        </div>

        {onToggleBookmark && (
          <button
            onClick={onToggleBookmark}
            className={`p-1 rounded-md text-xs transition flex items-center gap-1 ${
              isBookmarked
                ? 'text-amber-500 bg-amber-500/10'
                : 'text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300'
            }`}
            title={isBookmarked ? 'Remove Bookmark' : 'Bookmark this lesson'}
          >
            <Bookmark className={`w-3.5 h-3.5 ${isBookmarked ? 'fill-current' : ''}`} />
            <span className="text-xs font-mono">{isBookmarked ? 'Saved' : 'Save'}</span>
          </button>
        )}
      </div>

      <div className="space-y-1">
        <span className="text-xs font-mono font-semibold uppercase tracking-wider text-zinc-400 block px-1">
          On This Page
        </span>

        <div className="space-y-1 max-h-[calc(100vh-14rem)] overflow-y-auto pr-1">
          {headings.map((h, i) => {
            const isActive = activeHeadingId === h.text;
            return (
              <button
                key={i}
                onClick={() => scrollToHeading(h.text)}
                className={`w-full text-left py-1.5 px-2.5 rounded-lg text-xs leading-relaxed transition break-words block ${
                  isActive
                    ? 'bg-blue-500/15 text-blue-600 dark:text-blue-400 font-semibold border-l-2 border-blue-500 shadow-sm'
                    : h.level === 3 
                    ? 'pl-4 text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200' 
                    : 'font-medium text-zinc-700 dark:text-zinc-300 hover:text-blue-500 dark:hover:text-blue-400'
                } hover:bg-zinc-100/70 dark:hover:bg-zinc-800/50`}
                title={h.text}
              >
                {h.text}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
