import { useState, useEffect } from 'react';
import { ProgressPayload } from '../types';
import { fetchProgress, saveProgress } from '../services/api';

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
    };
  });

  // Sync from server on mount
  useEffect(() => {
    fetchProgress().then((remote) => {
      if (remote && remote.last_updated > (progress.last_updated || 0)) {
        setProgress(remote);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(remote));
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
      const completed_lessons = exists
        ? prev.completed_lessons.filter((id) => id !== lessonId)
        : [...prev.completed_lessons, lessonId];
      return { ...prev, completed_lessons };
    });
  };

  const toggleTheme = () => {
    updateProgress((prev) => {
      const theme = prev.theme === 'dark' ? 'light' : 'dark';
      return { ...prev, theme };
    });
  };

  return {
    progress,
    toggleLesson,
    toggleTheme,
    updateProgress,
    isLessonCompleted: (id: string) => progress.completed_lessons.includes(id),
  };
}
