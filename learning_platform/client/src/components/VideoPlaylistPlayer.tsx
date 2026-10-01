import React, { useMemo, useState } from 'react';
import { ExternalLink, PlayCircle } from 'lucide-react';
import { ModuleVideo } from '../types';

interface ActiveVideo {
  title: string;
  url: string;
  embed_url: string;
  channel: string;
  /** The primary's "why this video" blurb, or a supplementary's "covers: X". */
  note: string;
}

/** Player + switcher for a module's curated video(s).
 *
 * A module whose topic names several concepts ("Vector Spaces, Span, Bases &
 * Rank") isn't fully taught by one video, so `video.supplementary` holds
 * further videos each pinned to the concept the primary doesn't cover. This
 * plays the primary by default and lets the viewer switch to any of them -
 * shared between the syllabus's video modal and the in-lesson "Watch Video"
 * tab so the two don't drift into different behaviour.
 */
export const VideoPlaylistPlayer: React.FC<{ video: ModuleVideo }> = ({ video }) => {
  const [activeIndex, setActiveIndex] = useState(0); // 0 = primary, 1.. = supplementary

  const playlist: ActiveVideo[] = useMemo(() => [
    { title: video.title, url: video.url, embed_url: video.embed_url, channel: video.channel, note: video.focus },
    ...video.supplementary.map((s) => ({
      title: s.title,
      url: s.url,
      embed_url: s.embed_url,
      channel: s.channel,
      note: `Covers: ${s.covers}`,
    })),
  ], [video]);

  const active = playlist[Math.min(activeIndex, playlist.length - 1)];

  return (
    <div className="space-y-3">
      <div className="aspect-video rounded-2xl overflow-hidden bg-black border border-border shadow-card">
        <iframe
          key={active.embed_url}
          className="w-full h-full"
          src={`${active.embed_url}?rel=0`}
          title={active.title}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      </div>

      <div className="px-1 space-y-2">
        <div className="flex items-start justify-between gap-3">
          <h3 className="text-sm font-semibold text-fg leading-snug">{active.title}</h3>
          <a
            href={active.url}
            target="_blank"
            rel="noopener noreferrer"
            className="shrink-0 inline-flex items-center gap-1.5 text-xs font-medium text-blue-600 dark:text-blue-400 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 rounded"
          >
            Open on YouTube <ExternalLink className="w-3 h-3" />
          </a>
        </div>
        <p className="text-xs text-fg-muted">
          <span className="font-medium text-fg-subtle">{active.channel}</span>
          {active.note && <span> &middot; {active.note}</span>}
        </p>

        {playlist.length > 1 && (
          <div className="pt-1 flex flex-wrap gap-2">
            {playlist.map((p, i) => (
              <button
                key={p.embed_url}
                type="button"
                onClick={() => setActiveIndex(i)}
                className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium border transition-colors max-w-[220px] ${
                  i === activeIndex
                    ? 'bg-rose-600 border-rose-600 text-white'
                    : 'bg-zinc-100 dark:bg-zinc-800 border-border text-fg-muted hover:text-fg'
                }`}
                title={p.title}
              >
                <PlayCircle className="w-3.5 h-3.5 shrink-0" />
                <span className="truncate">{i === 0 ? 'Main lecture' : p.note.replace(/^Covers:\s*/, '')}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
