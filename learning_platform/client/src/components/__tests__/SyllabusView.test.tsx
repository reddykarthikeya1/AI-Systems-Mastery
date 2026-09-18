import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { SyllabusView } from '../SyllabusView';
import { CourseSummary, ModuleItem, ProgressPayload } from '../../types';

const mockCourse: CourseSummary = {
  id: '01_advanced_python',
  title: 'Advanced Python Mastery',
  folder_name: '01_Advanced_Python',
  module_count: 2,
  course_num: 1,
  category: 'Python Engineering',
  difficulty: 'Staff',
  estimated_hours: 12,
  description: 'Master advanced Python internals',
};

const mockModules: ModuleItem[] = [
  {
    id: 'mod_00',
    title: 'Environment Tooling Workflow',
    module_num: 0,
    folder_path: '01_Advanced_Python/Module_00_Environment',
    has_starter: true,
    has_solution: true,
    lessons: [
      {
        id: 'lesson_00_01',
        title: 'Theoretical Foundations & Architecture',
        file_path: '01_Advanced_Python/Module_00_Environment/01_theory.md',
        type: 'theory',
      },
      {
        id: 'lesson_00_02',
        title: 'PowerShell Automation: Setup And Verify',
        file_path: '01_Advanced_Python/Module_00_Environment/02_powershell.md',
        type: 'theory',
      },
    ],
  },
  {
    id: 'mod_01',
    title: 'Python Fundamentals & Data Model',
    module_num: 1,
    folder_path: '01_Advanced_Python/Module_01_Fundamentals',
    has_starter: true,
    has_solution: true,
    lessons: [
      {
        id: 'lesson_01_01',
        title: 'Deep-Dive Object Internals',
        file_path: '01_Advanced_Python/Module_01_Fundamentals/01_internals.md',
        type: 'theory',
      },
      {
        id: 'lesson_01_02',
        title: 'Custom MetaClasses and Descriptors',
        file_path: '01_Advanced_Python/Module_01_Fundamentals/02_descriptors.md',
        type: 'project',
      },
    ],
  },
];

const mockProgress: ProgressPayload = {
  completed_lessons: ['lesson_00_01', 'lesson_00_02'], // mod_00 is 100% complete
  completed_modules: ['mod_00'],
  last_updated: Date.now(),
  theme: 'dark',
};

describe('SyllabusView Collapsible Module Cards', () => {
  it('expands the first incomplete module by default and collapses others', () => {
    render(
      <SyllabusView
        course={mockCourse}
        modules={mockModules}
        progress={mockProgress}
        onBack={() => {}}
        onSelectLesson={() => {}}
      />
    );

    // Module 01 (incomplete) should be expanded by default
    expect(screen.getByText('Deep-Dive Object Internals')).toBeDefined();
    expect(screen.getByText('Custom MetaClasses and Descriptors')).toBeDefined();

    // Module 00 (completed) should start collapsed
    expect(screen.queryByText('Theoretical Foundations & Architecture')).toBeNull();
  });

  it('toggles a module open and closed on click', () => {
    render(
      <SyllabusView
        course={mockCourse}
        modules={mockModules}
        progress={mockProgress}
        onBack={() => {}}
        onSelectLesson={() => {}}
      />
    );

    // Click on Module 00 header to expand it
    const mod00Title = screen.getByText('Environment Tooling Workflow');
    fireEvent.click(mod00Title);

    // Now Module 00 lessons should be visible
    expect(screen.getByText('Theoretical Foundations & Architecture')).toBeDefined();

    // Click again to collapse
    fireEvent.click(mod00Title);
    expect(screen.queryByText('Theoretical Foundations & Architecture')).toBeNull();
  });

  it('expands all and collapses all modules using the global controls', () => {
    render(
      <SyllabusView
        course={mockCourse}
        modules={mockModules}
        progress={mockProgress}
        onBack={() => {}}
        onSelectLesson={() => {}}
      />
    );

    const expandAllBtn = screen.getByText('Expand All');
    const collapseAllBtn = screen.getByText('Collapse All');

    // Click Expand All: both module 00 and 01 lessons should be visible
    fireEvent.click(expandAllBtn);
    expect(screen.getByText('Theoretical Foundations & Architecture')).toBeDefined();
    expect(screen.getByText('Deep-Dive Object Internals')).toBeDefined();

    // Click Collapse All: no lessons should be visible
    fireEvent.click(collapseAllBtn);
    expect(screen.queryByText('Theoretical Foundations & Architecture')).toBeNull();
    expect(screen.queryByText('Deep-Dive Object Internals')).toBeNull();
  });
});
