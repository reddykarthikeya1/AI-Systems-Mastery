import React, { useState, useEffect } from 'react';
import { ArrowLeft, CheckCircle2, ChevronRight, ChevronLeft, BookOpen, Code2, Terminal as TermIcon, Award, Copy, Check } from 'lucide-react';
import { marked } from 'marked';
import katex from 'katex';
import confetti from 'canvas-confetti';
import { ModuleItem, LessonItem, TestResult } from '../types';
import { fetchFileContent, runTestCommand } from '../services/api';
import { TerminalRunner } from './TerminalRunner';

interface ClassroomViewProps {
  courseTitle: string;
  module: ModuleItem;
  currentLesson: LessonItem;
  allLessons: LessonItem[];
  isCompleted: boolean;
  onToggleComplete: () => void;
  onBackToSyllabus: () => void;
  onSelectLesson: (filePath: string, lessonId: string) => void;
}

export const ClassroomView: React.FC<ClassroomViewProps> = ({
  courseTitle,
  module,
  currentLesson,
  allLessons,
  isCompleted,
  onToggleComplete,
  onBackToSyllabus,
  onSelectLesson,
}) => {
  const [activeTab, setActiveTab] = useState<'theory' | 'code' | 'test'>('theory');
  const [content, setContent] = useState<string>('Loading lesson content...');
  const [codeContent, setCodeContent] = useState<string>('');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  // Load lesson content
  useEffect(() => {
    setContent('Loading lesson content...');
    fetchFileContent(currentLesson.file_path).then((data) => {
      setContent(data.content);
    }).catch((err) => {
      setContent(`Failed to load content: ${err.message}`);
    });
  }, [currentLesson.file_path]);

  // Load code preview if available
  useEffect(() => {
    const solutionTest = `${module.folder_path}/project_solution/`;
    // Try to fetch starter or test file
    fetchFileContent(`${module.folder_path}/00_quickstart_interactive_demo.py`).then((d) => {
      setCodeContent(d.content);
    }).catch(() => {
      setCodeContent('# Code preview available via terminal runner.');
    });
  }, [module.folder_path]);

  const handleCompleteClick = () => {
    if (!isCompleted) {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 },
      });
    }
    onToggleComplete();
  };

  const handleRunTests = async () => {
    setIsRunning(true);
    setTestResult(null);
    try {
      const res = await runTestCommand(module.folder_path, 'pytest');
      setTestResult(res);
    } catch (e: any) {
      setTestResult({
        exit_code: -1,
        stdout: '',
        stderr: e.message || 'Execution failed',
        duration_sec: 0,
        status: 'error',
      });
    } finally {
      setIsRunning(false);
    }
  };

  const handleRunDemo = async () => {
    if (!module.quickstart_script) return;
    setIsRunning(true);
    setTestResult(null);
    try {
      const res = await runTestCommand(module.quickstart_script, 'python');
      setTestResult(res);
    } catch (e: any) {
      setTestResult({
        exit_code: -1,
        stdout: '',
        stderr: e.message || 'Demo failed',
        duration_sec: 0,
        status: 'error',
      });
    } finally {
      setIsRunning(false);
    }
  };

  const currentIndex = allLessons.findIndex((l) => l.id === currentLesson.id);
  const prevLesson = currentIndex > 0 ? allLessons[currentIndex - 1] : null;
  const nextLesson = currentIndex < allLessons.length - 1 ? allLessons[currentIndex + 1] : null;

  // Render markdown with basic KaTeX rendering
  const renderMarkdown = (raw: string): string => {
    try {
      return marked.parse(raw, { async: false }) as string;
    } catch {
      return raw;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      {/* Breadcrumb & Navigation Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-zinc-200/80 dark:border-zinc-800/80">
        <button
          onClick={onBackToSyllabus}
          className="inline-flex items-center gap-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> {courseTitle}
        </button>

        <div className="flex items-center gap-2.5">
          <button
            onClick={handleCompleteClick}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all border ${
              isCompleted
                ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300'
                : 'bg-zinc-100 dark:bg-zinc-800/80 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            {isCompleted ? 'Completed' : 'Mark as Complete'}
          </button>

          <div className="flex items-center gap-1">
            <button
              onClick={() => prevLesson && onSelectLesson(prevLesson.file_path, prevLesson.id)}
              disabled={!prevLesson}
              className="p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-800 disabled:opacity-30 hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-400 transition-colors"
              title="Previous Lesson"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => nextLesson && onSelectLesson(nextLesson.file_path, nextLesson.id)}
              disabled={!nextLesson}
              className="p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-800 disabled:opacity-30 hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-400 transition-colors"
              title="Next Lesson"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Grid: Sidebar + Content */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
        {/* Left Sidebar: Lesson Outline */}
        <div className="lg:col-span-1 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 p-4 shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-3 sticky top-20">
          <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider block">
            Module {module.module_num.toString().padStart(2, '0')} Outline
          </span>

          <div className="space-y-1">
            {allLessons.map((l) => {
              const active = l.id === currentLesson.id;
              return (
                <button
                  key={l.id}
                  onClick={() => onSelectLesson(l.file_path, l.id)}
                  className={`w-full text-left px-2.5 py-1.5 rounded-md text-xs transition-colors line-clamp-1 ${
                    active
                      ? 'bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 font-medium border-l-2 border-coursera-blue pl-2'
                      : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-50 dark:hover:bg-zinc-800/40'
                  }`}
                >
                  {l.title}
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Area: Tabs & Player */}
        <div className="lg:col-span-3 space-y-4">
          {/* Content Tabs */}
          <div className="flex items-center gap-1.5 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-2">
            <button
              onClick={() => setActiveTab('theory')}
              className={`px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-1.5 transition-colors ${
                activeTab === 'theory'
                  ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900'
                  : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" /> Lesson Architecture
            </button>

            <button
              onClick={() => setActiveTab('test')}
              className={`px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-1.5 transition-colors ${
                activeTab === 'test'
                  ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900'
                  : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
              }`}
            >
              <TermIcon className="w-3.5 h-3.5" /> Test & Execution Console
            </button>
          </div>

          {/* Active Tab Views */}
          {activeTab === 'theory' && (
            <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 p-8 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
              <div
                className="markdown-body text-zinc-800 dark:text-zinc-200 text-sm leading-relaxed"
                dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
              />
            </div>
          )}

          {activeTab === 'test' && (
            <div className="space-y-4">
              <TerminalRunner
                result={testResult}
                isRunning={isRunning}
                onRunTest={handleRunTests}
                onRunDemo={handleRunDemo}
                hasDemo={Boolean(module.quickstart_script)}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
