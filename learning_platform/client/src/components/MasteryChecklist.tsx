import React, { useState, useEffect, useMemo } from 'react';
import { CheckSquare, Square, Award } from 'lucide-react';

interface MasteryChecklistProps {
  lessonId: string;
  content: string;
}

export const MasteryChecklist: React.FC<MasteryChecklistProps> = ({ lessonId, content }) => {
  // Extract mastery checklist items
  const items = useMemo(() => {
    if (!content) return [];
    const lines = content.split('\n');
    const result: string[] = [];
    let inMasterySection = false;

    for (const line of lines) {
      const trimmed = line.trim();
      if (
        trimmed.startsWith('## You have mastered this when you can') ||
        trimmed.startsWith('## Mastery Checklist') ||
        trimmed.startsWith('### What You Should Now Be Able To Do') ||
        trimmed.startsWith('## Core Competencies')
      ) {
        inMasterySection = true;
        continue;
      }

      if (inMasterySection && trimmed.startsWith('## ')) {
        // Next major section reached
        break;
      }

      if (inMasterySection) {
        const match = trimmed.match(/^[-*]\s+\[[ xX]?\]\s+(.+)/);
        if (match) {
          result.push(match[1].trim());
        } else if (trimmed.match(/^[-*]\s+(.+)/) && trimmed.length > 5) {
          result.push(trimmed.replace(/^[-*]\s+/, '').trim());
        }
      }
    }

    return result;
  }, [content]);

  const storageKey = `mastery_${lessonId}`;
  const [checkedIndices, setCheckedIndices] = useState<number[]>([]);

  useEffect(() => {
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        setCheckedIndices(JSON.parse(saved));
      } else {
        setCheckedIndices([]);
      }
    } catch {
      setCheckedIndices([]);
    }
  }, [storageKey]);

  const toggleIndex = (idx: number) => {
    const updated = checkedIndices.includes(idx)
      ? checkedIndices.filter((i) => i !== idx)
      : [...checkedIndices, idx];
    setCheckedIndices(updated);
    try {
      localStorage.setItem(storageKey, JSON.stringify(updated));
    } catch {
      // ignore
    }
  };

  if (items.length === 0) return null;

  const percent = Math.round((checkedIndices.length / items.length) * 100);

  return (
    <div className="mt-10 p-6 rounded-2xl bg-zinc-50/90 dark:bg-zinc-900/50 border border-border shadow-xs space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-border/80 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-blue-500/10 text-blue-500">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-fg">
              You should now be able to...
            </h3>
            <p className="text-xs text-fg-subtle">
              Self-assess your engineering grasp before advancing.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="w-24 h-2 rounded-full bg-zinc-200 dark:bg-zinc-800 overflow-hidden">
            <div
              className="h-full bg-blue-500 transition-all duration-300"
              style={{ width: `${percent}%` }}
            />
          </div>
          <span className="text-xs font-mono font-bold text-blue-600 dark:text-blue-400">
            {checkedIndices.length}/{items.length} ({percent}%)
          </span>
        </div>
      </div>

      <div className="space-y-2">
        {items.map((item, idx) => {
          const isChecked = checkedIndices.includes(idx);
          return (
            <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 w-full text-left p-3 rounded-xl border text-xs leading-relaxed flex items-start gap-3 transition-all ${
                isChecked
                  ? 'bg-blue-50/50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-900/40 text-fg'
                  : 'bg-surface border-border text-fg-muted hover:border-blue-300 dark:hover:border-blue-800'
              }`} key={idx}
              onClick={() => toggleIndex(idx)} >
              <div className="mt-0.5 shrink-0 text-blue-500">
                {isChecked ? <CheckSquare className="w-4 h-4" /> : <Square className="w-4 h-4 text-zinc-400" />}
              </div>
              <span className={isChecked ? 'line-through opacity-80' : ''}>
                {item}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
