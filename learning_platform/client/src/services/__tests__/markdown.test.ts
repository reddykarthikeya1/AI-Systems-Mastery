import { describe, it, expect } from 'vitest';
import { renderMarkdownWithMath, annotateGlossaryTerms } from '../markdown';

describe('Markdown & KaTeX Math Rendering Service', () => {
  it('renders inline math expressions with KaTeX', () => {
    const input = 'The energy equivalence formula is $E = mc^2$.';
    const html = renderMarkdownWithMath(input);
    expect(html).toContain('katex');
    expect(html).toContain('c^2');
  });

  it('renders display block math expressions', () => {
    const input = '$$W = \\sum_{i=1}^{n} w_i x_i$$';
    const html = renderMarkdownWithMath(input);
    expect(html).toContain('katex-display-wrapper');
    expect(html).toContain('katex-display');
  });

  it('preserves code blocks without corrupting math-like code', () => {
    const input = '```python\nx = 10\ny = x $ 2  # not math\n```';
    const html = renderMarkdownWithMath(input);
    expect(html).toContain('<pre><code');
    expect(html).toContain('y = x $ 2');
  });

  it('does not falsely convert dollar prices or numbers into math', () => {
    const input = 'The server costs $100 per month or $50 on discount.';
    const html = renderMarkdownWithMath(input);
    expect(html).not.toContain('katex');
    expect(html).toContain('$100');
    expect(html).toContain('$50');
  });

  it('annotates glossary terms with interactive tooltips', () => {
    const input = '<p>We evaluate the KV Cache footprint during autoregressive decoding.</p>';
    const annotated = annotateGlossaryTerms(input);
    expect(annotated).toContain('glossary-term');
    expect(annotated).toContain('data-definition');
  });

  it('does not annotate glossary terms inside pre/code blocks', () => {
    const input = '<pre><code>const kv_cache = create_kv_cache();</code></pre>';
    const annotated = annotateGlossaryTerms(input);
    expect(annotated).not.toContain('class="glossary-term');
  });
});
