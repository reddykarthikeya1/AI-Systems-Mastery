import glob
import os
import re

REPLACEMENTS = [
    # Hex background consolidations to semantic tokens
    (r'\bbg-white\s+dark:bg-\[#111622\]', 'bg-surface'),
    (r'\bbg-white/95\s+dark:bg-\[#111622\]/95', 'bg-surface/95'),
    (r'\bbg-zinc-50\s+dark:bg-\[#111622\]', 'bg-surface'),
    (r'\bbg-zinc-100\s+dark:bg-\[#161B22\]', 'bg-surface-raised'),
    (r'\bbg-zinc-50\s+dark:bg-\[#0D1117\]', 'bg-surface'),
    (r'\bdark:bg-\[#111622\]', 'dark:bg-surface'),
    (r'\bdark:bg-\[#0D1117\]', 'dark:bg-bg'),
    (r'\bdark:bg-\[#161B22\]', 'dark:bg-surface-raised'),
    (r'\bdark:bg-\[#0A0D12\]', 'dark:bg-bg'),
    (r'\bdark:bg-\[#0B0F17\]', 'dark:bg-bg'),
    (r'\bdark:bg-\[#0c0e14\]', 'dark:bg-bg'),
    (r'\bbg-\[#0D1117\]', 'bg-bg'),
    (r'\bbg-\[#161B22\]/60', 'bg-surface-raised/60'),
    (r'\bbg-\[#161B22\]', 'bg-surface-raised'),
    (r'\bbg-\[#0A0D12\]', 'bg-bg'),
    (r'\bbg-\[#0B0F17\]', 'bg-bg'),
    (r'\bbg-\[#0C1017\]', 'bg-bg'),
    (r'\bbg-\[#141A24\]', 'bg-surface-raised'),
    (r'\bbg-\[#090D13\]', 'bg-bg'),
    (r'\bbg-\[#090D14\]', 'bg-bg'),
    (r'\btext-\[#E6EDF3\]', 'text-fg'),

    # Redundant dark: color pairs to semantic tokens
    (r'\btext-zinc-900\s+dark:text-zinc-100\b', 'text-fg'),
    (r'\btext-zinc-100\s+dark:text-zinc-900\b', 'text-fg'),
    (r'\btext-zinc-500\s+dark:text-zinc-400\b', 'text-fg-muted'),
    (r'\btext-zinc-400\s+dark:text-zinc-500\b', 'text-fg-muted'),
    (r'\bborder-zinc-200\s+dark:border-zinc-800\b', 'border-border'),
    (r'\bborder-zinc-800\s+dark:border-zinc-200\b', 'border-border'),
    (r'\bborder-zinc-200/80\s+dark:border-zinc-800\b', 'border-border'),
    (r'\bborder-zinc-200/80\s+dark:border-zinc-800/80\b', 'border-border'),
    (r'\bborder-zinc-200/60\s+dark:border-zinc-800/60\b', 'border-border'),
    (r'\bbg-white\s+dark:bg-zinc-900\b', 'bg-surface'),
    (r'\bbg-zinc-50\s+dark:bg-zinc-900\b', 'bg-surface'),
]

def main():
    files = glob.glob('learning_platform/client/src/**/*.tsx', recursive=True) + glob.glob('learning_platform/client/src/**/*.ts', recursive=True)
    files = [f for f in files if '__tests__' not in f and 'glossary.ts' not in f and 'ArchitectureCanvasView.tsx' not in f]

    total_changes = 0
    updated_files = 0

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        changes_in_file = 0

        for pattern, repl in REPLACEMENTS:
            matches = len(re.findall(pattern, new_content))
            if matches > 0:
                new_content = re.sub(pattern, repl, new_content)
                changes_in_file += matches

        if changes_in_file > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files += 1
            total_changes += changes_in_file
            print(f"Updated {fpath} ({changes_in_file} token replacements)")

    print(f"\nDone! Made {total_changes} token replacements across {updated_files} files.")

if __name__ == '__main__':
    main()
