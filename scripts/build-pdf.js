const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { marked } = require('marked');
const hljs = require('highlight.js');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const ASSETS_DIR = path.resolve(__dirname, 'assets');
const TEMPLATES_DIR = path.resolve(__dirname, 'templates');
const MERMAID_JS = path.resolve(ASSETS_DIR, 'mermaid.min.js').replace(/\\/g, '/');
const CSS_PATH = path.resolve(TEMPLATES_DIR, 'pdf-style.css');
const KATEX_DIR = path.resolve(__dirname, '..', 'node_modules', 'katex', 'dist').replace(/\\/g, '/');
const LITE_TRACKS = ['01-Python-Mastery', '02-Low-Level-Design', '03-High-Level-Design', '04-Agentic-AI', '05-DSA-Interview-Playbook'];

// Configure marked with highlight.js
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value;
      } catch (e) {}
    }
    return hljs.highlightAuto(code).value;
  },
  breaks: false,
  gfm: true
});

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// Custom renderer for mermaid and callouts
const renderer = new marked.Renderer();
const originalCodeRenderer = renderer.code.bind(renderer);

renderer.code = function(token, lang, isEscaped) {
  const code = typeof token === 'object' ? token.text : token;
  const language = typeof token === 'object' ? token.lang : lang;
  if (language === 'mermaid') {
    return `<div class="mermaid">\n${escapeHtml(code)}\n</div>`;
  }
  return originalCodeRenderer(code, language, isEscaped);
};

marked.use({ renderer });

// Transform GitHub callout blockquotes into HTML callouts
function transformCallouts(html) {
  const alertTypes = ['NOTE', 'TIP', 'IMPORTANT', 'WARNING', 'CAUTION'];
  for (const type of alertTypes) {
    const regex = new RegExp(`<blockquote>\\s*<p>\\s*\\[!${type}\\]\\s*([\\s\\S]*?)<\\/blockquote>`, 'gi');
    html = html.replace(regex, (match, content) => {
      return `<div class="callout callout-${type.toLowerCase()}">
        <div class="callout-title">${type}</div>
        <p>${content}</div>`;
    });
  }
  return html;
}

// Protect math ($...$ and $$...$$) from markdown processing (marked would eat backslash-underscore and backslash-dollar)
function protectMath(md) {
  const store = [];
  const re = /(```[\s\S]*?```|`[^`\n]+`)|(\$\$(?:\\.|[^$\\])+?\$\$)|(\$(?:\\.|[^$\\\n])+?\$)|(\\\$)/g;
  const out = md.replace(re, (m, code, disp, inl, esc) => {
    if (code || esc) return m;
    store.push(m);
    return '@@MATH' + (store.length - 1) + '@@';
  });
  return { md: out, store };
}
function restoreMath(html, store) {
  return html.replace(/@@MATH(\d+)@@/g, (m, i) => store[+i].replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'));
}

function convertMarkdownToHtml(mdFilePath) {
  const rawMd = fs.readFileSync(mdFilePath, 'utf8');
  const pm = protectMath(rawMd);
  let bodyHtml = restoreMath(marked.parse(pm.md), pm.store);
  bodyHtml = transformCallouts(bodyHtml);
  // Print has no click: expand every <details> (the Check Yourself answers) so the PDF is complete
  bodyHtml = bodyHtml.replace(/<details>/g, '<details open>');

  const cssContent = fs.readFileSync(CSS_PATH, 'utf8');
  const title = path.basename(mdFilePath, '.md').replace(/-/g, ' ');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>${title}</title>
  <style>
    ${cssContent}
  </style>
  <link rel="stylesheet" href="file:///${KATEX_DIR}/katex.min.css">
  <script src="file:///${KATEX_DIR}/katex.min.js"></script>
  <script src="file:///${KATEX_DIR}/contrib/auto-render.min.js"></script>
  <script src="file:///${MERMAID_JS}"></script>
  <script>
    document.addEventListener("DOMContentLoaded", function() {
      if (typeof renderMathInElement === 'function') {
        renderMathInElement(document.body, { delimiters: [{ left: '$$', right: '$$', display: true }, { left: '$', right: '$', display: false }], ignoredClasses: ['mermaid'], ignoredTags: ['script', 'style', 'pre', 'code', 'svg'], throwOnError: false });
      }
      mermaid.initialize({
        startOnLoad: true,
        theme: 'neutral',
        fontFamily: 'Inter, -apple-system, sans-serif',
        flowchart: { curve: 'basis', htmlLabels: true },
        sequence: { showSequenceNumbers: true, actorMargin: 40, messageMargin: 30 }
      });
    });
  </script>
</head>
<body>
  ${bodyHtml}
</body>
</html>`;
}

