import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  ChevronLeft,
  ChevronRight,
  RotateCcw,
  Activity,
  Sliders,
  Sparkles,
  Layers,
} from 'lucide-react';

export interface TraceFrame {
  step: number;
  description: string;
  array?: (number | string)[];
  pointers?: Record<string, number>; // e.g., { left: 0, right: 7, mid: 3 }
  highlights?: Record<number, 'active' | 'comparing' | 'pivot' | 'sorted' | 'swapped' | 'visited'>;
  variables?: Record<string, string | number | boolean>;
  callStack?: string[];
  invariants?: string;
}

export interface TraceData {
  title: string;
  algorithm: string;
  timeComplexity: string;
  spaceComplexity: string;
  frames: TraceFrame[];
}

// Built-in sample trace for Binary Search if none is passed
const DEFAULT_SAMPLE_TRACE: TraceData = {
  title: 'Binary Search Step-by-Step State Scrubber',
  algorithm: 'Binary Search (Find Target = 23)',
  timeComplexity: 'O(log n)',
  spaceComplexity: 'O(1)',
  frames: [
    {
      step: 1,
      description: 'Initialize search window: left = 0, right = 7. Target is 23.',
      array: [2, 5, 8, 12, 16, 23, 38, 56],
      pointers: { left: 0, right: 7 },
      highlights: { 0: 'active', 7: 'active' },
      variables: { left: 0, right: 7, mid: -1, target: 23, found: false },
      invariants: 'Search space: indices [0..7]',
    },
    {
      step: 2,
      description: 'Compute mid = (0 + 7) // 2 = 3. Compare array[3] (12) with target (23).',
      array: [2, 5, 8, 12, 16, 23, 38, 56],
      pointers: { left: 0, mid: 3, right: 7 },
      highlights: { 0: 'active', 3: 'comparing', 7: 'active' },
      variables: { left: 0, right: 7, mid: 3, 'array[mid]': 12, target: 23 },
      invariants: '12 < 23 → Target must reside in right half [mid + 1..right]',
    },
    {
      step: 3,
      description: 'Adjust window: left = mid + 1 = 4. Discard left sub-array [0..3].',
      array: [2, 5, 8, 12, 16, 23, 38, 56],
      pointers: { left: 4, right: 7 },
      highlights: { 4: 'active', 7: 'active' },
      variables: { left: 4, right: 7, mid: 3, target: 23 },
      invariants: 'Active search range contracted to [4..7]',
    },
    {
      step: 4,
      description: 'Compute new mid = (4 + 7) // 2 = 5. Compare array[5] (23) with target (23).',
      array: [2, 5, 8, 12, 16, 23, 38, 56],
      pointers: { left: 4, mid: 5, right: 7 },
      highlights: { 4: 'active', 5: 'comparing', 7: 'active' },
      variables: { left: 4, right: 7, mid: 5, 'array[mid]': 23, target: 23 },
      invariants: 'Target match detected at index 5!',
    },
    {
      step: 5,
      description: 'Target 23 found at index 5. Return 5 in 2 comparisons.',
      array: [2, 5, 8, 12, 16, 23, 38, 56],
      pointers: { match: 5 },
      highlights: { 5: 'sorted' },
      variables: { resultIndex: 5, comparisons: 2, status: 'SUCCESS' },
      invariants: 'Invariant maintained: 23 == array[5]',
    },
  ],
};

interface AlgorithmTraceScrubberProps {
  trace?: TraceData;
  onStepChange?: (step: number) => void;
  className?: string;
}

