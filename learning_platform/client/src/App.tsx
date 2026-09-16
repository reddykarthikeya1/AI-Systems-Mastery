import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Routes, Route, useNavigate, useParams, useLocation, Navigate } from 'react-router-dom';
import { CourseSummary, ModuleItem, LessonItem, CustomSrsCard } from './types';
import { fetchCourses, fetchCourseModules } from './services/api';
import { useProgress } from './hooks/useProgress';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { CourseCatalog } from './components/CourseCatalog';
import { SyllabusView } from './components/SyllabusView';
import { ClassroomView } from './components/ClassroomView';
import { MasteryGateView } from './components/MasteryGateView';
import { CommandPalette } from './components/CommandPalette';
import { StudyStatsModal } from './components/StudyStatsModal';
import { BookmarksModal } from './components/BookmarksModal';
import { FlashcardsModal } from './components/FlashcardsModal';
import { PortfolioModal } from './components/PortfolioModal';
import { McqQuestion } from './components/McqQuizView';
import { soundService } from './services/sound';

export const App: React.FC = () => {
  const { 
    progress, 
    toggleLesson, 
    toggleTheme, 
    toggleSound,
    setLastPosition,
    updateProgress, 
    isLessonCompleted,
    isBookmarked,
    toggleBookmark,
    saveQuizScore,
    saveNote,
    updateMasteryGate,
    addCustomSrsCard,
  } = useProgress();

  const navigate = useNavigate();
  const location = useLocation();

  const [courses, setCourses] = useState<CourseSummary[]>([]);
  const [modulesMap, setModulesMap] = useState<Record<string, ModuleItem[]>>({});
  const [loading, setLoading] = useState(true);

  // Modal dialog states
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
  const [isStatsOpen, setIsStatsOpen] = useState(false);
  const [isBookmarksOpen, setIsBookmarksOpen] = useState(false);
  const [isFlashcardsOpen, setIsFlashcardsOpen] = useState(false);
  const [isPortfolioOpen, setIsPortfolioOpen] = useState(false);

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

  // Helper to fetch or get cached modules
  const getCourseModules = useCallback(async (courseId: string): Promise<ModuleItem[]> => {
    if (modulesMap[courseId]) return modulesMap[courseId];
    try {
      const mods = await fetchCourseModules(courseId);
      setModulesMap((prev) => ({ ...prev, [courseId]: mods }));
      return mods;
    } catch (e) {
      console.error(`Failed to load modules for ${courseId}`, e);
      return [];
    }
  }, [modulesMap]);

  // Helper to resolve navigation to a file path and lesson ID
  const navigateToLesson = useCallback(async (filePath: string, lessonId: string, initialTab?: string) => {
    const parts = filePath.replace(/\\/g, '/').split('/');
    const courseFolder = parts[0];
    if (!courseFolder) return;

    const mods = await getCourseModules(courseFolder);
    for (const mod of mods) {
      const found = mod.lessons.find((l) => l.id === lessonId || l.file_path === filePath);
      if (found) {
        const modNumStr = mod.module_num.toString().padStart(2, '0');
        const tabQuery = initialTab ? `?tab=${initialTab}` : '';
        navigate(`/course/${courseFolder}/module/${modNumStr}/lesson/${found.id}${tabQuery}`);
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
      }
    }
  }, [getCourseModules, navigate]);

  // Handle auto-capturing missed quiz questions into Spaced Repetition (SRS)
  const handleQuizMistake = useCallback((question: McqQuestion, chosenOption: string) => {
    const cardId = `mistake-${question.id}-${question.question.slice(0, 20).toLowerCase().replace(/[^a-z0-9]/g, '')}`;
    const newCard: CustomSrsCard = {
      id: cardId,
      category: question.category || 'Quiz Mistakes',
      question: question.question,
      answer: question.explanation || (question.options[question.correctIndex] ?? ''),
      keyTakeaway: `Key Takeaway: ${question.options[question.correctIndex]} (Your choice: ${chosenOption})`,
      createdAt: Date.now(),
    };
    addCustomSrsCard(newCard);
  }, [addCustomSrsCard]);

  // Handle Jump Back In / Resume Last Position
  const handleResumeLastPosition = useCallback(async () => {
    const pos = progress.last_position;
    if (!pos) return;
    const mods = await getCourseModules(pos.course_id);
    const mod = mods.find((m) => m.id === pos.module_id) || mods[0];
    if (!mod) return;
    const modNumStr = mod.module_num.toString().padStart(2, '0');
    const lesson = mod.lessons.find((l) => l.id === pos.lesson_id || l.file_path === pos.lesson_path) || mod.lessons[0];
    if (lesson) {
      navigate(`/course/${pos.course_id}/module/${modNumStr}/lesson/${lesson.id}`);
    } else {
      navigate(`/course/${pos.course_id}`);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [progress.last_position, getCourseModules, navigate]);

  // Flatten all modules for bookmarks
  const allCachedModules = useMemo(() => {
    return Object.values(modulesMap).flat();
  }, [modulesMap]);

  // ---------------------------------------------------------------------------
  // Route Components
  // ---------------------------------------------------------------------------

  // 1. Course Syllabus Route Component
  const CourseSyllabusRoute: React.FC = () => {
    const { courseId } = useParams<{ courseId: string }>();
    const [mods, setMods] = useState<ModuleItem[]>([]);
    const [isLoadingMods, setIsLoadingMods] = useState(true);

    const course = courses.find((c) => c.id === courseId);

    useEffect(() => {
      if (!courseId) return;
      getCourseModules(courseId).then((data) => {
        setMods(data);
        setIsLoadingMods(false);
      });
    }, [courseId]);

    if (!course && !loading) {
      return <Navigate to="/" replace />;
    }

    if (isLoadingMods || !course) {
      return (
        <div className="flex items-center justify-center h-96 text-zinc-400 text-xs font-mono">
          Loading track modules and assessments...
        </div>
      );
    }

    return (
      <SyllabusView
        course={course}
        modules={mods}
        progress={progress}
        onBack={() => navigate('/')}
        onSelectLesson={(filePath, lessonId, initialTab) => {
          navigateToLesson(filePath, lessonId, initialTab);
        }}
        onOpenMasteryGate={(mod) => {
          const modNumStr = mod.module_num.toString().padStart(2, '0');
          navigate(`/course/${courseId}/module/${modNumStr}/gate`);
        }}
      />
    );
  };

  // 2. Classroom Lesson Route Component
  const ClassroomRoute: React.FC = () => {
    const { courseId, moduleNum, lessonId } = useParams<{ courseId: string; moduleNum: string; lessonId: string }>();
    const [mods, setMods] = useState<ModuleItem[]>([]);
    const [isLoadingMods, setIsLoadingMods] = useState(true);

    const course = courses.find((c) => c.id === courseId);

    useEffect(() => {
      if (!courseId) return;
      getCourseModules(courseId).then((data) => {
        setMods(data);
        setIsLoadingMods(false);
      });
    }, [courseId]);

    const activeModule = useMemo(() => {
      if (!mods.length || !moduleNum) return null;
      return mods.find(
        (m) =>
          m.module_num.toString().padStart(2, '0') === moduleNum ||
          m.module_num.toString() === moduleNum ||
          m.id === moduleNum
      );
    }, [mods, moduleNum]);

    const activeLesson = useMemo(() => {
      if (!activeModule || !lessonId) return null;
      return (
        activeModule.lessons.find((l) => l.id === lessonId || l.file_path.endsWith(lessonId)) ||
        activeModule.lessons[0]
      );
    }, [activeModule, lessonId]);

    // Record last visited position
    useEffect(() => {
      if (course && activeModule && activeLesson) {
        setLastPosition({
          course_id: course.id,
          course_title: course.title,
          module_id: activeModule.id,
          module_title: activeModule.title,
          lesson_id: activeLesson.id,
          lesson_title: activeLesson.title,
          lesson_path: activeLesson.file_path,
          updated_at: Date.now(),
        });
      }
    }, [course, activeModule, activeLesson]);

    if (!course && !loading) {
      return <Navigate to="/" replace />;
    }

    if (isLoadingMods || !course || !activeModule || !activeLesson) {
      return (
        <div className="flex items-center justify-center h-96 text-zinc-400 text-xs font-mono">
          Loading lesson runtime environment...
        </div>
      );
    }

    return (
      <ClassroomView
        courseTitle={course.title}
        courseId={course.id}
        module={activeModule}
        currentLesson={activeLesson}
        allLessons={activeModule.lessons}
        isCompleted={isLessonCompleted(activeLesson.id)}
        isBookmarked={isBookmarked(activeLesson.id)}
        savedQuizScore={progress.quiz_scores?.[activeLesson.id] || progress.quiz_scores?.[activeModule.id]}
        savedNote={progress.notes?.[activeLesson.id] || ''}
        completedLessons={progress.completed_lessons}
        onToggleComplete={() => toggleLesson(activeLesson.id)}
        onToggleBookmark={() => toggleBookmark(activeLesson.id)}
        onSaveQuizScore={(score, total, passed) => {
          saveQuizScore(activeLesson.id, score, total, passed);
          saveQuizScore(activeModule.id, score, total, passed);
          if (passed) {
            updateMasteryGate(activeModule.id, { quizPassed: true });
          }
        }}
        onPassLab={() => {
          updateMasteryGate(activeModule.id, { labPassed: true });
        }}
        onSaveNote={(text) => saveNote(activeLesson.id, text)}
        onBackToSyllabus={() => navigate(`/course/${courseId}`)}
        onSelectLesson={(filePath: string, nextId: string, initialTab?: string) => {
          navigateToLesson(filePath, nextId, initialTab);
        }}
        onOpenMasteryGate={() => {
          navigate(`/course/${courseId}/module/${moduleNum}/gate`);
        }}
        onQuizMistake={handleQuizMistake}
        onUpdateLastPosition={setLastPosition}
      />
    );
  };

  // 3. Module Mastery Gate Route Component
  const MasteryGateRoute: React.FC = () => {
    const { courseId, moduleNum } = useParams<{ courseId: string; moduleNum: string }>();
    const [mods, setMods] = useState<ModuleItem[]>([]);
    const [isLoadingMods, setIsLoadingMods] = useState(true);

    const course = courses.find((c) => c.id === courseId);

    useEffect(() => {
      if (!courseId) return;
      getCourseModules(courseId).then((data) => {
        setMods(data);
        setIsLoadingMods(false);
      });
    }, [courseId]);

    const activeModuleIndex = mods.findIndex(
      (m) =>
        m.module_num.toString().padStart(2, '0') === moduleNum ||
        m.module_num.toString() === moduleNum ||
        m.id === moduleNum
    );
    const activeModule = activeModuleIndex >= 0 ? mods[activeModuleIndex] : null;
    const nextModule = activeModuleIndex >= 0 && activeModuleIndex < mods.length - 1 ? mods[activeModuleIndex + 1] : null;

    if (!course && !loading) {
      return <Navigate to="/" replace />;
    }

    if (isLoadingMods || !course || !activeModule) {
      return (
        <div className="flex items-center justify-center h-96 text-zinc-400 text-xs font-mono">
          Evaluating module mastery requirements...
        </div>
      );
    }

    const quizLesson = activeModule.lessons.find((l) => l.type === 'quiz');
    const completedCount = activeModule.lessons.filter((l) => progress.completed_lessons.includes(l.id)).length;
    const gateStatus = progress.mastery_gates?.[activeModule.id];
    const quizScore = quizLesson 
      ? progress.quiz_scores?.[quizLesson.id] 
      : (activeModule.lessons.map((l) => progress.quiz_scores?.[l.id]).find(Boolean) || progress.quiz_scores?.[activeModule.id]);

    return (
      <MasteryGateView
        module={activeModule}
        courseTitle={course.title}
        gateStatus={gateStatus}
        completedLessonsCount={completedCount}
        totalLessonsCount={activeModule.lessons.length}
        quizScore={quizScore}
        onLaunchQuiz={() => {
          const target = quizLesson || activeModule.lessons[0];
          if (target) {
            navigate(`/course/${courseId}/module/${moduleNum}/lesson/${target.id}?tab=quiz`);
          }
        }}
        onLaunchLab={() => {
          if (activeModule.lessons.length > 0) {
            navigate(`/course/${courseId}/module/${moduleNum}/lesson/${activeModule.lessons[0].id}?tab=debug`);
          }
        }}
        onLaunchLesson={(lId) => {
          navigate(`/course/${courseId}/module/${moduleNum}/lesson/${lId}`);
        }}
        onClearGate={() => {
          updateMasteryGate(activeModule.id, { cleared: true, quizPassed: true, labPassed: true });
        }}
        onNextModule={
          nextModule
            ? () => {
                const nextNumStr = nextModule.module_num.toString().padStart(2, '0');
                if (nextModule.lessons.length > 0) {
                  navigate(`/course/${courseId}/module/${nextNumStr}/lesson/${nextModule.lessons[0].id}`);
                } else {
                  navigate(`/course/${courseId}`);
                }
              }
            : undefined
        }
        onBackToSyllabus={() => navigate(`/course/${courseId}`)}
      />
    );
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-[#0B0F17] text-slate-900 dark:text-slate-100 transition-colors font-sans antialiased">
      <Header
        progress={progress}
        courses={courses}
        onToggleTheme={toggleTheme}
        onToggleSound={toggleSound}
        onOpenSearch={() => setIsCommandPaletteOpen(true)}
        onOpenStats={() => setIsStatsOpen(true)}
        onOpenBookmarks={() => setIsBookmarksOpen(true)}
        onOpenFlashcards={() => setIsFlashcardsOpen(true)}
        onOpenPortfolio={() => setIsPortfolioOpen(true)}
        onNavigateHome={() => navigate('/')}
      />

      <main className="flex-1">
        {loading ? (
          <div className="flex items-center justify-center h-96 text-slate-500 text-xs font-mono">
            Loading Systems Engineering Academy Tracks...
          </div>
        ) : (
          <Routes>
            <Route
              path="/"
              element={
                <CourseCatalog
                  courses={courses}
                  progress={progress}
                  onSelectCourse={(courseId) => navigate(`/course/${courseId}`)}
                  onResumeLastPosition={handleResumeLastPosition}
                  onOpenFlashcards={() => setIsFlashcardsOpen(true)}
                  onOpenPortfolio={() => setIsPortfolioOpen(true)}
                />
              }
            />
            <Route path="/course/:courseId" element={<CourseSyllabusRoute />} />
            <Route path="/course/:courseId/module/:moduleNum/lesson/:lessonId" element={<ClassroomRoute />} />
            <Route path="/course/:courseId/module/:moduleNum/gate" element={<MasteryGateRoute />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        )}
      </main>

      <Footer />

      {/* Global Command Palette (Ctrl+K) */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onNavigateLesson={(path, id) => {
          navigateToLesson(path, id);
          setIsCommandPaletteOpen(false);
        }}
        onNavigateCourse={(cId) => {
          navigate(`/course/${cId}`);
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
        modules={allCachedModules}
        onSelectLesson={navigateToLesson}
        onRemoveBookmark={toggleBookmark}
      />

      {/* Spaced Repetition Flashcards Modal */}
      <FlashcardsModal
        isOpen={isFlashcardsOpen}
        onClose={() => setIsFlashcardsOpen(false)}
      />

      {/* Engineering Portfolio & Transcript Exporter Modal */}
      <PortfolioModal
        isOpen={isPortfolioOpen}
        onClose={() => setIsPortfolioOpen(false)}
        courses={courses}
        progress={progress}
      />
    </div>
  );
};
