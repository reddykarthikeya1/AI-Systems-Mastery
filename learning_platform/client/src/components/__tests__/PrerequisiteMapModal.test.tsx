import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { PrerequisiteMapModal } from '../PrerequisiteMapModal';

const MOCK_COURSES = [
  { id: '01_Advanced_Python', title: 'Advanced Python & Runtime Internals', description: '', modules_count: 10 },
  { id: '02_Data_Structures_and_Algorithms', title: 'High-Performance Algorithms & Structures', description: '', modules_count: 17 },
  { id: '03_Databases_and_Storage_Engines', title: 'Database Internals & Storage Engines', description: '', modules_count: 13 },
];

describe('PrerequisiteMapModal Component', () => {
  it('renders nothing when isOpen is false', () => {
    const { container } = render(
      <PrerequisiteMapModal isOpen={false} onClose={vi.fn()} courses={MOCK_COURSES as any} />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders curriculum roadmap modal with tiers when isOpen is true', () => {
    render(
      <PrerequisiteMapModal isOpen={true} onClose={vi.fn()} courses={MOCK_COURSES as any} />
    );

    expect(screen.getByText('Curriculum Dependency Map')).toBeDefined();
    expect(screen.getByText('Systems & Algorithmic Engineering')).toBeDefined();
    expect(screen.getByText('Mathematical Foundations of AI')).toBeDefined();
    expect(screen.getByText('Deep Learning & GPU Infrastructure')).toBeDefined();
    expect(screen.getByText('Inference Engines, Agents & Safety')).toBeDefined();
  });

  it('calls onSelectCourse and onClose when a course card is clicked', () => {
    const handleSelect = vi.fn();
    const handleClose = vi.fn();

    render(
      <PrerequisiteMapModal
        isOpen={true}
        onClose={handleClose}
        courses={MOCK_COURSES as any}
        onSelectCourse={handleSelect}
      />
    );

    const dsaCourse = screen.getByText('High-Performance Algorithms & Structures');
    fireEvent.click(dsaCourse);

    expect(handleSelect).toHaveBeenCalledWith('02_Data_Structures_and_Algorithms');
    expect(handleClose).toHaveBeenCalled();
  });

  it('calls onClose when Escape key is pressed', () => {
    const handleClose = vi.fn();

    render(
      <PrerequisiteMapModal isOpen={true} onClose={handleClose} courses={MOCK_COURSES as any} />
    );

    fireEvent.keyDown(window, { key: 'Escape', code: 'Escape' });
    expect(handleClose).toHaveBeenCalledTimes(1);
  });
});
