import React from 'react';
import { FileText, Save } from 'lucide-react';

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
          <button
            onClick={onSaveNote}
            className="px-3 py-1.5 rounded-lg text-xs font-medium bg-blue-600 hover:bg-blue-700 text-white flex items-center gap-1.5 transition-colors"
          >
            <Save className="w-3.5 h-3.5" /> Save Notes
          </button>
        </div>
      </div>

      <textarea
        value={noteText}
        onChange={(e) => onChangeNoteText(e.target.value)}
        placeholder="Write key takeaways, performance equations, and interview questions here..."
        className="w-full h-80 p-4 font-mono text-xs rounded-xl border border-border bg-zinc-50 dark:bg-zinc-900/50 text-fg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y leading-relaxed"
      />
    </div>
  );
};
