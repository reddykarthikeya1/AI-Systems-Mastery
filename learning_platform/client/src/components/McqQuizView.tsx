import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { CheckCircle2, XCircle, HelpCircle, Award, RotateCcw, ArrowRight, FileText, Check, AlertCircle, Sparkles } from 'lucide-react';
import confetti from 'canvas-confetti';
import { fetchModuleQuiz } from '../services/api';
import { soundService } from '../services/sound';

export interface McqQuestion {
  id: number;
  question: string;
  category?: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  lessonRef?: string;
}

interface McqQuizViewProps {
  rawContent: string;
  lessonTitle: string;
  moduleTitle: string;
  courseTitle: string;
  lessonId: string;
  moduleFolderPath?: string;
  onPassQuiz: (score: number, total: number) => void;
  savedScore?: { score: number; total: number; passed: boolean };
  onQuizMistake?: (question: McqQuestion, chosenOption: string) => void;
}

// Fisher-Yates true random shuffle
function shuffleArray<T>(array: T[]): T[] {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

export const McqQuizView: React.FC<McqQuizViewProps> = ({
  rawContent,
  lessonTitle,
  moduleTitle,
  courseTitle,
  lessonId,
  moduleFolderPath,
  onPassQuiz,
  savedScore,
  onQuizMistake,
}) => {
  const [questions, setQuestions] = useState<McqQuestion[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});
  const [checkedQuestions, setCheckedQuestions] = useState<Record<number, boolean>>({});
  const [isSubmitted, setIsSubmitted] = useState<boolean>(Boolean(savedScore?.passed));
  const [autoCapturedCount, setAutoCapturedCount] = useState<number>(0);
  const [score, setScore] = useState<number>(savedScore?.score || 0);

  // Load and shuffle structured questions from API or local JSON
  const loadQuestions = useCallback(async () => {
    setLoading(true);
    let loadedRaw: any[] = [];

    if (moduleFolderPath) {
      loadedRaw = await fetchModuleQuiz(moduleFolderPath);
    }

    if (loadedRaw && loadedRaw.length > 0) {
      // Process structured questions with true randomized option shuffle
      const formatted: McqQuestion[] = loadedRaw.map((q: any, qIdx: number) => {
        const rawOptions = q.options || [];
        // Extract correct text and distractors
        let correctText = '';
        const distractors: string[] = [];
        rawOptions.forEach((opt: any) => {
          if (opt.is_correct) {
            correctText = opt.text;
          } else {
            distractors.push(opt.text);
          }
        });

        if (!correctText && rawOptions.length > 0) {
          correctText = rawOptions[0].text;
        }

        // Shuffle all 4 options randomly
        const allOpts: { text: string; is_correct: boolean }[] = rawOptions.map((o: any) => ({ text: String(o.text), is_correct: Boolean(o.is_correct) }));
        const shuffledOpts = shuffleArray<{ text: string; is_correct: boolean }>(allOpts);
        const correctIndex = shuffledOpts.findIndex((o) => o.is_correct);

        return {
          id: q.id || qIdx + 1,
          question: q.question,
          category: q.category || 'Systems Architecture',
          options: shuffledOpts.map((o) => o.text),
          correctIndex: correctIndex >= 0 ? correctIndex : 0,
          explanation: q.explanation || 'Refer to the module technical specifications for detailed analysis.',
          lessonRef: q.lesson_ref || '01_README.md',
        };
      });

      setQuestions(formatted);
      setLoading(false);
      return;
    }

    // Fallback: Parse markdown text dynamically if API returned empty
    const lines = rawContent.split('\n');
    let inQuestions = false;
    let inAnswers = false;
    const rawQuestions: { num: number; text: string; category?: string }[] = [];
    const rawAnswers: Record<number, string> = {};

    let currentQNum = 0;
    let currentQText = '';
    let currentCategory = '';

    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed.includes('## Part 1') || trimmed.includes('### Questions') || trimmed.includes('## Conceptual') || trimmed.includes('### Scenario')) {
        inQuestions = true;
        inAnswers = false;
        continue;
      }
      if (trimmed.includes('## Part 2') || trimmed.includes('Answer Key') || trimmed.includes('Staff-Level Solution') || trimmed.includes('**Solution**:')) {
        inQuestions = false;
        inAnswers = true;
        if (currentQNum > 0 && currentQText) {
          rawQuestions.push({ num: currentQNum, text: currentQText.trim(), category: currentCategory });
          currentQNum = 0;
          currentQText = '';
        }
        continue;
      }
      if (trimmed.includes('## Part 3') || trimmed.includes('Practical Coding')) {
        inAnswers = false;
        break;
      }

      if (inQuestions) {
        const qMatch = trimmed.match(/^(\d+)\.\s+(?:\*\*(.*?)\*\*:?\s*)?(.*)/) || trimmed.match(/^###\s+(?:Question|Scenario)\s+(\d+):?\s*(.*)/);
        if (qMatch) {
          if (currentQNum > 0 && currentQText) {
            rawQuestions.push({ num: currentQNum, text: currentQText.trim(), category: currentCategory });
          }
          currentQNum = parseInt(qMatch[1], 10);
          currentCategory = qMatch[2] || 'Core Architecture';
          currentQText = qMatch[3] || qMatch[2] || '';
        } else if (currentQNum > 0 && trimmed && !trimmed.startsWith('---')) {
          currentQText += ' ' + trimmed;
        }
      }

      if (inAnswers) {
        const aMatch = trimmed.match(/####\s+Answer\s+(\d+):?\s*(.*)/) || trimmed.match(/^(\d+)\.\s+(.*)/);
        if (aMatch) {
          const aNum = parseInt(aMatch[1], 10);
          rawAnswers[aNum] = aMatch[2] || '';
          currentQNum = aNum;
        } else if (currentQNum > 0 && trimmed && !trimmed.startsWith('<') && !trimmed.startsWith('---')) {
          rawAnswers[currentQNum] = (rawAnswers[currentQNum] || '') + ' ' + trimmed;
        }
      }
    }

    if (currentQNum > 0 && currentQText && inQuestions) {
      rawQuestions.push({ num: currentQNum, text: currentQText.trim(), category: currentCategory });
    }

    const domainDistractors = [
      'The operation creates a race condition that triggers unhandled deadlock under concurrent execution.',
      'Memory bus bandwidth saturation forces thread execution to throttle below throughput SLAs.',
      'A partial write causes unrecoverable state divergence without an atomic write-ahead log replay barrier.',
      'The algorithmic complexity degenerates to linear scan because index prefix constraints are violated.',
      'Unbounded queue accumulation triggers aggressive backpressure shedding and dropped packets.',
    ];

    const fallbackList: McqQuestion[] = rawQuestions.map((q, i) => {
      const ansText = rawAnswers[q.num] || rawAnswers[i + 1] || 'Verified reference answer in curriculum specs.';
      const cleanAns = ansText.replace(/^[\s*#-]+/, '').slice(0, 180).trim();
      const correctOpt = cleanAns.length > 20 ? cleanAns : `${cleanAns} (Verified systems invariant)`;

      const opts = [
        { text: correctOpt, is_correct: true },
        { text: domainDistractors[i % domainDistractors.length], is_correct: false },
        { text: domainDistractors[(i + 1) % domainDistractors.length], is_correct: false },
        { text: domainDistractors[(i + 2) % domainDistractors.length], is_correct: false },
      ];
      const shuffled = shuffleArray(opts);
      const cIdx = shuffled.findIndex((o) => o.is_correct);

      return {
        id: q.num,
        question: q.text,
        category: q.category,
        options: shuffled.map((o) => o.text),
        correctIndex: cIdx >= 0 ? cIdx : 0,
        explanation: ansText,
        lessonRef: '01_README.md',
      };
    });

    setQuestions(fallbackList);
    setLoading(false);
  }, [moduleFolderPath, rawContent]);

  useEffect(() => {
    loadQuestions();
  }, [loadQuestions]);

  const handleSelectOption = (qId: number, optIdx: number) => {
    if (isSubmitted) return;
    soundService.playClick();
    setSelectedAnswers((prev) => ({ ...prev, [qId]: optIdx }));
  };

  const handleCheckQuestion = (qId: number) => {
    setCheckedQuestions((prev) => ({ ...prev, [qId]: true }));
    const q = questions.find((item) => item.id === qId);
    if (!q) return;

    const chosenIdx = selectedAnswers[qId];
    if (chosenIdx === undefined) return;

    if (chosenIdx === q.correctIndex) {
      soundService.playSuccess();
    } else {
      soundService.playError();
      if (onQuizMistake) {
        onQuizMistake(q, q.options[chosenIdx]);
        setAutoCapturedCount((c) => c + 1);
      }
    }
  };

  const handleSubmitQuiz = () => {
    let correctCount = 0;
    let mistakes = 0;
    questions.forEach((q) => {
      if (selectedAnswers[q.id] === q.correctIndex) {
        correctCount++;
      } else {
        mistakes++;
        if (onQuizMistake && selectedAnswers[q.id] !== undefined) {
          onQuizMistake(q, q.options[selectedAnswers[q.id]]);
        }
      }
    });

    const total = questions.length;
    const finalScore = total > 0 ? Math.round((correctCount / total) * 100) : 0;
    setScore(finalScore);
    setIsSubmitted(true);
    if (mistakes > 0) {
      setAutoCapturedCount(mistakes);
    }

    if (finalScore >= 70) {
      soundService.playFanfare();
      confetti({
        particleCount: 120,
        spread: 70,
        origin: { y: 0.6 },
      });
      onPassQuiz(finalScore, total);
    } else {
      soundService.playError();
    }
  };

  const handleRetake = () => {
    soundService.playClick();
    setSelectedAnswers({});
    setCheckedQuestions({});
    setIsSubmitted(false);
    setAutoCapturedCount(0);
    loadQuestions(); // re-shuffles all options!
  };

  const answeredCount = Object.keys(selectedAnswers).length;
  const isAllAnswered = questions.length > 0 && answeredCount === questions.length;

  if (loading) {
    return (
      <div className="rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-12 text-center space-y-3">
        <div className="w-8 h-8 mx-auto border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-xs font-mono text-zinc-500">Loading structured module assessment & distractor bank...</p>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="rounded-2xl bg-white dark:bg-[#111622] border border-zinc-200/80 dark:border-zinc-800/80 p-8 text-center space-y-4">
        <div className="w-12 h-12 mx-auto rounded-full bg-amber-100 dark:bg-amber-950/60 text-amber-600 flex items-center justify-center">
          <HelpCircle className="w-6 h-6" />
        </div>
        <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-100">No Assessment Questions Found</h3>
        <p className="text-xs text-zinc-500 max-w-md mx-auto">
          This lesson does not currently have interactive quiz questions configured.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-transparent border border-amber-500/20 p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-500/30 flex items-center gap-1">
              <Award className="w-3 h-3" /> Technical Assessment
            </span>
            <span className="text-xs font-mono text-zinc-400">{moduleTitle}</span>
          </div>
          <h2 className="text-lg font-bold text-zinc-900 dark:text-zinc-100">
            {lessonTitle}
          </h2>
          <p className="text-xs text-zinc-500">
            Pass with <strong className="text-zinc-700 dark:text-zinc-300">70% or higher</strong> to clear this mastery criterion. Options are dynamically shuffled per attempt.
          </p>
        </div>

        {/* Score Pill & Retake */}
        <div className="flex items-center gap-3">
          {isSubmitted && (
            <div className={`px-4 py-2 rounded-xl border flex items-center gap-2 font-mono text-xs ${
              score >= 70
                ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-500/40 text-emerald-600 dark:text-emerald-400'
                : 'bg-rose-50 dark:bg-rose-950/40 border-rose-500/40 text-rose-600 dark:text-rose-400'
            }`}>
              {score >= 70 ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
              <span className="font-bold">{score}% ({score >= 70 ? 'PASSED' : 'RETRY'})</span>
            </div>
          )}

          {isSubmitted && (
            <button
              onClick={handleRetake}
              className="px-3.5 py-2 rounded-xl text-xs font-medium border border-zinc-200/80 dark:border-zinc-800 bg-white dark:bg-zinc-900 hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-700 dark:text-zinc-300 transition-colors flex items-center gap-1.5 shadow-sm"
            >
              <RotateCcw className="w-3.5 h-3.5" /> Retake
            </button>
          )}
        </div>
      </div>

      {/* Auto-captured SRS Mistake Notification */}
      {autoCapturedCount > 0 && (
        <div className="rounded-xl bg-gradient-to-r from-amber-500/15 via-orange-500/10 to-amber-500/5 border border-amber-500/30 p-4 flex items-center justify-between gap-3 shadow-sm animate-in fade-in duration-300">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-amber-500/20 text-amber-600 dark:text-amber-400">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <p className="text-xs font-bold text-zinc-900 dark:text-zinc-100">
                Active Recall Loop: {autoCapturedCount} Missed Concept{autoCapturedCount > 1 ? 's' : ''} Saved
              </p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400">
                These questions have been automatically added to your SuperMemo SM-2 deck for scheduled spaced review.
              </p>
            </div>
          </div>
          <span className="text-xs font-mono font-bold px-2 py-1 rounded bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-500/30">
            SRS Active
          </span>
        </div>
      )}

      {/* Questions List */}
      <div className="space-y-6">
        {questions.map((q, qIndex) => {
          const isAnswered = selectedAnswers[q.id] !== undefined;
          const isChecked = checkedQuestions[q.id] || isSubmitted;
          const chosenIdx = selectedAnswers[q.id];
          const isCorrect = chosenIdx === q.correctIndex;

          return (
            <div
              key={q.id}
              className={`rounded-2xl bg-white dark:bg-[#111622] border transition-all p-6 space-y-4 shadow-sm ${
                isChecked
                  ? isCorrect
                    ? 'border-emerald-500/40 bg-emerald-50/20 dark:bg-emerald-950/10'
                    : 'border-rose-500/40 bg-rose-50/20 dark:bg-rose-950/10'
                  : 'border-zinc-200/80 dark:border-zinc-800/80 hover:border-zinc-300 dark:hover:border-zinc-700'
              }`}
            >
              {/* Question Header */}
              <div className="flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700">
                      Question {qIndex + 1} of {questions.length}
                    </span>
                    {q.category && (
                      <span className="text-xs font-mono text-amber-600 dark:text-amber-400">
                        {q.category}
                      </span>
                    )}
                  </div>
                  <h3 className="text-sm sm:text-base font-semibold text-zinc-900 dark:text-zinc-100 leading-relaxed pt-1">
                    {q.question}
                  </h3>
                </div>

                {isChecked && (
                  <div className="shrink-0 pt-1">
                    {isCorrect ? (
                      <span className="inline-flex items-center gap-1 text-xs font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-950/60 px-2 py-1 rounded-lg border border-emerald-500/30">
                        <Check className="w-3.5 h-3.5" /> Correct
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-xs font-bold text-rose-600 dark:text-rose-400 bg-rose-100 dark:bg-rose-950/60 px-2 py-1 rounded-lg border border-rose-500/30">
                        <XCircle className="w-3.5 h-3.5" /> Missed
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Options */}
              <div className="grid grid-cols-1 gap-2.5 pt-1">
                {q.options.map((opt, optIdx) => {
                  const isSelected = chosenIdx === optIdx;
                  const isThisCorrect = optIdx === q.correctIndex;
                  const letter = String.fromCharCode(65 + optIdx);

                  let optClass = 'border-zinc-200 dark:border-zinc-800 bg-zinc-50/70 dark:bg-zinc-900/60 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 text-zinc-800 dark:text-zinc-200';

                  if (isChecked) {
                    if (isThisCorrect) {
                      optClass = 'border-emerald-500 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 font-medium';
                    } else if (isSelected && !isThisCorrect) {
                      optClass = 'border-rose-500 bg-rose-500/10 text-rose-700 dark:text-rose-300 line-through';
                    } else {
                      optClass = 'border-zinc-200/50 dark:border-zinc-800/50 opacity-50 text-zinc-500';
                    }
                  } else if (isSelected) {
                    optClass = 'border-blue-500 bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 font-medium shadow-sm';
                  }

                  return (
                    <button
                      key={optIdx}
                      disabled={isSubmitted}
                      onClick={() => handleSelectOption(q.id, optIdx)}
                      className={`w-full text-left p-3 rounded-xl border text-xs sm:text-sm flex items-start gap-3 transition-all ${optClass}`}
                    >
                      <span className={`w-6 h-6 rounded-lg flex items-center justify-center font-mono text-xs font-bold shrink-0 mt-0.5 border ${
                        isChecked && isThisCorrect
                          ? 'bg-emerald-500 text-white border-emerald-600'
                          : isChecked && isSelected && !isThisCorrect
                          ? 'bg-rose-500 text-white border-rose-600'
                          : isSelected
                          ? 'bg-blue-600 text-white border-blue-700'
                          : 'bg-white dark:bg-zinc-800 border-zinc-300 dark:border-zinc-700 text-zinc-500'
                      }`}>
                        {letter}
                      </span>
                      <span className="leading-relaxed flex-1 pt-0.5">{opt}</span>
                    </button>
                  );
                })}
              </div>

              {/* Instant Check Button (Before Submit) */}
              {!isSubmitted && !checkedQuestions[q.id] && isAnswered && (
                <div className="pt-2 flex justify-end">
                  <button
                    onClick={() => handleCheckQuestion(q.id)}
                    className="px-3.5 py-1.5 rounded-lg text-xs font-mono font-medium border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition text-zinc-600 dark:text-zinc-300 flex items-center gap-1.5"
                  >
                    Check Answer
                  </button>
                </div>
              )}

              {/* Detailed Explanation Drawer */}
              {isChecked && (
                <div className="pt-3 border-t border-zinc-200/60 dark:border-zinc-800/60 space-y-2 text-xs">
                  <div className="flex items-center gap-1.5 font-bold font-mono text-zinc-700 dark:text-zinc-300">
                    <FileText className="w-3.5 h-3.5 text-blue-500" />
                    <span>Technical Explanation & Rationale:</span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-zinc-100/70 dark:bg-zinc-900/90 text-zinc-700 dark:text-zinc-300 leading-relaxed font-normal whitespace-pre-wrap">
                    {q.explanation}
                  </div>
                  {q.lessonRef && (
                    <div className="text-zinc-500 text-xs font-mono pt-1">
                      📖 Reference: <span className="underline">{q.lessonRef}</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Bottom Submit Dock */}
      {!isSubmitted && (
        <div className="sticky bottom-4 z-20 rounded-2xl bg-white/95 dark:bg-[#111622]/95 backdrop-blur-md p-4 border border-zinc-200/90 dark:border-zinc-800 shadow-xl flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-zinc-500">
              Answered {answeredCount} of {questions.length} questions
            </span>
            <div className="w-32 h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-600 transition-all duration-300"
                style={{ width: `${(answeredCount / questions.length) * 100}%` }}
              />
            </div>
          </div>

          <button
            disabled={!isAllAnswered}
            onClick={handleSubmitQuiz}
            className="w-full sm:w-auto px-6 py-2.5 rounded-xl font-bold text-xs bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:pointer-events-none text-white transition-all shadow-md flex items-center justify-center gap-2"
          >
            <span>Submit Assessment & Grade</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
};
