import React, { useEffect } from 'react';
import { FileText, Save, Sparkles } from 'lucide-react';

interface NotesTabProps {
  noteText: string;
  onChangeNoteText: (text: string) => void;
  onSaveNote: () => void;
  noteSavedAlert: boolean;
}

export const NotesTab: React.FC<NotesTabProps> = ({
  noteText,
  onChangeNoteText,
  onSaveNote,
  noteSavedAlert,
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') {
        e.preventDefault();
        onSaveNote();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onSaveNote]);

  const handleInsertPrompt = (prompt: string) => {
    onChangeNoteText((noteText ? noteText + '\n\n' : '') + prompt);
  };

  return (
    <div className="rounded-2xl bg-surface border border-border p-6 sm:p-8 shadow-sm space-y-4">
      <div className="flex items-center justify-between border-b border-border pb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-blue-500/10 text-blue-500">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-fg">Engineering Notebook</h2>
            <p className="text-xs text-fg-subtle">
              Notes automatically persist to your local study profile.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {noteSavedAlert && (
            <span className="text-xs font-mono text-emerald-500 flex items-center gap-1">
              ✓ Saved to study profile
            </span>
          )}
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 rounded-lg text-xs font-medium bg-blue-600 hover:bg-blue-700 text-white flex items-center gap-1.5 transition-colors shadow-xs" onClick={onSaveNote} >
            <Save className="w-3.5 h-3.5" />
            <span>Save Notes</span>
            <kbd className="hidden sm:inline-block text-[10px] font-mono px-1 py-0.2 rounded bg-blue-700 text-blue-200">
              Ctrl+S
            </kbd>
          </button>
        </div>
      </div>

      {!noteText.trim() && (
        <div className="p-3.5 rounded-xl bg-blue-50/60 dark:bg-blue-950/20 border border-blue-200/50 dark:border-blue-900/40 text-xs text-blue-900 dark:text-blue-300 space-y-2">
          <div className="flex items-center gap-1.5 font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-blue-500" />
            <span>Quick Start Prompts for Active Recall:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => handleInsertPrompt('### 🔑 Core Mathematical Invariants:\n- ')}
              className="px-2.5 py-1 rounded-lg bg-surface border border-blue-200 dark:border-blue-800 text-xs hover:bg-blue-50 dark:hover:bg-blue-900/40 transition"
            >
              + Core Invariants
            </button>
            <button
              onClick={() => handleInsertPrompt('### ⏱️ Complexity & Memory Footprint:\n- Time Complexity: O()\n- Space Complexity: O()\n- Cache / Allocations: ')}
              className="px-2.5 py-1 rounded-lg bg-surface border border-blue-200 dark:border-blue-800 text-xs hover:bg-blue-50 dark:hover:bg-blue-900/40 transition"
            >
              + Complexity Template
            </button>
            <button
              onClick={() => handleInsertPrompt('### ⚠️ Forensic Traps & Edge Cases:\n- ')}
              className="px-2.5 py-1 rounded-lg bg-surface border border-blue-200 dark:border-blue-800 text-xs hover:bg-blue-50 dark:hover:bg-blue-900/40 transition"
            >
              + Forensic Traps
            </button>
          </div>
        </div>
      )}

      <textarea
        value={noteText}
        onChange={(e) => onChangeNoteText(e.target.value)}
        placeholder="Write key takeaways, performance equations, and interview questions here..."
        className="w-full h-80 p-4 font-mono text-xs rounded-xl border border-border bg-surface/50 text-fg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y leading-relaxed"
      />
    </div>
  );
};
