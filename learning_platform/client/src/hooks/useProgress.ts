import { useState, useEffect } from 'react';
import { ProgressPayload, LastPosition, SrsCardReview } from '../types';
import { fetchProgress, saveProgress } from '../services/api';
import { soundService } from '../services/sound';

const STORAGE_KEY = 'study_progress_v2';

export function useProgress() {
  const [progress, setProgress] = useState<ProgressPayload>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) return JSON.parse(saved);
    } catch (e) {
      console.warn('Failed to parse local storage progress', e);
    }
    return {
      completed_lessons: [],
      completed_modules: [],
      last_updated: Date.now(),
      theme: 'dark',
      sound_enabled: true,
      quiz_scores: {},
      bookmarks: [],
      notes: {},
      srs_card_reviews: {},
      srs_custom_cards: [],
      mastery_gates: {},
      last_position: null,
      study_streak_days: 1,
    };
  });

  // Sync from server on mount
  useEffect(() => {
    fetchProgress().then((remote) => {
      if (remote && remote.last_updated > (progress.last_updated || 0)) {
        setProgress(remote);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(remote));
        if (remote.sound_enabled !== undefined) {
          soundService.setEnabled(remote.sound_enabled);
        }
      }
    });
  }, []);

  const updateProgress = (updater: (prev: ProgressPayload) => ProgressPayload) => {
    setProgress((prev) => {
      const next = updater(prev);
      next.last_updated = Date.now();
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      saveProgress(next);
      return next;
    });
  };

  const toggleLesson = (lessonId: string) => {
    updateProgress((prev) => {
      const exists = prev.completed_lessons.includes(lessonId);
      if (!exists) {
        soundService.playSuccess();
      } else {
        soundService.playClick();
      }
      const completed_lessons = exists
        ? prev.completed_lessons.filter((id) => id !== lessonId)
        : [...prev.completed_lessons, lessonId];
      return { ...prev, completed_lessons };
    });
  };

  const markLessonCompleted = (lessonId: string, completed: boolean = true) => {
    updateProgress((prev) => {
      const exists = prev.completed_lessons.includes(lessonId);
      if (completed && !exists) {
        soundService.playSuccess();
        return { ...prev, completed_lessons: [...prev.completed_lessons, lessonId] };
      } else if (!completed && exists) {
        return { ...prev, completed_lessons: prev.completed_lessons.filter((id) => id !== lessonId) };
      }
      return prev;
    });
  };

  const setLastPosition = (pos: LastPosition) => {
    updateProgress((prev) => ({
      ...prev,
      last_position: pos,
      current_course: pos.course_id,
      current_lesson: pos.lesson_id,
    }));
  };

  const toggleSound = () => {
    const nextState = soundService.toggle();
    updateProgress((prev) => ({
      ...prev,
      sound_enabled: nextState,
    }));
    return nextState;
  };

  const updateSrsReview = (cardId: string, rating: number) => {
    // SuperMemo SM-2 algorithm
    updateProgress((prev) => {
      const reviews = { ...(prev.srs_card_reviews || {}) };
      const current: SrsCardReview = reviews[cardId] || {
        interval_days: 0,
        repetition: 0,
        ease_factor: 2.5,
        next_review_epoch: 0,
      };

      let { repetition, interval_days, ease_factor } = current;
      const q = Math.max(0, Math.min(5, rating));

      // EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
      ease_factor = ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02));
      if (ease_factor < 1.3) ease_factor = 1.3;

      if (q < 3) {
        repetition = 0;
        interval_days = 1;
      } else {
        if (repetition === 0) {
          interval_days = 1;
        } else if (repetition === 1) {
          interval_days = 6;
        } else {
          interval_days = Math.round(interval_days * ease_factor);
        }
        repetition += 1;
      }

      const next_review_epoch = Date.now() + interval_days * 24 * 60 * 60 * 1000;
      reviews[cardId] = {
        interval_days,
        repetition,
        ease_factor: Number(ease_factor.toFixed(3)),
        next_review_epoch,
      };

      if (q >= 3) {
        soundService.playSuccess();
      } else {
        soundService.playError();
      }

      return {
        ...prev,
        srs_card_reviews: reviews,
      };
    });
  };

  const toggleTheme = () => {
    updateProgress((prev) => {
      soundService.playClick();
      const theme = prev.theme === 'dark' ? 'light' : 'dark';
      return { ...prev, theme };
    });
  };

  const saveQuizScore = (lessonId: string, score: number, total: number, passed: boolean) => {
    updateProgress((prev) => {
      const quiz_scores = { ...(prev.quiz_scores || {}) };
      quiz_scores[lessonId] = { score, total, passed } as any;
      if (passed) {
        soundService.playFanfare();
      } else {
        soundService.playError();
      }
      const completed_lessons = passed && !prev.completed_lessons.includes(lessonId)
        ? [...prev.completed_lessons, lessonId]
        : prev.completed_lessons;
      return { ...prev, quiz_scores, completed_lessons };
    });
  };

  const toggleBookmark = (lessonId: string) => {
    updateProgress((prev) => {
      soundService.playClick();
      const currentBookmarks = prev.bookmarks || [];
      const exists = currentBookmarks.includes(lessonId);
      const bookmarks = exists
        ? currentBookmarks.filter((id) => id !== lessonId)
        : [...currentBookmarks, lessonId];
      return { ...prev, bookmarks };
    });
  };

  const saveNote = (lessonId: string, text: string) => {
    updateProgress((prev) => {
      const notes = { ...(prev.notes || {}) };
      notes[lessonId] = text;
      return { ...prev, notes };
    });
  };

  const updateMasteryGate = (moduleId: string, updates: Partial<import('../types').MasteryGateStatus>) => {
    updateProgress((prev) => {
      const gates = { ...(prev.mastery_gates || {}) };
      const current = gates[moduleId] || {
        quizPassed: false,
        labPassed: false,
        cleared: false,
      };
      const updated = { ...current, ...updates };
      const isCleared = Boolean(updated.cleared || (updated.quizPassed && updated.labPassed));
      updated.cleared = isCleared;
      if (isCleared && !current.cleared) {
        updated.cleared_at = Date.now();
        soundService.playFanfare();
      }
      gates[moduleId] = updated;
      const completed_modules = isCleared && !prev.completed_modules.includes(moduleId)
        ? [...prev.completed_modules, moduleId]
        : prev.completed_modules;
      return { ...prev, mastery_gates: gates, completed_modules };
    });
  };

  const addCustomSrsCard = (card: import('../types').CustomSrsCard) => {
    updateProgress((prev) => {
      const existing = prev.srs_custom_cards || [];
      if (existing.some((c) => c.id === card.id || c.question === card.question)) {
        return prev;
      }
      const reviews = { ...(prev.srs_card_reviews || {}) };
      reviews[card.id] = {
        interval_days: 0,
        repetition: 0,
        ease_factor: 2.5,
        next_review_epoch: Date.now(),
      };
      return {
        ...prev,
        srs_custom_cards: [...existing, card],
        srs_card_reviews: reviews,
      };
    });
  };

  return {
    progress,
    toggleLesson,
    markLessonCompleted,
    setLastPosition,
    toggleSound,
    updateSrsReview,
    toggleTheme,
    updateProgress,
    saveQuizScore,
    toggleBookmark,
    saveNote,
    updateMasteryGate,
    addCustomSrsCard,
    isLessonCompleted: (id: string) => progress.completed_lessons.includes(id),
    isBookmarked: (id: string) => Boolean(progress.bookmarks?.includes(id)),
  };
}
