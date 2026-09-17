import React from 'react';

export const LessonSkeleton: React.FC = () => {
  return (
    <div className="animate-pulse space-y-6 w-full max-w-[68ch] mx-auto py-6" aria-label="Loading lesson content">
      <div className="space-y-2">
        <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-1/4" />
        <div className="h-8 bg-zinc-200 dark:bg-zinc-800 rounded w-3/4" />
      </div>
      <div className="flex gap-2">
        <div className="h-5 bg-zinc-200 dark:bg-zinc-800 rounded-full w-24" />
        <div className="h-5 bg-zinc-200 dark:bg-zinc-800 rounded-full w-28" />
      </div>
      <div className="h-px bg-zinc-200 dark:bg-zinc-800 my-4" />
      <div className="space-y-3">
        <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-full" />
        <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-11/12" />
        <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-5/6" />
      </div>
      <div className="rounded-xl border border-border overflow-hidden bg-zinc-100 dark:bg-zinc-900/60 p-5 space-y-2.5">
        <div className="h-3.5 bg-zinc-200 dark:bg-zinc-800 rounded w-1/3" />
        <div className="h-3.5 bg-zinc-200 dark:bg-zinc-800 rounded w-2/3" />
        <div className="h-3.5 bg-zinc-200 dark:bg-zinc-800 rounded w-1/2" />
        <div className="h-3.5 bg-zinc-200 dark:bg-zinc-800 rounded w-3/4" />
      </div>
      <div className="space-y-3">
        <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-full" />
        <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-4/5" />
      </div>
    </div>
  );
};