function convertFileToPdf(mdFilePath, outDir = null) {
  if (!fs.existsSync(mdFilePath)) {
    console.error(`File not found: ${mdFilePath}`);
    return;
  }

  const rootDir = path.resolve(__dirname, '..');
  const relPath = path.relative(rootDir, mdFilePath);
  const targetDir = outDir || path.resolve(rootDir, 'pdfs', path.dirname(relPath));
  
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  const baseName = path.basename(mdFilePath, '.md');
  const targetPdf = path.resolve(targetDir, `${baseName}.pdf`);
  const tempHtml = path.resolve(targetDir, `${baseName}.tmp.html`);

  const html = convertMarkdownToHtml(mdFilePath);
  fs.writeFileSync(tempHtml, html, 'utf8');

  console.log(`Rendering PDF: ${relPath} -> ${path.relative(rootDir, targetPdf)}`);
  try {
    execSync(`"${CHROME_PATH}" --headless --disable-gpu --allow-file-access-from-files --virtual-time-budget=3500 --print-to-pdf="${targetPdf}" "${tempHtml}"`, {
      stdio: 'pipe'
    });
    const sizeKb = (fs.statSync(targetPdf).size / 1024).toFixed(1);
    console.log(`  -> Completed: ${sizeKb} KB`);
  } catch (err) {
    console.error(`  -> Failed to render ${mdFilePath}:`, err.message);
  } finally {
    if (fs.existsSync(tempHtml)) {
      fs.unlinkSync(tempHtml);
    }
  }
}

function walkDir(dir, fileList = []) {
  if (!fs.existsSync(dir)) return fileList;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.resolve(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== 'node_modules' && entry.name !== 'scripts' && entry.name !== 'pdfs' && entry.name !== '.git') {
        walkDir(fullPath, fileList);
      }
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

// CLI handler
const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '--help') {
  console.log(`
Usage:
  node scripts/build-pdf.js <path-to-markdown-file>
  node scripts/build-pdf.js <directory-name>
  node scripts/build-pdf.js --all
  `);
  process.exit(0);
}

const rootDir = path.resolve(__dirname, '..');

if (args.length === 0 || args.includes('--all')) {
  const allMdFiles = LITE_TRACKS.flatMap(t => walkDir(path.resolve(rootDir, t))).concat([path.resolve(rootDir, 'README.md')]);
  console.log(`Found ${allMdFiles.length} Markdown files to compile to PDF...`);
  allMdFiles.forEach(f => convertFileToPdf(f));
} else {
  args.forEach(tgt => {
    const resolvedTarget = path.resolve(rootDir, tgt);
    if (fs.existsSync(resolvedTarget)) {
      const stat = fs.statSync(resolvedTarget);
      if (stat.isDirectory()) {
        const files = walkDir(resolvedTarget);
        console.log(`Found ${files.length} Markdown files in ${tgt}...`);
        files.forEach(f => convertFileToPdf(f));
      } else if (stat.isFile() && resolvedTarget.endsWith('.md')) {
        convertFileToPdf(resolvedTarget);
      }
    } else {
      console.error(`Target not found: ${resolvedTarget}`);
    }
  });
}
