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

interface ReaderSettings {
  fontSize: 'sm' | 'md' | 'lg' | 'xl';
  measure: 'narrow' | 'normal' | 'wide' | 'full';
  fontFamily: 'sans' | 'serif' | 'mono';
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
          wrapper.className = 'my-6 p-4 rounded-2xl bg-zinc-50 dark:bg-[#0D1117] border border-zinc-200/80 dark:border-zinc-800/80 flex justify-center items-center overflow-x-auto shadow-sm transition-all';
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
        header.className = 'flex items-center justify-between px-3.5 py-1.5 bg-[#161B22] border-b border-zinc-800 text-xs font-mono text-zinc-400 select-none';

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
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-4">
        <div className="flex items-center gap-3">
          <button
            onClick={onBackToSyllabus}
            className="p-2 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 transition-colors text-zinc-600 dark:text-zinc-400"
            title="Back to Course Syllabus"
            aria-label="Back to Course Syllabus"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 transition-colors text-zinc-600 dark:text-zinc-400 hidden lg:flex items-center justify-center"
            title={isSidebarOpen ? "Hide syllabus rail" : "Show syllabus rail"}
            aria-label={isSidebarOpen ? "Hide syllabus rail" : "Show syllabus rail"}
          >
            {isSidebarOpen ? <PanelLeftClose className="w-4 h-4" /> : <PanelLeftOpen className="w-4 h-4" />}
          </button>

          <div>
            <nav aria-label="Breadcrumb" className="text-xs font-mono text-zinc-400 dark:text-zinc-500 uppercase tracking-wider flex items-center gap-1.5 flex-wrap">
              <button 
                onClick={onBackToSyllabus}
                className="hover:text-zinc-700 dark:hover:text-zinc-300 transition-colors underline-offset-2 hover:underline"
              >
                {courseTitle}
              </button>
              <ChevronRight className="w-3 h-3 text-zinc-400" />
              <span>Module {module.module_num.toString().padStart(2, '0')}</span>
              <ChevronRight className="w-3 h-3 text-zinc-400" />
              <span className="text-zinc-700 dark:text-zinc-300 font-medium truncate max-w-[200px] sm:max-w-xs">{currentLesson.title}</span>
            </nav>
            <h1 className="text-base sm:text-lg font-semibold text-zinc-900 dark:text-zinc-100 line-clamp-1 mt-0.5">
              {currentLesson.title}
            </h1>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700">
                ⏱️ ~{readingMinutes} min read
              </span>
              <span className={`text-xs font-mono px-2 py-0.5 rounded-full border ${
                complexityBadge === 'Advanced Systems'
                  ? 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/30'
                  : complexityBadge === 'Foundational'
                  ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
                  : 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30'
              }`}>
                ⚡ {complexityBadge}
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2.5 self-stretch md:self-auto justify-end flex-wrap">
          {/* Reader Preferences Bar */}
          <div className="hidden sm:flex items-center gap-1.5 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-xs select-none" aria-label="Reader Controls">
            {/* Font Size */}
            <div className="flex items-center border-r border-zinc-200 dark:border-zinc-700/80 pr-1 gap-0.5">
              <button
                onClick={() => {
                  const sizes: ('sm' | 'md' | 'lg' | 'xl')[] = ['sm', 'md', 'lg', 'xl'];
                  const idx = sizes.indexOf(readerSettings.fontSize);
                  if (idx > 0) updateReaderSettings({ fontSize: sizes[idx - 1] });
                }}
                disabled={readerSettings.fontSize === 'sm'}
                className="px-1.5 py-0.5 rounded font-mono font-bold text-zinc-600 dark:text-zinc-300 hover:bg-white dark:hover:bg-zinc-800 disabled:opacity-30 transition-colors"
                title="Decrease reading font size"
                aria-label="Decrease font size"
              >
                A−
              </button>
              <span className="text-[11px] font-mono text-zinc-400 px-0.5">
                {readerSettings.fontSize.toUpperCase()}
              </span>
              <button
                onClick={() => {
                  const sizes: ('sm' | 'md' | 'lg' | 'xl')[] = ['sm', 'md', 'lg', 'xl'];
                  const idx = sizes.indexOf(readerSettings.fontSize);
                  if (idx < sizes.length - 1) updateReaderSettings({ fontSize: sizes[idx + 1] });
                }}
                disabled={readerSettings.fontSize === 'xl'}
                className="px-1.5 py-0.5 rounded font-mono font-bold text-zinc-600 dark:text-zinc-300 hover:bg-white dark:hover:bg-zinc-800 disabled:opacity-30 transition-colors"
                title="Increase reading font size"
                aria-label="Increase font size"
              >
                A+
              </button>
            </div>

