import { describe, it, expect } from 'vitest';
import { extractExpectedOutputFromCode } from '../SideCodeRunner';

/**
 * Compares stdout with expected output, ignoring trailing whitespace differences
 */
export function verifyOutputMatches(stdout: string, expected: string): boolean {
  const normalize = (s: string) =>
    s
      .trim()
      .split('\n')
      .map((l) => l.trimEnd())
      .join('\n');
  return normalize(stdout) === normalize(expected);
}

describe('SideCodeRunner Output Verification & Diff Logic', () => {
  it('extracts expected output block from single-line comment', () => {
    const code = `
x = 10 * 2
print(x)
# Expected Output: 20
`;
    expect(extractExpectedOutputFromCode(code)).toBe('20');
  });

  it('extracts multiline expected output comments', () => {
    const code = `
print("Matrix Dimension: 2048 x 2048")
print("Total Computation: 17.18 GFLOPs")
# Expected Output:
# Matrix Dimension: 2048 x 2048
# Total Computation: 17.18 GFLOPs
`;
    expect(extractExpectedOutputFromCode(code)).toBe(
      'Matrix Dimension: 2048 x 2048\nTotal Computation: 17.18 GFLOPs'
    );
  });

  it('returns null if no expected output comment is present', () => {
    const code = `
def add(a, b):
    return a + b
# Just a normal comment
`;
    expect(extractExpectedOutputFromCode(code)).toBeNull();
  });

  it('verifies exact match between stdout and expected target', () => {
    const stdout = 'Matrix Dimension: 2048 x 2048\nTotal Computation: 17.18 GFLOPs\n';
    const expected = 'Matrix Dimension: 2048 x 2048\nTotal Computation: 17.18 GFLOPs';
    expect(verifyOutputMatches(stdout, expected)).toBe(true);
  });

  it('detects discrepancies in output', () => {
    const stdout = 'Total Computation: 15.00 GFLOPs';
    const expected = 'Total Computation: 17.18 GFLOPs';
    expect(verifyOutputMatches(stdout, expected)).toBe(false);
  });
});
