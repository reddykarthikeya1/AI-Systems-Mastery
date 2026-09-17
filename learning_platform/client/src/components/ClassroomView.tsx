import React, { useState, useEffect, useMemo, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import mermaid from 'mermaid';
import { 
  ArrowLeft, CheckCircle2, ChevronRight, ChevronLeft, BookOpen, Terminal as TermIcon, 
  Terminal, Bookmark, FileText, Bug, Hammer, CheckSquare, Sparkles, MessageSquare, Save,
  Play, Code2, Copy, Check, FileCode, ExternalLink, Layers, Eye, Brain, Database,
  ArrowUp, PanelLeftClose, PanelLeftOpen
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { ModuleItem, LessonItem, TestResult, RunnerMode, LastPosition } from '../types';
import { fetchFileContent, runTestCommand } from '../services/api';
import { renderMarkdownWithMath } from '../services/markdown';
import { TerminalRunner } from './TerminalRunner';
import { SideCodeRunner, PageSnippet } from './SideCodeRunner';
import { McqQuizView } from './McqQuizView';
import { ProjectStudio } from './ProjectStudio';
import { DebugLabView } from './DebugLabView';
import { DsaArenaView } from './DsaArenaView';
import { TableOfContents } from './TableOfContents';
import { SqlPlaygroundView } from './SqlPlaygroundView';
import { ArchitectureCanvasView } from './ArchitectureCanvasView';
import { LessonSkeleton } from './LessonSkeleton';
import { soundService } from '../services/sound';
import { ReaderToolbar, ReaderSettings } from './classroom/ReaderToolbar';
import { SyllabusRail } from './classroom/SyllabusRail';
import { ScriptViewer } from './classroom/ScriptViewer';
import { NotebookViewer } from './classroom/NotebookViewer';
import { MarkdownViewer } from './classroom/MarkdownViewer';
import { NotesTab } from './classroom/NotesTab';

interface ClassroomViewProps {
  courseTitle: string;
  courseId?: string;
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
  onSelectLesson: (filePath: string, lessonId: string, initialTab?: string) => void;
  completedLessons?: string[];
  onUpdateLastPosition?: (pos: LastPosition) => void;
  onOpenMasteryGate?: () => void;
  onQuizMistake?: (question: import('./McqQuizView').McqQuestion, chosenOption: string) => void;
  onPassLab?: () => void;
  onSrsReview?: (rating: number) => void;
}



const DEFAULT_READER_SETTINGS: ReaderSettings = {
  fontSize: 'md',
  measure: 'wide',
  fontFamily: 'sans',
};

export const ClassroomView: React.FC<ClassroomViewProps> = ({
  courseTitle,
  courseId,
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
  onUpdateLastPosition,
  onOpenMasteryGate,
  onQuizMistake,
  onPassLab,
  onSrsReview,
}) => {
  const [searchParams] = useSearchParams();
  const requestedTab = searchParams.get('tab') as 'theory' | 'project' | 'quiz' | 'debug' | 'test' | 'notes' | 'arena' | 'sql' | 'arch' | null;

  // Determine initial tab based on lesson type or URL parameter
  const defaultTab = useMemo<'theory' | 'project' | 'quiz' | 'debug' | 'test' | 'notes' | 'arena' | 'sql' | 'arch'>(() => {
    if (requestedTab && ['theory', 'project', 'quiz', 'debug', 'test', 'notes', 'arena', 'sql', 'arch'].includes(requestedTab)) {
      return requestedTab;
    }
    if (currentLesson.type === 'challenge' || currentLesson.title.toLowerCase().includes('leetcode') || currentLesson.file_path.toLowerCase().includes('leetcode')) return 'arena';
    if (currentLesson.type === 'project') return 'project';
    if (currentLesson.type === 'quiz') return 'quiz';
    return 'theory';
  }, [requestedTab, currentLesson.id, currentLesson.type, currentLesson.title, currentLesson.file_path]);

  const [activeTab, setActiveTab] = useState<'theory' | 'project' | 'quiz' | 'debug' | 'test' | 'notes' | 'arena' | 'sql' | 'arch'>(defaultTab);
  const [content, setContent] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [codeCopied, setCodeCopied] = useState<boolean>(false);

  // Persistent Reader Experience Settings
  const [readerSettings, setReaderSettings] = useState<ReaderSettings>(() => {
    try {
      const saved = localStorage.getItem('academy_reader_settings');
      if (saved) return { ...DEFAULT_READER_SETTINGS, ...JSON.parse(saved) };
    } catch {}
    return DEFAULT_READER_SETTINGS;
  });

  const updateReaderSettings = (updates: Partial<ReaderSettings>) => {
    setReaderSettings((prev) => {
      const next = { ...prev, ...updates };
      localStorage.setItem('academy_reader_settings', JSON.stringify(next));
      return next;
    });
  };

  // Sidebar visibility state
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(() => {
    return localStorage.getItem('academy_sidebar_open') !== 'false';
  });

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => {
      const next = !prev;
      localStorage.setItem('academy_sidebar_open', String(next));
      return next;
    });
  };

  // Confidence rating toast feedback
  const [confidenceRated, setConfidenceRated] = useState<string | null>(null);
  const handleConfidenceClick = (rating: number, feedback: string) => {
    if (onSrsReview) {
      onSrsReview(rating);
    }
    setConfidenceRated(feedback);
    setTimeout(() => setConfidenceRated(null), 4000);
  };

  // Back to top button state
  const [showBackToTop, setShowBackToTop] = useState<boolean>(false);

  // Toggle for syllabus sidebar in Project Studio mode
  const [isSyllabusSidebarOpen, setIsSyllabusSidebarOpen] = useState<boolean>(true);

  // Student personal notes state
  const [noteText, setNoteText] = useState<string>(savedNote);
  const [noteSavedAlert, setNoteSavedAlert] = useState<boolean>(false);

  // Sync note when lesson changes
  useEffect(() => {
    setNoteText(savedNote);
  }, [currentLesson.id, savedNote]);

  // Sync tab if URL search parameter changes
  useEffect(() => {
    if (requestedTab && ['theory', 'project', 'quiz', 'debug', 'test', 'notes', 'arena', 'sql', 'arch'].includes(requestedTab)) {
      setActiveTab(requestedTab);
    }
  }, [requestedTab]);

  // Update tab if lesson type switches directly
  useEffect(() => {
    if (requestedTab && ['theory', 'project', 'quiz', 'debug', 'test', 'notes', 'arena', 'sql', 'arch'].includes(requestedTab)) {
      return;
    }
    if (currentLesson.type === 'challenge' || currentLesson.title.toLowerCase().includes('leetcode') || currentLesson.file_path.toLowerCase().includes('leetcode')) {
      setActiveTab('arena');
    } else if (currentLesson.type === 'project') {
      setActiveTab('project');
    } else if (currentLesson.type === 'quiz') {
      setActiveTab('quiz');
    } else {
      setActiveTab('theory');
    }
  }, [currentLesson.id, currentLesson.type, currentLesson.title, currentLesson.file_path, requestedTab]);

  // Track last visited position for 1-click resume
  const lastRecordedRef = useRef<string | null>(null);
  useEffect(() => {
    if (onUpdateLastPosition && currentLesson?.id && lastRecordedRef.current !== currentLesson.id) {
      lastRecordedRef.current = currentLesson.id;
      onUpdateLastPosition({
        course_id: courseId || module.folder_path.split('/')[0],
        course_title: courseTitle,
        module_id: module.id,
        module_title: module.title,
        lesson_id: currentLesson.id,
        lesson_title: currentLesson.title,
        lesson_path: currentLesson.file_path,
        updated_at: Date.now(),
      });
    }
  }, [currentLesson?.id, module?.id]);

  // Parse Jupyter Notebook cells if current file is an .ipynb
  const notebookCells = useMemo<{ type: 'markdown' | 'code'; source: string }[]>(() => {
    if (currentLesson.type !== 'notebook' || !content || content.startsWith('Loading')) return [];
    try {
      const parsed = JSON.parse(content);
      if (parsed && Array.isArray(parsed.cells)) {
        return parsed.cells.map((c: any) => ({
          type: c.cell_type === 'code' ? 'code' : 'markdown',
          source: Array.isArray(c.source) ? c.source.join('') : (c.source || ''),
        }));
      }
    } catch {
      return [];
    }
    return [];
  }, [content, currentLesson.type]);

  // Ref for theory content container to hydrate Mermaid diagrams
  const theoryContentRef = useRef<HTMLDivElement>(null);

  // Automatic Mermaid Diagram Hydration for lesson prose and notebooks
  useEffect(() => {
    if (activeTab !== 'theory') return;

    try {
      mermaid.initialize({
        startOnLoad: false,
        theme: document.documentElement.classList.contains('dark') ? 'dark' : 'default',
        securityLevel: 'loose',
        fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
      });
    } catch {
      // ignore init race
    }

    const renderMermaidBlocks = async () => {
      if (!theoryContentRef.current) return;
      const codeBlocks = theoryContentRef.current.querySelectorAll('pre code.language-mermaid');
      for (let i = 0; i < codeBlocks.length; i++) {
        const codeEl = codeBlocks[i];
        const preEl = codeEl.parentElement;
        if (!preEl || (preEl as any).dataset?.mermaidRendered) continue;
        const rawCode = codeEl.textContent || '';
        if (!rawCode.trim()) continue;
        const renderId = `mermaid-lesson-${Date.now()}-${i}`;
        try {
          const { svg } = await mermaid.render(renderId, rawCode.trim());
          const wrapper = document.createElement('div');
          wrapper.className = 'my-6 p-4 rounded-2xl bg-surface border border-border/80 flex justify-center items-center overflow-x-auto shadow-sm transition-all';
          wrapper.innerHTML = svg;
          (preEl as any).dataset.mermaidRendered = 'true';
          preEl.replaceWith(wrapper);
        } catch (err) {
          console.warn('Failed to render Mermaid diagram in lesson:', err);
        }
      }
    };

    const timer = setTimeout(() => {
      renderMermaidBlocks();
    }, 60);

    return () => clearTimeout(timer);
  }, [content, activeTab, notebookCells]);

  // Reading time and complexity badge estimation
  const { readingMinutes, complexityBadge } = useMemo(() => {
    const text = typeof content === 'string' ? content : '';
    const words = text.trim().split(/\s+/).filter(Boolean).length;
    const readingMinutes = Math.max(1, Math.ceil(words / 180));
    let complexityBadge = 'Intermediate';
    if (words > 1600 || text.includes('B-Tree') || text.includes('Raft') || text.includes('Triton')) {
      complexityBadge = 'Advanced Systems';
    } else if (words < 400 && !text.includes('class ')) {
      complexityBadge = 'Foundational';
    }
    return { readingMinutes, complexityBadge };
  }, [content]);

  const isStorageCourse = courseTitle.toLowerCase().includes('database') || courseTitle.toLowerCase().includes('storage') || module.folder_path.toLowerCase().includes('03_');
  const isDistributedCourse = courseTitle.toLowerCase().includes('distributed') || module.folder_path.toLowerCase().includes('04_');

  // Side-by-side interactive code runner state
  const [isScratchpadOpen, setIsScratchpadOpen] = useState<boolean>(false);
  const [scratchpadCode, setScratchpadCode] = useState<string>('');
  const [scratchpadMode, setScratchpadMode] = useState<RunnerMode>(
    currentLesson.type === 'powershell' ? 'powershell' : 'python'
  );

  // Extract page code snippets from content markdown
  const pageSnippets = useMemo<PageSnippet[]>(() => {
    if (!content || content.startsWith('Loading')) return [];
    const snippets: PageSnippet[] = [];

    // If current lesson is a raw code script, add the whole file as the primary snippet
    if (currentLesson.type === 'code' || currentLesson.type === 'powershell') {
      snippets.push({
        id: 'full-file',
        title: currentLesson.title,
        code: content,
        lang: currentLesson.type === 'powershell' ? 'POWERSHELL' : 'PYTHON',
      });
      return snippets;
    }

    // If current lesson is a notebook, extract code cells
    if (currentLesson.type === 'notebook' && notebookCells.length > 0) {
      let cIdx = 1;
      for (const cell of notebookCells) {
        if (cell.type === 'code' && cell.source.trim()) {
          snippets.push({
            id: `nb-cell-${cIdx++}`,
            title: `Cell #${cIdx - 1}: ${cell.source.split('\n')[0].slice(0, 28)}`,
            code: cell.source,
            lang: 'PYTHON',
          });
        }
      }
      return snippets;
    }

    // Extract markdown code blocks
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
  }, [content, currentLesson.type, currentLesson.title, notebookCells]);

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
    setIsLoading(true);
    setContent('');
    fetchFileContent(currentLesson.file_path).then((data) => {
      setContent(data.content);
      setIsLoading(false);
      // If the lesson is a script, pre-fill the runner
      if (currentLesson.type === 'code') {
        setScratchpadCode(data.content);
        setScratchpadMode('python');
      } else if (currentLesson.type === 'powershell') {
        setScratchpadCode(data.content);
        setScratchpadMode('powershell');
      }
    }).catch((err) => {
      setContent(`Failed to load content: ${err.message}`);
      setIsLoading(false);
    });
  }, [currentLesson.file_path, currentLesson.type]);

  // Back to top visibility listener and scroll position persistence
  useEffect(() => {
    const handleScroll = () => {
      setShowBackToTop(window.scrollY > 400);
      sessionStorage.setItem(`scroll_pos_${currentLesson.id}`, window.scrollY.toString());
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [currentLesson.id]);

  // Restore scroll position when lesson loads
  useEffect(() => {
    if (!isLoading) {
      const savedPos = sessionStorage.getItem(`scroll_pos_${currentLesson.id}`);
      if (savedPos) {
        const top = parseInt(savedPos, 10);
        if (!isNaN(top) && top > 60) {
          const timer = setTimeout(() => {
            window.scrollTo({ top, behavior: 'smooth' });
          }, 100);
          return () => clearTimeout(timer);
        }
      }
    }
  }, [currentLesson.id, isLoading]);

  const fontSizeClass = useMemo(() => {
    switch (readerSettings.fontSize) {
      case 'sm': return 'text-[15px] leading-[1.7]';
      case 'lg': return 'text-[19px] leading-[1.85]';
      case 'xl': return 'text-[21px] leading-[1.9]';
      default: return 'text-[17px] leading-[1.8]';
    }
  }, [readerSettings.fontSize]);

  const measureClass = useMemo(() => {
    switch (readerSettings.measure) {
      case 'narrow': return 'max-w-[64ch]';
      case 'wide': return 'max-w-[90ch]';
      case 'full': return 'max-w-none';
      default: return 'max-w-[76ch]';
    }
  }, [readerSettings.measure]);

  const fontFamilyClass = useMemo(() => {
    switch (readerSettings.fontFamily) {
      case 'serif': return 'font-serif-reading';
      case 'mono': return 'font-mono-reading';
      default: return 'font-sans-reading';
    }
  }, [readerSettings.fontFamily]);

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
        header.className = 'flex items-center justify-between px-3.5 py-1.5 bg-surface-raised border-b border-zinc-800 text-xs font-mono text-zinc-400 select-none';

        const label = document.createElement('span');
        label.className = 'font-semibold text-zinc-300';
        label.innerText = lang;

        const btnGroup = document.createElement('div');
        btnGroup.className = 'flex items-center gap-2';

        const runSnippetBtn = document.createElement('button');
        runSnippetBtn.className = 'hover:text-emerald-300 px-2 py-0.5 rounded hover:bg-emerald-950/60 transition-colors flex items-center gap-1 text-emerald-400 font-semibold text-xs border border-emerald-500/30';
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
          copyBtn.classList.add('text-emerald-400');
          setTimeout(() => {
            copyBtn.innerText = 'Copy';
            copyBtn.classList.remove('text-emerald-400');
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
        wrapper.className = 'my-5 rounded-xl border border-zinc-300 dark:border-zinc-800 overflow-hidden shadow-sm bg-bg';

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
  const currentLessonIndex = currentIndex;
  const prevLesson = currentIndex > 0 ? allLessons[currentIndex - 1] : null;
  const nextLesson = currentIndex < allLessons.length - 1 ? allLessons[currentIndex + 1] : null;

  // Scroll Progress tracking for reading
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const totalScroll = document.documentElement.scrollHeight - window.innerHeight;
      if (totalScroll > 0) {
        const currentProgress = (window.scrollY / totalScroll) * 100;
        setScrollProgress(Math.min(100, Math.max(0, currentProgress)));
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [currentLesson.id]);

  // Keyboard navigation shortcuts (j for next, k for previous)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      if (
        target &&
        (target.tagName === 'INPUT' ||
          target.tagName === 'TEXTAREA' ||
          target.isContentEditable ||
          target.closest('.monaco-editor') ||
          target.closest('textarea'))
      ) {
        return;
      }
      if (e.key === 'j') {
        if (nextLesson) {
          soundService.playClick();
          onSelectLesson(nextLesson.file_path, nextLesson.id);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        } else if (onOpenMasteryGate) {
          onOpenMasteryGate();
        }
      } else if (e.key === 'k') {
        if (prevLesson) {
          soundService.playClick();
          onSelectLesson(prevLesson.file_path, prevLesson.id);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [nextLesson, prevLesson, onOpenMasteryGate, onSelectLesson]);

  const handlePrevLesson = () => {
    if (prevLesson) {
      soundService.playClick();
      onSelectLesson(prevLesson.file_path, prevLesson.id);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleCompleteAndNext = () => {
    if (!isCompleted) {
      onToggleComplete();
    }
    if (nextLesson) {
      soundService.playSuccess();
      onSelectLesson(nextLesson.file_path, nextLesson.id);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (onOpenMasteryGate) {
      soundService.playFanfare();
      onOpenMasteryGate();
    } else {
      soundService.playFanfare();
      confetti({ particleCount: 90, spread: 75, origin: { y: 0.6 } });
    }
  };

  // Detect availability of specialized features
  const hasProject = Boolean(module.has_starter || module.has_solution || allLessons.some((l) => l.type === 'project'));
  const hasQuiz = Boolean((module.quiz_question_count ?? 0) > 0 || allLessons.some((l) => l.type === 'quiz') || true);
  const hasDebugLab = Boolean(module.has_debug_lab);
  const hasDsaArena = Boolean(
    courseTitle.toLowerCase().includes('data structure') ||
    courseTitle.toLowerCase().includes('dsa') ||
    module.folder_path.toLowerCase().includes('02_data_structures') ||
    allLessons.some((l) => l.type === 'challenge' || l.title.toLowerCase().includes('leetcode') || l.file_path.toLowerCase().includes('leetcode'))
  );

  const getLessonBadge = (type: string) => {
    switch (type) {
      case 'challenge':
        return <span className="text-xs font-mono uppercase px-1 py-0.5 rounded bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-300">LeetCode</span>;
      case 'project':
        return <span className="text-xs font-mono uppercase px-1 py-0.5 rounded bg-purple-100 dark:bg-purple-950/60 text-purple-600 dark:text-purple-300">Project</span>;
      case 'quiz':
        return <span className="text-xs font-mono uppercase px-1 py-0.5 rounded bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-300">Quiz</span>;
      case 'playground':
        return <span className="text-xs font-mono uppercase px-1 py-0.5 rounded bg-cyan-100 dark:bg-cyan-950/60 text-cyan-600 dark:text-cyan-300">Intro</span>;
      case 'code':
        return <span className="text-xs font-mono uppercase px-1 py-0.5 rounded bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-300">Code</span>;
      case 'powershell':
        return <span className="text-xs font-mono uppercase px-1 py-0.5 rounded bg-sky-100 dark:bg-sky-950/60 text-sky-600 dark:text-sky-300">PS1</span>;
      case 'notebook':
        return <span className="text-xs font-mono uppercase px-1 py-0.5 rounded bg-orange-100 dark:bg-orange-950/60 text-orange-600 dark:text-orange-300">Notebook</span>;
      case 'troubleshooting':
        return <span className="text-xs font-mono uppercase px-1 py-0.5 rounded bg-rose-100 dark:bg-rose-950/60 text-rose-600 dark:text-rose-300">Debug</span>;
      default:
        return null;
    }
  };

  return (
    <>
      {/* Reading Scroll Progress Bar */}
      <div 
        className="fixed top-0 left-0 right-0 h-1 z-50 bg-gradient-to-r from-blue-600 via-indigo-500 to-emerald-500 transition-all duration-100 ease-out"
        style={{ width: `${scrollProgress}%` }}
      />
      <div className="w-full max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 xl:px-10 py-6 space-y-6 transition-all duration-300">
      {/* Top Bar Navigation & Reader Controls */}
      <ReaderToolbar
        courseTitle={courseTitle}
        moduleNum={module.module_num}
        currentLesson={currentLesson}
        onBackToSyllabus={onBackToSyllabus}
        isSidebarOpen={isSidebarOpen}
        onToggleSidebar={toggleSidebar}
        readingMinutes={readingMinutes}
        complexityBadge={complexityBadge}
        readerSettings={readerSettings}
        onUpdateReaderSettings={updateReaderSettings}
        isBookmarked={isBookmarked}
        onToggleBookmark={onToggleBookmark}
        isScratchpadOpen={isScratchpadOpen}
        onToggleScratchpad={() => setIsScratchpadOpen(!isScratchpadOpen)}
        isCompleted={isCompleted}
        onToggleComplete={handleCompleteClick}
      />

      {/* Navigation Sub-Tabs */}
      <div className="flex items-center gap-1.5 border-b border-border/80 pb-2 overflow-x-auto">
        <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'theory'
              ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 shadow-sm'
              : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
          }`} onClick={() => setActiveTab('theory')} >
          {currentLesson.type === 'code' || currentLesson.type === 'powershell' ? (
            <Code2 className="w-3.5 h-3.5" />
          ) : currentLesson.type === 'notebook' ? (
            <Layers className="w-3.5 h-3.5" />
          ) : (
            <BookOpen className="w-3.5 h-3.5" />
          )}
          <span>{currentLesson.type === 'code' ? 'Interactive Code Lab' : currentLesson.type === 'powershell' ? 'PowerShell Script' : currentLesson.type === 'notebook' ? 'Jupyter Notebook' : 'Lesson Architecture'}</span>
        </button>

        {hasProject && (
          <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'project'
                ? 'bg-purple-600 text-white shadow-sm font-bold'
                : 'text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-950/30'
            }`} onClick={() => setActiveTab('project')} >
            <Hammer className="w-3.5 h-3.5" /> In-Browser Project Studio
            <span className="text-xs px-1 py-0.5 rounded bg-purple-200 dark:bg-purple-900/60 text-purple-900 dark:text-purple-200 font-mono">
              IDE
            </span>
          </button>
        )}

        {hasDsaArena && (
          <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'arena'
                ? 'bg-amber-600 text-white shadow-sm font-bold'
                : 'text-amber-600 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-950/30'
            }`} onClick={() => setActiveTab('arena')} >
            <Brain className="w-3.5 h-3.5 text-amber-300" /> LeetCode Arena
            <span className="text-xs px-1.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 font-mono font-bold">
              Sandbox
            </span>
          </button>
        )}

        {hasQuiz && (
          <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'quiz'
                ? 'bg-amber-600 text-white shadow-sm'
                : 'text-amber-600 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-950/30'
            }`} onClick={() => setActiveTab('quiz')} >
            <CheckSquare className="w-3.5 h-3.5" /> Interactive Assessment (MCQ)
            {savedQuizScore?.passed && (
              <span className="text-xs px-1 py-0.5 rounded bg-emerald-500 text-white font-mono">
                {savedQuizScore.score}%
              </span>
            )}
          </button>
        )}

        {hasDebugLab && (
          <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'debug'
                ? 'bg-rose-600 text-white shadow-sm'
                : 'text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/30'
            }`} onClick={() => setActiveTab('debug')} >
            <Bug className="w-3.5 h-3.5" /> Bug Hunter Lab
            <span className="text-xs px-1 py-0.5 rounded bg-rose-200 dark:bg-rose-900/60 text-rose-900 dark:text-rose-200 font-mono">
              Drill
            </span>
          </button>
        )}

        <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'test'
              ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 shadow-sm'
              : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
          }`} onClick={() => setActiveTab('test')} >
          <TermIcon className="w-3.5 h-3.5" /> Pytest & Execution Console
        </button>

        <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'notes'
              ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 shadow-sm'
              : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
          }`} onClick={() => setActiveTab('notes')} >
          <FileText className="w-3.5 h-3.5" /> Personal Notes
          {noteText.trim().length > 0 && (
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
          )}
        </button>

        {/* Storage & SQL Sandbox Tab */}
        {(isStorageCourse || activeTab === 'sql') && (
          <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'sql'
                ? 'bg-emerald-600 text-white shadow-sm font-bold'
                : 'text-emerald-600 dark:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-950/30'
            }`} onClick={() => setActiveTab('sql')} >
            <Database className="w-3.5 h-3.5" /> Storage & SQL Sandbox
            <span className="text-xs px-1.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono font-bold">
              B-Tree
            </span>
          </button>
        )}

        {/* Distributed Architecture Canvas Tab */}
        {(isDistributedCourse || activeTab === 'arch') && (
          <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'arch'
                ? 'bg-indigo-600 text-white shadow-sm font-bold'
                : 'text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-950/30'
            }`} onClick={() => setActiveTab('arch')} >
            <Layers className="w-3.5 h-3.5" /> Architecture Canvas
            <span className="text-xs px-1.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 font-mono font-bold">
              Mermaid
            </span>
          </button>
        )}
      </div>

      {/* Main Content Stage */}
      {activeTab === 'sql' ? (
        <div className="w-full h-[750px]">
          <SqlPlaygroundView onClose={() => setActiveTab('theory')} />
        </div>
      ) : activeTab === 'arch' ? (
        <div className="w-full h-[750px]">
          <ArchitectureCanvasView onClose={() => setActiveTab('theory')} />
        </div>
      ) : activeTab === 'project' ? (
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
      ) : activeTab === 'arena' ? (
        <div className="w-full">
          <DsaArenaView
            moduleTitle={module.title}
            moduleFolderPath={module.folder_path}
            onBackToLesson={() => setActiveTab('theory')}
          />
        </div>
      ) : (
        /* 2. REGULAR LESSON VIEWS: Responsive Full-Width 3-Pane Architecture */
        <div className="flex gap-6 2xl:gap-8 items-start w-full">
          {/* Left Sidebar: Lesson Outline (Collapsible) */}
          {isSidebarOpen && (
            <SyllabusRail
              moduleNum={module.module_num}
              allLessons={allLessons}
              currentLessonId={currentLesson.id}
              completedLessons={completedLessons}
              onSelectLesson={onSelectLesson}
              getLessonBadge={getLessonBadge}
            />
          )}

          {/* Center Area: Active View (Fluid, Takes ALL remaining width) */}
          <div className="flex-1 min-w-0 space-y-4">
            {/* TAB: THEORY & SCRIPT READER */}
            {activeTab === 'theory' && (
              <div ref={theoryContentRef}>
                {(currentLesson.type === 'code' || currentLesson.type === 'powershell' || currentLesson.type === 'shell') ? (
                  <ScriptViewer
                    currentLesson={currentLesson}
                    content={content}
                    onOpenInRunner={(code, mode) => {
                      setScratchpadCode(code);
                      setScratchpadMode(mode);
                      setIsScratchpadOpen(true);
                    }}
                  />
                ) : currentLesson.type === 'notebook' && notebookCells.length > 0 ? (
                  <NotebookViewer
                    currentLesson={currentLesson}
                    notebookCells={notebookCells}
                    renderMarkdownWithMath={renderMarkdownWithMath}
                    onRunCode={(code) => {
                      setScratchpadCode(code);
                      setScratchpadMode('python');
                      setIsScratchpadOpen(true);
                    }}
                  />
                ) : (
                  <MarkdownViewer
                    isLoading={isLoading}
                    content={content}
                    lessonId={currentLesson.id}
                    measureClass={measureClass}
                    fontSizeClass={fontSizeClass}
                    fontFamilyClass={fontFamilyClass}
                    renderMarkdownWithMath={renderMarkdownWithMath}
                    confidenceRated={confidenceRated}
                    onConfidenceClick={handleConfidenceClick}
                    nextLesson={nextLesson}
                    prevLesson={prevLesson}
                    currentLessonIndex={currentLessonIndex}
                    allLessons={allLessons}
                    moduleNum={module.module_num}
                    isCompleted={isCompleted}
                    onPrevLesson={handlePrevLesson}
                    onCompleteAndNext={handleCompleteAndNext}
                    onOpenMasteryGate={onOpenMasteryGate}
                    getLessonBadge={getLessonBadge}
                  />
                )}
              </div>
            )}

            {/* TAB: INTERACTIVE MCQ ASSESSMENT */}
            {activeTab === 'quiz' && (
              <div className="w-full">
                <McqQuizView
                  rawContent={content}
                  lessonTitle={currentLesson.title}
                  moduleTitle={module.title}
                  courseTitle={courseTitle}
                  lessonId={currentLesson.id}
                  moduleFolderPath={module.folder_path}
                  savedScore={savedQuizScore}
                  onQuizMistake={onQuizMistake}
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

            {/* TAB: BUG HUNTER LAB */}
            {activeTab === 'debug' && (
              <div className="w-full">
                <DebugLabView
                  moduleFolderPath={module.folder_path}
                  moduleTitle={module.title}
                  onPassLab={() => {
                    confetti({ particleCount: 100, spread: 80, origin: { y: 0.6 } });
                    if (onPassLab) {
                      onPassLab();
                    }
                  }}
                />
              </div>
            )}

            {/* TAB: PYTEST & EXECUTION CONSOLE */}
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

            {/* TAB: PERSONAL STUDY NOTES */}
            {activeTab === 'notes' && (
              <NotesTab
                noteText={noteText}
                onChangeNoteText={setNoteText}
                onSaveNote={handleSaveNoteClick}
                noteSavedAlert={noteSavedAlert}
              />
            )}
          </div>

          {/* Right Rail: Page-Aware Interactive Runner OR Sticky Quick-Reach TOC */}
          {isScratchpadOpen ? (
            <aside aria-label="Interactive multi-runtime code runner" className="w-96 2xl:w-[480px] shrink-0 sticky top-20 h-[calc(100vh-6rem)] rounded-2xl overflow-hidden border border-border/80 shadow-2xl">
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
            </aside>
          ) : (
            activeTab === 'theory' && (
              <aside aria-label="On this page quick reach" className="w-72 2xl:w-80 shrink-0 sticky top-20 hidden xl:block">
                <TableOfContents
                  content={content}
                  isBookmarked={isBookmarked}
                  onToggleBookmark={onToggleBookmark}
                />
              </aside>
            )
          )}
        </div>
      )}
      {showBackToTop && (
        <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 fixed bottom-8 right-8 z-30 p-3 rounded-full bg-zinc-900/90 dark:bg-zinc-100/90 text-white dark:text-zinc-900 shadow-xl hover:scale-110 active:scale-95 transition-all border border-zinc-700/50 dark:border-zinc-300/50" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          
          title="Back to top"
          aria-label="Back to top" >
          <ArrowUp className="w-4 h-4" />
        </button>
      )}
    </div>
    </>
  );
};
