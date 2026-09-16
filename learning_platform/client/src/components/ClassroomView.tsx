import React, { useState, useEffect, useMemo, useRef } from 'react';
import { 
  ArrowLeft, CheckCircle2, ChevronRight, ChevronLeft, BookOpen, Terminal as TermIcon, 
  Terminal, Bookmark, FileText, Bug, Hammer, CheckSquare, Sparkles, MessageSquare, Save
} from 'lucide-react';
import { marked } from 'marked';
import confetti from 'canvas-confetti';
import { ModuleItem, LessonItem, TestResult, RunnerMode } from '../types';
import { fetchFileContent, runTestCommand } from '../services/api';
import { TerminalRunner } from './TerminalRunner';
import { SideCodeRunner, PageSnippet } from './SideCodeRunner';
import { McqQuizView } from './McqQuizView';
import { ProjectStudio } from './ProjectStudio';
import { DebugLabView } from './DebugLabView';
import { TableOfContents } from './TableOfContents';

interface ClassroomViewProps {
  courseTitle: string;
  module: ModuleItem;
  currentLesson: LessonItem;
  allLessons: LessonItem[];
  isCompleted: boolean;
  isBookmarked?: boolean;
  savedQuizScore?: { score: number; total: number; passed: boolean };
  savedNote?: string;
  onToggleComplete: () => void;
  onToggleBookmark?: () => void;
  onSaveQuizScore?: (score: number, total: number, passed: boolean) => void;
  onSaveNote?: (text: string) => void;
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
  isBookmarked = false,
  savedQuizScore,
  savedNote = '',
  onToggleComplete,
  onToggleBookmark,
  onSaveQuizScore,
  onSaveNote,
  onBackToSyllabus,
  onSelectLesson,
  completedLessons = [],
}) => {
  // Determine initial tab based on lesson type
  const defaultTab = useMemo<'theory' | 'project' | 'quiz' | 'debug' | 'test' | 'notes'>(() => {
    if (currentLesson.type === 'project') return 'project';
    if (currentLesson.type === 'quiz') return 'quiz';
    return 'theory';
  }, [currentLesson.id, currentLesson.type]);

  const [activeTab, setActiveTab] = useState<'theory' | 'project' | 'quiz' | 'debug' | 'test' | 'notes'>(defaultTab);
  const [content, setContent] = useState<string>('Loading lesson content...');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [testResult, setTestResult] = useState<TestResult | null>(null);

  // Student personal notes state
  const [noteText, setNoteText] = useState<string>(savedNote);
  const [noteSavedAlert, setNoteSavedAlert] = useState<boolean>(false);

  // Sync note when lesson changes
  useEffect(() => {
    setNoteText(savedNote);
  }, [currentLesson.id, savedNote]);

  // Update tab if lesson type switches directly
  useEffect(() => {
    if (currentLesson.type === 'project') {
      setActiveTab('project');
    } else if (currentLesson.type === 'quiz') {
      setActiveTab('quiz');
    } else {
      setActiveTab('theory');
    }
  }, [currentLesson.id, currentLesson.type]);

  // Side-by-side interactive code runner state
  const [isScratchpadOpen, setIsScratchpadOpen] = useState<boolean>(false);
  const [scratchpadCode, setScratchpadCode] = useState<string>('');
  const [scratchpadMode, setScratchpadMode] = useState<RunnerMode>('python');

  // Extract page code snippets from content markdown
  const pageSnippets = useMemo<PageSnippet[]>(() => {
    if (!content || content.startsWith('Loading')) return [];
    const snippets: PageSnippet[] = [];
    const regex = /```(\w+)?\n([\s\S]*?)```/g;
    let match: RegExpExecArray | null;
    let count = 1;

    while ((match = regex.exec(content)) !== null) {
      const rawLang = (match[1] || 'code').toUpperCase();
      const rawCode = match[2].trim();
      if (!rawCode) continue;

      let langLabel = 'PYTHON';
      if (rawLang === 'BASH' || rawLang === 'SH' || rawCode.startsWith('$') || rawCode.includes('pytest')) {
        langLabel = 'BASH';
      } else if (rawLang === 'POWERSHELL' || rawLang === 'PS1' || rawCode.startsWith('PS >')) {
        langLabel = 'POWERSHELL';
      } else if (rawLang === 'PYTHON' || rawLang === 'PY' || rawCode.includes('def ') || rawCode.includes('import ') || rawCode.includes('class ')) {
        langLabel = 'PYTHON';
      }

      let title = `Snippet #${count}`;
      const firstLine = rawCode.split('\n')[0].trim();
      if (firstLine.startsWith('#')) {
        title = firstLine.replace(/^[#\s]+/, '');
      } else if (firstLine.length > 0) {
        title = firstLine.slice(0, 32);
      }

      snippets.push({
        id: `snippet-${count++}`,
        title,
        code: rawCode,
        lang: langLabel,
      });
    }

    return snippets;
  }, [content]);

  // Event listener for "Run" button clicks from rendered code blocks
  useEffect(() => {
    const handleSnippetRun = (e: any) => {
      if (e.detail?.code) {
        setScratchpadCode(e.detail.code);
        if (e.detail?.mode) setScratchpadMode(e.detail.mode);
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

  // Enhance rendered code blocks with language badge, 1-click copy, and multi-runtime "Run" button
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

        let lang = 'Code';
        let detectedMode: RunnerMode = 'python';

        if (codeEl) {
          const match = codeEl.className.match(/language-(\w+)/);
          if (match) lang = match[1].toUpperCase();
        }

        if (lang === 'BASH' || lang === 'SH' || codeText.startsWith('$') || codeText.includes('pytest') || codeText.includes('pip install')) {
          lang = 'BASH / CMD';
          detectedMode = 'shell';
        } else if (lang === 'POWERSHELL' || lang === 'PS1' || codeText.startsWith('PS >')) {
          lang = 'POWERSHELL';
          detectedMode = 'powershell';
        } else if (lang === 'PYTHON' || lang === 'PY' || codeText.includes('def ') || codeText.includes('import ') || codeText.includes('class ') || codeText.includes('print(')) {
          lang = 'PYTHON';
          detectedMode = 'python';
        }

        let executableCode = codeText;
        if (detectedMode === 'shell') {
          executableCode = executableCode.replace(/^\$\s+/gm, '');
        } else if (detectedMode === 'powershell') {
          executableCode = executableCode.replace(/^PS\s+>\s+/gm, '');
        }

        const header = document.createElement('div');
        header.className = 'flex items-center justify-between px-3.5 py-1.5 bg-[#161B22] border-b border-zinc-800 text-[11px] font-mono text-zinc-400 select-none';

        const label = document.createElement('span');
        label.className = 'font-semibold text-zinc-300';
        label.innerText = lang;

        const btnGroup = document.createElement('div');
        btnGroup.className = 'flex items-center gap-2';

        const runSnippetBtn = document.createElement('button');
        runSnippetBtn.className = 'hover:text-emerald-300 px-2 py-0.5 rounded hover:bg-emerald-950/60 transition-colors flex items-center gap-1 text-emerald-400 font-semibold text-[11px] border border-emerald-500/30';
        const runLabel = detectedMode === 'python' ? '▶ Run' : detectedMode === 'powershell' ? '▶ Run PS' : '▶ Run Shell';
        runSnippetBtn.innerHTML = `<span>${runLabel}</span>`;
        runSnippetBtn.title = `Execute snippet in Page-Aware ${detectedMode.toUpperCase()} Runner`;
        runSnippetBtn.onclick = () => {
          window.dispatchEvent(new CustomEvent('open-scratchpad-with-code', { 
            detail: { code: executableCode, mode: detectedMode } 
          }));
        };
        btnGroup.appendChild(runSnippetBtn);

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

  const handleSaveNoteClick = () => {
    if (onSaveNote) {
      onSaveNote(noteText);
      setNoteSavedAlert(true);
      setTimeout(() => setNoteSavedAlert(false), 2500);
    }
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

  // Detect availability of specialized features
  const hasProject = Boolean(module.has_starter || module.has_solution || allLessons.some((l) => l.type === 'project'));
  const hasQuiz = Boolean(allLessons.some((l) => l.type === 'quiz'));
  const hasDebugLab = Boolean(module.has_debug_lab);

  return (
    <div className={`mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 transition-all duration-300 ${isScratchpadOpen ? 'max-w-[1780px]' : 'max-w-7xl'}`}>
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

        <div className="flex items-center gap-2 self-stretch sm:self-auto justify-end flex-wrap">
          {/* Bookmark Toggle */}
          {onToggleBookmark && (
            <button
              onClick={onToggleBookmark}
              className={`p-2 rounded-lg border text-xs font-medium transition-colors flex items-center gap-1.5 ${
                isBookmarked
                  ? 'bg-amber-50 dark:bg-amber-950/50 border-amber-300 dark:border-amber-800 text-amber-600 dark:text-amber-400'
                  : 'bg-zinc-100 dark:bg-zinc-800/90 border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900'
              }`}
              title={isBookmarked ? 'Bookmarked' : 'Bookmark this lesson'}
            >
              <Bookmark className={`w-3.5 h-3.5 ${isBookmarked ? 'fill-current' : ''}`} />
              <span className="hidden sm:inline">{isBookmarked ? 'Bookmarked' : 'Bookmark'}</span>
            </button>
          )}

          {/* Live Side Runner Toggle */}
          <button
            onClick={() => setIsScratchpadOpen(!isScratchpadOpen)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-2 transition-all shadow-sm ${
              isScratchpadOpen
                ? 'bg-emerald-50 dark:bg-emerald-950/60 border-emerald-300 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300'
                : 'bg-zinc-100 dark:bg-zinc-800/90 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700'
            }`}
            title="Toggle Page-Aware Interactive Runner (Python, PowerShell, Shell)"
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
            {isCompleted ? 'Completed' : 'Mark Complete'}
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

      {/* Navigation Sub-Tabs: Architecture, Project Studio, MCQ Quiz, Bug Hunter, Console, Notes */}
      <div className="flex items-center gap-1.5 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('theory')}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'theory'
              ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 shadow-sm'
              : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" /> Lesson Architecture
        </button>

        {hasProject && (
          <button
            onClick={() => setActiveTab('project')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'project'
                ? 'bg-purple-600 text-white shadow-sm'
                : 'text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-950/30'
            }`}
          >
            <Hammer className="w-3.5 h-3.5" /> In-Browser Project Studio
            <span className="text-[10px] px-1 py-0.2 rounded bg-purple-200 dark:bg-purple-900/60 text-purple-900 dark:text-purple-200 font-mono">
              IDE
            </span>
          </button>
        )}

        {hasQuiz && (
          <button
            onClick={() => setActiveTab('quiz')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'quiz'
                ? 'bg-amber-600 text-white shadow-sm'
                : 'text-amber-600 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-950/30'
            }`}
          >
            <CheckSquare className="w-3.5 h-3.5" /> Interactive Assessment (MCQ)
            {savedQuizScore?.passed && (
              <span className="text-[10px] px-1 py-0.2 rounded bg-emerald-500 text-white font-mono">
                {savedQuizScore.score}%
              </span>
            )}
          </button>
        )}

        {hasDebugLab && (
          <button
            onClick={() => setActiveTab('debug')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'debug'
                ? 'bg-rose-600 text-white shadow-sm'
                : 'text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/30'
            }`}
          >
            <Bug className="w-3.5 h-3.5" /> Bug Hunter Lab
            <span className="text-[10px] px-1 py-0.2 rounded bg-rose-200 dark:bg-rose-900/60 text-rose-900 dark:text-rose-200 font-mono">
              Drill
            </span>
          </button>
        )}

        <button
          onClick={() => setActiveTab('test')}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'test'
              ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 shadow-sm'
              : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
          }`}
        >
          <TermIcon className="w-3.5 h-3.5" /> Pytest & Execution Console
        </button>

        <button
          onClick={() => setActiveTab('notes')}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'notes'
              ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 shadow-sm'
              : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
          }`}
        >
          <FileText className="w-3.5 h-3.5" /> Personal Study Notes
          {noteText.trim().length > 0 && (
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
          )}
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex gap-6 items-start">
        {/* Left Outline + Center Reader/Studio */}
        <div className="flex-1 min-w-0">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
            {/* Left Sidebar: Lesson Outline */}
            <div className="lg:col-span-1 rounded-xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-4 shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-3 sticky top-20">
              <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-2">
                <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider">
                  Module {module.module_num.toString().padStart(2, '0')} Syllabus
                </span>
                <span className="text-[10px] font-mono text-zinc-400">
                  {allLessons.filter((l) => completedLessons.includes(l.id)).length}/{allLessons.length}
                </span>
              </div>

              <div className="space-y-1">
                {allLessons.map((l, idx) => {
                  const active = l.id === currentLesson.id;
                  const isDone = completedLessons.includes(l.id);

                  // Lesson type badge tag
                  let typeTag = '';
                  if (l.type === 'project') typeTag = 'Project';
                  else if (l.type === 'quiz') typeTag = 'Quiz';
                  else if (l.type === 'playground') typeTag = 'Intro';

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
                      <div className="flex items-center gap-1.5 shrink-0">
                        {typeTag && (
                          <span className="text-[9px] font-mono uppercase px-1 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-500">
                            {typeTag}
                          </span>
                        )}
                        {isDone ? (
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                        ) : (
                          <div className="w-1.5 h-1.5 rounded-full bg-zinc-300 dark:bg-zinc-700 shrink-0" />
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Center Area: Active Tab View */}
            <div className="lg:col-span-3 space-y-4">
              {/* TAB 1: THEORY / ARCHITECTURE */}
              {activeTab === 'theory' && (
                <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 items-start">
                  {/* Markdown Body */}
                  <div className="xl:col-span-3 rounded-xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-8 sm:p-10 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
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

                  {/* Sticky Table of Contents Sidebar */}
                  {!isScratchpadOpen && (
                    <div className="hidden xl:block xl:col-span-1">
                      <TableOfContents
                        content={content}
                        isBookmarked={isBookmarked}
                        onToggleBookmark={onToggleBookmark}
                      />
                    </div>
                  )}
                </div>
              )}

              {/* TAB 2: IN-BROWSER PROJECT STUDIO */}
              {activeTab === 'project' && (
                <div className="w-full">
                  <ProjectStudio
                    moduleFolderPath={module.folder_path}
                    moduleTitle={module.title}
                    courseTitle={courseTitle}
                    guideMarkdown={content}
                    onCompleteProject={handleCompleteClick}
                    isProjectCompleted={isCompleted}
                  />
                </div>
              )}

              {/* TAB 3: INTERACTIVE MCQ ASSESSMENT */}
              {activeTab === 'quiz' && (
                <div className="w-full">
                  <McqQuizView
                    rawContent={content}
                    lessonTitle={currentLesson.title}
                    moduleTitle={module.title}
                    courseTitle={courseTitle}
                    lessonId={currentLesson.id}
                    savedScore={savedQuizScore}
                    onPassQuiz={(score, total) => {
                      if (onSaveQuizScore) {
                        onSaveQuizScore(score, total, true);
                      }
                      if (!isCompleted) {
                        onToggleComplete();
                      }
                    }}
                  />
                </div>
              )}

              {/* TAB 4: BUG HUNTER LAB */}
              {activeTab === 'debug' && (
                <div className="w-full">
                  <DebugLabView
                    moduleFolderPath={module.folder_path}
                    moduleTitle={module.title}
                    onPassLab={() => {
                      confetti({ particleCount: 100, spread: 80, origin: { y: 0.6 } });
                    }}
                  />
                </div>
              )}

              {/* TAB 5: PYTEST & EXECUTION CONSOLE */}
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

              {/* TAB 6: PERSONAL STUDY NOTES */}
              {activeTab === 'notes' && (
                <div className="rounded-xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-6 space-y-4">
                  <div className="flex items-center justify-between border-b border-zinc-200/80 dark:border-zinc-800 pb-3">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4 text-blue-500" />
                      <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                        Personal Study Notes for: {currentLesson.title}
                      </h3>
                    </div>
                    <div className="flex items-center gap-2">
                      {noteSavedAlert && (
                        <span className="text-xs font-mono text-emerald-500 flex items-center gap-1">
                          ✓ Saved to study profile
                        </span>
                      )}
                      <button
                        onClick={handleSaveNoteClick}
                        className="px-3 py-1.5 rounded-lg text-xs font-medium bg-blue-600 hover:bg-blue-700 text-white flex items-center gap-1.5 transition-colors"
                      >
                        <Save className="w-3.5 h-3.5" /> Save Notes
                      </button>
                    </div>
                  </div>

                  <p className="text-xs text-zinc-500 dark:text-zinc-400">
                    Your notes are automatically saved locally and synchronized to your offline progress file. Use this space for architectural takeaways, interview flashcards, and edge cases.
                  </p>

                  <textarea
                    value={noteText}
                    onChange={(e) => setNoteText(e.target.value)}
                    placeholder="Write key takeaways, performance equations, and interview questions here..."
                    className="w-full h-80 p-4 font-mono text-xs rounded-lg border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-1 focus:ring-blue-500 resize-y leading-relaxed"
                  />
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Side: Page-Aware Interactive Multi-Runtime Runner */}
        {isScratchpadOpen && (
          <div className="sticky top-20 shrink-0 h-[calc(100vh-6rem)] rounded-xl overflow-hidden border border-zinc-200/80 dark:border-zinc-800/80 shadow-2xl">
            <SideCodeRunner
              initialCode={scratchpadCode}
              initialMode={scratchpadMode}
              courseTitle={courseTitle}
              moduleTitle={module.title}
              moduleFolderPath={module.folder_path}
              lessonTitle={currentLesson.title}
              lessonFilePath={currentLesson.file_path}
              pageSnippets={pageSnippets}
              onClose={() => setIsScratchpadOpen(false)}
            />
          </div>
        )}
      </div>
    </div>
  );
};
