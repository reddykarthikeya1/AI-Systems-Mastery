import { marked } from 'marked';
import katex from 'katex';
import { GLOSSARY } from '../data/glossary';

/**
 * Renders Markdown content into HTML with full KaTeX mathematical symbol rendering.
 * Handles both block math ($$...$$) and inline math ($...$), protecting code blocks.
 */
export function renderMarkdownWithMath(raw: string): string {
  if (!raw) return '';

  // 0. Clean redundant "Recommended Step-by-Step Learning Path" section (tracked in interactive syllabus rail)
  const cleanedRaw = raw.replace(
    /(?:^|\n)(?:---\s*\n+)?##\s*🗺️?\s*Recommended Step-by-Step Learning Path[\s\S]*?(?=(?:\n##\s|\n#\s|$))/gi,
    '\n'
  ).replace(/\n---\s*\n+\s*---/g, '\n---');

  // 1. Protect code blocks (```...``` and `...`) so math regex won't touch code
  const codeBlocks: string[] = [];
  let protectedText = cleanedRaw.replace(/(```[\s\S]*?```|`[^`\n]+`)/g, (match) => {
    codeBlocks.push(match);
    return `%%%MATH_CODEBLOCK_${codeBlocks.length - 1}%%%`;
  });

  // 2. Render display math: $$...$$ or \[...\]
  protectedText = protectedText.replace(/\$\$([\s\S]*?)\$\$/g, (match, math) => {
    try {
      const rendered = katex.renderToString(math.trim(), {
        displayMode: true,
        throwOnError: false,
      });
      return `<div class="katex-display-wrapper my-4 text-center overflow-x-auto">${rendered}</div>`;
    } catch {
      return match;
    }
  });

  protectedText = protectedText.replace(/\\\[([\s\S]*?)\\\]/g, (match, math) => {
    try {
      const rendered = katex.renderToString(math.trim(), {
        displayMode: true,
        throwOnError: false,
      });
      return `<div class="katex-display-wrapper my-4 text-center overflow-x-auto">${rendered}</div>`;
    } catch {
      return match;
    }
  });

  // 3. Render inline math: $...$ (requiring non-whitespace immediately inside delimiters) or \(...\)
  protectedText = protectedText.replace(/\$(?!\s)([^$\n\r]+?)(?<!\s)\$/g, (match, math) => {
    const trimmed = math.trim();
    // Avoid false positives for currency numbers or standalone numbers
    if (!trimmed || /^\d+(\.\d+)?$/.test(trimmed)) {
      return match;
    }
    try {
      return katex.renderToString(trimmed, {
        displayMode: false,
        throwOnError: false,
      });
    } catch {
      return match;
    }
  });

  protectedText = protectedText.replace(/\\\(([^\n\r]+?)\\\)/g, (match, math) => {
    const trimmed = math.trim();
    try {
      return katex.renderToString(trimmed, {
        displayMode: false,
        throwOnError: false,
      });
    } catch {
      return match;
    }
  });

  // 4. Restore protected code blocks
  const restored = protectedText.replace(/%%%MATH_CODEBLOCK_(\d+)%%%/g, (match, idx) => {
    return codeBlocks[parseInt(idx, 10)];
  });

  // 5. Parse markdown with marked
  let html = '';
  try {
    html = marked.parse(restored, { async: false }) as string;
  } catch (err) {
    try {
      html = marked.parse(raw, { async: false }) as string;
    } catch {
      html = raw;
    }
  }

  // 6. Annotate technical glossary terms with interactive tooltips
  return annotateGlossaryTerms(html);
}

/**
 * Annotates the first occurrence of technical terms with interactive tooltips.
 * Preserves pre/code blocks and existing HTML tags.
 */
export function annotateGlossaryTerms(html: string): string {
  if (!html) return '';
  try {
    const matchedTerms = new Set<string>();

    // Split into HTML tags/code blocks vs regular prose text
    const segments = html.split(/(<pre[\s\S]*?<\/pre>|<code[\s\S]*?<\/code>|<[^>]+>)/gi);
    for (let i = 0; i < segments.length; i++) {
      // Even indices are prose text outside HTML tags and code blocks
      if (i % 2 === 0 && segments[i]) {
        let segmentText = segments[i];

        for (const [key, entry] of Object.entries(GLOSSARY as Record<string, any>)) {
          if (matchedTerms.has(key)) continue;

          const aliases = [entry.term, ...(entry.aliases || [])];
          for (const alias of aliases) {
            if (matchedTerms.has(key)) break;
            if (alias.length < 3) continue; // Skip very short abbreviations to prevent accidental matches

            const termRegex = new RegExp(`\\b(${alias.replace(/[.*+?^${}()|[\\]\\]/g, '\\$&')})\\b`, 'i');
            if (termRegex.test(segmentText)) {
              matchedTerms.add(key);
              segmentText = segmentText.replace(
                termRegex,
                `<span class="glossary-term cursor-help border-b border-dotted border-sky-500/80 text-sky-600 dark:text-sky-400 font-medium" data-definition="${entry.definition}" title="${entry.term} (${entry.category}): ${entry.definition}">$1</span>`
              );
              break;
            }
          }
        }
        segments[i] = segmentText;
      }
    }
    return segments.join('');
  } catch {
    return html;
  }
}

/**
 * Formats quiz text (questions, options, explanations) supporting KaTeX math and inline code tags.
 */
export function renderQuizMarkdown(raw: string): string {
  if (!raw) return '';
  const rendered = renderMarkdownWithMath(raw);
  const trimmed = rendered.trim();
  // Strip outer single <p> ... </p> tag for clean inline placement if applicable
  if (trimmed.startsWith('<p>') && trimmed.endsWith('</p>') && trimmed.indexOf('<p>', 3) === -1) {
    return trimmed.slice(3, -4);
  }
  return trimmed;
}
