import React, { useState, useEffect } from 'react';
import { CourseSummary, ModuleItem, LessonItem } from './types';
import { fetchCourses, fetchCourseModules } from './services/api';
import { useProgress } from './hooks/useProgress';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { CourseCatalog } from './components/CourseCatalog';
import { SyllabusView } from './components/SyllabusView';
import { ClassroomView } from './components/ClassroomView';
import { CommandPalette } from './components/CommandPalette';
import { StudyStatsModal } from './components/StudyStatsModal';
import { BookmarksModal } from './components/BookmarksModal';

export const App: React.FC = () => {
  const { 
    progress, 
    toggleLesson, 
    toggleTheme, 
    updateProgress, 
    isLessonCompleted,
    isBookmarked,
    toggleBookmark,
    saveQuizScore,
    saveNote,
  } = useProgress();

  const [courses, setCourses] = useState<CourseSummary[]>([]);
  const [currentCourseId, setCurrentCourseId] = useState<string | null>(null);
  const [modules, setModules] = useState<ModuleItem[]>([]);
  const [currentModule, setCurrentModule] = useState<ModuleItem | null>(null);
  const [currentLesson, setCurrentLesson] = useState<LessonItem | null>(null);

  // Modal dialog states
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
  const [isStatsOpen, setIsStatsOpen] = useState(false);
  const [isBookmarksOpen, setIsBookmarksOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  // Sync theme class to HTML element
  useEffect(() => {
    if (progress.theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [progress.theme]);

  // Load all courses on mount
  useEffect(() => {
    fetchCourses().then((data) => {
      setCourses(data);
      setLoading(false);
    }).catch((e) => {
      console.error('Error fetching courses:', e);
      setLoading(false);
    });
  }, []);

  // Global Keyboard shortcuts: Ctrl+K or Cmd+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleSelectCourse = async (courseId: string) => {
    setCurrentCourseId(courseId);
    setCurrentModule(null);
    setCurrentLesson(null);
    updateProgress((prev) => ({ ...prev, current_course: courseId }));
    try {
      const mods = await fetchCourseModules(courseId);
      setModules(mods);
    } catch (e) {
      console.error('Failed to load modules', e);
    }
  };

  const handleSelectLesson = (filePath: string, lessonId: string) => {
    for (const mod of modules) {
      const found = mod.lessons.find((l) => l.id === lessonId || l.file_path === filePath);
      if (found) {
        setCurrentModule(mod);
        setCurrentLesson(found);
        updateProgress((prev) => ({ ...prev, current_lesson: lessonId }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
        break;
      }
    }
  };

  // Navigate directly from global search / spotlight palette
  const handleNavigateFromSearch = async (filePath: string, lessonId: string) => {
    const parts = filePath.replace(/\\/g, '/').split('/');
    const courseFolder = parts[0];

    if (courseFolder && courseFolder !== currentCourseId) {
      try {
        const mods = await fetchCourseModules(courseFolder);
        setModules(mods);
        setCurrentCourseId(courseFolder);
        for (const mod of mods) {
          const found = mod.lessons.find((l) => l.id === lessonId || l.file_path === filePath);
          if (found) {
            setCurrentModule(mod);
            setCurrentLesson(found);
            updateProgress((prev) => ({ ...prev, current_course: courseFolder, current_lesson: lessonId }));
            window.scrollTo({ top: 0, behavior: 'smooth' });
            break;
          }
        }
      } catch (e) {
        console.error('Failed to switch course from search', e);
      }
    } else {
      handleSelectLesson(filePath, lessonId);
    }
  };

  const activeCourse = courses.find((c) => c.id === currentCourseId);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-[#0B0F17] text-slate-900 dark:text-slate-100 transition-colors font-sans antialiased">
      <Header
        progress={progress}
        courses={courses}
        onToggleTheme={toggleTheme}
        onOpenSearch={() => setIsCommandPaletteOpen(true)}
        onOpenStats={() => setIsStatsOpen(true)}
        onOpenBookmarks={() => setIsBookmarksOpen(true)}
        onNavigateHome={() => {
          setCurrentCourseId(null);
          setCurrentModule(null);
          setCurrentLesson(null);
        }}
      />

      <main className="flex-1">
        {loading ? (
          <div className="flex items-center justify-center h-96 text-slate-500 text-sm font-mono">
            Loading Principal Engineering Academy Curriculums...
          </div>
        ) : currentLesson && currentModule && activeCourse ? (
          <ClassroomView
            courseTitle={activeCourse.title}
            module={currentModule}
            currentLesson={currentLesson}
            allLessons={currentModule.lessons}
            isCompleted={isLessonCompleted(currentLesson.id)}
            isBookmarked={isBookmarked(currentLesson.id)}
            savedQuizScore={progress.quiz_scores?.[currentLesson.id] as any}
            savedNote={progress.notes?.[currentLesson.id] || ''}
            completedLessons={progress.completed_lessons}
            onToggleComplete={() => toggleLesson(currentLesson.id)}
            onToggleBookmark={() => toggleBookmark(currentLesson.id)}
            onSaveQuizScore={(score, total, passed) => saveQuizScore(currentLesson.id, score, total, passed)}
            onSaveNote={(text) => saveNote(currentLesson.id, text)}
            onBackToSyllabus={() => {
              setCurrentModule(null);
              setCurrentLesson(null);
            }}
            onSelectLesson={handleSelectLesson}
          />
        ) : activeCourse ? (
          <SyllabusView
            course={activeCourse}
            modules={modules}
            progress={progress}
            onBack={() => setCurrentCourseId(null)}
            onSelectLesson={handleSelectLesson}
          />
        ) : (
          <CourseCatalog
            courses={courses}
            progress={progress}
            onSelectCourse={handleSelectCourse}
          />
        )}
      </main>

      <Footer />

      {/* Global Command Palette (Ctrl+K) */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onNavigateLesson={(path, id) => {
          handleNavigateFromSearch(path, id);
          setIsCommandPaletteOpen(false);
        }}
        onNavigateCourse={(cId) => {
          handleSelectCourse(cId);
          setIsCommandPaletteOpen(false);
        }}
        onToggleTheme={toggleTheme}
        theme={progress.theme}
        onOpenStats={() => {
          setIsCommandPaletteOpen(false);
          setIsStatsOpen(true);
        }}
      />

      {/* Daily Study Streak & Learning Analytics Modal */}
      <StudyStatsModal
        isOpen={isStatsOpen}
        onClose={() => setIsStatsOpen(false)}
        progress={progress}
        courses={courses}
      />

      {/* Bookmarked Lessons Modal */}
      <BookmarksModal
        isOpen={isBookmarksOpen}
        onClose={() => setIsBookmarksOpen(false)}
        bookmarks={progress.bookmarks || []}
        modules={modules}
        onSelectLesson={handleSelectLesson}
        onRemoveBookmark={toggleBookmark}
      />
    </div>
  );
};
