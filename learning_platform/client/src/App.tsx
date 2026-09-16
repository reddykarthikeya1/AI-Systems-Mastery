import React, { useState, useEffect } from 'react';
import { CourseSummary, ModuleItem, LessonItem } from './types';
import { fetchCourses, fetchCourseModules } from './services/api';
import { useProgress } from './hooks/useProgress';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { CourseCatalog } from './components/CourseCatalog';
import { SyllabusView } from './components/SyllabusView';
import { ClassroomView } from './components/ClassroomView';
import { SearchModal } from './components/SearchModal';

export const App: React.FC = () => {
  const { progress, toggleLesson, toggleTheme, updateProgress, isLessonCompleted } = useProgress();
  const [courses, setCourses] = useState<CourseSummary[]>([]);
  const [currentCourseId, setCurrentCourseId] = useState<string | null>(null);
  const [modules, setModules] = useState<ModuleItem[]>([]);
  const [currentModule, setCurrentModule] = useState<ModuleItem | null>(null);
  const [currentLesson, setCurrentLesson] = useState<LessonItem | null>(null);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
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

  // Keyboard shortcut Ctrl+K for search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setIsSearchOpen(true);
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
    // Find module and lesson
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

  const activeCourse = courses.find((c) => c.id === currentCourseId);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-[#0B0F17] text-slate-900 dark:text-slate-100 transition-colors">
      <Header
        progress={progress}
        courses={courses}
        onToggleTheme={toggleTheme}
        onOpenSearch={() => setIsSearchOpen(true)}
        onNavigateHome={() => {
          setCurrentCourseId(null);
          setCurrentModule(null);
          setCurrentLesson(null);
        }}
      />

      <main className="flex-1">
        {loading ? (
          <div className="flex items-center justify-center h-96 text-slate-500 text-sm">
            Loading Engineering Academy Curriculums...
          </div>
        ) : currentLesson && currentModule && activeCourse ? (
          <ClassroomView
            courseTitle={activeCourse.title}
            module={currentModule}
            currentLesson={currentLesson}
            allLessons={currentModule.lessons}
            isCompleted={isLessonCompleted(currentLesson.id)}
            completedLessons={progress.completed_lessons}
            onToggleComplete={() => toggleLesson(currentLesson.id)}
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

      <SearchModal
        isOpen={isSearchOpen}
        courses={courses}
        onClose={() => setIsSearchOpen(false)}
        onSelectCourse={handleSelectCourse}
      />
    </div>
  );
};
