import { marked } from 'marked';
import katex from 'katex';

/**
 * Renders Markdown content into HTML with full KaTeX mathematical symbol rendering.
 * Handles both block math ($$...$$) and inline math ($...$), protecting code blocks.
 */
export function renderMarkdownWithMath(raw: string): string {
  if (!raw) return '';

  // 1. Protect code blocks (```...``` and `...`) so math regex won't touch code
  const codeBlocks: string[] = [];
  let protectedText = raw.replace(/(```[\s\S]*?```|`[^`\n]+`)/g, (match) => {
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

  // 3. Render inline math: $...$ or \(...\)
  protectedText = protectedText.replace(/\$([^$\n\r]+?)\$/g, (match, math) => {
    const trimmed = math.trim();
    // Avoid false positives for prices or empty strings
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
  try {
    return marked.parse(restored, { async: false }) as string;
  } catch (err) {
    try {
      return marked.parse(raw, { async: false }) as string;
    } catch {
      return raw;
    }
  }
}
