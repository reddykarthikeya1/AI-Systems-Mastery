import { describe, it, expect, vi } from 'vitest';
import { resolveRelativePath, parseRepoPath, handleMarkdownLinkClick } from '../linkInterceptor';

describe('linkInterceptor Service', () => {
  describe('resolveRelativePath', () => {
    it('resolves sibling files in current directory', () => {
      const res = resolveRelativePath('01_Advanced_Python/Module_01_Basics', '02_CONTROL_FLOW.md');
      expect(res).toBe('01_Advanced_Python/Module_01_Basics/02_CONTROL_FLOW.md');
    });

    it('resolves relative parent directory paths', () => {
      const res = resolveRelativePath('01_Advanced_Python/Module_01_Basics', '../Module_02_OOP/01_README.md');
      expect(res).toBe('01_Advanced_Python/Module_02_OOP/01_README.md');
    });

    it('normalizes backslashes to forward slashes', () => {
      const res = resolveRelativePath('01_Advanced_Python\\Module_01', '.\\starter\\main.py');
      expect(res).toBe('01_Advanced_Python/Module_01/starter/main.py');
    });
  });

  describe('parseRepoPath', () => {
    it('extracts course, module, and filename correctly', () => {
      const parsed = parseRepoPath('01_Advanced_Python/Module_02_OOP/03_INTERMEDIATE.md');
      expect(parsed.courseId).toBe('01_Advanced_Python');
      expect(parsed.moduleFolderName).toBe('Module_02_OOP');
      expect(parsed.moduleNum).toBe(2);
      expect(parsed.filename).toBe('03_INTERMEDIATE.md');
    });
  });

  describe('handleMarkdownLinkClick', () => {
    it('intercepts external URLs and opens in new window', () => {
      const openSpy = vi.spyOn(window, 'open').mockImplementation(() => null);
      const a = document.createElement('a');
      a.href = 'https://docs.python.org/3/';
      const event = {
        target: a,
        preventDefault: vi.fn(),
      } as unknown as MouseEvent;

      const handled = handleMarkdownLinkClick(event, {});
      expect(handled).toBe(true);
      expect(event.preventDefault).toHaveBeenCalled();
      expect(openSpy).toHaveBeenCalledWith('https://docs.python.org/3/', '_blank', 'noopener,noreferrer');
      openSpy.mockRestore();
    });

    it('navigates in-app to matching lesson item', () => {
      const onSelectLesson = vi.fn();
      const a = document.createElement('a');
      a.setAttribute('href', '02_FUNCTIONS.md');
      const event = {
        target: a,
        preventDefault: vi.fn(),
      } as unknown as MouseEvent;

      const handled = handleMarkdownLinkClick(event, {
        moduleFolderPath: '01_Advanced_Python/Module_01',
        allLessons: [
          { id: 'l1', title: 'Intro', file_path: '01_Advanced_Python/Module_01/01_INTRO.md', type: 'theory' },
          { id: 'l2', title: 'Functions', file_path: '01_Advanced_Python/Module_01/02_FUNCTIONS.md', type: 'theory' },
        ],
        onSelectLesson,
      });

      expect(handled).toBe(true);
      expect(onSelectLesson).toHaveBeenCalledWith(
        '01_Advanced_Python/Module_01/02_FUNCTIONS.md',
        'l2',
        'theory'
      );
    });

    it('switches to project tab on PROJECT_GUIDE.md links', () => {
      const onNavigateTab = vi.fn();
      const a = document.createElement('a');
      a.setAttribute('href', '../PROJECT_GUIDE.md');
      const event = {
        target: a,
        preventDefault: vi.fn(),
      } as unknown as MouseEvent;

      const handled = handleMarkdownLinkClick(event, {
        moduleFolderPath: '01_Advanced_Python/Module_01',
        onNavigateTab,
      });

      expect(handled).toBe(true);
      expect(onNavigateTab).toHaveBeenCalledWith('project');
    });
  });
});
