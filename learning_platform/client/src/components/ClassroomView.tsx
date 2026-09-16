import React, { useState, useEffect } from 'react';
import { ArrowLeft, CheckCircle2, ChevronRight, ChevronLeft, BookOpen, Code2, Terminal as TermIcon, Award, Copy, Check, Play, Terminal } from 'lucide-react';
import { marked } from 'marked';
import katex from 'katex';
import confetti from 'canvas-confetti';
import { ModuleItem, LessonItem, TestResult } from '../types';
import { fetchFileContent, runTestCommand } from '../services/api';
import { TerminalRunner } from './TerminalRunner';
import { SideCodeRunner } from './SideCodeRunner';

interface ClassroomViewProps {
  courseTitle: string;
  module: ModuleItem;
  currentLesson: LessonItem;
  allLessons: LessonItem[];
  isCompleted: boolean;
  onToggleComplete: () => void;
  onBackToSyllabus: () => void;
  onSelectLesson: (filePath: string, lessonId: string) => void;
  completedLessons?: string[];
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
  completedLessons = [],
}) => {
  const [activeTab, setActiveTab] = useState<'theory' | 'code' | 'test'>('theory');
  const [content, setContent] = useState<string>('Loading lesson content...');
  const [codeContent, setCodeContent] = useState<string>('');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [testResult, setTestResult] = useState<TestResult | null>(null);

  // Side-by-side interactive code runner state
  const [isScratchpadOpen, setIsScratchpadOpen] = useState<boolean>(false);
  const [scratchpadCode, setScratchpadCode] = useState<string>('');

  // Event listener for "Try in Scratchpad" button clicks from rendered code blocks
  useEffect(() => {
    const handleSnippetRun = (e: any) => {
      if (e.detail?.code) {
        setScratchpadCode(e.detail.code);
        setIsScratchpadOpen(true);
      }
    };
    window.addEventListener('open-scratchpad-with-code', handleSnippetRun);
    return () => window.removeEventListener('open-scratchpad-with-code', handleSnippetRun);
  }, []);

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
    fetchFileContent(`${module.folder_path}/00_quickstart_interactive_demo.py`).then((d) => {
      setCodeContent(d.content);
    }).catch(() => {
      setCodeContent('# Code preview available via terminal runner.');
    });
  }, [module.folder_path]);

  // Enhance rendered code blocks with language badge, 1-click copy, and "Try It" run button
  useEffect(() => {
    if (activeTab !== 'theory') return;
    const timer = setTimeout(() => {
      const container = document.querySelector('.markdown-body');
      if (!container) return;

      const preElements = container.querySelectorAll('pre');
      preElements.forEach((pre) => {
        if (pre.getAttribute('data-enhanced')) return;
        pre.setAttribute('data-enhanced', 'true');

        const codeEl = pre.querySelector('code');
        const codeText = codeEl ? codeEl.innerText : pre.innerText;

        // Detect language
        let lang = 'Code';
        let isPython = false;
        if (codeEl) {
          const match = codeEl.className.match(/language-(\w+)/);
          if (match) lang = match[1].toUpperCase();
          else if (codeText.startsWith('$') || codeText.includes('pytest') || codeText.includes('python -m')) lang = 'BASH';
          else if (codeText.includes('def ') || codeText.includes('import ') || codeText.includes('class ') || codeText.includes('print(')) {
            lang = 'PYTHON';
            isPython = true;
          }
        }
        if (lang === 'PYTHON' || lang === 'PY') isPython = true;

        // Create top bar
        const header = document.createElement('div');
        header.className = 'flex items-center justify-between px-3.5 py-1.5 bg-[#161B22] border-b border-zinc-800 text-[11px] font-mono text-zinc-400 select-none';

        const label = document.createElement('span');
        label.className = 'font-semibold text-zinc-300';
        label.innerText = lang;

        const btnGroup = document.createElement('div');
        btnGroup.className = 'flex items-center gap-2';

        // Add "Try It / Run" button for Python snippets
        if (isPython || (!codeText.startsWith('$') && !codeText.includes('bash'))) {
          const runSnippetBtn = document.createElement('button');
          runSnippetBtn.className = 'hover:text-emerald-300 px-2 py-0.5 rounded hover:bg-emerald-950/60 transition-colors flex items-center gap-1 text-emerald-400 font-semibold text-[11px] border border-emerald-500/30';
          runSnippetBtn.innerHTML = '<span>▶ Run</span>';
          runSnippetBtn.title = 'Open in Live Scratchpad and Execute';
          runSnippetBtn.onclick = () => {
            window.dispatchEvent(new CustomEvent('open-scratchpad-with-code', { detail: { code: codeText } }));
          };
          btnGroup.appendChild(runSnippetBtn);
        }

        const copyBtn = document.createElement('button');
        copyBtn.className = 'hover:text-white px-2 py-0.5 rounded hover:bg-zinc-800/80 transition-colors flex items-center gap-1';
        copyBtn.innerText = 'Copy';
        copyBtn.onclick = () => {
          navigator.clipboard.writeText(codeText);
          copyBtn.innerText = '✓ Copied';
          copyBtn.style.color = '#34D399';
          setTimeout(() => {
            copyBtn.innerText = 'Copy';
            copyBtn.style.color = '';
          }, 2000);
        };

        btnGroup.appendChild(copyBtn);
        header.appendChild(label);
        header.appendChild(btnGroup);

        pre.style.marginTop = '0';
        pre.style.borderTop = 'none';
        pre.style.borderTopLeftRadius = '0';
        pre.style.borderTopRightRadius = '0';

        const wrapper = document.createElement('div');
        wrapper.className = 'my-5 rounded-xl border border-zinc-300 dark:border-zinc-800 overflow-hidden shadow-sm bg-[#0D1117]';

        pre.parentNode?.insertBefore(wrapper, pre);
        wrapper.appendChild(header);
        wrapper.appendChild(pre);
      });
    }, 100);

    return () => clearTimeout(timer);
  }, [content, activeTab]);

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

  const renderMarkdown = (raw: string): string => {
    try {
      return marked.parse(raw, { async: false }) as string;
    } catch {
      return raw;
    }
  };

  return (
    <div className={`mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 transition-all duration-300 ${isScratchpadOpen ? 'max-w-[1720px]' : 'max-w-7xl'}`}>
      {/* Top Bar Navigation & Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-4">
        <div className="flex items-center gap-3">
          <button
            onClick={onBackToSyllabus}
            className="p-2 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 transition-colors text-zinc-600 dark:text-zinc-400"
            title="Back to Course Syllabus"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="text-[11px] font-mono text-zinc-400 dark:text-zinc-500 uppercase tracking-wider flex items-center gap-1.5">
              <span>{courseTitle}</span>
              <ChevronRight className="w-3 h-3 text-zinc-400" />
              <span>Module {module.module_num.toString().padStart(2, '0')}</span>
            </div>
            <h1 className="text-base sm:text-lg font-semibold text-zinc-900 dark:text-zinc-100 line-clamp-1">
              {currentLesson.title}
            </h1>
          </div>
        </div>

        <div className="flex items-center gap-2 self-stretch sm:self-auto justify-end">
          {/* Live Side Runner Toggle */}
          <button
            onClick={() => setIsScratchpadOpen(!isScratchpadOpen)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-2 transition-all shadow-sm ${
              isScratchpadOpen
                ? 'bg-emerald-50 dark:bg-emerald-950/60 border-emerald-300 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300'
                : 'bg-zinc-100 dark:bg-zinc-800/90 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700'
            }`}
            title="Toggle side-by-side interactive code runner"
          >
            <Terminal className="w-3.5 h-3.5 text-emerald-500" />
            <span>Live Runner</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          </button>

          {/* Mark Complete Toggle */}
          <button
            onClick={handleCompleteClick}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-1.5 transition-all shadow-sm ${
              isCompleted
                ? 'bg-emerald-50 dark:bg-emerald-950/50 border-emerald-300 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300'
                : 'bg-zinc-100 dark:bg-zinc-800/90 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
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

      {/* Main Container: Left Syllabus + Center Reader + Right Live Code Runner */}
      <div className="flex gap-6 items-start">
        {/* Left Column + Center Reader */}
        <div className="flex-1 min-w-0">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
            {/* Left Sidebar: Lesson Outline */}
            <div className="lg:col-span-1 rounded-xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-4 shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-3 sticky top-20">
              <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-2">
                <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider">
                  Module {module.module_num.toString().padStart(2, '0')} Outline
                </span>
                <span className="text-[10px] font-mono text-zinc-400">
                  {allLessons.filter((l) => completedLessons.includes(l.id)).length}/{allLessons.length}
                </span>
              </div>

              <div className="space-y-1">
                {allLessons.map((l, idx) => {
                  const active = l.id === currentLesson.id;
                  const isDone = completedLessons.includes(l.id);

                  return (
                    <button
                      key={l.id}
                      onClick={() => onSelectLesson(l.file_path, l.id)}
                      className={`w-full text-left px-2.5 py-2 rounded-lg text-xs transition-all flex items-center justify-between gap-2 ${
                        active
                          ? 'bg-blue-50 dark:bg-blue-950/60 text-coursera-blue dark:text-blue-400 font-semibold border border-blue-200 dark:border-blue-900/60 shadow-sm'
                          : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100/70 dark:hover:bg-zinc-800/50'
                      }`}
                    >
                      <span className="line-clamp-1 flex items-center gap-2">
                        <span className="font-mono text-[10px] text-zinc-400">0{idx + 1}</span>
                        <span>{l.title}</span>
                      </span>
                      {isDone ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      ) : (
                        <div className="w-1.5 h-1.5 rounded-full bg-zinc-300 dark:bg-zinc-700 shrink-0" />
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Right Area: Tabs & Reader */}
            <div className="lg:col-span-3 space-y-4">
              {/* Content Tabs */}
              <div className="flex items-center gap-2 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-2">
                <button
                  onClick={() => setActiveTab('theory')}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 transition-colors ${
                    activeTab === 'theory'
                      ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 shadow-sm'
                      : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
                  }`}
                >
                  <BookOpen className="w-3.5 h-3.5" /> Lesson Architecture
                </button>

                <button
                  onClick={() => setActiveTab('test')}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 transition-colors ${
                    activeTab === 'test'
                      ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 shadow-sm'
                      : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
                  }`}
                >
                  <TermIcon className="w-3.5 h-3.5" /> Pytest & Execution Console
                </button>
              </div>

              {/* Active Tab Views */}
              {activeTab === 'theory' && (
                <div className="rounded-xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-8 sm:p-10 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
                  <div
                    className="markdown-body text-zinc-800 dark:text-zinc-200 text-sm leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
                  />

                  {/* Bottom Lesson Navigation Cards */}
                  <div className="mt-12 pt-8 border-t border-zinc-200/80 dark:border-zinc-800/80 flex flex-col sm:flex-row items-center justify-between gap-4">
                    {prevLesson ? (
                      <button
                        onClick={() => onSelectLesson(prevLesson.file_path, prevLesson.id)}
                        className="w-full sm:w-auto p-4 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 bg-zinc-50/50 dark:bg-zinc-900/50 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 transition-colors text-left flex items-center gap-3 group"
                      >
                        <ChevronLeft className="w-5 h-5 text-zinc-400 group-hover:-translate-x-1 transition-transform" />
                        <div>
                          <div className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider">Previous Lesson</div>
                          <div className="text-xs font-semibold text-zinc-800 dark:text-zinc-200 line-clamp-1">{prevLesson.title}</div>
                        </div>
                      </button>
                    ) : <div />}

                    {nextLesson ? (
                      <button
                        onClick={() => onSelectLesson(nextLesson.file_path, nextLesson.id)}
                        className="w-full sm:w-auto p-4 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 bg-zinc-50/50 dark:bg-zinc-900/50 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 transition-colors text-right flex items-center justify-end gap-3 group"
                      >
                        <div>
                          <div className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider">Next Lesson</div>
                          <div className="text-xs font-semibold text-zinc-800 dark:text-zinc-200 line-clamp-1">{nextLesson.title}</div>
                        </div>
                        <ChevronRight className="w-5 h-5 text-zinc-400 group-hover:translate-x-1 transition-transform" />
                      </button>
                    ) : <div />}
                  </div>
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

        {/* Right Side: Interactive Python Scratchpad */}
        {isScratchpadOpen && (
          <div className="sticky top-20 shrink-0 h-[calc(100vh-6rem)] rounded-xl overflow-hidden border border-zinc-200/80 dark:border-zinc-800/80 shadow-2xl">
            <SideCodeRunner
              initialCode={scratchpadCode}
              onClose={() => setIsScratchpadOpen(false)}
            />
          </div>
        )}
      </div>
    </div>
  );
};
