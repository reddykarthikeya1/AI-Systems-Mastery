import React from 'react';
import { ShieldCheck, Terminal, Award } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-20 border-t border-border/80 bg-white dark:bg-zinc-950 py-10 transition-colors text-zinc-500 text-xs">
      <div className="w-full max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 xl:px-10 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-1 text-center md:text-left">
          <div className="flex items-center justify-center md:justify-start gap-2 font-semibold text-fg">
            <span>AI Systems Mastery</span>
            <span className="text-xs font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
              Open Curriculum
            </span>
          </div>
          <p className="text-zinc-500 max-w-xl">
            Built for all types of learners and curated for everyone interested—from first-principles beginners to Staff/Principal systems architects.
          </p>
          <p className="text-xs text-zinc-400">
            © Karthikeya Reddy. All rights reserved.
          </p>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-5 text-xs font-mono text-zinc-500">
          <span className="flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" /> 1,609 Tests Verified
          </span>
          <span className="flex items-center gap-1.5">
            <Terminal className="w-3.5 h-3.5 text-zinc-400" /> Zero-Dependency Core
          </span>
          <span className="flex items-center gap-1.5">
            <Award className="w-3.5 h-3.5 text-zinc-400" /> Level 12 Standard
          </span>
        </div>
      </div>
    </footer>
  );
};
