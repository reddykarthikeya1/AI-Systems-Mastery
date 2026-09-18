import React from 'react';
import { LessonItem } from '../types';

export interface LinkResolutionContext {
  currentFilePath?: string;
  moduleFolderPath?: string;
  courseId?: string;
  allLessons?: LessonItem[];
  onSelectLesson?: (filePath: string, lessonId: string, initialTab?: string) => void;
  onNavigateTab?: (tab: string) => void;
  onShowNotice?: (message: string, commandToCopy?: string) => void;
}

/**
 * Normalizes and resolves a relative path against a base directory.
 * E.g. resolveRelativePath('01_Advanced_Python/Module_01', '02_FOUNDATIONS.md')
 *   -> '01_Advanced_Python/Module_01/02_FOUNDATIONS.md'
 * E.g. resolveRelativePath('01_Advanced_Python/Module_01', '../Module_02/01_README.md')
 *   -> '01_Advanced_Python/Module_02/01_README.md'
 */
export function resolveRelativePath(baseDir: string, relativePath: string): string {
  const normBase = baseDir.replace(/\\/g, '/').replace(/^\/+|\/+$/g, '');
  const normRel = relativePath.replace(/\\/g, '/');

  const baseSegments = normBase ? normBase.split('/') : [];
  const relSegments = normRel.split('/');

  for (const seg of relSegments) {
    if (!seg || seg === '.') {
      continue;
    } else if (seg === '..') {
      if (baseSegments.length > 0) {
        baseSegments.pop();
      }
    } else {
      baseSegments.push(seg);
    }
  }

  return baseSegments.join('/');
}

/**
 * Extracts courseId, moduleNum, and lesson info from a repo relative path.
 * E.g. '01_Advanced_Python/Module_02_Functions/01_README.md'
 */
export function parseRepoPath(fullPath: string): {
  courseId?: string;
  moduleFolderName?: string;
  moduleNum?: number;
  filename: string;
} {
  const norm = fullPath.replace(/\\/g, '/').replace(/^\/+|\/+$/g, '');
  const parts = norm.split('/');
  const filename = parts[parts.length - 1] || '';

  let courseId: string | undefined;
  let moduleFolderName: string | undefined;
  let moduleNum: number | undefined;

  // Only examine directory segments (exclude the terminal filename)
  const dirParts = parts.length > 1 ? parts.slice(0, -1) : parts;
  for (let i = 0; i < dirParts.length; i++) {
    if (/^\d{2}_/.test(dirParts[i]) && !dirParts[i].startsWith('Module_')) {
      courseId = dirParts[i];
    }
    const mMatch = dirParts[i].match(/Module_(\d+)/i);
    if (mMatch) {
      moduleFolderName = dirParts[i];
      moduleNum = parseInt(mMatch[1], 10);
    }
  }

  return { courseId, moduleFolderName, moduleNum, filename };
}

/**
 * Handles link clicks inside rendered markdown content.
 * Returns true if the link was intercepted and handled, false otherwise.
 */
export function handleMarkdownLinkClick(
  e: React.MouseEvent<HTMLElement> | MouseEvent,
  context: LinkResolutionContext
): boolean {
  const target = (e.target as HTMLElement).closest('a');
  if (!target) return false;

  const rawHref = target.getAttribute('href');
  if (!rawHref) return false;

  const href = rawHref.trim();

  // 1. External URLs (http, https, mailto)
  if (/^(https?:\/\/|mailto:)/i.test(href)) {
    e.preventDefault();
    window.open(href, '_blank', 'noopener,noreferrer');
    return true;
  }

  // 2. Pure in-page anchor (#heading)
  if (href.startsWith('#')) {
    e.preventDefault();
    const anchorId = decodeURIComponent(href.slice(1)).toLowerCase().replace(/[^a-z0-9-_]/g, '');
    const anchorEl = 
      document.getElementById(anchorId) || 
      document.getElementById(href.slice(1)) || 
      document.querySelector(`[name="${anchorId}"]`);
    if (anchorEl) {
      anchorEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    return true;
  }

  // 3. Relative file or directory path
  e.preventDefault();

  // Strip query/hash from the file target
  const [cleanPath, anchorPart] = href.split('#');
  const targetPath = cleanPath.trim();

  // Determine base folder: directory of currentFilePath or moduleFolderPath
  let baseFolder = context.moduleFolderPath || '';
  if (context.currentFilePath) {
    const parts = context.currentFilePath.replace(/\\/g, '/').split('/');
    if (parts.length > 1) {
      baseFolder = parts.slice(0, -1).join('/');
    }
  }

  const resolved = resolveRelativePath(baseFolder, targetPath);
  const { courseId, moduleNum, filename } = parseRepoPath(resolved);
  const ext = filename.includes('.') ? filename.slice(filename.lastIndexOf('.')).toLowerCase() : '';

  // Case A: Directory targets
  if (
    targetPath.endsWith('/') ||
    targetPath === 'starter' ||
    targetPath.endsWith('/starter') ||
    filename.toLowerCase() === 'starter'
  ) {
    if (context.onNavigateTab) {
      context.onNavigateTab('project');
      return true;
    }
  }

  if (
    targetPath === 'debug_lab' ||
    targetPath.endsWith('/debug_lab') ||
    filename.toLowerCase() === 'debug_lab'
  ) {
    if (context.onNavigateTab) {
      context.onNavigateTab('debug');
      return true;
    }
  }

  if (
    targetPath === 'problems' ||
    targetPath.endsWith('/problems') ||
    filename.toLowerCase() === 'problems'
  ) {
    if (context.onNavigateTab) {
      context.onNavigateTab('arena');
      return true;
    }
  }

  // Case B: PROJECT_GUIDE.md target
  if (/project_guide/i.test(filename)) {
    if (context.onNavigateTab) {
      context.onNavigateTab('project');
      return true;
    }
  }

  // Case C: Matches a lesson in the current module's allLessons
  if (context.allLessons && context.onSelectLesson) {
    const matched = context.allLessons.find((l) => {
      const normLessonPath = l.file_path.replace(/\\/g, '/');
      return (
        normLessonPath === resolved ||
        normLessonPath.endsWith('/' + filename) ||
        l.id.endsWith('_' + filename)
      );
    });

    if (matched) {
      context.onSelectLesson(matched.file_path, matched.id, 'theory');
      if (anchorPart) {
        setTimeout(() => {
          const el = document.getElementById(anchorPart.toLowerCase());
          if (el) el.scrollIntoView({ behavior: 'smooth' });
        }, 150);
      }
      return true;
    }
  }

  // Case D: References another module in the same course or another course
  if (courseId && moduleNum !== undefined) {
    const lessonIdHint = filename ? `Module_${String(moduleNum).padStart(2, '0')}_${filename}` : '';
    const hash = lessonIdHint
      ? `#/course/${encodeURIComponent(courseId)}/module/${moduleNum}/lesson/${encodeURIComponent(lessonIdHint)}`
      : `#/course/${encodeURIComponent(courseId)}/module/${moduleNum}`;
    window.location.hash = hash;
    return true;
  }

  // Case E: Script files or Notebooks
  if (ext === '.py' || ext === '.ipynb' || ext === '.sh' || ext === '.ps1' || ext === '.rs') {
    if (context.onShowNotice) {
      context.onShowNotice(
        `File reference: ${filename}`,
        `code "${resolved}"`
      );
    }
    return true;
  }

  // Case F: Fallback notice
  if (context.onShowNotice) {
    context.onShowNotice(
      `File location: ${resolved}`,
      `code "${resolved}"`
    );
  }

  return true;
}
