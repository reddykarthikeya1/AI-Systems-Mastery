import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, Save, RotateCcw, CheckCircle2, AlertCircle, FileCode, CheckSquare, 
  Eye, Terminal, Clock, Folder, ChevronRight, Lock, Check, Columns, Maximize2, 
  FileText, Sparkles, Sliders, Split, Code2, AlertTriangle, BookOpen
} from 'lucide-react';
import { fetchFileContent, runTestCommand, formatCode } from '../services/api';
import { TestResult } from '../types';
import { renderMarkdownWithMath } from '../services/markdown';
import { soundService } from '../services/sound';

interface ProjectStudioProps {
  moduleFolderPath: string;
  moduleTitle: string;
  courseTitle: string;
  guideMarkdown: string;
  onCompleteProject: () => void;
  isProjectCompleted: boolean;
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

export const ProjectStudio: React.FC<ProjectStudioProps> = ({
  moduleFolderPath,
  moduleTitle,
  courseTitle,
  guideMarkdown,
  onCompleteProject,
  isProjectCompleted,
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
  const [activeTerminalTab, setActiveTerminalTab] = useState<'tests' | 'diff'>('tests');

  const [milestones, setMilestones] = useState<Record<string, boolean>>({
    m1: false,
    m2: false,
    m3: false,
  });

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

  const handleResetStarter = () => {
    if (!activeFile) return;
    soundService.playClick();
    setFiles((prev) =>
      prev.map((f, i) =>
        i === activeFileIndex
          ? { ...f, content: f.starter_content, is_modified: false }
          : f
      )
    );
  };

  const handleRunTests = async () => {
    setIsRunningTests(true);
    setTestResult(null);
    setActiveTerminalTab('tests');
    soundService.playClick();
    try {
      await handleSaveWorkspace();
      const res = await runTestCommand(moduleFolderPath, 'pytest');
      setTestResult(res);
      if (res.exit_code === 0) {
        soundService.playFanfare();
        setMilestones({ m1: true, m2: true, m3: true });
        onCompleteProject();
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
      return;
    }

    const pairs: Record<string, string> = {
      '(': ')',
      '[': ']',
      '{': '}',
      '"': '"',
      "'": "'",
    };

    if (pairs[e.key]) {
      e.preventDefault();
      const closeChar = pairs[e.key];
      const selectedText = content.substring(start, end);
      const newCode = content.substring(0, start) + e.key + selectedText + closeChar + content.substring(end);
      handleCodeChange(newCode);
      setTimeout(() => {
        if (selectedText.length > 0) {
          textarea.selectionStart = start + 1;
          textarea.selectionEnd = end + 1;
        } else {
          textarea.selectionStart = textarea.selectionEnd = start + 1;
        }
      }, 0);
      return;
    }

    if (e.key === 'Backspace' && start === end && start > 0) {
      const prevChar = content[start - 1];
      const nextChar = content[start];
      const matchClose = pairs[prevChar];
      if (matchClose && matchClose === nextChar) {
        e.preventDefault();
        const newCode = content.substring(0, start - 1) + content.substring(start + 1);
        handleCodeChange(newCode);
        setTimeout(() => {
          textarea.selectionStart = textarea.selectionEnd = start - 1;
        }, 0);
        return;
      }
    }
  };

  const toggleMilestone = (key: string) => {
    setMilestones((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  if (loading) {
    return (
      <div className="p-16 text-center text-zinc-500 font-mono text-sm animate-pulse flex flex-col items-center gap-3">
        <Code2 className="w-8 h-8 text-purple-500 animate-spin" />
        <span>Initializing Project Studio Environment & Local Workspaces...</span>
      </div>
    );
  }

  const completedMilestones = Object.values(milestones).filter(Boolean).length;

  return (
    <div className="space-y-4 w-full">
      {/* Studio Master Toolbar */}
      <div className="rounded-2xl p-4 sm:p-5 bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 shadow-md flex flex-col xl:flex-row items-start xl:items-center justify-between gap-4 transition-all">
        <div className="flex items-center gap-3 min-w-0">
          <div className="p-2.5 rounded-xl bg-purple-100 dark:bg-purple-950/60 text-purple-600 dark:text-purple-400 border border-purple-200 dark:border-purple-800/60 shrink-0">
            <Code2 className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="px-2 py-0.5 rounded text-xs font-mono font-bold uppercase tracking-wider bg-purple-500/10 text-purple-600 dark:text-purple-400 border border-purple-500/20">
                In-Browser Project Studio
              </span>
              <span className="text-xs font-mono text-zinc-400 truncate">
                {moduleFolderPath}
              </span>
            </div>
            <h2 className="text-base sm:text-lg font-bold text-zinc-900 dark:text-zinc-100 mt-0.5 truncate">
              {moduleTitle}
            </h2>
          </div>
        </div>

        {/* View Mode & Primary Action Controls */}
        <div className="flex items-center gap-2.5 flex-wrap self-stretch xl:self-auto justify-between xl:justify-end">
          {/* View Mode Toggle: Split | Focus Editor | Focus Spec */}
          <div className="flex items-center rounded-xl bg-zinc-100 dark:bg-zinc-900/80 p-1 border border-zinc-200 dark:border-zinc-800">
            <button
              onClick={() => setViewMode('split')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                viewMode === 'split'
                  ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 shadow-xs'
                  : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
              }`}
              title="Dual-pane split view"
            >
              <Split className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Split</span>
            </button>

            <button
              onClick={() => setViewMode('editor')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                viewMode === 'editor'
                  ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 shadow-xs'
                  : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
              }`}
              title="Full-width code editor focus"
            >
              <Maximize2 className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Code Focused</span>
            </button>

            <button
              onClick={() => setViewMode('spec')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                viewMode === 'spec'
                  ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 shadow-xs'
                  : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
              }`}
              title="Full-width specification reading focus"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Spec Only</span>
            </button>
          </div>

          {/* Save Workspace */}
          <button
            onClick={handleSaveWorkspace}
            disabled={saving}
            className="px-3 py-1.5 rounded-xl text-xs font-medium border border-zinc-300 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1.5"
            title="Persist changes to local workspace"
          >
            {savedSuccess ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Save className="w-3.5 h-3.5" />}
            <span>{savedSuccess ? 'Saved' : 'Save'}</span>
          </button>

          {/* Format Code */}
          <button
            onClick={handleFormatCode}
            disabled={isFormatting || activeFile?.read_only}
            className="px-3 py-1.5 rounded-xl text-xs font-medium border border-zinc-300 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1.5 text-zinc-700 dark:text-zinc-300"
            title="Format Python code with Ruff / PEP8"
          >
            <Sparkles className={`w-3.5 h-3.5 text-amber-500 ${isFormatting ? 'animate-spin' : ''}`} />
            <span>{formatSuccess ? 'Formatted!' : 'Format'}</span>
          </button>

          {/* Reset Starter */}
          <button
            onClick={handleResetStarter}
            className="px-3 py-1.5 rounded-xl text-xs font-medium border border-zinc-300 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1.5 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900"
            title="Reset current file to starter template"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Reset</span>
          </button>

          {/* Run Pytest Harness */}
          <button
            onClick={handleRunTests}
            disabled={isRunningTests}
            className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm transition-all ${
              isRunningTests
                ? 'bg-zinc-400 text-white cursor-not-allowed'
                : 'bg-emerald-600 hover:bg-emerald-500 text-white active:scale-95 ring-2 ring-emerald-500/20'
            }`}
            title="Execute test suite (Ctrl + Enter)"
          >
            <Play className={`w-3.5 h-3.5 ${isRunningTests ? 'animate-spin' : 'fill-current'}`} />
            <span>{isRunningTests ? 'Testing...' : 'Run Tests (Ctrl+Enter)'}</span>
          </button>
        </div>
      </div>

      {/* Main Studio Dual Pane */}
      <div className={`grid gap-6 items-start transition-all ${
        viewMode === 'split' 
          ? 'grid-cols-1 xl:grid-cols-12' 
          : 'grid-cols-1'
      }`}>
        {/* Left Column: Project Specification & Milestones */}
        {(viewMode === 'split' || viewMode === 'spec') && (
          <div className={`${viewMode === 'split' ? 'xl:col-span-5' : 'w-full'} space-y-4`}>
            {/* Milestone Checklist Card */}
            <div className="rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-5 shadow-sm space-y-3.5">
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
                  className="h-full bg-purple-600 rounded-full transition-all duration-300"
                  style={{ width: `${(completedMilestones / 3) * 100}%` }}
                />
              </div>

              <div className="space-y-2.5 pt-1">
                <label
                  onClick={() => toggleMilestone('m1')}
                  className={`flex items-start gap-3 p-3 rounded-xl border transition-all cursor-pointer ${
                    milestones.m1
                      ? 'bg-emerald-50/60 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-800/60'
                      : 'bg-zinc-50/60 dark:bg-zinc-900/40 border-zinc-200/80 dark:border-zinc-800/80 hover:bg-zinc-100/60'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={milestones.m1}
                    onChange={() => {}}
                    className="mt-0.5 rounded border-zinc-300 text-emerald-600 focus:ring-0"
                  />
                  <div className="text-xs">
                    <span className="font-bold text-zinc-900 dark:text-zinc-100">Tier 1: Functional MVP</span>
                    <p className="text-zinc-500 dark:text-zinc-400 mt-0.5 leading-relaxed">
                      Core data structures, interfaces, and primary functionality implemented.
                    </p>
                  </div>
                </label>

                <label
                  onClick={() => toggleMilestone('m2')}
                  className={`flex items-start gap-3 p-3 rounded-xl border transition-all cursor-pointer ${
                    milestones.m2
                      ? 'bg-emerald-50/60 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-800/60'
                      : 'bg-zinc-50/60 dark:bg-zinc-900/40 border-zinc-200/80 dark:border-zinc-800/80 hover:bg-zinc-100/60'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={milestones.m2}
                    onChange={() => {}}
                    className="mt-0.5 rounded border-zinc-300 text-emerald-600 focus:ring-0"
                  />
                  <div className="text-xs">
                    <span className="font-bold text-zinc-900 dark:text-zinc-100">Tier 2: Robustness & Failure Modes</span>
                    <p className="text-zinc-500 dark:text-zinc-400 mt-0.5 leading-relaxed">
                      Input boundary checks, graceful exception handling, and concurrent guards.
                    </p>
                  </div>
                </label>

                <label
                  onClick={() => toggleMilestone('m3')}
                  className={`flex items-start gap-3 p-3 rounded-xl border transition-all cursor-pointer ${
                    milestones.m3
                      ? 'bg-emerald-50/60 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-800/60'
                      : 'bg-zinc-50/60 dark:bg-zinc-900/40 border-zinc-200/80 dark:border-zinc-800/80 hover:bg-zinc-100/60'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={milestones.m3}
                    onChange={() => {}}
                    className="mt-0.5 rounded border-zinc-300 text-emerald-600 focus:ring-0"
                  />
                  <div className="text-xs">
                    <span className="font-bold text-zinc-900 dark:text-zinc-100">Tier 3: Production Scale & Benchmarks</span>
                    <p className="text-zinc-500 dark:text-zinc-400 mt-0.5 leading-relaxed">
                      Zero memory leaks, optimal cache efficiency, and 100% automated pytest suite passing.
                    </p>
                  </div>
                </label>
              </div>
            </div>

            {/* Guide Specification Reader with full KaTeX Math */}
            <div className="rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-6 sm:p-7 shadow-sm max-h-[720px] overflow-y-auto">
              <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-3 mb-5">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-500">
                  Architectural Specification
                </span>
                <span className="text-xs font-mono text-zinc-400">
                  Live Docs
                </span>
              </div>
              <div
                className="markdown-body text-xs sm:text-sm text-zinc-800 dark:text-zinc-200 leading-relaxed space-y-4"
                dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(guideMarkdown) }}
              />
            </div>
          </div>
        )}

        {/* Right Column: Multi-File Code Editor & Test Harness */}
        {(viewMode === 'split' || viewMode === 'editor') && (
          <div className={`${viewMode === 'split' ? 'xl:col-span-7' : 'w-full'} space-y-4`}>
            {/* Editor Container */}
            <div className="rounded-2xl bg-[#0D1117] border border-zinc-800 shadow-xl overflow-hidden flex flex-col">
              {/* File Tabs & Controls Header */}
              <div className="flex items-center justify-between px-3 py-2 bg-[#161B22] border-b border-zinc-800 overflow-x-auto gap-2 select-none">
                {/* File Tabs */}
                <div className="flex items-center gap-1 min-w-0">
                  {files.map((file, idx) => (
                    <button
                      key={file.filename}
                      onClick={() => setActiveFileIndex(idx)}
                      className={`px-3 py-1.5 text-xs rounded-lg font-mono flex items-center gap-2 transition-all shrink-0 ${
                        idx === activeFileIndex
                          ? 'bg-[#0D1117] text-white border border-zinc-700 shadow-sm font-semibold'
                          : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60'
                      }`}
                    >
                      <FileCode className="w-3.5 h-3.5 text-blue-400" />
                      <span>{file.filename}</span>
                      {file.is_modified && (
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-400" title="Modified in workspace" />
                      )}
                      {file.read_only && (
                        <span title="Reference File (Read Only)">
                          <Lock className="w-3 h-3 text-zinc-500" />
                        </span>
                      )}
                    </button>
                  ))}
                </div>

                {/* Right toolbar controls inside editor */}
                <div className="flex items-center gap-2 shrink-0">
                  {/* Font Size Toggle */}
                  <div className="flex items-center bg-zinc-900 rounded-lg p-0.5 border border-zinc-800 text-xs font-mono text-zinc-400">
                    <button
                      onClick={() => setFontSize('sm')}
                      className={`px-1.5 py-0.5 rounded ${fontSize === 'sm' ? 'bg-zinc-800 text-zinc-200' : ''}`}
                    >
                      sm
                    </button>
                    <button
                      onClick={() => setFontSize('base')}
                      className={`px-1.5 py-0.5 rounded ${fontSize === 'base' ? 'bg-zinc-800 text-zinc-200' : ''}`}
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
                          ? 'bg-amber-500/10 text-amber-400 border-amber-500/40'
                          : 'bg-zinc-800/80 text-zinc-400 border-zinc-700 hover:text-zinc-200'
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
                  className={`w-full min-h-[560px] p-5 font-mono bg-[#0D1117] text-zinc-100 focus:outline-none focus:ring-0 resize-y leading-relaxed selection:bg-blue-600/60 ${
                    fontSize === 'sm' ? 'text-xs' : 'text-sm'
                  }`}
                  placeholder="# Write your implementation here..."
                />
              </div>

              {/* Editor Footer Status Bar */}
              <div className="flex items-center justify-between px-4 py-2 bg-[#161B22] border-t border-zinc-800 text-xs font-mono text-zinc-400 select-none">
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
                  <span>UTF-8</span>
                  <span>Python 3.11+</span>
                </div>
              </div>
            </div>

            {/* Test Runner & Reference Diff Output Panel */}
            <div className="rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 shadow-sm overflow-hidden">
              {/* Panel Header Tabs */}
              <div className="flex items-center justify-between px-4 py-2.5 bg-zinc-50 dark:bg-zinc-900/60 border-b border-zinc-200/80 dark:border-zinc-800">
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setActiveTerminalTab('tests')}
                    className={`px-3 py-1 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                      activeTerminalTab === 'tests'
                        ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 font-semibold'
                        : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
                    }`}
                  >
                    <Terminal className="w-3.5 h-3.5" />
                    <span>Test Results</span>
                    {testResult && (
                      <span className={`w-2 h-2 rounded-full ${testResult.exit_code === 0 ? 'bg-emerald-400' : 'bg-rose-400'}`} />
                    )}
                  </button>

                  {activeFile?.solution_content && showSolutionDiff && (
                    <button
                      onClick={() => setActiveTerminalTab('diff')}
                      className={`px-3 py-1 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                        activeTerminalTab === 'diff'
                          ? 'bg-amber-600 text-white font-semibold'
                          : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-200'
                      }`}
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>Reference Solution Diff</span>
                    </button>
                  )}
                </div>

                {testResult && (
                  <div className="flex items-center gap-2 text-xs font-mono">
                    <span className="text-zinc-400">{testResult.duration_sec}s</span>
                    <span className={`px-2 py-0.5 rounded-full font-bold ${
                      testResult.exit_code === 0
                        ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/30'
                        : 'bg-rose-500/10 text-rose-500 border border-rose-500/30'
                    }`}>
                      {testResult.exit_code === 0 ? 'PASSED' : 'FAILED'}
                    </span>
                  </div>
                )}
              </div>

              {/* Panel Content */}
              <div className="p-4 bg-zinc-950 font-mono text-xs text-zinc-300 max-h-72 overflow-y-auto">
                {activeTerminalTab === 'tests' && (
                  <div>
                    {!testResult && !isRunningTests && (
                      <div className="text-zinc-500 py-6 text-center">
                        <Terminal className="w-6 h-6 mx-auto mb-2 opacity-40" />
                        <p>No tests run yet.</p>
                        <p className="text-xs text-zinc-600 mt-0.5">Click "Run Tests (Ctrl+Enter)" above to execute automated pytest verification.</p>
                      </div>
                    )}
                    {isRunningTests && (
                      <div className="text-emerald-400 py-6 text-center animate-pulse">
                        <Play className="w-5 h-5 mx-auto mb-2 animate-spin" />
                        <p>Executing automated pytest test suite against workspace...</p>
                      </div>
                    )}
                    {testResult && (
                      <pre className="whitespace-pre-wrap leading-relaxed">
                        {testResult.stdout || testResult.stderr || 'No console output generated.'}
                      </pre>
                    )}
                  </div>
                )}

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
