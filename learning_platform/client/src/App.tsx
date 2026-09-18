import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
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
import { PrerequisiteMapModal } from './components/PrerequisiteMapModal';
import { HardwareTopologyModal } from './components/HardwareTopologyModal';
import { LocalIdeGuideModal } from './components/LocalIdeGuideModal';
import { ErrorBoundary } from './components/ErrorBoundary';
import { LessonSkeleton } from './components/LessonSkeleton';
import { McqQuestion } from './components/McqQuizView';
import { AlertCircle, RotateCcw } from 'lucide-react';
// -----------------------------------------------------------------------------
// Top-Level Route Components (Declared outside App for stable component identities)
// -----------------------------------------------------------------------------

interface CourseSyllabusRouteProps {
  courses: CourseSummary[];
  loading: boolean;
  progress: any;
  getCourseModules: (courseId: string) => Promise<ModuleItem[]>;
  navigateToLesson: (filePath: string, lessonId: string, initialTab?: string) => void;
  navigate: (path: string) => void;
}

const CourseSyllabusRoute: React.FC<CourseSyllabusRouteProps> = ({
  courses,
  loading,
  progress,
  getCourseModules,
  navigateToLesson,
  navigate,
}) => {
  const { courseId } = useParams<{ courseId: string }>();
  const [mods, setMods] = useState<ModuleItem[]>([]);
  const [isLoadingMods, setIsLoadingMods] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  const course = courses.find((c) => c.id === courseId || c.folder_name === courseId);

  const loadModules = useCallback(() => {
    if (!courseId) return;
    setIsLoadingMods(true);
    setLoadError(null);
    let isMounted = true;
    getCourseModules(courseId)
      .then((data) => {
        if (isMounted) {
          if (!data || data.length === 0) {
            setLoadError('Failed to load track modules. The server returned an empty syllabus or is unreachable.');
          } else {
            setMods(data);
          }
          setIsLoadingMods(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setLoadError(err?.message || 'Failed to load track modules.');
          setIsLoadingMods(false);
        }
      });
    return () => { isMounted = false; };
  }, [courseId, getCourseModules]);

  useEffect(() => {
    const cleanup = loadModules();
    return cleanup;
  }, [loadModules]);

  if (!course && !loading) {
    return <Navigate to="/" replace />;
  }

  if (loadError) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-16 text-center">
        <div className="p-8 rounded-2xl bg-surface border border-border/80 shadow-sm space-y-4">
          <div className="w-12 h-12 mx-auto rounded-full bg-rose-500/10 text-rose-500 flex items-center justify-center">
            <AlertCircle className="w-6 h-6" />
          </div>
          <h2 className="text-lg font-bold text-fg">Failed to Load Track Modules</h2>
          <p className="text-sm text-fg-muted max-w-md mx-auto">
            {loadError}
          </p>
          <div className="pt-2">
            <button
              onClick={loadModules}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold uppercase tracking-wider transition-colors shadow-sm cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Retry Loading
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (isLoadingMods || !course) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <LessonSkeleton />
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

interface ClassroomRouteProps {
  courses: CourseSummary[];
  loading: boolean;
  progress: any;
  getCourseModules: (courseId: string) => Promise<ModuleItem[]>;
  navigateToLesson: (filePath: string, lessonId: string, initialTab?: string) => void;
  navigate: (path: string) => void;
  isLessonCompleted: (lessonId: string) => boolean;
  isBookmarked: (lessonId: string) => boolean;
  toggleLesson: (lessonId: string) => void;
  toggleBookmark: (lessonId: string) => void;
  saveQuizScore: (id: string, score: number, total: number, passed: boolean) => void;
  updateMasteryGate: (moduleId: string, updates: any) => void;
  saveNote: (lessonId: string, text: string) => void;
  handleQuizMistake: (question: McqQuestion, chosenOption: string) => void;
  setLastPosition: (pos: any) => void;
  updateSrsReview: (cardId: string, rating: number) => void;
}

const ClassroomRoute: React.FC<ClassroomRouteProps> = ({
  courses,
  loading,
  progress,
  getCourseModules,
  navigateToLesson,
  navigate,
  isLessonCompleted,
  isBookmarked,
  toggleLesson,
  toggleBookmark,
  saveQuizScore,
  updateMasteryGate,
  saveNote,
  handleQuizMistake,
  setLastPosition,
  updateSrsReview,
}) => {
  const { courseId, moduleNum, lessonId } = useParams<{ courseId: string; moduleNum: string; lessonId?: string }>();
  const [mods, setMods] = useState<ModuleItem[]>([]);
  const [isLoadingMods, setIsLoadingMods] = useState(true);

  const course = courses.find((c) => c.id === courseId || c.folder_name === courseId);

  useEffect(() => {
    if (!courseId) return;
    let isMounted = true;
    getCourseModules(courseId).then((data) => {
      if (isMounted) {
        setMods(data);
        setIsLoadingMods(false);
      }
    }).catch((err) => {
      if (isMounted) {
        console.error(`Failed to load modules for classroom ${courseId}:`, err);
        setIsLoadingMods(false);
      }
    });
    return () => { isMounted = false; };
  }, [courseId, getCourseModules]);

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
    if (!activeModule) return null;
    if (!lessonId) return activeModule.lessons[0] || null;
    return (
      activeModule.lessons.find((l) => l.id === lessonId || l.file_path.endsWith(lessonId)) ||
      activeModule.lessons[0] || null
    );
  }, [activeModule, lessonId]);

  // Record last visited position only once when activeLesson actually changes
  const recordedLessonIdRef = useRef<string | null>(null);
  useEffect(() => {
    if (course && activeModule && activeLesson) {
      if (recordedLessonIdRef.current !== activeLesson.id) {
        recordedLessonIdRef.current = activeLesson.id;
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
    }
  }, [course?.id, activeModule?.id, activeLesson?.id, setLastPosition]);

  if (!course && !loading) {
    return <Navigate to="/" replace />;
  }

  if (isLoadingMods || !course || !activeModule || !activeLesson) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <LessonSkeleton />
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
      onSrsReview={(rating) => updateSrsReview(activeLesson.id, rating)}
    />
  );
};

