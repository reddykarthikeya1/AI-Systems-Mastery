import React from 'react';
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MasteryChecklist } from '../MasteryChecklist';

const MOCK_CONTENT = `
# Lesson: CUDA Memory Hierarchy

## Core Concepts
Memory spaces in CUDA include global, shared, local, and constant.

## Mastery Checklist
- [ ] Explain the 32-bank conflict mechanism in Shared Memory
- [ ] Calculate effective memory bandwidth with coalesced vs uncoalesced memory access
- [ ] Implement a 2D matrix tile in __shared__ memory with pad padding

## Next Steps
Continue to warp shuffle primitives.
`;

describe('MasteryChecklist Component', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders mastery items extracted from markdown', () => {
    const { container } = render(<MasteryChecklist lessonId="cuda-mem-01" content={MOCK_CONTENT} />);

    expect(screen.getByText('You should now be able to...')).toBeDefined();
    expect(screen.getByText(/Explain the 32-bank conflict mechanism/)).toBeDefined();
    expect(screen.getByText(/Calculate effective memory bandwidth/)).toBeDefined();
    expect(screen.getByText(/Implement a 2D matrix tile/)).toBeDefined();
    expect(container.querySelector('.font-mono')?.textContent).toContain('0/3');
  });

  it('toggles an item on click and updates localStorage and completion counter', () => {
    const { container } = render(<MasteryChecklist lessonId="cuda-mem-01" content={MOCK_CONTENT} />);

    const firstBtn = screen.getByText(/Explain the 32-bank conflict mechanism/).closest('button')!;
    fireEvent.click(firstBtn);

    // Should update counter to 1/3
    expect(container.querySelector('.font-mono')?.textContent).toContain('1/3');

    // Check localStorage
    const saved = localStorage.getItem('mastery_cuda-mem-01');
    expect(saved).toBe(JSON.stringify([0]));

    // Click again to uncheck
    fireEvent.click(firstBtn);
    expect(container.querySelector('.font-mono')?.textContent).toContain('0/3');
  });

  it('loads previously checked items from localStorage', () => {
    localStorage.setItem('mastery_cuda-mem-02', JSON.stringify([1, 2]));

    const { container } = render(<MasteryChecklist lessonId="cuda-mem-02" content={MOCK_CONTENT} />);
    expect(container.querySelector('.font-mono')?.textContent).toContain('2/3');
  });

  it('renders nothing if markdown contains no mastery section', () => {
    const noMastery = '# Simple Doc\nJust regular text with no checklist.';
    const { container } = render(<MasteryChecklist lessonId="doc-01" content={noMastery} />);
    expect(container.firstChild).toBeNull();
  });
});
