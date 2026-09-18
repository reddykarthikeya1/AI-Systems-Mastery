import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, Save, RotateCcw, CheckCircle2, XCircle, AlertCircle, FileCode, CheckSquare, 
  Eye, Terminal, Clock, Folder, ChevronRight, ChevronDown, Lock, Check, Columns, Maximize2, 
  FileText, Sparkles, Sliders, Split, Code2, AlertTriangle, BookOpen, Compass, ShieldCheck,
  Lightbulb, Layers, Flame, ArrowRight, RefreshCw, ArrowLeft, Copy
} from 'lucide-react';
import { fetchFileContent, runTestCommand, formatCode } from '../services/api';
import { TestResult, SingleTestCaseResult, ModuleItem } from '../types';
import { renderMarkdownWithMath } from '../services/markdown';
import { soundService } from '../services/sound';
import { fireConfettiBurst } from '../services/confetti';
import { useMermaid } from '../hooks/useMermaid';
import { handleMarkdownLinkClick } from '../services/linkInterceptor';

interface ProjectStudioProps {
  moduleFolderPath: string;
  moduleTitle: string;
  courseTitle: string;
  guideMarkdown: string;
  onCompleteProject: () => void;
  isProjectCompleted: boolean;
  onBackToLesson?: () => void;
  currentLessonTitle?: string;
  module?: ModuleItem;
}

interface StudioFile {
  filename: string;
  content: string;
  starter_content: string;
  solution_content?: string | null;
  is_modified: boolean;
  read_only?: boolean;
}

type ViewMode = 'split' | 'editor' | 'spec';
type LeftTab = 'orientation' | 'roadmap' | 'guide' | 'tests';

interface ExtractedItem {
  name: string;
  params: string;
  returnType: string;
  docstring?: string;
}

