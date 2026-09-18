import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ProjectStudio } from '../ProjectStudio';

describe('ProjectStudio Component', () => {
  beforeEach(() => {
    global.fetch = vi.fn().mockImplementation((url: string) => {
      if (url.includes('project-files')) {
        return Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              module_path: '01_Advanced_Python/Module_01_Python_Fundamentals',
              files: [
                {
                  filename: 'calculator.py',
                  content: 'def calculate_compound_interest(principal, annual_rate, years):\n    pass\n',
                  starter_content: 'def calculate_compound_interest(principal, annual_rate, years):\n    pass\n',
                  solution_content: 'def calculate_compound_interest(principal, annual_rate, years):\n    return 100.0, 10.0\n',
                  is_modified: false,
                },
              ],
            }),
        });
      }
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ status: 'ok' }),
      });
    });
  });

  it('renders guided roadmap tabs and extracted directives', async () => {
    render(
      <ProjectStudio
        moduleFolderPath="01_Advanced_Python/Module_01_Python_Fundamentals"
        moduleTitle="Financial Calculator System"
        courseTitle="Advanced Python"
        guideMarkdown="# Project Guide\n\nImplement compound interest."
        onCompleteProject={() => {}}
        isProjectCompleted={false}
      />
    );

    expect(await screen.findByText('Financial Calculator System')).toBeDefined();
    expect(screen.getByText('Orientation')).toBeDefined();
    expect(screen.getByText('Milestones')).toBeDefined();
    expect(screen.getByText('Project Guide')).toBeDefined();
    expect(screen.getByText('Test Plan')).toBeDefined();

    // Verify extracted function directive under Milestones tab
    const milestonesTab = screen.getByText('Milestones');
    fireEvent.click(milestonesTab);
    expect(await screen.findByText('Step-by-Step Directives')).toBeDefined();
    const directives = await screen.findAllByText(/calculate_compound_interest/);
    expect(directives.length).toBeGreaterThan(0);
  });

  it('switches between Orientation, Milestones, Project Guide, and Test Plan tabs', async () => {
    render(
      <ProjectStudio
        moduleFolderPath="01_Advanced_Python/Module_01_Python_Fundamentals"
        moduleTitle="Financial Calculator System"
        courseTitle="Advanced Python"
        guideMarkdown="# Project Guide\n\nImplement compound interest."
        onCompleteProject={() => {}}
        isProjectCompleted={false}
      />
    );

    const guideTab = screen.getByText('Project Guide');
    fireEvent.click(guideTab);
    expect(await screen.findByText(/Implement compound interest/)).toBeDefined();

    const testPlanTab = screen.getByText('Test Plan');
    fireEvent.click(testPlanTab);
    expect(await screen.findByText('Test Harness Plan')).toBeDefined();
  });
});
