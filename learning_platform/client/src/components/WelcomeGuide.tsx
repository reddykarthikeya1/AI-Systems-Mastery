import React from 'react';
import { BookOpen, Bug, ShieldCheck, ArrowRight, X } from 'lucide-react';
import { soundService } from '../services/sound';

interface WelcomeGuideProps {
  /** Where "Start the first lesson" goes. */
  onStartHere: () => void;
  onDismiss: () => void;
}

const STEPS = [
  {
    icon: BookOpen,
    title: 'Read, then run it',
    body:
      'Every module opens with a plain-language guide and a playground script you ' +
      'run yourself. Nothing is asserted that you cannot check.',
    tint: 'text-sky-500 bg-sky-500/10 border-sky-500/30',
  },
  {
    icon: Bug,
    title: 'Break something on purpose',
    body:
      'Each module ships a Bug Lab: working code with one real defect planted in ' +
      'it. You read the symptoms, find the cause, and patch it.',
    tint: 'text-rose-500 bg-rose-500/10 border-rose-500/30',
  },
  {
    icon: ShieldCheck,
    title: 'Clear the gate',
    body:
      'A module counts as done when the lessons are read, the quiz is passed, the ' +
      'lab is fixed and the project tests go green. Not before.',
    tint: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/30',
  },
];

/** First-run orientation.
 *
 * Shown only while nothing has been completed. Twelve tracks and 175 modules is
 * a lot to land on with no route through it, and the catalog's own advice - that
 * you need not follow any particular order - is the wrong first thing to read if
 * you do not yet know where the bottom of the ladder is.
 */
export const WelcomeGuide: React.FC<WelcomeGuideProps> = ({ onStartHere, onDismiss }) => (
  <section
    aria-labelledby="welcome-heading"
    className="relative rounded-2xl border border-blue-500/30 bg-gradient-to-br from-blue-500/10 via-indigo-500/5 to-transparent p-6 sm:p-7 shadow-sm"
  >
    <button
      type="button"
      onClick={() => {
        soundService.playClick();
        onDismiss();
      }}
      aria-label="Dismiss the getting started guide"
      className="absolute top-4 right-4 p-1.5 rounded-lg text-fg-muted hover:text-fg hover:bg-zinc-500/10 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500"
    >
      <X className="w-4 h-4" />
    </button>

    <p className="text-xs font-mono uppercase tracking-wider text-blue-500 font-bold">
      New here
    </p>
    <h2 id="welcome-heading" className="mt-1 text-xl sm:text-2xl font-bold text-fg">
      Three steps, then you are off
    </h2>
    <p className="mt-2 text-sm text-fg-muted max-w-2xl">
      You do not need to pick a track yet. Start at the first lesson of Advanced
      Python &mdash; it assumes nothing &mdash; and the rest of the catalog will make
      more sense once one module is behind you.
    </p>

    <ol className="mt-6 grid gap-4 sm:grid-cols-3">
      {STEPS.map((step, i) => (
        <li
          key={step.title}
          className="rounded-xl border border-border/80 bg-surface/60 p-4 space-y-2"
        >
          <div className="flex items-center gap-2.5">
            <span
              className={`w-8 h-8 rounded-lg border flex items-center justify-center shrink-0 ${step.tint}`}
            >
              <step.icon className="w-4 h-4" />
            </span>
            <span className="text-xs font-mono text-fg-muted">Step {i + 1}</span>
          </div>
          <h3 className="text-sm font-semibold text-fg">{step.title}</h3>
          <p className="text-xs text-fg-muted leading-relaxed">{step.body}</p>
        </li>
      ))}
    </ol>

    <div className="mt-6 flex flex-wrap items-center gap-3">
      <button
        type="button"
        onClick={() => {
          soundService.playClick();
          onStartHere();
        }}
        className="px-5 py-2.5 rounded-lg font-semibold text-xs bg-blue-600 hover:bg-blue-500 text-white transition-colors flex items-center gap-2 shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500"
      >
        Start the first lesson
        <ArrowRight className="w-3.5 h-3.5" />
      </button>
      <button
        type="button"
        onClick={() => {
          soundService.playClick();
          onDismiss();
        }}
        className="px-3 py-2 rounded-lg text-xs font-medium text-fg-muted hover:text-fg hover:bg-zinc-500/10 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500"
      >
        I have done this before
      </button>
    </div>
  </section>
);