export const ProjectStudio: React.FC<ProjectStudioProps> = ({
  moduleFolderPath,
  moduleTitle,
  courseTitle,
  guideMarkdown,
  onCompleteProject,
  isProjectCompleted,
  onBackToLesson,
  currentLessonTitle,
  module,
}) => {
  const [files, setFiles] = useState<StudioFile[]>([]);
  const [activeFileIndex, setActiveFileIndex] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [savedSuccess, setSavedSuccess] = useState<boolean>(false);
  const [isRunningTests, setIsRunningTests] = useState<boolean>(false);
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [showSolutionDiff, setShowSolutionDiff] = useState<boolean>(false);
  const [viewMode, setViewMode] = useState<ViewMode>('split');
  const [fontSize, setFontSize] = useState<'sm' | 'base'>('sm');
  const [activeTerminalTab, setActiveTerminalTab] = useState<'breakdown' | 'tests' | 'diff'>('breakdown');
  const [testScope, setTestScope] = useState<'workspace' | 'solution'>('workspace');
  const [leftTab, setLeftTab] = useState<LeftTab>('orientation');
  const [orientationSubTab, setOrientationSubTab] = useState<'delta' | 'manifest' | 'phases'>('delta');
  const [showResetConfirm, setShowResetConfirm] = useState<boolean>(false);
  const [expandedTestIdx, setExpandedTestIdx] = useState<number | null>(null);
  const [openHintIndex, setOpenHintIndex] = useState<number | null>(null);

  const guideContainerRef = useRef<HTMLDivElement>(null);
  useMermaid(guideContainerRef, [guideMarkdown, leftTab]);

  const [milestones, setMilestones] = useState<Record<string, boolean>>({
    m1: false,
    m2: false,
    m3: false,
  });

  const [copiedCmd, setCopiedCmd] = useState<string | null>(null);
  const workspaceRelativePath = `user_workspaces/${moduleFolderPath}`;

  const handleCopyCmd = (cmd: string, id: string) => {
    navigator.clipboard.writeText(cmd);
    setCopiedCmd(id);
    soundService.playClick();
    setTimeout(() => setCopiedCmd(null), 2500);
  };

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Load project starter and solution files from server
  useEffect(() => {
    setLoading(true);
    fetch(`/api/project-files?module_path=${encodeURIComponent(moduleFolderPath)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.files && data.files.length > 0) {
          setFiles(data.files);
        } else {
          setFiles([
            {
              filename: 'solution.py',
              content: '# In-Browser Guided Project Studio\n# Implement your production solution below:\n\ndef solution():\n    pass\n',
              starter_content: '# Starter template\n',
              is_modified: false,
            },
          ]);
        }
      })
      .catch(() => {
        setFiles([
          {
            filename: 'solution.py',
            content: '# Project workspace ready.\n',
            starter_content: '',
            is_modified: false,
          },
        ]);
      })
      .finally(() => setLoading(false));
  }, [moduleFolderPath]);

  const activeFile = files[activeFileIndex] || files[0];

  const handleCodeChange = (newCode: string) => {
    setFiles((prev) =>
      prev.map((f, i) =>
        i === activeFileIndex
          ? { ...f, content: newCode, is_modified: newCode !== f.starter_content }
          : f
      )
    );
  };

  const [isFormatting, setIsFormatting] = useState<boolean>(false);
  const [formatSuccess, setFormatSuccess] = useState<boolean>(false);

  const handleFormatCode = async () => {
    if (!activeFile || isFormatting || activeFile.read_only) return;
    setIsFormatting(true);
    soundService.playClick();
    try {
      const res = await formatCode(activeFile.content, 'python');
      if (res.formatted && res.formatted !== activeFile.content) {
        handleCodeChange(res.formatted);
        soundService.playSuccess();
        setFormatSuccess(true);
        setTimeout(() => setFormatSuccess(false), 2000);
      }
    } catch (e) {
      soundService.playError();
    } finally {
      setIsFormatting(false);
    }
  };

  const handleSaveWorkspace = async () => {
    if (!activeFile) return;
    setSaving(true);
    try {
      await fetch('/api/save-project-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          module_path: moduleFolderPath,
          filename: activeFile.filename,
          content: activeFile.content,
        }),
      });
      soundService.playClick();
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 2000);
    } catch (e) {
      console.warn('Failed to save project file', e);
    } finally {
      setSaving(false);
    }
  };

  const confirmResetStarter = () => {
    if (!activeFile) return;
    soundService.playClick();
    setFiles((prev) =>
      prev.map((f, i) =>
        i === activeFileIndex
          ? { ...f, content: f.starter_content, is_modified: false }
          : f
      )
    );
    setShowResetConfirm(false);
  };

  const handleRunTests = async (overrideScope?: 'workspace' | 'solution') => {
    const targetScope = overrideScope || testScope;
    setIsRunningTests(true);
    setTestResult(null);
    setActiveTerminalTab('breakdown');
    soundService.playClick();
    try {
      if (targetScope === 'workspace') {
        await handleSaveWorkspace();
      }
      const res = await runTestCommand(moduleFolderPath, 'pytest', targetScope);
      setTestResult(res);

      if (res.exit_code === 0 && (res.passed_tests || 0) > 0) {
        soundService.playFanfare();
        fireConfettiBurst();
        setMilestones({ m1: true, m2: true, m3: true });
        onCompleteProject();
      } else if ((res.passed_tests || 0) > 0) {
        const percent = res.percent || 0;
        setMilestones({
          m1: percent >= 25,
          m2: percent >= 65,
          m3: percent === 100,
        });
        soundService.playClick();
      } else {
        soundService.playError();
      }
    } catch (err: any) {
      soundService.playError();
      setTestResult({
        exit_code: -1,
        stdout: '',
        stderr: err.message || 'Project test harness execution failed',
        duration_sec: 0,
        status: 'error',
        total_tests: 0,
        passed_tests: 0,
        failed_tests: 0,
        percent: 0,
        tests: [],
      });
    } finally {
      setIsRunningTests(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    const textarea = textareaRef.current;
    if (!textarea || activeFile?.read_only) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const content = activeFile.content;

    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') {
      e.preventDefault();
      handleSaveWorkspace();
      return;
    }

    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRunTests();
      return;
    }

    if (e.key === 'Tab') {
      e.preventDefault();
      const newCode = content.substring(0, start) + '    ' + content.substring(end);
      handleCodeChange(newCode);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 4;
      }, 0);
      return;
    }

    if (e.key === 'Enter') {
      e.preventDefault();
      const linesBefore = content.substring(0, start).split('\n');
      const currentLine = linesBefore[linesBefore.length - 1] || '';
      const match = currentLine.match(/^(\s*)/);
      let indent = match ? match[1] : '';
      if (currentLine.trim().endsWith(':')) {
        indent += '    ';
      }
      const newCode = content.substring(0, start) + '\n' + indent + content.substring(end);
      handleCodeChange(newCode);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 1 + indent.length;
      }, 0);
    }
  };

  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') {
        e.preventDefault();
        handleSaveWorkspace();
      } else if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        handleRunTests();
      }
    };
    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, [activeFile]);

  // Helper to extract function and method declarations for the Guided Roadmap
  const extractedItems: ExtractedItem[] = React.useMemo(() => {
    const source = activeFile?.starter_content || activeFile?.content || '';
    const items: ExtractedItem[] = [];
    const lines = source.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const fnMatch = line.match(/def\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)(?:\s*->\s*([^:]+))?:/);
      if (fnMatch) {
        let doc: string | undefined = undefined;
        if (i + 1 < lines.length && lines[i + 1].includes('"""')) {
          doc = lines[i + 1].replace(/"""/g, '').trim();
        }
        items.push({
          name: fnMatch[1],
          params: fnMatch[2].trim(),
          returnType: fnMatch[3] ? fnMatch[3].trim() : 'Any',
          docstring: doc,
        });
      }
    }
    return items;
  }, [activeFile]);

  const completedMilestones = Object.values(milestones).filter(Boolean).length;
  const toggleMilestone = (key: 'm1' | 'm2' | 'm3') => {
    soundService.playClick();
    setMilestones((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="w-full space-y-5 animate-in fade-in duration-200">
      {/* Reset Confirmation Modal */}
      {showResetConfirm && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-surface border border-border max-w-md w-full rounded-2xl p-6 shadow-2xl space-y-4 animate-in zoom-in-95">
            <div className="flex items-center gap-3 text-amber-400">
              <AlertTriangle className="w-6 h-6" />
              <h3 className="font-bold text-base text-fg">Reset Workspace to Starter?</h3>
            </div>
            <p className="text-sm text-fg-muted leading-relaxed">
              This will discard all uncommitted changes to <span className="font-mono text-fg font-semibold">{activeFile?.filename}</span> and restore the pristine starter template.
            </p>
            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setShowResetConfirm(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-surface-raised hover:bg-zinc-800 text-fg transition"
              >
                Cancel
              </button>
              <button
                onClick={confirmResetStarter}
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-rose-600 hover:bg-rose-500 text-white transition shadow-sm"
              >
                Yes, Reset Code
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header Bar */}
      <div className="flex flex-col xl:flex-row xl:items-center justify-between gap-4 p-5 sm:p-6 rounded-2xl bg-surface border border-border shadow-sm">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 shrink-0 shadow-inner">
            <Code2 className="w-6 h-6" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="px-2 py-0.5 rounded text-xs font-mono font-bold uppercase tracking-wider bg-purple-500/10 text-purple-600 dark:text-purple-400 border border-purple-500/20">
                In-Browser Project Studio
              </span>
              <span className="text-xs font-mono text-zinc-400 truncate">
                {moduleFolderPath}
              </span>
            </div>
            <h2 className="text-base sm:text-lg font-bold text-fg mt-0.5 truncate">
              {moduleTitle}
            </h2>
          </div>
        </div>

        {/* View Mode & Primary Action Controls */}
        <div className="flex items-center gap-2.5 flex-wrap self-stretch xl:self-auto justify-between xl:justify-end">
          {/* View Mode Toggle */}
          <div className="flex items-center rounded-xl bg-zinc-100 dark:bg-zinc-900/80 p-1 border border-border">
            <button
              onClick={() => setViewMode('split')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                viewMode === 'split'
                  ? 'bg-white dark:bg-zinc-800 text-fg shadow-xs font-semibold'
                  : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
              }`}
            >
              <Split className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Split</span>
            </button>
            <button
              onClick={() => setViewMode('editor')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                viewMode === 'editor'
                  ? 'bg-white dark:bg-zinc-800 text-fg shadow-xs font-semibold'
                  : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
              }`}
            >
              <Maximize2 className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Code Focused</span>
            </button>
            <button
              onClick={() => setViewMode('spec')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                viewMode === 'spec'
                  ? 'bg-white dark:bg-zinc-800 text-fg shadow-xs font-semibold'
                  : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Roadmap Only</span>
            </button>
          </div>

          {/* Save Workspace */}
          <button
            onClick={handleSaveWorkspace}
            disabled={saving}
            className="px-3 py-1.5 rounded-xl text-xs font-medium border border-zinc-300 dark:border-zinc-700 bg-surface hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1.5 text-fg"
            title="Persist changes to local workspace"
          >
            {savedSuccess ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Save className="w-3.5 h-3.5" />}
            <span>{savedSuccess ? 'Saved' : 'Save'}</span>
          </button>

          {/* Format Code */}
          <button
            onClick={handleFormatCode}
            disabled={isFormatting || activeFile?.read_only}
            className="px-3 py-1.5 rounded-xl text-xs font-medium border border-zinc-300 dark:border-zinc-700 bg-surface hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1.5 text-zinc-700 dark:text-zinc-300"
            title="Format Python code"
          >
            <Sparkles className={`w-3.5 h-3.5 text-amber-500 ${isFormatting ? 'animate-spin' : ''}`} />
            <span>{formatSuccess ? 'Formatted!' : 'Format'}</span>
          </button>

          {/* Reset Starter */}
          <button
            onClick={() => setShowResetConfirm(true)}
            className="px-3 py-1.5 rounded-xl text-xs font-medium border border-zinc-300 dark:border-zinc-700 bg-surface hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1.5 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900"
            title="Reset to starter template"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Reset</span>
          </button>

          {/* Run Pytest Harness */}
          <button
            onClick={() => handleRunTests()}
            disabled={isRunningTests}
            className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm transition-all ${
              isRunningTests
                ? 'bg-zinc-400 text-white cursor-not-allowed'
                : 'bg-emerald-600 hover:bg-emerald-500 text-white active:scale-95 ring-2 ring-emerald-500/20'
            }`}
            title="Execute test suite (Ctrl + Enter)"
          >
            <Play className={`w-3.5 h-3.5 ${isRunningTests ? 'animate-spin' : 'fill-current'}`} />
            <span>{isRunningTests ? 'Verifying...' : 'Run Project Tests (Ctrl+Enter)'}</span>
          </button>
        </div>
      </div>

      {/* Dual-Mode IDE & Local Terminal Workflow Bar */}
      <div className="rounded-2xl border border-blue-200 dark:border-blue-900/60 bg-blue-50/70 dark:bg-blue-950/30 p-4 shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-3 min-w-0">
          <div className="p-2.5 rounded-xl bg-blue-600 text-white shrink-0 shadow-xs">
            <Code2 className="w-4 h-4" />
          </div>
          <div className="space-y-0.5 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-bold text-blue-900 dark:text-blue-100 text-sm">Dual-Mode Workflow:</span>
              <span className="text-blue-700 dark:text-blue-300 font-medium">Build in-app with Live Runner &bull; Or build in VS Code / external IDE</span>
            </div>
            <p className="text-blue-600 dark:text-blue-400 font-mono text-xs flex items-center gap-1.5 truncate">
              <span>Local Workspace:</span>
              <span className="font-semibold text-fg px-1.5 py-0.5 rounded bg-surface border border-blue-200 dark:border-blue-900/60">{workspaceRelativePath}</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0 flex-wrap">
          <button
            onClick={() => handleCopyCmd(`code "${workspaceRelativePath}"`, 'code')}
            className="px-3 py-1.5 rounded-xl border border-blue-300 dark:border-blue-800 bg-surface text-blue-700 dark:text-blue-300 hover:bg-blue-100/60 dark:hover:bg-blue-900/50 font-mono text-xs font-semibold flex items-center gap-1.5 transition shadow-xs"
            title="Copy command to open this project directory in VS Code"
          >
            {copiedCmd === 'code' ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Terminal className="w-3.5 h-3.5 text-blue-500" />}
            <span>{copiedCmd === 'code' ? 'Copied code command!' : 'Open in VS Code: code .'}</span>
          </button>
          <button
            onClick={() => handleCopyCmd(`pytest "${workspaceRelativePath}" -v`, 'pytest')}
            className="px-3 py-1.5 rounded-xl border border-blue-300 dark:border-blue-800 bg-surface text-blue-700 dark:text-blue-300 hover:bg-blue-100/60 dark:hover:bg-blue-900/50 font-mono text-xs font-semibold flex items-center gap-1.5 transition shadow-xs"
            title="Copy pytest command to run in your local terminal"
          >
            {copiedCmd === 'pytest' ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <CheckSquare className="w-3.5 h-3.5 text-emerald-500" />}
            <span>{copiedCmd === 'pytest' ? 'Copied CLI pytest!' : 'Run in Terminal: pytest'}</span>
          </button>
        </div>
      </div>

      {/* Main Studio Dual Pane */}
      <div className={`grid gap-6 items-start transition-all ${
        viewMode === 'split' 
          ? 'grid-cols-1 xl:grid-cols-12' 
          : 'grid-cols-1'
      }`}>
        {/* Left Column: Guided Direction, Roadmap & Specifications */}
        {(viewMode === 'split' || viewMode === 'spec') && (
          <div className={`${viewMode === 'split' ? 'xl:col-span-5' : 'w-full'} space-y-4`}>
            {/* Left Navigation Tabs: Orientation | Milestones | Project Guide | Test Plan */}
            <div className="rounded-2xl bg-surface border border-border/80 p-2 shadow-sm flex items-center gap-1">
              <button
                onClick={() => setLeftTab('orientation')}
                className={`flex-1 py-2 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition ${
                  leftTab === 'orientation'
                    ? 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30'
                    : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'
                }`}
              >
                <Compass className="w-4 h-4" />
                <span>Orientation</span>
              </button>
              <button
                onClick={() => setLeftTab('roadmap')}
                className={`flex-1 py-2 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition ${
                  leftTab === 'roadmap'
                    ? 'bg-sky-500/15 text-sky-500 dark:text-sky-400 border border-sky-500/30'
                    : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'
                }`}
              >
                <CheckSquare className="w-4 h-4" />
                <span>Milestones</span>
              </button>
              <button
                onClick={() => setLeftTab('guide')}
                className={`flex-1 py-2 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition ${
                  leftTab === 'guide'
                    ? 'bg-sky-500/15 text-sky-500 dark:text-sky-400 border border-sky-500/30'
                    : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'
                }`}
              >
                <BookOpen className="w-4 h-4" />
                <span>Project Guide</span>
              </button>
              <button
                onClick={() => setLeftTab('tests')}
                className={`flex-1 py-2 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition ${
                  leftTab === 'tests'
                    ? 'bg-sky-500/15 text-sky-500 dark:text-sky-400 border border-sky-500/30'
                    : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200'
                }`}
              >
                <ShieldCheck className="w-4 h-4" />
                <span>Test Plan</span>
              </button>
            </div>

            {/* TAB 0: ARCHITECTURAL ORIENTATION & CAPSTONE BRIDGE */}
            {leftTab === 'orientation' && (
              <div className="rounded-2xl bg-surface border border-border/80 p-5 shadow-sm space-y-4 max-h-[720px] overflow-y-auto">
                <div className="flex items-center justify-between border-b border-border pb-3">
                  <div className="flex items-center gap-2">
                    <Compass className="w-4 h-4 text-emerald-500" />
                    <span className="text-xs font-mono font-bold uppercase tracking-wider text-fg">
                      Architectural Blueprint & Bridge
                    </span>
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 font-semibold">
                    Mental Model Bridge
                  </span>
                </div>

                {/* Sub-tab pills */}
                <div className="flex items-center gap-1.5 p-1 rounded-xl bg-surface-raised border border-border text-xs">
                  <button
                    onClick={() => setOrientationSubTab('delta')}
                    className={`flex-1 py-1.5 rounded-lg font-medium transition ${
                      orientationSubTab === 'delta'
                        ? 'bg-emerald-500 text-white shadow-xs'
                        : 'text-fg-muted hover:text-fg'
                    }`}
                  >
                    Model Delta
                  </button>
                  <button
                    onClick={() => setOrientationSubTab('manifest')}
                    className={`flex-1 py-1.5 rounded-lg font-medium transition ${
                      orientationSubTab === 'manifest'
                        ? 'bg-emerald-500 text-white shadow-xs'
                        : 'text-fg-muted hover:text-fg'
                    }`}
                  >
                    Directory Tour
                  </button>
                  <button
                    onClick={() => setOrientationSubTab('phases')}
                    className={`flex-1 py-1.5 rounded-lg font-medium transition ${
                      orientationSubTab === 'phases'
                        ? 'bg-emerald-500 text-white shadow-xs'
                        : 'text-fg-muted hover:text-fg'
                    }`}
                  >
                    3 Tiers
                  </button>
                </div>

                {orientationSubTab === 'delta' && (
                  <div className="space-y-3 text-xs leading-relaxed">
                    <div className="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/60 text-emerald-800 dark:text-emerald-300">
                      <strong>The Pedagogical Bridge:</strong> The beginner playground simplifies external realities so you grasp the core invariant. The production implementation wraps that same invariant in real-world concurrency, durability, and fault tolerance.
                    </div>
                    <div className="grid grid-cols-1 gap-3">
                      <div className="p-3.5 rounded-xl bg-surface-raised border border-border space-y-2">
                        <span className="font-bold text-amber-600 dark:text-amber-400 uppercase text-[11px] block">
                          Beginner Playground (Mental Model)
                        </span>
                        <ul className="space-y-1.5 text-fg-muted">
                          <li>• In-memory primitives (dict, list) with no disk sync</li>
                          <li>• Synchronous single-threaded function execution</li>
                          <li>• Self-validating print blocks to observe state</li>
                        </ul>
                      </div>
                      <div className="p-3.5 rounded-xl bg-surface-raised border border-border space-y-2">
                        <span className="font-bold text-emerald-600 dark:text-emerald-400 uppercase text-[11px] block">
                          Production Implementation (System Reality)
                        </span>
                        <ul className="space-y-1.5 text-fg-muted">
                          <li>• Write-Ahead Logs (WAL), atomic fsync, and binary serialization</li>
                          <li>• Concurrency locks, thread-safe channels, and race protection</li>
                          <li>• Automated pytest invariant suites and property-based tests</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                )}

                {orientationSubTab === 'manifest' && (
                  <div className="space-y-2.5 text-xs">
                    <p className="text-fg-muted">
                      Standard module layout for hands-on project engineering:
                    </p>
                    <div className="p-3 rounded-xl bg-surface-raised border border-border font-mono text-[11px] space-y-1.5 text-fg">
                      <div>📁 <strong>starter/</strong> — Unimplemented scaffolds with type signatures & docstrings.</div>
                      <div>📁 <strong>project_solution/</strong> — Fully implemented reference solution with production tests.</div>
                      <div>📄 <strong>PROJECT_GUIDE.md</strong> — Architectural specification & 3-tier milestone roadmap.</div>
                    </div>
                  </div>
                )}

                {orientationSubTab === 'phases' && (
                  <div className="space-y-2 text-xs">
                    <div className="p-3 rounded-xl bg-surface-raised border border-border space-y-1">
                      <strong className="text-blue-600 dark:text-blue-400">Tier 1: Guided Implementation</strong>
                      <p className="text-fg-muted">Follow function signatures and inline hints to establish baseline behavior.</p>
                    </div>
                    <div className="p-3 rounded-xl bg-surface-raised border border-border space-y-1">
                      <strong className="text-amber-600 dark:text-amber-400">Tier 2: Boundary Invariants & Hardening</strong>
                      <p className="text-fg-muted">Add validation for zero, negative, and invalid inputs with proper exceptions.</p>
                    </div>
                    <div className="p-3 rounded-xl bg-surface-raised border border-border space-y-1">
                      <strong className="text-emerald-600 dark:text-emerald-400">Tier 3: Full Verification & Mastery</strong>
                      <p className="text-fg-muted">Pass all automated assertions and compare against the production solution.</p>
                    </div>
                  </div>
                )}

                <div className="pt-2 border-t border-border flex justify-end">
                  <button
                    onClick={() => setLeftTab('guide')}
                    className="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white flex items-center gap-1.5 transition shadow-xs"
                  >
                    <span>Proceed to Project Guide</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            )}

            {/* TAB 1: STEP-BY-STEP GUIDED ROADMAP */}
            {leftTab === 'roadmap' && (
              <div className="space-y-4">
                {/* Milestone Checklist Card */}
                <div className="rounded-2xl bg-surface border border-border/80 p-5 shadow-sm space-y-3.5">
                  <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-3">
                    <div className="flex items-center gap-2">
                      <CheckSquare className="w-4 h-4 text-purple-500" />
                      <span className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-700 dark:text-zinc-300">
                        Milestone Verification Checklist
                      </span>
                    </div>
                    <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded-full bg-purple-50 dark:bg-purple-950/60 text-purple-600 dark:text-purple-300 border border-purple-200 dark:border-purple-800/60">
                      {completedMilestones}/3 Finished
                    </span>
                  </div>

                  {/* Progress bar */}
                  <div className="w-full h-1.5 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-purple-500 to-emerald-500 rounded-full transition-all duration-500"
                      style={{ width: `${(completedMilestones / 3) * 100}%` }}
                    />
                  </div>

                  <div className="space-y-2.5 pt-1">
                    <label
                      onClick={() => toggleMilestone('m1')}
                      className={`flex items-start gap-3 p-3 rounded-xl border transition-all cursor-pointer ${
                        milestones.m1
                          ? 'bg-emerald-50/60 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-800/60'
                          : 'bg-zinc-50/60 dark:bg-zinc-900/40 border-border/80 hover:bg-zinc-100/60'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={milestones.m1}
                        onChange={() => {}}
                        className="mt-0.5 rounded border-zinc-300 text-emerald-600 focus:ring-0"
                      />
                      <div className="text-xs">
                        <span className="font-bold text-fg">Tier 1: Core Domain Logic</span>
                        <p className="text-fg-muted mt-0.5 leading-relaxed">
                          Core mathematical calculations, data structures, and happy-path inputs.
                        </p>
                      </div>
                    </label>

                    <label
                      onClick={() => toggleMilestone('m2')}
                      className={`flex items-start gap-3 p-3 rounded-xl border transition-all cursor-pointer ${
                        milestones.m2
                          ? 'bg-emerald-50/60 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-800/60'
                          : 'bg-zinc-50/60 dark:bg-zinc-900/40 border-border/80 hover:bg-zinc-100/60'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={milestones.m2}
                        onChange={() => {}}
                        className="mt-0.5 rounded border-zinc-300 text-emerald-600 focus:ring-0"
                      />
                      <div className="text-xs">
                        <span className="font-bold text-fg">Tier 2: Invariants & Boundary Guards</span>
                        <p className="text-fg-muted mt-0.5 leading-relaxed">
                          Input validation, negative/zero edge cases, and appropriate exception handling.
                        </p>
                      </div>
                    </label>

                    <label
                      onClick={() => toggleMilestone('m3')}
                      className={`flex items-start gap-3 p-3 rounded-xl border transition-all cursor-pointer ${
                        milestones.m3
                          ? 'bg-emerald-50/60 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-800/60'
                          : 'bg-zinc-50/60 dark:bg-zinc-900/40 border-border/80 hover:bg-zinc-100/60'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={milestones.m3}
                        onChange={() => {}}
                        className="mt-0.5 rounded border-zinc-300 text-emerald-600 focus:ring-0"
                      />
                      <div className="text-xs">
                        <span className="font-bold text-fg">Tier 3: 100% Pytest Verification</span>
                        <p className="text-fg-muted mt-0.5 leading-relaxed">
                          Pass all automated assertions in the project verification test suite.
                        </p>
                      </div>
                    </label>
                  </div>
                </div>

                {/* Step-by-Step Function Cards */}
                <div className="rounded-2xl bg-surface border border-border/80 p-5 shadow-sm space-y-3">
                  <div className="flex items-center justify-between pb-2 border-b border-zinc-100 dark:border-zinc-800">
                    <span className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-600 dark:text-zinc-400">
                      Step-by-Step Directives
                    </span>
                    <span className="text-xs font-mono text-zinc-400">
                      {extractedItems.length} Functions to Implement
                    </span>
                  </div>

                  {extractedItems.length > 0 ? (
                    <div className="space-y-3">
                      {extractedItems.map((item, idx) => (
                        <div key={idx} className="p-3.5 rounded-xl bg-surface-raised border border-border/80 space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="w-5 h-5 rounded-full bg-sky-500/10 text-sky-500 font-bold text-xs flex items-center justify-center">
                                {idx + 1}
                              </span>
                              <span className="font-mono text-xs font-bold text-sky-400">
                                {item.name}()
                              </span>
                            </div>
                            <span className="text-xs font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-300">
                              → {item.returnType}
                            </span>
                          </div>

                          <div className="p-2 rounded bg-zinc-950 font-mono text-xs text-zinc-300 overflow-x-auto">
                            def {item.name}({item.params}):
                          </div>

                          {item.docstring && (
                            <p className="text-xs text-zinc-400 leading-relaxed italic">
                              "{item.docstring}"
                            </p>
                          )}

                          {/* Collapsible Hint */}
                          <div className="pt-1">
                            <button
                              onClick={() => setOpenHintIndex(openHintIndex === idx ? null : idx)}
                              className="text-xs text-amber-400 hover:text-amber-300 font-semibold flex items-center gap-1 transition"
                            >
                              <Lightbulb className="w-3.5 h-3.5" />
                              <span>{openHintIndex === idx ? 'Hide Hint' : 'Show Implementation Hint'}</span>
                              <ChevronDown className={`w-3.5 h-3.5 transition-transform ${openHintIndex === idx ? 'rotate-180' : ''}`} />
                            </button>
                            {openHintIndex === idx && (
                              <div className="mt-2 p-2.5 rounded-lg bg-amber-950/20 border border-amber-500/20 text-xs text-amber-200/90 leading-relaxed font-sans animate-in fade-in">
                                Remember to validate all input bounds (e.g. check for negative values and zero before dividing). Round currency or percentages to 2 decimal places with <code className="font-mono text-amber-300">round(val, 2)</code>.
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="p-4 rounded-xl bg-surface-raised border border-border text-xs text-fg-muted space-y-2">
                      <p>Implement the architectural components requested in <code className="text-blue-600 dark:text-sky-300 font-mono font-bold">{activeFile?.filename}</code>.</p>
                      <p>Run tests at any time with <span className="font-mono text-emerald-600 dark:text-emerald-400 font-bold">Ctrl+Enter</span> to inspect current acceptance criteria.</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* TAB 2: ARCHITECTURAL SPECIFICATION */}
            {leftTab === 'guide' && (
              <div className="rounded-2xl bg-surface border border-border/80 p-6 sm:p-7 shadow-sm max-h-[720px] overflow-y-auto space-y-4">
                <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-3">
                  <span className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-500">
                    Architectural Specification
                  </span>
                  <span className="text-xs font-mono text-zinc-400">
                    Live Documentation
                  </span>
                </div>
                <div
                  ref={guideContainerRef}
                  onClick={(e) =>
                    handleMarkdownLinkClick(e, {
                      moduleFolderPath,
                      onNavigateTab: (tab) => setLeftTab(tab as any),
                    })
                  }
                  className="markdown-body text-xs sm:text-sm text-fg leading-relaxed space-y-4"
                  dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(guideMarkdown) }}
                />
              </div>
            )}

            {/* TAB 3: VALIDATION & TEST PLAN */}
            {leftTab === 'tests' && (
              <div className="rounded-2xl bg-surface border border-border/80 p-6 shadow-sm space-y-4 max-h-[720px] overflow-y-auto">
                <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-3">
                  <span className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-500">
                    Test Harness Plan
                  </span>
                  <span className="text-xs font-mono text-emerald-400">
                    Pytest Invariants
                  </span>
                </div>

                <div className="space-y-3 text-xs text-zinc-300 leading-relaxed">
                  <div className="p-3.5 rounded-xl bg-zinc-900/60 border border-zinc-800 space-y-1.5">
                    <span className="font-bold text-sky-400">1. Functional Acceptance Tests</span>
                    <p className="text-zinc-400">
                      Asserts that standard mathematical computations, data transformations, and method calls produce mathematically exact values under standard operating conditions.
                    </p>
                  </div>

                  <div className="p-3.5 rounded-xl bg-zinc-900/60 border border-zinc-800 space-y-1.5">
                    <span className="font-bold text-amber-400">2. Boundary & Error Invariants</span>
                    <p className="text-zinc-400">
                      Asserts that invalid inputs (e.g. negative principals, 0-year terms, division by zero) raise explicit standard library exceptions (<code className="font-mono text-amber-300">ValueError</code>) rather than silently returning corrupted numbers.
                    </p>
                  </div>

                  <div className="p-3.5 rounded-xl bg-zinc-900/60 border border-zinc-800 space-y-1.5">
                    <span className="font-bold text-emerald-400">3. Invariant & Monotonicity Constraints</span>
                    <p className="text-zinc-400">
                      Asserts that iterative processes (e.g. amortization schedules, cache evictions, log appends) satisfy strict invariants: strictly decreasing balances, zero-sum totals, and no data leaks.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Right Column: Multi-File Code Editor & Test Harness */}
        {(viewMode === 'split' || viewMode === 'editor') && (
          <div className={`${viewMode === 'split' ? 'xl:col-span-7' : 'w-full'} space-y-4`}>
            {/* Editor Container */}
            <div className="rounded-2xl bg-surface border border-border shadow-card overflow-hidden flex flex-col">
              {/* In-App Workflow & Shortcut Guide */}
              <div className="flex items-center justify-between px-4 py-2 bg-blue-50/70 dark:bg-blue-950/30 border-b border-blue-200/60 dark:border-blue-900/40 text-xs text-blue-900 dark:text-blue-300">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400 shrink-0" />
                  <span>
                    <strong>In-App Workflow:</strong> 1. Review <strong>Orientation & Guide</strong> on left · 2. Complete the functions below · 3. Click <strong>Run Project Tests</strong>
                  </span>
                </div>
                <span className="font-mono text-[11px] px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300 font-semibold border border-blue-200 dark:border-blue-800/60">
                  Ctrl+Enter to test
                </span>
              </div>

              {/* File Tabs & Controls Header */}
              <div className="flex items-center justify-between px-3 py-2 bg-surface-raised border-b border-border overflow-x-auto gap-2 select-none">
                {/* File Tabs */}
                <div className="flex items-center gap-1 min-w-0">
                  {files.map((file, idx) => (
                    <button
                      key={file.filename}
                      onClick={() => setActiveFileIndex(idx)}
                      className={`px-3 py-1.5 text-xs rounded-lg font-mono flex items-center gap-2 transition-all shrink-0 ${
                        idx === activeFileIndex
                          ? 'bg-surface text-blue-600 dark:text-blue-400 border border-border shadow-xs font-semibold'
                          : 'text-fg-muted hover:text-fg hover:bg-surface/60'
                      }`}
                    >
                      <FileCode className="w-3.5 h-3.5 text-blue-500" />
                      <span>{file.filename}</span>
                      {file.is_modified && (
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-500" title="Modified in workspace" />
                      )}
                      {file.read_only && (
                        <span title="Reference File (Read Only)">
                          <Lock className="w-3 h-3 text-zinc-400" />
                        </span>
                      )}
                    </button>
                  ))}
                </div>

                {/* Right toolbar controls inside editor */}
                <div className="flex items-center gap-2 shrink-0">
                  {/* Font Size Toggle */}
                  <div className="flex items-center bg-surface rounded-lg p-0.5 border border-border text-xs font-mono text-fg-muted">
                    <button
                      onClick={() => setFontSize('sm')}
                      className={`px-1.5 py-0.5 rounded ${fontSize === 'sm' ? 'bg-surface-raised text-fg font-semibold shadow-xs' : ''}`}
                    >
                      sm
                    </button>
                    <button
                      onClick={() => setFontSize('base')}
                      className={`px-1.5 py-0.5 rounded ${fontSize === 'base' ? 'bg-surface-raised text-fg font-semibold shadow-xs' : ''}`}
                    >
                      md
                    </button>
                  </div>

                  {/* Solution Diff Toggle */}
                  {activeFile?.solution_content && (
                    <button
                      onClick={() => {
                        setShowSolutionDiff(!showSolutionDiff);
                        setActiveTerminalTab('diff');
                      }}
                      className={`px-2.5 py-1 text-xs rounded-lg border font-mono flex items-center gap-1.5 transition-all ${
                        showSolutionDiff
                          ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/40 font-semibold'
                          : 'bg-surface text-fg-muted border-border hover:text-fg hover:bg-surface-raised'
                      }`}
                      title="Compare your code with the reference implementation"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>Reference Diff</span>
                    </button>
                  )}
                </div>
              </div>

              {/* Code Editor Body */}
              <div className="relative">
                <textarea
                  ref={textareaRef}
                  value={activeFile?.content || ''}
                  onChange={(e) => handleCodeChange(e.target.value)}
                  onKeyDown={handleKeyDown}
                  readOnly={activeFile?.read_only}
                  spellCheck={false}
                  className={`w-full min-h-[520px] p-5 font-mono bg-surface text-fg dark:bg-[#0c1017] dark:text-[#e6edf3] focus:outline-none focus:ring-0 resize-y leading-relaxed selection:bg-blue-500/30 ${
                    fontSize === 'sm' ? 'text-xs' : 'text-sm'
                  }`}
                  placeholder="# Write your implementation here..."
                />
              </div>

              {/* Editor Footer Status Bar */}
              <div className="flex items-center justify-between px-4 py-2 bg-surface-raised border-t border-border text-xs font-mono text-fg-muted select-none">
                <div className="flex items-center gap-3">
                  <span>Lines: {activeFile?.content.split('\n').length || 0}</span>
                  <span>Chars: {activeFile?.content.length || 0}</span>
                  {activeFile?.is_modified ? (
                    <span className="text-blue-400 font-semibold">● Workspace Modified</span>
                  ) : (
                    <span className="text-zinc-500">Unmodified</span>
                  )}
                </div>
                <div className="flex items-center gap-3 text-zinc-500">
                  <span>Tab: 4 Spaces</span>
                  <span>Python 3.11+</span>
                </div>
              </div>
            </div>

            {/* Validation Dashboard & Test Runner Results Panel */}
            <div className="rounded-2xl bg-surface border border-border/80 shadow-sm overflow-hidden flex flex-col">
              {/* Panel Header & Test Scope Toggle */}
              <div className="flex items-center justify-between px-4 py-2.5 bg-surface-raised border-b border-border flex-wrap gap-2">
                <div className="flex items-center gap-2">
                  {/* Test Breakdown Tab */}
                  <button
                    onClick={() => setActiveTerminalTab('breakdown')}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                      activeTerminalTab === 'breakdown'
                        ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 font-semibold shadow-xs'
                        : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
                    }`}
                  >
                    <CheckSquare className="w-3.5 h-3.5" />
                    <span>Test Breakdown</span>
                    {testResult && testResult.total_tests ? (
                      <span className={`px-1.5 py-0.2 rounded-full text-xs font-bold ${
                        testResult.exit_code === 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                      }`}>
                        {testResult.passed_tests}/{testResult.total_tests}
                      </span>
                    ) : null}
                  </button>

                  {/* Raw Pytest Console Tab */}
                  <button
                    onClick={() => setActiveTerminalTab('tests')}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                      activeTerminalTab === 'tests'
                        ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 font-semibold shadow-xs'
                        : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
                    }`}
                  >
                    <Terminal className="w-3.5 h-3.5" />
                    <span>Pytest Console</span>
                  </button>

                  {/* Solution Diff Tab */}
                  {activeFile?.solution_content && showSolutionDiff && (
                    <button
                      onClick={() => setActiveTerminalTab('diff')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                        activeTerminalTab === 'diff'
                          ? 'bg-amber-600 text-white font-semibold'
                          : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
                      }`}
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>Solution Diff</span>
                    </button>
                  )}
                </div>

                {/* Scope Switcher: Workspace vs Solution */}
                <div className="flex items-center gap-2">
                  <div className="flex items-center rounded-lg bg-zinc-900 p-0.5 border border-zinc-800 text-xs font-mono">
                    <button
                      onClick={() => {
                        setTestScope('workspace');
                        handleRunTests('workspace');
                      }}
                      className={`px-2.5 py-1 rounded text-xs transition ${
                        testScope === 'workspace'
                          ? 'bg-blue-600 text-white font-bold'
                          : 'text-zinc-400 hover:text-zinc-200'
                      }`}
                      title="Test code currently in your editor workspace"
                    >
                      ⚡ Test My Code
                    </button>
                    <button
                      onClick={() => {
                        setTestScope('solution');
                        handleRunTests('solution');
                      }}
                      className={`px-2.5 py-1 rounded text-xs transition ${
                        testScope === 'solution'
                          ? 'bg-purple-600 text-white font-bold'
                          : 'text-zinc-400 hover:text-zinc-200'
                      }`}
                      title="Run tests against verified reference solution"
                    >
                      📖 Test Solution
                    </button>
                  </div>

                  {testResult && (
                    <span className="text-xs font-mono text-zinc-400">
                      {testResult.duration_sec}s
                    </span>
                  )}
                </div>
              </div>

              {/* Progress Summary Bar */}
              {testResult && testResult.total_tests !== undefined && testResult.total_tests > 0 && (
                <div className="px-5 py-3 border-b border-border bg-surface flex flex-col gap-1.5">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <div className="flex items-center gap-2">
                      <span className={`font-bold flex items-center gap-1.5 ${
                        testResult.exit_code === 0 ? 'text-emerald-500' : 'text-rose-500'
                      }`}>
                        {testResult.exit_code === 0 ? (
                          <>
                            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                            <span>Accepted — All Acceptance Criteria Met!</span>
                          </>
                        ) : (
                          <>
                            <XCircle className="w-4 h-4 text-rose-500" />
                            <span>{testResult.passed_tests} of {testResult.total_tests} Tests Passed</span>
                          </>
                        )}
                      </span>
                    </div>
                    <span className="font-bold text-fg">
                      {testResult.percent}% Passing
                    </span>
                  </div>

                  <div className="w-full h-2 bg-zinc-800 rounded-full overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-500 rounded-full ${
                        testResult.exit_code === 0
                          ? 'bg-gradient-to-r from-emerald-500 to-teal-400 shadow-sm shadow-emerald-500/50'
                          : (testResult.percent || 0) > 50
                          ? 'bg-gradient-to-r from-amber-500 to-emerald-500'
                          : 'bg-gradient-to-r from-rose-500 to-amber-500'
                      }`}
                      style={{ width: `${testResult.percent}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Panel Content Body */}
              <div className="p-4 bg-zinc-950 font-mono text-xs text-zinc-300 min-h-[160px] max-h-80 overflow-y-auto">
                {/* 1. GRANULAR TEST BREAKDOWN */}
                {activeTerminalTab === 'breakdown' && (
                  <div>
                    {!testResult && !isRunningTests && (
                      <div className="text-zinc-500 py-8 text-center space-y-2">
                        <Terminal className="w-8 h-8 mx-auto opacity-30 text-sky-400" />
                        <p className="font-sans font-semibold text-zinc-400">Ready to verify implementation.</p>
                        <p className="text-xs text-zinc-600 font-sans">
                          Click <span className="text-emerald-400 font-mono font-bold">Run Project Tests (Ctrl+Enter)</span> to execute automated pytest assertions against your workspace.
                        </p>
                      </div>
                    )}

                    {isRunningTests && (
                      <div className="text-emerald-400 py-8 text-center animate-pulse space-y-2">
                        <Play className="w-6 h-6 mx-auto animate-spin" />
                        <p className="font-sans font-semibold">Running automated test assertions in isolated workspace...</p>
                        <p className="text-xs text-zinc-500 font-mono">Scope: {testScope.toUpperCase()}</p>
                      </div>
                    )}

                    {testResult && testResult.tests && testResult.tests.length > 0 && (
                      <div className="space-y-2">
                        {testResult.tests.map((t, idx) => (
                          <div 
                            key={idx} 
                            onClick={() => t.error && setExpandedTestIdx(expandedTestIdx === idx ? null : idx)}
                            className={`p-3 rounded-xl border transition-all ${
                              t.status === 'passed'
                                ? 'bg-emerald-950/20 border-emerald-500/20 text-emerald-300'
                                : 'bg-rose-950/20 border-rose-500/30 text-rose-300 cursor-pointer hover:bg-rose-950/30'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2.5">
                                {t.status === 'passed' ? (
                                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                                ) : (
                                  <XCircle className="w-4 h-4 text-rose-400 shrink-0" />
                                )}
                                <span className="font-bold text-xs">
                                  {t.name}
                                </span>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                                  t.status === 'passed'
                                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                                    : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                                }`}>
                                  {t.status.toUpperCase()}
                                </span>
                                {t.error && (
                                  <ChevronDown className={`w-3.5 h-3.5 text-zinc-400 transition-transform ${
                                    expandedTestIdx === idx ? 'rotate-180' : ''
                                  }`} />
                                )}
                              </div>
                            </div>

                            {/* Failure Traceback Accordion */}
                            {t.error && expandedTestIdx === idx && (
                              <div className="mt-3 p-3 rounded-lg bg-zinc-950/80 border border-rose-500/30 text-rose-200 text-xs whitespace-pre-wrap font-mono leading-relaxed">
                                {t.error}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}

                    {testResult && (!testResult.tests || testResult.tests.length === 0) && (
                      <pre className="whitespace-pre-wrap leading-relaxed text-zinc-300">
                        {testResult.stdout || testResult.stderr || 'Execution finished with no output.'}
                      </pre>
                    )}
                  </div>
                )}

                {/* 2. RAW PYTEST CONSOLE */}
                {activeTerminalTab === 'tests' && (
                  <pre className="whitespace-pre-wrap leading-relaxed text-zinc-300">
                    {testResult?.stdout || testResult?.stderr || 'No pytest output captured yet. Run tests to see output.'}
                  </pre>
                )}

                {/* 3. REFERENCE SOLUTION DIFF */}
                {activeTerminalTab === 'diff' && activeFile?.solution_content && (
                  <div className="space-y-3">
                    <div className="text-xs text-amber-400 flex items-center gap-1.5 pb-2 border-b border-zinc-800">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Production Reference Solution for {activeFile.filename}:</span>
                    </div>
                    <pre className="text-zinc-300 text-xs whitespace-pre-wrap leading-relaxed">
                      {activeFile.solution_content}
                    </pre>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