            {/* Typeface Toggle */}
            <div className="flex items-center gap-0.5 border-r border-zinc-200 dark:border-zinc-700/80 pr-1">
              {(['sans', 'serif', 'mono'] as const).map((font) => (
                <button
                  key={font}
                  onClick={() => updateReaderSettings({ fontFamily: font })}
                  className={`px-1.5 py-0.5 rounded text-xs transition-colors ${
                    readerSettings.fontFamily === font
                      ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 font-semibold shadow-xs'
                      : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'
                  }`}
                  title={`${font.charAt(0).toUpperCase() + font.slice(1)} typeface`}
                  aria-label={`${font} typeface`}
                >
                  {font === 'sans' ? 'Sans' : font === 'serif' ? 'Serif' : 'Mono'}
                </button>
              ))}
            </div>

            {/* Measure Toggle */}
            <div className="flex items-center gap-0.5">
              {(['narrow', 'normal', 'wide', 'full'] as const).map((measure) => (
                <button
                  key={measure}
                  onClick={() => updateReaderSettings({ measure })}
                  className={`px-1.5 py-0.5 rounded text-xs font-mono transition-colors ${
                    readerSettings.measure === measure
                      ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 font-semibold shadow-xs'
                      : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'
                  }`}
                  title={`Reading measure: ${measure === 'narrow' ? '64ch' : measure === 'normal' ? '76ch' : measure === 'wide' ? '90ch' : 'Full Page Width'}`}
                  aria-label={`Reading width ${measure}`}
                >
                  {measure === 'narrow' ? '64ch' : measure === 'normal' ? '76ch' : measure === 'wide' ? '90ch' : 'Full'}
                </button>
              ))}
            </div>
          </div>

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
              aria-label={isBookmarked ? 'Bookmarked' : 'Bookmark this lesson'}
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
            aria-label="Toggle Page-Aware Interactive Runner"
          >
            <Terminal className="w-3.5 h-3.5 text-emerald-500" />
            <span>Live Runner</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          </button>

