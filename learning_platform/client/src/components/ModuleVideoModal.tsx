import React, { useEffect, useState } from 'react';
import { X, Loader2, AlertTriangle, Film } from 'lucide-react';
import { fetchModuleVideo } from '../services/api';
import { ModuleVideo } from '../types';
import { soundService } from '../services/sound';
import { VideoPlaylistPlayer } from './VideoPlaylistPlayer';

interface ModuleVideoModalProps {
  modulePath: string;
  moduleTitle: string;
  onClose: () => void;
}

/** Watch this module instead of - or alongside - reading it.
 *
 * Replaces the old syllabus "Video" button, which opened the entire course's
 * CURATED_VIDEO_LECTURES.md and left the reader to find their own module in
 * it. This fetches and plays the videos for exactly the module the reader
 * clicked - the primary lecture, plus any supplementary videos that between
 * them cover every concept the module's topic names.
 */
export const ModuleVideoModal: React.FC<ModuleVideoModalProps> = ({
  modulePath,
  moduleTitle,
  onClose,
}) => {
  const [video, setVideo] = useState<ModuleVideo | null>(null);
  const [state, setState] = useState<'loading' | 'ready' | 'missing'>('loading');

  useEffect(() => {
    let cancelled = false;
    setState('loading');
    fetchModuleVideo(modulePath).then((v) => {
      if (cancelled) return;
      if (v) {
        setVideo(v);
        setState('ready');
      } else {
        setState('missing');
      }
    });
    return () => {
      cancelled = true;
    };
  }, [modulePath]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [onClose]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={`Watch lecture for ${moduleTitle}`}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-3xl rounded-2xl bg-surface border border-border shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4 px-5 py-4 border-b border-border/80">
          <div className="min-w-0">
            <p className="text-[11px] font-mono uppercase tracking-wider text-rose-500 font-bold flex items-center gap-1.5">
              <Film className="w-3.5 h-3.5" /> Curated Video Lecture
              {state === 'ready' && video && video.supplementary.length > 0 && (
                <span className="text-fg-subtle normal-case font-medium">
                  &middot; {video.supplementary.length + 1} videos
                </span>
              )}
            </p>
            <h2 className="text-sm font-semibold text-fg truncate mt-0.5">{moduleTitle}</h2>
          </div>
          <button
            type="button"
            onClick={() => {
              soundService.playClick();
              onClose();
            }}
            aria-label="Close video"
            className="p-1.5 rounded-lg text-fg-muted hover:text-fg hover:bg-zinc-500/10 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 shrink-0"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {state === 'loading' && (
          <div className="aspect-video flex items-center justify-center bg-black">
            <Loader2 className="w-8 h-8 text-zinc-500 animate-spin" />
          </div>
        )}
        {state === 'missing' && (
          <div className="aspect-video flex items-center justify-center bg-black">
            <div className="text-center px-6 text-zinc-400">
              <AlertTriangle className="w-6 h-6 mx-auto mb-2 text-amber-500" />
              <p className="text-sm">No curated video is indexed for this module yet.</p>
            </div>
          </div>
        )}
        {state === 'ready' && video && (
          <div className="pb-4">
            <VideoPlaylistPlayer video={video} />
          </div>
        )}
      </div>
    </div>
  );
};
