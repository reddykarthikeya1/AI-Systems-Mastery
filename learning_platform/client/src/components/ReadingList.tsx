import React from 'react';
import { ExternalLink } from 'lucide-react';
import { ModuleReading } from '../types';

/** Verified written explainers for a module - the read-instead-of-watch path.
 *
 * Each page was fetched and its text checked for the concepts shown as chips,
 * so a reader can see which concept each link is there to teach.
 */
export const ReadingList: React.FC<{ reading: ModuleReading }> = ({ reading }) => (
  <div className="space-y-3">
    <p className="text-xs text-zinc-500 dark:text-zinc-400">
      {reading.pages.length} verified {reading.pages.length === 1 ? 'page' : 'pages'} for this module. Links open in a new tab.
    </p>
    <ul className="space-y-3">
      {reading.pages.map((p) => (
        <li key={p.url}>
          <a
            href={p.url}
            target="_blank"
            rel="noopener noreferrer"
            className="block rounded-xl border border-border bg-card p-4 shadow-card hover:border-sky-500/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 transition-colors"
          >
            <div className="flex items-start justify-between gap-3">
              <span className="text-sm font-semibold text-foreground">{p.title}</span>
              <ExternalLink className="w-3.5 h-3.5 mt-0.5 shrink-0 text-zinc-400" aria-hidden />
            </div>
            <div className="mt-1 text-[11px] font-mono text-zinc-500">{p.host}</div>
            {p.covers.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1.5">
                {p.covers.map((c) => (
                  <span key={c} className="rounded-full bg-sky-500/10 px-2 py-0.5 text-[11px] text-sky-700 dark:text-sky-300">
                    {c}
                  </span>
                ))}
              </div>
            )}
          </a>
        </li>
      ))}
    </ul>
    {reading.uncovered.length > 0 && (
      <p className="text-xs text-amber-600 dark:text-amber-400">
        No verified page yet for: {reading.uncovered.join(', ')}. Use the lesson text for these.
      </p>
    )}
  </div>
);