export const AlgorithmTraceScrubber: React.FC<AlgorithmTraceScrubberProps> = ({
  trace = DEFAULT_SAMPLE_TRACE,
  onStepChange,
  className = '',
}) => {
  const [currentStepIdx, setCurrentStepIdx] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1000); // ms per step
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const frames = trace.frames || [];
  const currentFrame = frames[currentStepIdx] || frames[0];
  const totalSteps = frames.length;

  // Step navigation
  const goToStep = (idx: number) => {
    const clamped = Math.max(0, Math.min(totalSteps - 1, idx));
    setCurrentStepIdx(clamped);
    if (onStepChange) onStepChange(clamped + 1);
  };

  const handleNext = () => {
    if (currentStepIdx < totalSteps - 1) {
      goToStep(currentStepIdx + 1);
    } else {
      setIsPlaying(false);
    }
  };

  const handlePrev = () => {
    goToStep(currentStepIdx - 1);
  };

  const handleReset = () => {
    setIsPlaying(false);
    goToStep(0);
  };

  // Playback timer
  useEffect(() => {
    if (isPlaying) {
      timerRef.current = setInterval(() => {
        setCurrentStepIdx((prev) => {
          if (prev < totalSteps - 1) {
            return prev + 1;
          } else {
            setIsPlaying(false);
            return prev;
          }
        });
      }, playbackSpeed);
    } else if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, playbackSpeed, totalSteps]);

  // Pointer labels for an array index
  const getPointersForIndex = (idx: number): string[] => {
    if (!currentFrame?.pointers) return [];
    return Object.entries(currentFrame.pointers)
      .filter(([_, ptrIdx]) => ptrIdx === idx)
      .map(([ptrName]) => ptrName);
  };

  // Cell highlight style classes
  const getHighlightClass = (idx: number) => {
    const hl = currentFrame?.highlights?.[idx];
    switch (hl) {
      case 'active':
        return 'border-sky-500 bg-sky-500/15 text-sky-400 font-bold shadow-sm shadow-sky-500/20 ring-1 ring-sky-500/30';
      case 'comparing':
        return 'border-amber-500 bg-amber-500/20 text-amber-400 font-bold shadow-sm shadow-amber-500/20 scale-105 ring-2 ring-amber-500/40';
      case 'pivot':
        return 'border-violet-500 bg-violet-500/20 text-violet-400 font-bold shadow-sm shadow-violet-500/20 ring-2 ring-violet-500/40';
      case 'sorted':
        return 'border-emerald-500 bg-emerald-500/20 text-emerald-400 font-bold shadow-sm shadow-emerald-500/20 ring-2 ring-emerald-500/40';
      case 'swapped':
        return 'border-rose-500 bg-rose-500/20 text-rose-400 font-bold scale-105 ring-2 ring-rose-500/40';
      default:
        return 'border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900/60 text-zinc-700 dark:text-zinc-300';
    }
  };

  return (
    <div
      className={`rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-[#0c0e14] overflow-hidden shadow-sm my-6 ${className}`}
    >
      {/* Header bar */}
      <div className="px-5 py-3.5 border-b border-zinc-200 dark:border-zinc-800 flex flex-wrap items-center justify-between gap-3 bg-white/50 dark:bg-zinc-900/40">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-sky-500/10 text-sky-500 border border-sky-500/20">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-bold font-mono text-zinc-900 dark:text-zinc-100 uppercase tracking-wider flex items-center gap-2">
              <span>{trace.algorithm}</span>
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-500 font-normal">
                Trace Scrubber
              </span>
            </h4>
            <div className="flex items-center gap-2 text-[11px] font-mono text-zinc-500 dark:text-zinc-400">
              <span>Time: {trace.timeComplexity}</span>
              <span>•</span>
              <span>Space: {trace.spaceComplexity}</span>
            </div>
          </div>
        </div>

        {/* Step Indicator & Speed control */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1 bg-zinc-100 dark:bg-zinc-800/80 px-2.5 py-1 rounded-lg border border-zinc-200 dark:border-zinc-700/60 text-xs font-mono font-semibold text-zinc-700 dark:text-zinc-300">
            <span>Step</span>
            <span className="text-sky-500 font-bold">{currentStepIdx + 1}</span>
            <span className="text-zinc-400">/</span>
            <span>{totalSteps}</span>
          </div>

          <div className="flex items-center gap-1 text-[11px] font-mono">
            {[
              { label: '0.5x', ms: 1500 },
              { label: '1x', ms: 900 },
              { label: '2x', ms: 450 },
            ].map((spd) => (
              <button
                key={spd.label}
                onClick={() => setPlaybackSpeed(spd.ms)}
                className={`px-2 py-0.5 rounded text-xs transition-colors ${
                  playbackSpeed === spd.ms
                    ? 'bg-sky-500/20 text-sky-600 dark:text-sky-400 font-bold border border-sky-500/30'
                    : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'
                }`}
              >
                {spd.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Visualizer Area */}
      <div className="p-6 space-y-6">
        {/* Frame Explanation Banner */}
        <div className="p-3.5 rounded-xl bg-sky-500/10 dark:bg-sky-950/20 border border-sky-500/20 flex items-start gap-3">
          <Sparkles className="w-4 h-4 text-sky-500 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <p className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 leading-relaxed">
              {currentFrame?.description}
            </p>
            {currentFrame?.invariants && (
              <p className="text-[11px] font-mono text-sky-600 dark:text-sky-400">
                Invariant: {currentFrame.invariants}
              </p>
            )}
          </div>
        </div>

        {/* Array Visualization with Pointers */}
        {currentFrame?.array && currentFrame.array.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-[11px] font-mono text-zinc-500">
              <span className="flex items-center gap-1">
                <Layers className="w-3.5 h-3.5" /> Array State (Length: {currentFrame.array.length})
              </span>
              <span className="text-[10px] text-zinc-400">Hover cell for details</span>
            </div>

            <div className="flex items-end justify-center gap-2 sm:gap-3 py-4 overflow-x-auto min-h-[110px]">
              {currentFrame.array.map((val, idx) => {
                const pointers = getPointersForIndex(idx);
                return (
                  <div key={idx} className="flex flex-col items-center gap-1.5 shrink-0">
                    {/* Pointer Tags on top */}
                    <div className="h-5 flex items-center justify-center gap-1">
                      {pointers.map((ptr) => (
                        <span
                          key={ptr}
                          className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/20 text-amber-500 border border-amber-500/30 uppercase tracking-tight animate-bounce"
                        >
                          {ptr} ↓
                        </span>
                      ))}
                    </div>

                    {/* Array Cell */}
                    <div
                      className={`w-11 h-12 sm:w-13 sm:h-14 rounded-xl border flex items-center justify-center text-sm sm:text-base font-mono font-bold transition-all duration-300 ${getHighlightClass(
                        idx
                      )}`}
                    >
                      {val}
                    </div>

                    {/* Index Label */}
                    <span className="text-[10px] font-mono text-zinc-400 dark:text-zinc-600">
                      [{idx}]
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Variables Inspector */}
        {currentFrame?.variables && Object.keys(currentFrame.variables).length > 0 && (
          <div className="rounded-xl border border-zinc-200/80 dark:border-zinc-800 bg-white dark:bg-zinc-900/40 p-3.5 space-y-2">
            <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-1.5">
              <Sliders className="w-3.5 h-3.5" /> Internal Loop Variables
            </div>
            <div className="flex flex-wrap items-center gap-2">
              {Object.entries(currentFrame.variables).map(([key, val]) => (
                <div
                  key={key}
                  className="px-2.5 py-1 rounded-lg bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-xs font-mono flex items-center gap-1.5"
                >
                  <span className="text-zinc-500 dark:text-zinc-400">{key}:</span>
                  <span className="font-bold text-sky-600 dark:text-sky-400">
                    {String(val)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Timeline Slider */}
        <div className="space-y-1.5 pt-2">
          <input
            type="range"
            min="0"
            max={totalSteps - 1}
            value={currentStepIdx}
            onChange={(e) => goToStep(parseInt(e.target.value, 10))}
            className="w-full h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-sky-500"
          />
          <div className="flex justify-between text-[10px] font-mono text-zinc-400">
            <span>Start (Step 1)</span>
            <span>End (Step {totalSteps})</span>
          </div>
        </div>
      </div>

      {/* Control Toolbar */}
      <div className="px-5 py-3 border-t border-zinc-200 dark:border-zinc-800 bg-white/60 dark:bg-zinc-900/50 flex items-center justify-between">
        {/* Reset button */}
        <button
          onClick={handleReset}
          className="p-2 rounded-xl text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1.5 text-xs font-mono"
          title="Reset to Step 1"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Reset</span>
        </button>

        {/* Playback Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => goToStep(0)}
            disabled={currentStepIdx === 0}
            className="p-2 rounded-xl text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30 disabled:pointer-events-none transition-colors"
            title="First Step"
          >
            <SkipBack className="w-4 h-4" />
          </button>

          <button
            onClick={handlePrev}
            disabled={currentStepIdx === 0}
            className="p-2 rounded-xl text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30 disabled:pointer-events-none transition-colors"
            title="Previous Step"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>

          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`px-4 py-2 rounded-xl font-mono text-xs font-bold transition-all flex items-center gap-2 shadow-sm ${
              isPlaying
                ? 'bg-amber-500 hover:bg-amber-600 text-white shadow-amber-500/20'
                : 'bg-sky-500 hover:bg-sky-600 text-white shadow-sky-500/20'
            }`}
          >
            {isPlaying ? (
              <>
                <Pause className="w-4 h-4 fill-current" /> Pause
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" /> Auto Play
              </>
            )}
          </button>

          <button
            onClick={handleNext}
            disabled={currentStepIdx === totalSteps - 1}
            className="p-2 rounded-xl text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30 disabled:pointer-events-none transition-colors"
            title="Next Step"
          >
            <ChevronRight className="w-5 h-5" />
          </button>

          <button
            onClick={() => goToStep(totalSteps - 1)}
            disabled={currentStepIdx === totalSteps - 1}
            className="p-2 rounded-xl text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30 disabled:pointer-events-none transition-colors"
            title="Last Step"
          >
            <SkipForward className="w-4 h-4" />
          </button>
        </div>

        {/* Quick status */}
        <div className="text-right hidden sm:block">
          <span className="text-[11px] font-mono text-zinc-400">
            {currentStepIdx === totalSteps - 1 ? '✓ Complete' : 'Interactive Mode'}
          </span>
        </div>
      </div>
    </div>
  );
};
