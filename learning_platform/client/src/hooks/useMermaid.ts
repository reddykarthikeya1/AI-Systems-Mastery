import { useEffect } from 'react';
import mermaid from 'mermaid';

let mermaidInitialized = false;

function initMermaid() {
  try {
    const isDark = document.documentElement.classList.contains('dark');
    mermaid.initialize({
      startOnLoad: false,
      theme: isDark ? 'dark' : 'default',
      securityLevel: 'loose',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial, sans-serif',
      themeVariables: {
        fontSize: '14px',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial, sans-serif',
      },
      flowchart: {
        htmlLabels: true,
        padding: 32,
        nodeSpacing: 60,
        rankSpacing: 60,
        curve: 'basis',
      },
    });
    mermaidInitialized = true;
  } catch {
    // ignore init race
  }
}

/**
 * Universal hook that renders Mermaid diagrams inside any container element
 * and applies SVG post-render height expansion to eliminate all clipping.
 */
export function useMermaid(
  containerRef: React.RefObject<HTMLElement | null>,
  deps: React.DependencyList = []
) {
  useEffect(() => {
    initMermaid();

    const renderMermaidBlocks = async () => {
      const container = containerRef.current;
      if (!container) return;

      const codeBlocks = container.querySelectorAll<HTMLElement>(
        'pre code.language-mermaid, pre.language-mermaid'
      );

      for (let i = 0; i < codeBlocks.length; i++) {
        const codeEl = codeBlocks[i];
        const preEl = (codeEl.tagName === 'PRE' ? codeEl : codeEl.parentElement) as HTMLElement | null;
        if (!preEl || (preEl as any).dataset?.mermaidRendered) continue;

        const rawCode = codeEl.textContent || '';
        if (!rawCode.trim()) continue;

        const renderId = `mermaid-block-${Date.now()}-${i}-${Math.random().toString(36).slice(2, 6)}`;
        try {
          const { svg } = await mermaid.render(renderId, rawCode.trim());
          const wrapper = document.createElement('div');
          wrapper.className =
            'mermaid-diagram-card my-6 p-6 rounded-2xl bg-surface border border-border shadow-card flex justify-center items-center overflow-x-auto transition-all';
          wrapper.innerHTML = svg;
          (preEl as any).dataset.mermaidRendered = 'true';
          preEl.replaceWith(wrapper);

          // SVG post-render height expansion patch
          requestAnimationFrame(() => {
            const svgEl = wrapper.querySelector('svg');
            if (!svgEl) return;

            const foreignObjects = svgEl.querySelectorAll('foreignObject');
            let viewBoxNeedsUpdate = false;

            foreignObjects.forEach((fo) => {
              const foHeight = parseFloat(fo.getAttribute('height') || '0');
              const innerDiv = fo.querySelector('div');
              if (!innerDiv) return;

              const actualHeight = innerDiv.scrollHeight;
              const PADDING = 16;
              if (actualHeight + PADDING > foHeight) {
                const newHeight = actualHeight + PADDING;
                const heightDelta = newHeight - foHeight;
                fo.setAttribute('height', String(newHeight));

                const nodeGroup = fo.closest('.node, .label, g');
                if (nodeGroup) {
                  const rect = nodeGroup.querySelector('rect');
                  if (rect) {
                    const rectH = parseFloat(rect.getAttribute('height') || '0');
                    rect.setAttribute('height', String(rectH + heightDelta));
                  }
                  const polygon = nodeGroup.querySelector('polygon');
                  if (polygon) {
                    const points = polygon.getAttribute('points');
                    if (points) {
                      const pts = points.split(/[\s,]+/).map(Number);
                      for (let p = 1; p < pts.length; p += 2) {
                        if (pts[p] > 0) pts[p] += heightDelta / 2;
                        else pts[p] -= heightDelta / 2;
                      }
                      polygon.setAttribute('points', pts.join(','));
                    }
                  }
                }
                viewBoxNeedsUpdate = true;
              }
            });

            if (viewBoxNeedsUpdate) {
              const vb = svgEl.getAttribute('viewBox');
              if (vb) {
                const parts = vb.split(/[\s,]+/).map(Number);
                if (parts.length === 4) {
                  parts[3] += 60;
                  svgEl.setAttribute('viewBox', parts.join(' '));
                }
              }
              const svgHeight = svgEl.getAttribute('height');
              if (svgHeight) {
                const h = parseFloat(svgHeight);
                if (!isNaN(h)) svgEl.setAttribute('height', String(h + 60));
              }
            }
          });
        } catch (err) {
          console.warn('Failed to render Mermaid block:', err);
        }
      }
    };

    const timer = setTimeout(() => {
      renderMermaidBlocks();
    }, 40);

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}
