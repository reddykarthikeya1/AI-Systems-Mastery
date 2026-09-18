import React, { useMemo, useEffect, useState } from 'react';
import { List, Clock, Bookmark, BookOpen, ChevronRight, Terminal, Code2, Check, ArrowUp, Play } from 'lucide-react';
import { soundService } from '../services/sound';

export interface TocItem {
  id: string;
  text: string;
  level: number;
  type?: 'heading' | 'function' | 'class' | 'cell' | 'section';
  cellIndex?: number;
}

interface TableOfContentsProps {
  content: string;
  lessonFilePath?: string;
  lessonTitle?: string;
  lessonType?: string;
  notebookCells?: { type: 'markdown' | 'code'; source: string }[];
  isBookmarked?: boolean;
  onToggleBookmark?: () => void;
}

export const TableOfContents: React.FC<TableOfContentsProps> = ({
  content,
  lessonFilePath = '',
  lessonTitle = '',
  lessonType = 'theory',
  notebookCells = [],
  isBookmarked,
  onToggleBookmark,
}) => {
  const [activeHeadingId, setActiveHeadingId] = useState<string>('');
  const [copiedCmd, setCopiedCmd] = useState<string | null>(null);

  const handleCopy = (cmd: string, key: string) => {
    navigator.clipboard.writeText(cmd);
    setCopiedCmd(key);
    soundService.playClick();
    setTimeout(() => setCopiedCmd(null), 2500);
  };

  // Determine file extension and kind
  const isScript = lessonType === 'code' || lessonType === 'powershell' || lessonType === 'shell' || 
    /\.(py|sh|ps1|bash)$/i.test(lessonFilePath);
  const isNotebook = lessonType === 'notebook' || /\.(ipynb)$/i.test(lessonFilePath) || (notebookCells && notebookCells.length > 0);

  // Extract outline items depending on lesson type
  const items = useMemo<TocItem[]>(() => {
    // CASE 1: JUPYTER NOTEBOOK
    if (isNotebook && notebookCells.length > 0) {
      const cellItems: TocItem[] = [];
      notebookCells.forEach((cell, idx) => {
        if (cell.type === 'markdown') {
          const lines = cell.source.split('\n');
          lines.forEach((l) => {
            const hMatch = l.match(/^(#{1,4})\s+(.+)/);
            if (hMatch) {
              const text = hMatch[2].trim().replace(/[*`_]/g, '');
              cellItems.push({
                id: `cell-${idx}-${text.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`,
                text,
                level: hMatch[1].length,
                type: 'heading',
                cellIndex: idx,
              });
            }
          });
        } else if (cell.type === 'code') {
          const lines = cell.source.split('\n').map((s) => s.trim()).filter(Boolean);
          const funcLine = lines.find((l) => l.startsWith('def ') || l.startsWith('class '));
          const commentLine = lines.find((l) => l.startsWith('# '));
          const summary = funcLine 
            ? funcLine.replace(/^(def|class)\s+/, '').split('(')[0] + '()'
            : commentLine 
            ? commentLine.replace(/^#\s*/, '').slice(0, 24)
            : `Code Block ${idx + 1}`;

          cellItems.push({
            id: `cell-${idx}`,
            text: `[Cell ${idx + 1}] ${summary}`,
            level: 3,
            type: 'cell',
            cellIndex: idx,
          });
        }
      });
      if (cellItems.length > 0) return cellItems;
    }

    // CASE 2: PYTHON OR SHELL SCRIPT
    if (isScript && content) {
      const scriptItems: TocItem[] = [];
      const lines = content.split('\n');
      lines.forEach((line, idx) => {
        const trimmed = line.trim();
        const classMatch = trimmed.match(/^class\s+([A-Za-z0-9_]+)/);
        if (classMatch) {
          scriptItems.push({
            id: `class-${classMatch[1]}`,
            text: `class ${classMatch[1]}`,
            level: 2,
            type: 'class',
          });
          return;
        }

        const defMatch = trimmed.match(/^def\s+([A-Za-z0-9_]+)\s*\(/);
        if (defMatch) {
          scriptItems.push({
            id: `def-${defMatch[1]}`,
            text: `def ${defMatch[1]}()`,
            level: 3,
            type: 'function',
          });
          return;
        }

        if (trimmed.includes('if __name__ == "__main__":') || trimmed.includes("if __name__ == '__main__':")) {
          scriptItems.push({
            id: 'main-block',
            text: 'main() execution entry',
            level: 2,
            type: 'section',
          });
          return;
        }

        const bannerMatch = trimmed.match(/^#\s*[-=]{2,}\s*(.+?)\s*[-=]{2,}/);
        if (bannerMatch) {
          scriptItems.push({
            id: `banner-${idx}`,
            text: bannerMatch[1].trim(),
            level: 2,
            type: 'section',
          });
        }
      });
      if (scriptItems.length > 0) return scriptItems;
    }

    // CASE 3: MARKDOWN DOCUMENT
    if (content) {
      const mdItems: TocItem[] = [];
      const lines = content.split('\n');
      lines.forEach((line) => {
        const match = line.match(/^(#{1,4})\s+(.+)/);
        if (match) {
          const level = match[1].length;
          const rawText = match[2].trim().replace(/[*`_]/g, '');
          const id = rawText.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
          mdItems.push({ id, text: rawText, level, type: 'heading' });
        }
      });
      if (mdItems.length > 0) return mdItems;
    }

    // FALLBACK: Logical jump anchors so quick jump is never empty
    return [
      { id: 'top-of-lesson', text: 'Top of Lesson', level: 1, type: 'section' },
      { id: 'core-technical', text: 'Core Technical Architecture', level: 2, type: 'section' },
      { id: 'implementation', text: 'Implementation & Verification', level: 2, type: 'section' },
    ];
  }, [content, isNotebook, isScript, notebookCells]);

  // Estimated reading time
  const readingTime = useMemo(() => {
    if (!content) return 1;
    const words = content.trim().split(/\s+/).length;
    return Math.max(1, Math.ceil(words / 180));
  }, [content]);

  // Scroll Spy for active section
  useEffect(() => {
    const timer = setTimeout(() => {
      const container = document.querySelector('.markdown-body') || document.querySelector('main');
      if (!container) return;

      const headingEls = container.querySelectorAll('h1, h2, h3, h4');
      if (headingEls.length === 0) return;

      const observer = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) {
              const raw = entry.target.textContent || '';
              const match = items.find((h) =>
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
  }, [items]);

  // Scroll to section handler
  const scrollToItem = (item: TocItem) => {
    setActiveHeadingId(item.text);

    // If notebook cell
    if (item.cellIndex !== undefined) {
      const cellEl = document.getElementById(`notebook-cell-${item.cellIndex}`);
      if (cellEl) {
        cellEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        return;
      }
    }

    // If text heading in DOM
    const container = document.querySelector('.markdown-body') || document.body;
    const headingEls = container.querySelectorAll('h1, h2, h3, h4, [data-cell-index]');
    for (const el of Array.from(headingEls)) {
      if (el.textContent?.toLowerCase().includes(item.text.toLowerCase().slice(0, 18))) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        return;
      }
    }

    // Default: scroll to top if requested
    if (item.id === 'top-of-lesson') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="rounded-2xl bg-surface border border-border shadow-card p-4 space-y-4 sticky top-20">
      {/* Top Meta Bar */}
      <div className="flex items-center justify-between border-b border-border pb-3">
        <div className="flex items-center gap-1.5 text-fg-muted text-xs font-mono">
          <Clock className="w-3.5 h-3.5 text-blue-500" />
          <span>{readingTime} min read</span>
        </div>

        {onToggleBookmark && (
          <button 
            className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-2 py-1 rounded-lg text-xs transition flex items-center gap-1 border ${
              isBookmarked
                ? 'text-amber-600 dark:text-amber-400 bg-amber-500/10 border-amber-500/30 font-semibold'
                : 'text-fg-muted hover:text-fg border-border bg-surface-raised'
            }`} 
            onClick={onToggleBookmark}
            title={isBookmarked ? 'Remove Bookmark' : 'Bookmark this lesson'} 
          >
            <Bookmark className={`w-3 h-3 ${isBookmarked ? 'fill-current' : ''}`} />
            <span className="font-mono text-[11px]">{isBookmarked ? 'Saved' : 'Save'}</span>
          </button>
        )}
      </div>

      {/* Quick Jump List */}
      <div className="space-y-1.5">
        <div className="flex items-center justify-between px-1">
          <span className="text-xs font-mono font-bold uppercase tracking-wider text-fg-muted">
            {isScript ? 'Symbol Outline' : isNotebook ? 'Notebook Cells' : 'On This Page'}
          </span>
          <span className="text-[10px] font-mono text-fg-subtle">
            {items.length} sections
          </span>
        </div>

        <div className="space-y-0.5 max-h-[calc(100vh-21rem)] overflow-y-auto pr-1">
          {items.map((h, i) => {
            const isActive = activeHeadingId === h.text;
            return (
              <button 
                key={i}
                className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 w-full text-left py-1.5 px-2.5 rounded-lg text-xs leading-relaxed transition break-words block ${
                  isActive
                    ? 'bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 font-bold border-l-2 border-blue-600 shadow-xs'
                    : h.level >= 3 
                    ? 'pl-4 text-fg-muted hover:text-fg' 
                    : 'font-medium text-fg hover:text-blue-600 dark:hover:text-blue-400'
                } hover:bg-surface-raised`} 
                onClick={() => scrollToItem(h)}
                title={h.text} 
              >
                <div className="flex items-center gap-1.5 truncate">
                  {h.type === 'class' && <span className="text-[10px] font-mono px-1 py-0.2 rounded bg-purple-500/10 text-purple-600 dark:text-purple-400 font-bold">C</span>}
                  {h.type === 'function' && <span className="text-[10px] font-mono px-1 py-0.2 rounded bg-sky-500/10 text-sky-600 dark:text-sky-400 font-bold">f</span>}
                  <span className="truncate">{h.text}</span>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Local IDE Freedom Quick Actions Card */}
      {lessonFilePath && (
        <div className="pt-2 border-t border-border space-y-2">
          <div className="flex items-center gap-1.5 text-[11px] font-mono font-bold text-fg-muted uppercase tracking-wider">
            <Terminal className="w-3 h-3 text-blue-500" />
            <span>Local IDE & CLI</span>
          </div>

          <div className="grid grid-cols-2 gap-1.5">
            <button
              onClick={() => handleCopy(`code "${lessonFilePath}"`, 'code')}
              className="px-2 py-1.5 rounded-lg border border-border bg-surface-raised hover:bg-surface text-fg-muted hover:text-fg font-mono text-[10px] flex items-center justify-center gap-1 transition shadow-xs"
              title="Copy VS Code command"
            >
              {copiedCmd === 'code' ? <Check className="w-3 h-3 text-emerald-500" /> : <Code2 className="w-3 h-3 text-blue-500" />}
              <span>{copiedCmd === 'code' ? 'Copied!' : 'code .'}</span>
            </button>
            <button
              onClick={() => handleCopy(lessonFilePath.endsWith('.py') ? `python "${lessonFilePath}"` : `code "${lessonFilePath}"`, 'cli')}
              className="px-2 py-1.5 rounded-lg border border-border bg-surface-raised hover:bg-surface text-fg-muted hover:text-fg font-mono text-[10px] flex items-center justify-center gap-1 transition shadow-xs"
              title="Copy terminal path"
            >
              {copiedCmd === 'cli' ? <Check className="w-3 h-3 text-emerald-500" /> : <Play className="w-3 h-3 text-emerald-500" />}
              <span>{copiedCmd === 'cli' ? 'Copied!' : 'Copy CLI'}</span>
            </button>
          </div>

          <button
            onClick={scrollToTop}
            className="w-full py-1 rounded-lg text-fg-subtle hover:text-fg text-[11px] font-mono flex items-center justify-center gap-1 transition hover:bg-surface-raised"
          >
            <ArrowUp className="w-3 h-3" />
            <span>Top of Page</span>
          </button>
        </div>
      )}
    </div>
  );
};