          {/* Mark Complete Toggle */}
          <button
            onClick={handleCompleteClick}
            aria-label={isCompleted ? 'Completed' : 'Mark Complete'}
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
              aria-label="Previous Lesson"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => nextLesson && onSelectLesson(nextLesson.file_path, nextLesson.id)}
              disabled={!nextLesson}
              className="p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-800 disabled:opacity-30 hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-400 transition-colors"
              title="Next Lesson"
              aria-label="Next Lesson"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex items-center gap-1.5 border-b border-zinc-200/80 dark:border-zinc-800/80 pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('theory')}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
            activeTab === 'theory'
              ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 shadow-sm'
              : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
          }`}
        >
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
          <button
            onClick={() => setActiveTab('project')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'project'
                ? 'bg-purple-600 text-white shadow-sm font-bold'
                : 'text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-950/30'
            }`}
          >
            <Hammer className="w-3.5 h-3.5" /> In-Browser Project Studio
            <span className="text-xs px-1 py-0.5 rounded bg-purple-200 dark:bg-purple-900/60 text-purple-900 dark:text-purple-200 font-mono">
              IDE
            </span>
          </button>
        )}

        {hasDsaArena && (
          <button
            onClick={() => setActiveTab('arena')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'arena'
                ? 'bg-amber-600 text-white shadow-sm font-bold'
                : 'text-amber-600 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-950/30'
            }`}
          >
            <Brain className="w-3.5 h-3.5 text-amber-300" /> LeetCode Arena
            <span className="text-xs px-1.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 font-mono font-bold">
              Sandbox
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
              <span className="text-xs px-1 py-0.5 rounded bg-emerald-500 text-white font-mono">
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
            <span className="text-xs px-1 py-0.5 rounded bg-rose-200 dark:bg-rose-900/60 text-rose-900 dark:text-rose-200 font-mono">
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
          <FileText className="w-3.5 h-3.5" /> Personal Notes
          {noteText.trim().length > 0 && (
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
          )}
        </button>

        {/* Storage & SQL Sandbox Tab */}
        {(isStorageCourse || activeTab === 'sql') && (
          <button
            onClick={() => setActiveTab('sql')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'sql'
                ? 'bg-emerald-600 text-white shadow-sm font-bold'
                : 'text-emerald-600 dark:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-950/30'
            }`}
          >
            <Database className="w-3.5 h-3.5" /> Storage & SQL Sandbox
            <span className="text-xs px-1.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono font-bold">
              B-Tree
            </span>
          </button>
        )}

        {/* Distributed Architecture Canvas Tab */}
        {(isDistributedCourse || activeTab === 'arch') && (
          <button
            onClick={() => setActiveTab('arch')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
              activeTab === 'arch'
                ? 'bg-indigo-600 text-white shadow-sm font-bold'
                : 'text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-950/30'
            }`}
          >
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
            <aside aria-label="Module syllabus sidebar" className="w-72 2xl:w-80 shrink-0 rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-4 shadow-sm space-y-3 sticky top-20">
              <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-2">
                <span className="text-xs font-mono font-semibold text-zinc-400 uppercase tracking-wider">
                  Module {module.module_num.toString().padStart(2, '0')} Syllabus
                </span>
                <span className="text-xs font-mono text-zinc-400">
                  {allLessons.filter((l) => completedLessons.includes(l.id)).length}/{allLessons.length}
                </span>
              </div>

              <nav aria-label="Module Lessons" className="space-y-1 max-h-[75vh] overflow-y-auto">
                {allLessons.map((l, idx) => {
                  const active = l.id === currentLesson.id;
                  const isDone = completedLessons.includes(l.id);

                  return (
                    <button
                      key={l.id}
                      onClick={() => onSelectLesson(l.file_path, l.id)}
                      aria-label={`Lesson ${idx + 1}: ${l.title} ${isDone ? '(completed)' : ''}`}
                      className={`w-full text-left px-2.5 py-2 rounded-xl text-xs transition-all flex items-center justify-between gap-2 ${
                        active
                          ? 'bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 font-semibold border border-blue-200 dark:border-blue-900/60 shadow-sm'
                          : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100/70 dark:hover:bg-zinc-800/50'
                      }`}
                    >
                      <span className="line-clamp-1 flex items-center gap-2">
                        <span className="font-mono text-xs text-zinc-400">
                          {(idx + 1).toString().padStart(2, '0')}
                        </span>
                        <span>{l.title}</span>
                      </span>
                      <div className="flex items-center gap-1.5 shrink-0">
                        {getLessonBadge(l.type)}
                        {isDone ? (
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                        ) : (
                          <div className="w-1.5 h-1.5 rounded-full bg-zinc-300 dark:bg-zinc-700 shrink-0" />
                        )}
                      </div>
                    </button>
                  );
                })}
              </nav>
            </aside>
          )}

          {/* Center Area: Active View (Fluid, Takes ALL remaining width) */}
          <div className="flex-1 min-w-0 space-y-4">
                {/* TAB: THEORY & SCRIPT READER */}
                {activeTab === 'theory' && (
                  <div ref={theoryContentRef}>
                    {/* CASE A: PYTHON / POWERSHELL / SHELL SCRIPT VIEW */}
                    {(currentLesson.type === 'code' || currentLesson.type === 'powershell' || currentLesson.type === 'shell') ? (
                      <div className="rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 overflow-hidden shadow-sm space-y-0">
                        {/* Script Header Bar */}
                        <div className="p-5 border-b border-zinc-200/80 dark:border-zinc-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-zinc-50/70 dark:bg-[#161B22]">
                          <div className="flex items-center gap-3">
                            <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
                              <Code2 className="w-5 h-5" />
                            </div>
                            <div>
                              <div className="flex items-center gap-2">
                                <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold uppercase ${
                                  currentLesson.type === 'powershell'
                                    ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                                    : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                                }`}>
                                  {currentLesson.type === 'powershell' ? 'PowerShell Automation' : 'Python Script'}
                                </span>
                                <span className="text-xs font-mono text-zinc-400">{currentLesson.file_path}</span>
                              </div>
                              <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-100 mt-1">
                                {currentLesson.title}
                              </h2>
                            </div>
                          </div>

                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => {
                                navigator.clipboard.writeText(content);
                                setCodeCopied(true);
                                setTimeout(() => setCodeCopied(false), 2000);
                              }}
                              className="px-3 py-1.5 rounded-xl border border-zinc-300 dark:border-zinc-700 text-xs font-mono flex items-center gap-1.5 hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-300"
                            >
                              {codeCopied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                              <span>{codeCopied ? 'Copied' : 'Copy'}</span>
                            </button>

                            <button
                              onClick={() => {
                                setScratchpadCode(content);
                                setScratchpadMode(currentLesson.type === 'powershell' ? 'powershell' : 'python');
                                setIsScratchpadOpen(true);
                              }}
                              className="px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-2 shadow-sm transition-all"
                            >
                              <Play className="w-3.5 h-3.5 fill-current" />
                              <span>Run in Live Runner</span>
                            </button>
                          </div>
                        </div>

                        {/* Code Body */}
                        <div className="p-6 bg-[#0D1117] overflow-x-auto">
                          <pre className="font-mono text-xs sm:text-sm text-zinc-200 leading-relaxed whitespace-pre-wrap">
                            {content}
                          </pre>
                        </div>
                      </div>
                    ) : currentLesson.type === 'notebook' && notebookCells.length > 0 ? (
                      /* CASE B: JUPYTER NOTEBOOK VIEW */
                      <div className="rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-8 shadow-sm space-y-6">
                        <div className="flex items-center justify-between border-b border-zinc-200/80 dark:border-zinc-800 pb-4">
                          <div className="flex items-center gap-3">
                            <div className="p-2.5 rounded-xl bg-orange-500/10 text-orange-500 border border-orange-500/20">
                              <Layers className="w-5 h-5" />
                            </div>
                            <div>
                              <span className="text-xs font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-orange-500/10 text-orange-500 border border-orange-500/20">
                                Jupyter Visual Notebook
                              </span>
                              <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-100 mt-1">{currentLesson.title}</h2>
                            </div>
                          </div>

                          <button
                            onClick={() => {
                              const allCode = notebookCells.filter((c) => c.type === 'code').map((c) => c.source).join('\n\n');
                              setScratchpadCode(allCode);
                              setScratchpadMode('python');
                              setIsScratchpadOpen(true);
                            }}
                            className="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-orange-600 hover:bg-orange-500 text-white flex items-center gap-2 shadow-sm"
                          >
                            <Play className="w-3.5 h-3.5 fill-current" />
                            <span>Run All Cells</span>
                          </button>
                        </div>

                        {/* Cells List */}
                        <div className="space-y-6">
                          {notebookCells.map((cell, cIdx) => (
                            <div key={cIdx} className="space-y-2">
                              {cell.type === 'markdown' ? (
                                <div
                                  className="markdown-body text-zinc-800 dark:text-zinc-200 text-sm leading-relaxed"
                                  dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(cell.source) }}
                                />
                              ) : (
                                <div className="rounded-xl border border-zinc-800 bg-[#0D1117] overflow-hidden">
                                  <div className="flex items-center justify-between px-3 py-1.5 bg-[#161B22] border-b border-zinc-800 text-xs font-mono text-zinc-400">
                                    <span>Python Cell [{cIdx + 1}]</span>
                                    <button
                                      onClick={() => {
                                        setScratchpadCode(cell.source);
                                        setScratchpadMode('python');
                                        setIsScratchpadOpen(true);
                                      }}
                                      className="px-2 py-0.5 rounded hover:bg-emerald-950/60 text-emerald-400 flex items-center gap-1 border border-emerald-500/30"
                                    >
                                      <Play className="w-3 h-3 fill-current" />
                                      <span>Run Cell</span>
                                    </button>
                                  </div>
                                  <pre className="p-4 font-mono text-xs text-zinc-200 overflow-x-auto">
                                    {cell.source}
                                  </pre>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : (
                      /* CASE C: STANDARD MARKDOWN VIEW (With KaTeX Math) */
                      <div className="rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-8 sm:p-10 shadow-sm">
                        {isLoading ? (
                          <LessonSkeleton />
                        ) : (
                          <>
                            <div
                              className={`markdown-body text-zinc-800 dark:text-zinc-200 mx-auto transition-all ${measureClass} ${fontSizeClass} ${fontFamilyClass}`}
                              dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(content) }}
                            />

                            {/* 1-Tap Spaced Repetition Confidence Rating */}
                            <div className="mt-12 p-5 rounded-2xl bg-zinc-50/70 dark:bg-zinc-900/40 border border-zinc-200/80 dark:border-zinc-800/80 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                              <div>
                                <h4 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                                  How confident do you feel with this lesson?
                                </h4>
                                <p className="text-xs text-zinc-500 mt-0.5">
                                  Rates retention in your SuperMemo SM-2 spaced repetition deck.
                                </p>
                                {confidenceRated && (
                                  <span className="inline-flex items-center gap-1 text-xs text-emerald-600 dark:text-emerald-400 font-mono mt-1">
                                    ✓ {confidenceRated}
                                  </span>
                                )}
                              </div>
                              <div className="flex items-center gap-2">
                                <button
                                  onClick={() => handleConfidenceClick(5, '🟢 Solid retention scheduled (5/5)')}
                                  className="px-3 py-1.5 rounded-xl text-xs font-medium border border-emerald-300 dark:border-emerald-800/80 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100 dark:hover:bg-emerald-900/40 transition-colors flex items-center gap-1.5"
                                  title="Got it: high retention, intervals expand"
                                  aria-label="Got it (High confidence)"
                                >
                                  <span>🟢 Got it</span>
                                </button>
                                <button
                                  onClick={() => handleConfidenceClick(3, '🟡 Review scheduled for tomorrow (3/5)')}
                                  className="px-3 py-1.5 rounded-xl text-xs font-medium border border-amber-300 dark:border-amber-800/80 bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 hover:bg-amber-100 dark:hover:bg-amber-900/40 transition-colors flex items-center gap-1.5"
                                  title="Shaky: review tomorrow to solidify"
                                  aria-label="Shaky (Medium confidence)"
                                >
                                  <span>🟡 Shaky</span>
                                </button>
                                <button
                                  onClick={() => handleConfidenceClick(1, '🔴 Reset for immediate review today (1/5)')}
                                  className="px-3 py-1.5 rounded-xl text-xs font-medium border border-rose-300 dark:border-rose-800/80 bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 hover:bg-rose-100 dark:hover:bg-rose-900/40 transition-colors flex items-center gap-1.5"
                                  title="Lost: reset interval to 1 day"
                                  aria-label="Lost (Low confidence)"
                                >
                                  <span>🔴 Lost</span>
                                </button>
                              </div>
                            </div>

                            {/* Up Next Preview Card */}
                            {nextLesson ? (
                              <div className="my-8 p-5 sm:p-6 rounded-2xl bg-zinc-50/80 dark:bg-zinc-900/50 border border-zinc-200/80 dark:border-zinc-800/80 shadow-xs transition-all hover:border-blue-500/40 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                                <div className="space-y-1">
                                  <div className="flex items-center gap-2">
                                    <span className="text-xs font-mono font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                                      Up Next • Lesson {currentLessonIndex + 2} of {allLessons.length}
                                    </span>
                                    {getLessonBadge(nextLesson.type)}
                                  </div>
                                  <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
                                    {nextLesson.title}
                                  </h3>
                                </div>
                                <button
                                  onClick={handleCompleteAndNext}
                                  className="px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white flex items-center gap-1.5 shadow-sm transition-all active:scale-95 shrink-0"
                                  aria-label="Continue to Next Lesson"
                                >
                                  <span>Next Lesson</span>
                                  <ChevronRight className="w-4 h-4" />
                                </button>
                              </div>
                            ) : (
                              <div className="my-8 p-6 rounded-2xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200/80 dark:border-emerald-800/60 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                                <div className="space-y-1">
                                  <div className="flex items-center gap-2">
                                    <span className="text-xs font-mono font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
                                      Module Complete
                                    </span>
                                  </div>
                                  <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
                                    All lessons cleared for Module {module.module_num.toString().padStart(2, '0')}
                                  </h3>
                                  <p className="text-xs text-zinc-500">
                                    Ready to test your comprehension in the Module Mastery Gate?
                                  </p>
                                </div>
                                <button
                                  onClick={() => {
                                    if (onOpenMasteryGate) onOpenMasteryGate();
                                  }}
                                  className="px-4 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-2 shadow-sm transition-all active:scale-95 shrink-0"
                                  aria-label="Unlock Module Mastery Gate"
                                >
                                  <span>Mastery Gate 🛡️</span>
                                  <ChevronRight className="w-4 h-4" />
                                </button>
                              </div>
                            )}
                          </>
                        )}

                        {/* Bottom Lesson Navigation Dock */}
                        <div className="mt-12 pt-6 border-t border-zinc-200/80 dark:border-zinc-800/80 flex flex-col sm:flex-row items-center justify-between gap-4 sticky bottom-4 bg-white/95 dark:bg-[#111622]/95 backdrop-blur-md p-4 rounded-2xl border border-zinc-200/90 dark:border-zinc-800 shadow-xl z-20">
                          <div className="flex items-center gap-3 w-full sm:w-auto">
                            <button
                              onClick={handlePrevLesson}
                              disabled={!prevLesson}
                              className="flex-1 sm:flex-initial px-4 py-2.5 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 bg-zinc-50 dark:bg-zinc-900 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30 disabled:pointer-events-none transition-colors text-xs font-medium text-zinc-700 dark:text-zinc-300 flex items-center gap-2 shadow-sm"
                            >
                              <ChevronLeft className="w-4 h-4" />
                              <span>Previous Lesson</span>
                            </button>
                          </div>

                          <div className="flex items-center gap-3 text-xs font-mono text-zinc-500">
                            <span>Lesson {currentLessonIndex + 1} of {allLessons.length}</span>
                            <span className="text-zinc-300 dark:text-zinc-700">•</span>
                            <span className={`inline-flex items-center gap-1 font-semibold ${isCompleted ? 'text-emerald-500' : 'text-zinc-400'}`}>
                              <CheckCircle2 className="w-3.5 h-3.5" />
                              {isCompleted ? 'Completed' : 'In Progress'}
                            </span>
                          </div>

                          <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
                            <button
                              onClick={handleCompleteAndNext}
                              className="flex-1 sm:flex-initial px-5 py-2.5 rounded-xl text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center gap-2 shadow-md transition-all active:scale-95"
                            >
                              <span>{nextLesson ? 'Mark Complete & Next' : 'Unlock Module Mastery Gate 🛡️'}</span>
                              <ChevronRight className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      </div>
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
                  <div className="rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-6 space-y-4">
                    <div className="flex items-center justify-between border-b border-zinc-200/80 dark:border-zinc-800 pb-3">
                      <div className="flex items-center gap-2">
                        <FileText className="w-4 h-4 text-blue-500" />
                        <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                          Personal Study Notes: {currentLesson.title}
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

                    <textarea
                      value={noteText}
                      onChange={(e) => setNoteText(e.target.value)}
                      placeholder="Write key takeaways, performance equations, and interview questions here..."
                      className="w-full h-80 p-4 font-mono text-xs rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-1 focus:ring-blue-500 resize-y leading-relaxed"
                    />
                  </div>
                )}
              </div>

          {/* Right Rail: Page-Aware Interactive Runner OR Sticky Quick-Reach TOC */}
          {isScratchpadOpen ? (
            <aside aria-label="Interactive multi-runtime code runner" className="w-96 2xl:w-[480px] shrink-0 sticky top-20 h-[calc(100vh-6rem)] rounded-2xl overflow-hidden border border-zinc-200/80 dark:border-zinc-800/80 shadow-2xl">
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
        <button
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          className="fixed bottom-8 right-8 z-30 p-3 rounded-full bg-zinc-900/90 dark:bg-zinc-100/90 text-white dark:text-zinc-900 shadow-xl hover:scale-110 active:scale-95 transition-all border border-zinc-700/50 dark:border-zinc-300/50"
          title="Back to top"
          aria-label="Back to top"
        >
          <ArrowUp className="w-4 h-4" />
        </button>
      )}
    </div>
    </>
  );
};
