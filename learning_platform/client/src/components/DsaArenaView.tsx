import React, { useState, useEffect, useRef } from 'react';
import {
  Code2,
  CheckCircle2,
  XCircle,
  Play,
  Send,
  RotateCcw,
  Sparkles,
  Maximize2,
  Columns,
  BookOpen,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  Zap,
  Timer,
  Award,
  Lock,
  Unlock,
  AlertTriangle,
  Flame,
  Check
} from 'lucide-react';
import { DsaProblem, DsaRunResult } from '../types';
import { fetchDsaProblems, runDsaTest } from '../services/api';
import { renderMarkdownWithMath } from '../services/markdown';

interface DsaArenaViewProps {
  moduleTitle: string;
  moduleFolderPath: string;
  onBackToLesson?: () => void;
  onCompleteProblem?: (problemId: string) => void;
}

export const DsaArenaView: React.FC<DsaArenaViewProps> = ({
  moduleTitle,
  moduleFolderPath,
  onBackToLesson,
  onCompleteProblem,
}) => {
  const [problems, setProblems] = useState<DsaProblem[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userCode, setUserCode] = useState('');
  const [viewMode, setViewMode] = useState<'split' | 'code' | 'spec'>('split');
  const [fontSize, setFontSize] = useState<'sm' | 'md' | 'lg'>('md');
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [runResult, setRunResult] = useState<DsaRunResult | null>(null);
  const [activeCaseTab, setActiveCaseTab] = useState(0);
  const [showSolutionModal, setShowSolutionModal] = useState(false);
  const [solvedSet, setSolvedSet] = useState<Set<string>>(new Set());
  const [renderedDescription, setRenderedDescription] = useState('');
  const [renderedExplanation, setRenderedExplanation] = useState('');

  const editorRef = useRef<HTMLTextAreaElement>(null);
  const gutterRef = useRef<HTMLDivElement>(null);

  // Load solved problems from localStorage
  useEffect(() => {
    try {
      const savedSolved = localStorage.getItem('academy_dsa_solved');
      if (savedSolved) {
        setSolvedSet(new Set(JSON.parse(savedSolved)));
      }
    } catch {
      // ignore
    }
  }, []);

  // Fetch problems for current module
  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    fetchDsaProblems(moduleFolderPath)
      .then((data) => {
        if (!isMounted) return;
        setProblems(data);
        if (data.length > 0) {
          setCurrentIndex(0);
          loadProblemCode(data[0]);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load DSA problems', err);
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [moduleFolderPath]);

  const currentProblem = problems[currentIndex] || null;

  // Render KaTeX markdown when problem changes
  useEffect(() => {
    if (currentProblem) {
      setRenderedDescription(renderMarkdownWithMath(currentProblem.description));
    }
  }, [currentProblem]);

  // Load or restore code for the given problem
  const loadProblemCode = (prob: DsaProblem) => {
    const saved = localStorage.getItem(`academy_dsa_code_${prob.id}`);
    if (saved) {
      setUserCode(saved);
    } else {
      setUserCode(prob.starter_code);
    }
    setRunResult(null);
    setActiveCaseTab(0);
  };

  const handleSelectProblem = (index: number) => {
    if (index >= 0 && index < problems.length) {
      // Save current code first
      if (currentProblem) {
        localStorage.setItem(`academy_dsa_code_${currentProblem.id}`, userCode);
      }
      setCurrentIndex(index);
      loadProblemCode(problems[index]);
    }
  };

  const handleCodeChange = (newCode: string) => {
    setUserCode(newCode);
    if (currentProblem) {
      localStorage.setItem(`academy_dsa_code_${currentProblem.id}`, newCode);
    }
  };

  const handleResetCode = () => {
    if (currentProblem && window.confirm('Reset code to original starter template?')) {
      setUserCode(currentProblem.starter_code);
      localStorage.removeItem(`academy_dsa_code_${currentProblem.id}`);
      setRunResult(null);
    }
  };

  // Run code against visible testcases
  const handleRunCode = async () => {
    if (!currentProblem || isRunning || isSubmitting) return;
    setIsRunning(true);
    setRunResult(null);

    try {
      const res = await runDsaTest(currentProblem.id, userCode, false);
      setRunResult(res);
      setActiveCaseTab(0);
    } catch (err: any) {
      setRunResult({
        status: 'error',
        all_passed: false,
        total_cases: currentProblem.visible_testcases.length,
        passed_cases: 0,
        duration_ms: 0,
        results: [],
        error: err.message || 'Execution failed',
      });
    } finally {
      setIsRunning(false);
    }
  };

  // Submit code against visible + hidden testcases
  const handleSubmitCode = async () => {
    if (!currentProblem || isRunning || isSubmitting) return;
    setIsSubmitting(true);
    setRunResult(null);

    try {
      const res = await runDsaTest(currentProblem.id, userCode, true);
      setRunResult(res);
      setActiveCaseTab(0);

      if (res.all_passed) {
        const nextSolved = new Set(solvedSet);
        nextSolved.add(currentProblem.id);
        setSolvedSet(nextSolved);
        localStorage.setItem('academy_dsa_solved', JSON.stringify(Array.from(nextSolved)));

        if (res.explanation) {
          setRenderedExplanation(renderMarkdownWithMath(res.explanation));
        }

        if (onCompleteProblem) {
          onCompleteProblem(currentProblem.id);
        }
      }
    } catch (err: any) {
      setRunResult({
        status: 'error',
        all_passed: false,
        total_cases: currentProblem.visible_testcases.length + currentProblem.hidden_testcase_count,
        passed_cases: 0,
        duration_ms: 0,
        results: [],
        error: err.message || 'Submission evaluation failed',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Sync scrolling between line numbers and textarea
  const handleEditorScroll = () => {
    if (editorRef.current && gutterRef.current) {
      gutterRef.current.scrollTop = editorRef.current.scrollTop;
    }
  };

  // Handle Tab key indentation
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const ta = editorRef.current;
      if (!ta) return;
      const start = ta.selectionStart;
      const end = ta.selectionEnd;
      const val = ta.value;
      const newVal = val.substring(0, start) + '    ' + val.substring(end);
      handleCodeChange(newVal);
      setTimeout(() => {
        ta.selectionStart = ta.selectionEnd = start + 4;
      }, 0);
    }
  };

  const lineCount = Math.max(userCode.split('\n').length, 25);
  const lineNumbers = Array.from({ length: lineCount }, (_, i) => i + 1);

  const getDifficultyColor = (diff: string) => {
    switch (diff) {
      case 'Easy':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'Medium':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'Hard':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      default:
        return 'bg-slate-500/10 text-slate-400 border-slate-500/30';
    }
  };

  const fontSizeClass =
    fontSize === 'sm' ? 'text-xs font-mono' : fontSize === 'lg' ? 'text-base font-mono' : 'text-sm font-mono';

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[500px] text-slate-400 space-y-4">
        <div className="w-10 h-10 border-4 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="font-semibold text-slate-300">Loading Algorithmic Challenges...</p>
        <p className="text-xs text-slate-500">Preparing test harness sandbox and edge case suite</p>
      </div>
    );
  }

  if (problems.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center text-slate-400 max-w-xl mx-auto my-12">
        <Code2 className="w-16 h-16 text-slate-600 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-slate-200 mb-2">No LeetCode Problems Configured</h3>
        <p className="text-sm text-slate-400 mb-6">
          There are no interactive challenges registered for this module yet.
        </p>
        {onBackToLesson && (
          <button
            onClick={onBackToLesson}
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-semibold transition"
          >
            Return to Lesson
          </button>
        )}
      </div>
    );
  }

  const isCurrentSolved = currentProblem ? solvedSet.has(currentProblem.id) : false;
  const solvedCount = problems.filter((p) => solvedSet.has(p.id)).length;

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 rounded-2xl border border-slate-800/80 shadow-2xl overflow-hidden min-h-[820px]">
      {/* Top Header Bar */}
      <div className="flex flex-wrap items-center justify-between px-5 py-3.5 bg-slate-900/90 border-b border-slate-800/80 gap-3 backdrop-blur-sm">
        {/* Left Section: Back, Problem Selector, Navigation */}
        <div className="flex items-center gap-3 flex-wrap">
          {onBackToLesson && (
            <button
              onClick={onBackToLesson}
              className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition border border-slate-700/60"
            >
              <ChevronLeft className="w-4 h-4" />
              Lesson
            </button>
          )}

          {/* Problem Selector Dropdown */}
          <div className="relative">
            <select
              value={currentIndex}
              onChange={(e) => handleSelectProblem(Number(e.target.value))}
              className="bg-slate-950 text-slate-200 border border-slate-700/80 rounded-xl px-3 py-1.5 text-xs font-semibold pr-8 focus:outline-none focus:ring-2 focus:ring-amber-500 cursor-pointer shadow-sm"
            >
              {problems.map((p, idx) => (
                <option key={p.id} value={idx}>
                  {solvedSet.has(p.id) ? '✓ ' : ''}
                  {idx + 1}. {p.title} ({p.difficulty})
                </option>
              ))}
            </select>
          </div>

          {/* Prev/Next Buttons */}
          <div className="flex items-center gap-1">
            <button
              disabled={currentIndex === 0}
              onClick={() => handleSelectProblem(currentIndex - 1)}
              className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed text-slate-300 transition"
              title="Previous Problem"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-mono text-slate-400 px-1">
              {currentIndex + 1} / {problems.length}
            </span>
            <button
              disabled={currentIndex === problems.length - 1}
              onClick={() => handleSelectProblem(currentIndex + 1)}
              className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed text-slate-300 transition"
              title="Next Problem"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          {/* Solved Counter Pill */}
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-medium">
            <Award className="w-3.5 h-3.5" />
            <span>
              {solvedCount} of {problems.length} Solved
            </span>
          </div>
        </div>

        {/* Right Section: View Mode, Font Size, Reset */}
        <div className="flex items-center gap-2">
          {/* Font Size controls */}
          <div className="flex items-center bg-slate-950 rounded-lg border border-slate-800 p-0.5 text-xs font-mono text-slate-400">
            <button
              onClick={() => setFontSize('sm')}
              className={`px-2 py-1 rounded ${fontSize === 'sm' ? 'bg-slate-800 text-slate-100 font-bold' : 'hover:text-slate-200'}`}
              title="Small text"
            >
              A-
            </button>
            <button
              onClick={() => setFontSize('md')}
              className={`px-2 py-1 rounded ${fontSize === 'md' ? 'bg-slate-800 text-slate-100 font-bold' : 'hover:text-slate-200'}`}
              title="Normal text"
            >
              A
            </button>
            <button
              onClick={() => setFontSize('lg')}
              className={`px-2 py-1 rounded ${fontSize === 'lg' ? 'bg-slate-800 text-slate-100 font-bold' : 'hover:text-slate-200'}`}
              title="Large text"
            >
              A+
            </button>
          </div>

          {/* View Mode Buttons */}
          <div className="flex items-center bg-slate-950 rounded-lg border border-slate-800 p-0.5 text-xs font-medium text-slate-400">
            <button
              onClick={() => setViewMode('split')}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded ${viewMode === 'split' ? 'bg-amber-500/20 text-amber-400 font-semibold' : 'hover:text-slate-200'}`}
              title="Split View"
            >
              <Columns className="w-3.5 h-3.5" />
              Split
            </button>
            <button
              onClick={() => setViewMode('code')}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded ${viewMode === 'code' ? 'bg-amber-500/20 text-amber-400 font-semibold' : 'hover:text-slate-200'}`}
              title="Code Focused"
            >
              <Maximize2 className="w-3.5 h-3.5" />
              Code
            </button>
            <button
              onClick={() => setViewMode('spec')}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded ${viewMode === 'spec' ? 'bg-amber-500/20 text-amber-400 font-semibold' : 'hover:text-slate-200'}`}
              title="Description Only"
            >
              <BookOpen className="w-3.5 h-3.5" />
              Spec
            </button>
          </div>

          {/* Reset Code button */}
          <button
            onClick={handleResetCode}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition"
            title="Reset code to original starter template"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Dual-Pane Workspace */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Column: Problem Description & Invariants */}
        {(viewMode === 'split' || viewMode === 'spec') && (
          <div
            className={`${viewMode === 'spec' ? 'w-full' : 'w-1/2'} flex flex-col border-r border-slate-800/80 bg-slate-950 overflow-y-auto p-6 space-y-6`}
          >
            {/* Header: Title, Tags, Complexity */}
            <div className="space-y-3 pb-4 border-b border-slate-800">
              <div className="flex items-center justify-between gap-3">
                <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                  {currentProblem?.title}
                  {isCurrentSolved && (
                    <span className="flex items-center gap-1 text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                      <Check className="w-3.5 h-3.5" /> Solved
                    </span>
                  )}
                </h2>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <span
                  className={`text-xs font-bold px-2.5 py-1 rounded-full border ${getDifficultyColor(currentProblem?.difficulty || 'Medium')}`}
                >
                  {currentProblem?.difficulty}
                </span>

                <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
                  {currentProblem?.pattern}
                </span>

                {currentProblem?.time_complexity && (
                  <span className="text-xs font-mono px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                    Time: {currentProblem.time_complexity}
                  </span>
                )}

                {currentProblem?.space_complexity && (
                  <span className="text-xs font-mono px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                    Space: {currentProblem.space_complexity}
                  </span>
                )}
              </div>
            </div>

            {/* Rendered Description (with KaTeX formulas) */}
            <div
              className="prose prose-invert prose-slate max-w-none text-sm text-slate-300 leading-relaxed font-sans"
              dangerouslySetInnerHTML={{ __html: renderedDescription }}
            />

            {/* Visible Testcases Preview */}
            {currentProblem && currentProblem.visible_testcases.length > 0 && (
              <div className="space-y-3 pt-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-amber-400" />
                  Baseline Test Cases ({currentProblem.visible_testcases.length} Visible + {currentProblem.hidden_testcase_count} Hidden)
                </h4>
                <div className="space-y-2.5">
                  {currentProblem.visible_testcases.map((tc, idx) => (
                    <div
                      key={idx}
                      className="bg-slate-900/80 rounded-xl p-3 border border-slate-800/80 font-mono text-xs space-y-1.5"
                    >
                      <div className="text-slate-400 font-semibold">Example {idx + 1}:</div>
                      <div className="text-slate-300">
                        <span className="text-slate-500">Input: </span>
                        {JSON.stringify(tc.input)}
                      </div>
                      <div className="text-amber-400">
                        <span className="text-slate-500">Output: </span>
                        {JSON.stringify(tc.expected)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Unlocked Solution Accordion (if solved or completed) */}
            {isCurrentSolved && (
              <div className="mt-6 p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
                    <Sparkles className="w-4 h-4" />
                    Problem Mastered! Reference Solution Unlocked
                  </div>
                  <button
                    onClick={() => setShowSolutionModal(!showSolutionModal)}
                    className="text-xs px-3 py-1 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 rounded-lg font-semibold transition"
                  >
                    {showSolutionModal ? 'Hide Solution' : 'View Solution'}
                  </button>
                </div>

                {showSolutionModal && (
                  <div className="space-y-3 pt-2">
                    {runResult?.reference_solution && (
                      <pre className="p-4 bg-slate-950 rounded-xl border border-emerald-500/20 font-mono text-xs text-emerald-200 overflow-x-auto">
                        <code>{runResult.reference_solution}</code>
                      </pre>
                    )}
                    {runResult?.explanation && (
                      <div
                        className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-3.5 rounded-xl border border-slate-800"
                        dangerouslySetInnerHTML={{ __html: renderedExplanation }}
                      />
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Right Column: Code Editor & Test Execution Runner */}
        {(viewMode === 'split' || viewMode === 'code') && (
          <div
            className={`${viewMode === 'code' ? 'w-full' : 'w-1/2'} flex flex-col bg-slate-950 overflow-hidden`}
          >
            {/* Editor Workspace */}
            <div className="relative flex-1 flex bg-slate-950 overflow-hidden min-h-[380px]">
              {/* Line Numbers Gutter */}
              <div
                ref={gutterRef}
                className="w-12 py-4 select-none bg-slate-900/50 text-slate-600 font-mono text-xs text-right pr-3 border-r border-slate-800/60 overflow-hidden"
              >
                {lineNumbers.map((num) => (
                  <div key={num} className="leading-6">
                    {num}
                  </div>
                ))}
              </div>

              {/* Textarea Code Editor */}
              <textarea
                ref={editorRef}
                value={userCode}
                onChange={(e) => handleCodeChange(e.target.value)}
                onScroll={handleEditorScroll}
                onKeyDown={handleKeyDown}
                spellCheck={false}
                className={`flex-1 w-full h-full p-4 bg-transparent text-slate-100 ${fontSizeClass} leading-6 resize-none focus:outline-none font-mono selection:bg-amber-500/30 overflow-auto whitespace-pre`}
                placeholder="# Write your Python solution here..."
              />
            </div>

            {/* Bottom Execution Bar */}
            <div className="flex items-center justify-between px-5 py-3 bg-slate-900 border-t border-slate-800 gap-3">
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400 font-mono flex items-center gap-1.5">
                  <Flame className="w-3.5 h-3.5 text-amber-500" />
                  Python 3.11 Sandbox
                </span>
              </div>

              <div className="flex items-center gap-3">
                {/* Run Code Button */}
                <button
                  disabled={isRunning || isSubmitting}
                  onClick={handleRunCode}
                  className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 text-slate-200 text-xs font-bold rounded-xl transition border border-slate-700 shadow-sm"
                >
                  <Play className={`w-3.5 h-3.5 text-amber-400 ${isRunning ? 'animate-spin' : ''}`} />
                  {isRunning ? 'Running...' : 'Run Code'}
                </button>

                {/* Submit Solution Button */}
                <button
                  disabled={isRunning || isSubmitting}
                  onClick={handleSubmitCode}
                  className="flex items-center gap-2 px-5 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 disabled:opacity-50 text-white text-xs font-bold rounded-xl transition shadow-lg shadow-emerald-950/30"
                >
                  <Send className={`w-3.5 h-3.5 ${isSubmitting ? 'animate-bounce' : ''}`} />
                  {isSubmitting ? 'Evaluating Hidden Tests...' : 'Submit Solution'}
                </button>
              </div>
            </div>

            {/* Docked Test Results Panel */}
            {runResult && (
              <div className="border-t border-slate-800 bg-slate-900/90 max-h-[300px] flex flex-col overflow-hidden">
                {/* Result Header Banner */}
                <div
                  className={`flex items-center justify-between px-5 py-2.5 border-b ${
                    runResult.all_passed
                      ? 'bg-emerald-950/40 border-emerald-500/30 text-emerald-400'
                      : 'bg-rose-950/40 border-rose-500/30 text-rose-400'
                  }`}
                >
                  <div className="flex items-center gap-2 font-bold text-sm">
                    {runResult.all_passed ? (
                      <>
                        <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                        <span>Accepted</span>
                      </>
                    ) : (
                      <>
                        <XCircle className="w-5 h-5 text-rose-400" />
                        <span>
                          {runResult.status === 'time_limit_exceeded'
                            ? 'Time Limit Exceeded'
                            : runResult.status === 'runtime_error'
                            ? 'Runtime Error'
                            : 'Wrong Answer'}
                        </span>
                      </>
                    )}
                  </div>

                  <div className="flex items-center gap-4 text-xs font-mono text-slate-300">
                    <span className="flex items-center gap-1 text-slate-400">
                      <Timer className="w-3.5 h-3.5" />
                      {runResult.duration_ms} ms
                    </span>
                    <span>
                      Passed: {runResult.passed_cases} / {runResult.total_cases}
                    </span>
                  </div>
                </div>

                {/* Error Banner if any */}
                {runResult.error && (
                  <div className="p-4 bg-rose-950/20 text-rose-300 font-mono text-xs overflow-auto whitespace-pre-wrap border-b border-rose-500/20">
                    {runResult.error}
                  </div>
                )}

                {/* Test Case Tabs */}
                {runResult.results && runResult.results.length > 0 && (
                  <div className="flex flex-col flex-1 overflow-hidden">
                    <div className="flex items-center gap-1 px-4 py-2 bg-slate-950 border-b border-slate-800/80 overflow-x-auto">
                      {runResult.results.map((r, idx) => (
                        <button
                          key={idx}
                          onClick={() => setActiveCaseTab(idx)}
                          className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-mono font-medium transition ${
                            activeCaseTab === idx
                              ? 'bg-slate-800 text-slate-100 border border-slate-700'
                              : 'text-slate-400 hover:text-slate-200'
                          }`}
                        >
                          <span
                            className={`w-2 h-2 rounded-full ${r.passed ? 'bg-emerald-400' : 'bg-rose-500'}`}
                          />
                          {r.is_hidden ? `Hidden Case ${idx + 1}` : `Case ${idx + 1}`}
                        </button>
                      ))}
                    </div>

                    {/* Selected Test Case Inspection */}
                    {runResult.results[activeCaseTab] && (
                      <div className="p-4 overflow-y-auto space-y-2 font-mono text-xs text-slate-300">
                        {runResult.results[activeCaseTab].is_hidden ? (
                          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
                            <div className="text-slate-400 font-semibold flex items-center gap-2">
                              <ShieldCheck className="w-4 h-4 text-indigo-400" />
                              Hidden Edge Test Case
                            </div>
                            <p className="text-slate-400 text-xs font-sans">
                              Hidden test case inputs and expected outputs are obscured to assess real-world algorithmic invariants.
                            </p>
                            <div className="pt-2">
                              <span className="text-slate-400">Result: </span>
                              <span
                                className={`font-bold ${
                                  runResult.results[activeCaseTab].passed ? 'text-emerald-400' : 'text-rose-400'
                                }`}
                              >
                                {runResult.results[activeCaseTab].passed ? 'Match (Passed)' : 'Mismatch (Failed)'}
                              </span>
                            </div>
                          </div>
                        ) : (
                          <div className="space-y-2">
                            <div>
                              <span className="text-slate-500">Input: </span>
                              <div className="p-2 bg-slate-950 rounded-lg text-slate-200 mt-1">
                                {JSON.stringify(runResult.results[activeCaseTab].input)}
                              </div>
                            </div>
                            <div>
                              <span className="text-slate-500">Expected: </span>
                              <div className="p-2 bg-slate-950 rounded-lg text-amber-400 mt-1">
                                {JSON.stringify(runResult.results[activeCaseTab].expected)}
                              </div>
                            </div>
                            <div>
                              <span className="text-slate-500">Output: </span>
                              <div
                                className={`p-2 bg-slate-950 rounded-lg mt-1 font-bold ${
                                  runResult.results[activeCaseTab].passed ? 'text-emerald-400' : 'text-rose-400'
                                }`}
                              >
                                {JSON.stringify(runResult.results[activeCaseTab].actual)}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
