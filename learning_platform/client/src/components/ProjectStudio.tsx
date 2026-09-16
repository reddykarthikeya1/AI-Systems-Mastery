import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, Save, RotateCcw, CheckCircle2, AlertCircle, FileCode, CheckSquare, 
  Eye, Terminal, Clock, Folder, ChevronRight, Lock, Check 
} from 'lucide-react';
import { fetchFileContent, runTestCommand } from '../services/api';
import { TestResult } from '../types';
import { marked } from 'marked';

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
  const [milestones, setMilestones] = useState<Record<string, boolean>>({
    m1: false,
    m2: false,
    m3: false,
  });

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Load project files from API
  useEffect(() => {
    setLoading(true);
    fetch(`/api/project-files?module_path=${encodeURIComponent(moduleFolderPath)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.files && data.files.length > 0) {
          setFiles(data.files);
        } else {
          // Fallback: create default solution stub
          setFiles([
            {
              filename: 'solution.py',
              content: '# In-Browser Project Studio\n# Implement your project solution here...\n\ndef solution():\n    pass\n',
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
    try {
      // Auto-save first
      await handleSaveWorkspace();
      const res = await runTestCommand(moduleFolderPath, 'pytest');
      setTestResult(res);
      if (res.exit_code === 0) {
        setMilestones({ m1: true, m2: true, m3: true });
        onCompleteProject();
      }
    } catch (err: any) {
      setTestResult({
        exit_code: -1,
        stdout: '',
        stderr: err.message || 'Project tests failed to run',
        duration_sec: 0,
        status: 'error',
      });
    } finally {
      setIsRunningTests(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRunTests();
    } else if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (!textarea || activeFile?.read_only) return;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newCode = activeFile.content.substring(0, start) + '    ' + activeFile.content.substring(end);
      handleCodeChange(newCode);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 4;
      }, 0);
    }
  };

  const toggleMilestone = (key: string) => {
    setMilestones((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const renderGuideHtml = (raw: string) => {
    try {
      return marked.parse(raw, { async: false }) as string;
    } catch {
      return raw;
    }
  };

  if (loading) {
    return (
      <div className="p-12 text-center text-zinc-500 font-mono text-xs">
        Loading In-Browser Project Studio workspace...
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Studio Header Bar */}
      <div className="rounded-xl p-4 bg-zinc-50 dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold uppercase tracking-wider bg-indigo-500/10 text-indigo-500 border border-indigo-500/20">
              Guided Project Studio
            </span>
            <span className="text-[11px] font-mono text-zinc-500 truncate max-w-sm">
              {moduleFolderPath}
            </span>
          </div>
          <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-100 mt-1">
            {moduleTitle}: Hands-On Implementation
          </h2>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleSaveWorkspace}
            disabled={saving}
            className="px-3 py-1.5 rounded-lg text-xs font-medium border border-zinc-300 dark:border-zinc-700 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition flex items-center gap-1.5"
            title="Save changes to your local project workspace"
          >
            {savedSuccess ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Save className="w-3.5 h-3.5" />}
            <span>{savedSuccess ? 'Saved' : 'Save Workspace'}</span>
          </button>

          <button
            onClick={handleResetStarter}
            className="px-3 py-1.5 rounded-lg text-xs font-medium border border-zinc-300 dark:border-zinc-700 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition flex items-center gap-1.5 text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
            title="Reset active file to clean starter template"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Starter</span>
          </button>

          <button
            onClick={handleRunTests}
            disabled={isRunningTests}
            className={`px-4 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition ${
              isRunningTests
                ? 'bg-zinc-400 text-white cursor-not-allowed'
                : 'bg-emerald-600 hover:bg-emerald-500 text-white active:scale-95'
            }`}
          >
            <Play className={`w-3.5 h-3.5 ${isRunningTests ? 'animate-spin' : 'fill-current'}`} />
            <span>{isRunningTests ? 'Testing...' : 'Run Project Tests'}</span>
          </button>
        </div>
      </div>

      {/* Main Studio Dual Pane: Left Guide + Right Code Editor */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column (5 Cols): Project Guide & Milestone Checkpoints */}
        <div className="lg:col-span-5 space-y-4">
          {/* Milestone Checklist Card */}
          <div className="rounded-xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-4 shadow-sm space-y-3">
            <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800 pb-2">
              <span className="text-[11px] font-mono font-semibold uppercase tracking-wider text-zinc-400">
                Milestone Verification
              </span>
              <span className="text-[10px] font-mono text-zinc-400">
                {Object.values(milestones).filter(Boolean).length}/3 Completed
              </span>
            </div>

            <div className="space-y-2">
              <label
                onClick={() => toggleMilestone('m1')}
                className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-800/50 cursor-pointer text-xs"
              >
                <input
                  type="checkbox"
                  checked={milestones.m1}
                  onChange={() => {}}
                  className="mt-0.5 rounded border-zinc-300 text-emerald-600 focus:ring-0"
                />
                <div>
                  <span className="font-semibold text-zinc-800 dark:text-zinc-200">Tier 1: Functional MVP</span>
                  <p className="text-[11px] text-zinc-500">Core data structures and required public methods implemented.</p>
                </div>
              </label>

              <label
                onClick={() => toggleMilestone('m2')}
                className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-800/50 cursor-pointer text-xs"
              >
                <input
                  type="checkbox"
                  checked={milestones.m2}
                  onChange={() => {}}
                  className="mt-0.5 rounded border-zinc-300 text-emerald-600 focus:ring-0"
                />
                <div>
                  <span className="font-semibold text-zinc-800 dark:text-zinc-200">Tier 2: Robustness & Error Handling</span>
                  <p className="text-[11px] text-zinc-500">Input validation, boundary tests, and concurrency safeguards.</p>
                </div>
              </label>

              <label
                onClick={() => toggleMilestone('m3')}
                className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-800/50 cursor-pointer text-xs"
              >
                <input
                  type="checkbox"
                  checked={milestones.m3}
                  onChange={() => {}}
                  className="mt-0.5 rounded border-zinc-300 text-emerald-600 focus:ring-0"
                />
                <div>
                  <span className="font-semibold text-zinc-800 dark:text-zinc-200">Tier 3: Scale & Performance</span>
                  <p className="text-[11px] text-zinc-500">Memory efficiency, throughput benchmarks, and all tests passing.</p>
                </div>
              </label>
            </div>
          </div>

          {/* Guide Documentation Accordion */}
          <div className="rounded-xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-6 shadow-sm max-h-[600px] overflow-y-auto">
            <div className="text-xs font-mono font-semibold uppercase tracking-wider text-zinc-400 border-b border-zinc-100 dark:border-zinc-800 pb-2 mb-4">
              Project Specification
            </div>
            <div
              className="markdown-body text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed"
              dangerouslySetInnerHTML={{ __html: renderGuideHtml(guideMarkdown) }}
            />
          </div>
        </div>

        {/* Right Column (7 Cols): Multi-File Editor & Terminal */}
        <div className="lg:col-span-7 space-y-4">
          {/* File Tabs & Solution Diff Toggle */}
          <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-2">
            <div className="flex items-center gap-1 overflow-x-auto">
              {files.map((file, idx) => (
                <button
                  key={idx}
                  onClick={() => { setActiveFileIndex(idx); setShowSolutionDiff(false); }}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono flex items-center gap-1.5 transition ${
                    activeFileIndex === idx
                      ? 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 font-semibold shadow-sm'
                      : 'bg-zinc-100 dark:bg-zinc-800/80 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
                  }`}
                >
                  <FileCode className="w-3.5 h-3.5" />
                  <span>{file.filename}</span>
                  {file.is_modified && <span className="w-1.5 h-1.5 rounded-full bg-blue-400" title="Modified" />}
                  {file.read_only && (
                    <span title="Reference Only">
                      <Lock className="w-3 h-3 text-zinc-400" />
                    </span>
                  )}
                </button>
              ))}
            </div>

            {activeFile?.solution_content && (
              <button
                onClick={() => setShowSolutionDiff(!showSolutionDiff)}
                className={`px-2.5 py-1 text-xs rounded-md border font-medium flex items-center gap-1 transition ${
                  showSolutionDiff
                    ? 'bg-amber-500/10 text-amber-500 border-amber-500/30'
                    : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 border-zinc-200 dark:border-zinc-700'
                }`}
                title="Compare with reference implementation"
              >
                <Eye className="w-3.5 h-3.5" />
                <span>{showSolutionDiff ? 'Hide Solution' : 'Peek Solution'}</span>
              </button>
            )}
          </div>

          {/* Code Editor Surface */}
          <div className="rounded-xl overflow-hidden border border-zinc-200 dark:border-zinc-800 bg-[#0D1117] shadow-xl">
            <div className="px-4 py-2 bg-[#161B22] border-b border-zinc-800 flex items-center justify-between text-[11px] font-mono text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-300 font-semibold">
                <FileCode className="w-3.5 h-3.5 text-blue-400" />
                <span>{activeFile?.filename}</span>
                {activeFile?.read_only && <span className="text-zinc-500 text-[10px] font-normal">(Read-Only Test Suite)</span>}
              </span>
              <span>Ctrl + Enter to test</span>
            </div>

            {showSolutionDiff ? (
              <div className="grid grid-cols-2 divide-x divide-zinc-800 h-[420px] overflow-hidden text-xs font-mono">
                <div className="p-3 bg-[#0D1117] overflow-y-auto">
                  <div className="text-[10px] text-zinc-500 uppercase tracking-wider pb-2 border-b border-zinc-800 mb-2">Your Code</div>
                  <pre className="text-zinc-300 whitespace-pre-wrap">{activeFile?.content}</pre>
                </div>
                <div className="p-3 bg-[#0E1524] overflow-y-auto">
                  <div className="text-[10px] text-emerald-400 uppercase tracking-wider pb-2 border-b border-zinc-800 mb-2">Reference Solution</div>
                  <pre className="text-emerald-300/90 whitespace-pre-wrap">{activeFile?.solution_content}</pre>
                </div>
              </div>
            ) : (
              <div className="relative h-[420px]">
                <textarea
                  ref={textareaRef}
                  value={activeFile?.content || ''}
                  onChange={(e) => handleCodeChange(e.target.value)}
                  onKeyDown={handleKeyDown}
                  readOnly={activeFile?.read_only}
                  spellCheck={false}
                  placeholder="# Write your project implementation code here..."
                  className="w-full h-full p-4 font-mono text-xs text-[#E6EDF3] bg-transparent resize-none focus:outline-none leading-relaxed selection:bg-blue-500/30"
                />
              </div>
            )}
          </div>

          {/* Test Execution Output Terminal */}
          <div className="rounded-xl overflow-hidden border border-zinc-800 bg-[#0A0D12] text-xs font-mono">
            <div className="px-3.5 py-1.5 bg-[#161B22] border-b border-zinc-800 flex items-center justify-between text-[11px] text-zinc-400">
              <span className="font-semibold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5 text-emerald-400" />
                <span>Automated Pytest Harness</span>
              </span>
              {testResult && (
                <span className="flex items-center gap-2">
                  <span className="text-zinc-500">{testResult.duration_sec}s</span>
                  <span
                    className={`px-2 py-0.5 rounded-full font-medium ${
                      testResult.status === 'passed'
                        ? 'bg-emerald-500/10 text-emerald-400'
                        : 'bg-red-500/10 text-red-400'
                    }`}
                  >
                    {testResult.status === 'passed' ? 'ALL TESTS PASSED' : 'TESTS FAILED'}
                  </span>
                </span>
              )}
            </div>

            <div className="p-3.5 max-h-48 overflow-y-auto select-text leading-relaxed space-y-2">
              {!testResult && !isRunningTests && (
                <p className="text-zinc-600 italic">
                  Press "Run Project Tests" or Ctrl+Enter to execute the automated verification suite.
                </p>
              )}

              {isRunningTests && (
                <div className="flex items-center gap-2 text-emerald-400">
                  <span className="animate-spin text-sm">◷</span> Running pytest verification suite on project code...
                </div>
              )}

              {testResult && (
                <>
                  {testResult.stdout && (
                    <pre className="text-emerald-400 whitespace-pre-wrap break-all font-mono">
                      {testResult.stdout}
                    </pre>
                  )}
                  {testResult.stderr && (
                    <pre className="text-red-400 whitespace-pre-wrap break-all font-mono">
                      {testResult.stderr}
                    </pre>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