interface MasteryGateRouteProps {
  courses: CourseSummary[];
  loading: boolean;
  progress: any;
  getCourseModules: (courseId: string) => Promise<ModuleItem[]>;
  navigate: (path: string) => void;
  updateMasteryGate: (moduleId: string, updates: any) => void;
}

const MasteryGateRoute: React.FC<MasteryGateRouteProps> = ({
  courses,
  loading,
  progress,
  getCourseModules,
  navigate,
  updateMasteryGate,
}) => {
  const { courseId, moduleNum } = useParams<{ courseId: string; moduleNum: string }>();
  const [mods, setMods] = useState<ModuleItem[]>([]);
  const [isLoadingMods, setIsLoadingMods] = useState(true);

  const course = courses.find((c) => c.id === courseId || c.folder_name === courseId);

  useEffect(() => {
    if (!courseId) return;
    let isMounted = true;
    getCourseModules(courseId).then((data) => {
      if (isMounted) {
        setMods(data);
        setIsLoadingMods(false);
      }
    });
    return () => { isMounted = false; };
  }, [courseId, getCourseModules]);

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

export const App: React.FC = () => {
  const { 
    progress, 
    earnedXp,
    rankInfo,
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
    updateSrsReview,
    markProblemSolved,
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
  const [isPrereqMapOpen, setIsPrereqMapOpen] = useState(false);
  const [isHardwareModalOpen, setIsHardwareModalOpen] = useState(false);
  const [isIdeModalOpen, setIsIdeModalOpen] = useState(false);

  // Keyboard shortcut: Escape to close modals
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsCommandPaletteOpen(false);
        setIsStatsOpen(false);
        setIsBookmarksOpen(false);
        setIsFlashcardsOpen(false);
        setIsPortfolioOpen(false);
        setIsPrereqMapOpen(false);
        setIsHardwareModalOpen(false);
        setIsIdeModalOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Sync theme class to HTML element
  useEffect(() => {
    if (progress.theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [progress.theme]);

  // Clean Task Manager exit: notify backend when window or browser tab is closed
  useEffect(() => {
    const handleUnload = () => {
      try {
        if (navigator.sendBeacon) {
          navigator.sendBeacon('/api/client-disconnect');
        }
      } catch {
        // Ignore during fast unmount
      }
    };
    window.addEventListener('beforeunload', handleUnload);
    return () => window.removeEventListener('beforeunload', handleUnload);
  }, []);

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
    if (modulesMap[courseId] && modulesMap[courseId].length > 0) return modulesMap[courseId];
    try {
      const mods = await fetchCourseModules(courseId);
      if (mods && mods.length > 0) {
        setModulesMap((prev) => ({ ...prev, [courseId]: mods }));
      }
      return mods;
    } catch (e) {
      console.error(`Failed to load modules for ${courseId}`, e);
      throw e;
    }
  }, [modulesMap]);

  // Helper to resolve navigation to a file path and lesson ID
  const navigateToLesson = useCallback(async (filePath: string, lessonId: string, initialTab?: string) => {
    const parts = filePath.replace(/\\/g, '/').split('/');
    const courseFolder = parts[0];
    if (!courseFolder) return;

    try {
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
    } catch {
      // ignore
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



  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-bg text-slate-900 dark:text-slate-100 transition-colors font-sans antialiased">
      {/* Accessibility: Skip-to-content link */}
      <a 
        href="#main-content" 
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2.5 focus:bg-blue-600 focus:text-white focus:rounded-xl focus:shadow-2xl focus:font-semibold text-xs focus:ring-2 focus:ring-white"
      >
        Skip to main content
      </a>

      <Header
        progress={progress}
        courses={courses}
        rankInfo={rankInfo}
        earnedXp={earnedXp}
        onToggleTheme={toggleTheme}
        onToggleSound={toggleSound}
        onOpenSearch={() => setIsCommandPaletteOpen(true)}
        onOpenStats={() => setIsStatsOpen(true)}
        onOpenBookmarks={() => setIsBookmarksOpen(true)}
        onOpenFlashcards={() => setIsFlashcardsOpen(true)}
        onOpenPortfolio={() => setIsPortfolioOpen(true)}
        onOpenPrereqMap={() => setIsPrereqMapOpen(true)}
        onOpenHardwareTopology={() => setIsHardwareModalOpen(true)}
        onOpenIdeGuide={() => setIsIdeModalOpen(true)}
        onNavigateHome={() => navigate('/')}
      />

      <main id="main-content" role="main" tabIndex={-1} className="flex-1 focus:outline-none">
        <ErrorBoundary fallbackTitle="View Failed to Load">
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
                    onStartHere={() => {
                      // The first module of the first track assumes nothing. A
                      // newcomer should land in a lesson, not in a catalogue.
                      const first = courses[0];
                      navigate(first ? `/course/${first.id}/module/00` : '/');
                    }}
                    welcomeDismissed={progress.welcome_dismissed}
                    onDismissWelcome={() => updateProgress((prev) => ({
                      ...prev,
                      welcome_dismissed: true,
                    }))}
                    onResumeLastPosition={handleResumeLastPosition}
                    onOpenFlashcards={() => setIsFlashcardsOpen(true)}
                    onOpenPortfolio={() => setIsPortfolioOpen(true)}
                  />
                }
              />
              <Route
                path="/course/:courseId"
                element={
                  <CourseSyllabusRoute
                    courses={courses}
                    loading={loading}
                    progress={progress}
                    getCourseModules={getCourseModules}
                    navigateToLesson={navigateToLesson}
                    navigate={navigate}
                  />
                }
              />
              <Route
                path="/course/:courseId/module/:moduleNum"
                element={
                  <ClassroomRoute
                    courses={courses}
                    loading={loading}
                    progress={progress}
                    getCourseModules={getCourseModules}
                    navigateToLesson={navigateToLesson}
                    navigate={navigate}
                    isLessonCompleted={isLessonCompleted}
                    isBookmarked={isBookmarked}
                    toggleLesson={toggleLesson}
                    toggleBookmark={toggleBookmark}
                    saveQuizScore={saveQuizScore}
                    updateMasteryGate={updateMasteryGate}
                    saveNote={saveNote}
                    handleQuizMistake={handleQuizMistake}
                    setLastPosition={setLastPosition}
                    updateSrsReview={updateSrsReview}
                  />
                }
              />
              <Route
                path="/course/:courseId/module/:moduleNum/lesson/:lessonId"
                element={
                  <ClassroomRoute
                    courses={courses}
                    loading={loading}
                    progress={progress}
                    getCourseModules={getCourseModules}
                    navigateToLesson={navigateToLesson}
                    navigate={navigate}
                    isLessonCompleted={isLessonCompleted}
                    isBookmarked={isBookmarked}
                    toggleLesson={toggleLesson}
                    toggleBookmark={toggleBookmark}
                    saveQuizScore={saveQuizScore}
                    updateMasteryGate={updateMasteryGate}
                    saveNote={saveNote}
                    handleQuizMistake={handleQuizMistake}
                    setLastPosition={setLastPosition}
                    updateSrsReview={updateSrsReview}
                  />
                }
              />
              <Route
                path="/course/:courseId/module/:moduleNum/gate"
                element={
                  <MasteryGateRoute
                    courses={courses}
                    loading={loading}
                    progress={progress}
                    getCourseModules={getCourseModules}
                    navigate={navigate}
                    updateMasteryGate={updateMasteryGate}
                  />
                }
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          )}
        </ErrorBoundary>
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

      {/* Curriculum Dependency Roadmap Modal */}
      <PrerequisiteMapModal
        isOpen={isPrereqMapOpen}
        onClose={() => setIsPrereqMapOpen(false)}
        courses={courses as any}
        onSelectCourse={(courseId) => navigate(`/course/${courseId}`)}
      />

      {/* AI Systems Hardware Topology & Memory Hierarchy Explorer Modal */}
      <HardwareTopologyModal
        isOpen={isHardwareModalOpen}
        onClose={() => setIsHardwareModalOpen(false)}
      />

      {/* Local IDE & Terminal Workflow Guide Modal */}
      <LocalIdeGuideModal
        isOpen={isIdeModalOpen}
        onClose={() => setIsIdeModalOpen(false)}
      />
    </div>
  );
};
