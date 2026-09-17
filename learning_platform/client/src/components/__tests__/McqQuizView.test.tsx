import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { McqQuizView } from '../McqQuizView';
import * as api from '../../services/api';

vi.mock('canvas-confetti', () => ({
  default: vi.fn(),
}));

vi.mock('../../services/sound', () => ({
  soundService: {
    playClick: vi.fn(),
    playCorrect: vi.fn(),
    playIncorrect: vi.fn(),
    playComplete: vi.fn(),
    playSuccess: vi.fn(),
    playError: vi.fn(),
    playFanfare: vi.fn(),
  },
}));

vi.mock('../../services/api', () => ({
  fetchModuleQuiz: vi.fn(),
}));

const MOCK_QUESTIONS = [
  {
    id: 1,
    tier: 'Recall',
    question: 'What is the time complexity of binary search on N elements?',
    category: 'Complexity',
    options: [
      { text: 'O(log N)', is_correct: true },
      { text: 'O(N)', is_correct: false },
    ],
    explanation: 'Binary search halves the search window on each iteration.',
    lesson_ref: '01_README.md',
  },
  {
    id: 2,
    tier: 'Diagnose',
    question: 'Why does setting left = mid cause an infinite loop when right - left == 1?',
    category: 'Edge Cases',
    options: [
      { text: 'Integer division rounds down keeping mid == left', is_correct: true },
      { text: 'Stack overflow in recursion', is_correct: false },
    ],
    explanation: 'When right = left + 1, mid equals left. Updating left = mid repeats the same window.',
    lesson_ref: '02_FOUNDATIONS.md',
  },
];

describe('McqQuizView Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (api.fetchModuleQuiz as any).mockResolvedValue(MOCK_QUESTIONS);
  });

  it('renders loaded questions with tier badges and categories', async () => {
    render(
      <McqQuizView
        rawContent=""
        lessonTitle="Binary Search Invariants"
        moduleTitle="Module 02 Arrays"
        courseTitle="02 Data Structures"
        lessonId="lesson-02"
        moduleFolderPath="02_Data_Structures_and_Algorithms/Module_02"
        onPassQuiz={vi.fn()}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('What is the time complexity of binary search on N elements?')).toBeDefined();
    });

    expect(screen.getByText('Recall')).toBeDefined();
    expect(screen.getByText('Diagnose')).toBeDefined();
  });

  it('allows checking individual answer and revealing explanation drawer', async () => {
    render(
      <McqQuizView
        rawContent=""
        lessonTitle="Binary Search Invariants"
        moduleTitle="Module 02 Arrays"
        courseTitle="02 Data Structures"
        lessonId="lesson-02"
        moduleFolderPath="02_Data_Structures_and_Algorithms/Module_02"
        onPassQuiz={vi.fn()}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('What is the time complexity of binary search on N elements?')).toBeDefined();
    });

    // Select option
    const correctOpt1 = screen.getByText('O(log N)');
    fireEvent.click(correctOpt1);

    // Click Check Answer
    const checkBtn = screen.getAllByText(/Check Answer/i)[0];
    fireEvent.click(checkBtn);

    // Explanation drawer should now be visible
    expect(screen.getByText(/Technical Explanation & Rationale/i)).toBeDefined();
    expect(screen.getByText(/Binary search halves the search window/i)).toBeDefined();
  });

  it('allows answering all questions and submitting quiz for grading', async () => {
    const onPassQuiz = vi.fn();

    render(
      <McqQuizView
        rawContent=""
        lessonTitle="Binary Search Invariants"
        moduleTitle="Module 02 Arrays"
        courseTitle="02 Data Structures"
        lessonId="lesson-02"
        moduleFolderPath="02_Data_Structures_and_Algorithms/Module_02"
        onPassQuiz={onPassQuiz}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('What is the time complexity of binary search on N elements?')).toBeDefined();
    });

    // Select the correct option for question 1
    const correctOpt1 = screen.getByText('O(log N)');
    fireEvent.click(correctOpt1);

    // Select the correct option for question 2
    const correctOpt2 = screen.getByText('Integer division rounds down keeping mid == left');
    fireEvent.click(correctOpt2);

    // Click Submit Assessment & Grade button
    const submitBtn = screen.getByRole('button', { name: /Submit Assessment & Grade/i });
    fireEvent.click(submitBtn);

    expect(onPassQuiz).toHaveBeenCalledWith(100, 2);
  });
});
