import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { AlgorithmTraceScrubber, TraceData } from '../AlgorithmTraceScrubber';

const MOCK_TRACE: TraceData = {
  title: 'Two Pointers Search Verification',
  algorithm: 'Two Sum II (Sorted Array)',
  timeComplexity: 'O(n)',
  spaceComplexity: 'O(1)',
  frames: [
    {
      step: 1,
      description: 'Initialize left=0 and right=3. Sum is 2 + 15 = 17 > 9.',
      array: [2, 7, 11, 15],
      pointers: { left: 0, right: 3 },
      highlights: { 0: 'active', 3: 'active' },
      variables: { left: 0, right: 3, currentSum: 17, target: 9 },
      invariants: 'Sum too large: decrement right pointer',
    },
    {
      step: 2,
      description: 'Decrement right to 2. Sum is 2 + 11 = 13 > 9.',
      array: [2, 7, 11, 15],
      pointers: { left: 0, right: 2 },
      highlights: { 0: 'active', 2: 'active' },
      variables: { left: 0, right: 2, currentSum: 13, target: 9 },
      invariants: 'Sum still too large: decrement right pointer',
    },
    {
      step: 3,
      description: 'Decrement right to 1. Sum is 2 + 7 = 9 === target. Target pair found!',
      array: [2, 7, 11, 15],
      pointers: { left: 0, right: 1 },
      highlights: { 0: 'sorted', 1: 'sorted' },
      variables: { left: 0, right: 1, currentSum: 9, target: 9, found: true },
      invariants: 'Match confirmed: return [1, 2] 1-indexed',
    },
  ],
};

describe('AlgorithmTraceScrubber Component', () => {
  it('renders algorithm name, complexity badges, and initial frame', () => {
    render(<AlgorithmTraceScrubber trace={MOCK_TRACE} />);

    expect(screen.getByText('Two Sum II (Sorted Array)')).toBeDefined();
    expect(screen.getByText(/Time:\s*O\(n\)/)).toBeDefined();
    expect(screen.getByText(/Space:\s*O\(1\)/)).toBeDefined();

    // Check step indicator (Step 1 / 3)
    expect(screen.getByText('Step')).toBeDefined();
    expect(screen.getAllByText('3').length).toBeGreaterThan(0);
    expect(screen.getByText(/Initialize left=0 and right=3/)).toBeDefined();
  });

  it('navigates forward on Next Step click and displays updated state', () => {
    render(<AlgorithmTraceScrubber trace={MOCK_TRACE} />);

    const nextBtn = screen.getByTitle('Next Step');
    fireEvent.click(nextBtn);

    // Frame 2
    expect(screen.getByText(/Decrement right to 2/)).toBeDefined();
    expect(screen.getByText(/Sum still too large/i)).toBeDefined();
  });

  it('navigates to the end on Last Step click and resets on Reset click', () => {
    render(<AlgorithmTraceScrubber trace={MOCK_TRACE} />);

    const lastBtn = screen.getByTitle('Last Step');
    fireEvent.click(lastBtn);

    // Frame 3
    expect(screen.getByText(/Match confirmed/i)).toBeDefined();

    // Reset
    const resetBtn = screen.getByTitle('Reset to Step 1');
    fireEvent.click(resetBtn);

    // Should be back to frame 1
    expect(screen.getByText(/Initialize left=0 and right=3/)).toBeDefined();
  });

  it('allows changing playback speed', () => {
    render(<AlgorithmTraceScrubber trace={MOCK_TRACE} />);

    const speed2x = screen.getByText('2x');
    fireEvent.click(speed2x);
    expect(speed2x.className).toContain('font-bold');
  });
});
