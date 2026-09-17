import glob
import os
import re

FOCUS_CLASSES = "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500"

def find_button_spans(content):
    spans = []
    idx = 0
    while True:
        pos = content.find('<button', idx)
        if pos == -1:
            break
        i = pos + 7
        in_double = False
        in_single = False
        in_template = False
        brace_depth = 0
        while i < len(content):
            ch = content[i]
            prev = content[i-1] if i > 0 else ''
            if in_double:
                if ch == '"' and prev != '\\':
                    in_double = False
            elif in_single:
                if ch == "'" and prev != '\\':
                    in_single = False
            elif in_template:
                if ch == '`' and prev != '\\':
                    in_template = False
            else:
                if ch == '"':
                    in_double = True
                elif ch == "'":
                    in_single = True
                elif ch == '`':
                    in_template = True
                elif ch == '{':
                    brace_depth += 1
                elif ch == '}':
                    brace_depth -= 1
                elif ch == '>' and brace_depth == 0:
                    spans.append((pos, i + 1))
                    break
            i += 1
        idx = pos + 7
    return spans

def transform_button_tag(tag):
    # tag starts with <button and ends with > or />
    is_self_closing = tag.endswith('/>')
    closing = '/>' if is_self_closing else '>'
    tag_inner = tag[7:-2 if is_self_closing else -1].strip()

    # If focus-visible is already present anywhere, check if it's before any arrow function
    if 'focus-visible:' in tag_inner:
        # Check if => occurs before focus-visible:
        arrow_pos = tag_inner.find('=>')
        fv_pos = tag_inner.find('focus-visible:')
        if arrow_pos == -1 or fv_pos < arrow_pos:
            return tag # Already good!

    # Find className attribute
    # Cases:
    # 1. className="..."
    # 2. className={`...`}
    # 3. className={...}
    # 4. No className attribute

    # Match className="..."
    m_str = re.search(r'\bclassName="([^"]*)"', tag_inner)
    if m_str:
        classes = m_str.group(1).strip()
        if 'focus-visible:' not in classes:
            classes = f"{FOCUS_CLASSES} {classes}".strip()
        # Remove className from tag_inner
        tag_inner_no_cn = (tag_inner[:m_str.start()] + tag_inner[m_str.end():]).strip()
        # Reconstruct with className as the first attribute
        reconstructed = f'<button className="{classes}"'
        if tag_inner_no_cn:
            reconstructed += f' {tag_inner_no_cn}'
        reconstructed += f' {closing}' if not reconstructed.endswith(' ') else closing
        return reconstructed

    # Match className={`...`}
    m_tmpl = re.search(r'\bclassName=\{`([^`]*)`\}', tag_inner)
    if m_tmpl:
        classes = m_tmpl.group(1).strip()
        if 'focus-visible:' not in classes:
            classes = f"{FOCUS_CLASSES} {classes}".strip()
        tag_inner_no_cn = (tag_inner[:m_tmpl.start()] + tag_inner[m_tmpl.end():]).strip()
        reconstructed = f'<button className={{`{classes}`}}'
        if tag_inner_no_cn:
            reconstructed += f' {tag_inner_no_cn}'
        reconstructed += f' {closing}' if not reconstructed.endswith(' ') else closing
        return reconstructed

    # Match className={...} (dynamic expression)
    m_expr = re.search(r'\bclassName=\{([^}]*)\}', tag_inner)
    if m_expr:
        expr = m_expr.group(1).strip()
        if 'focus-visible:' not in expr:
            # Wrap with template literal or prepend
            classes_expr = f"`{FOCUS_CLASSES} ${{({expr})}}`"
        else:
            classes_expr = expr
        tag_inner_no_cn = (tag_inner[:m_expr.start()] + tag_inner[m_expr.end():]).strip()
        reconstructed = f'<button className={{{classes_expr}}}'
        if tag_inner_no_cn:
            reconstructed += f' {tag_inner_no_cn}'
        reconstructed += f' {closing}' if not reconstructed.endswith(' ') else closing
        return reconstructed

    # No className found at all
    reconstructed = f'<button className="{FOCUS_CLASSES}"'
    if tag_inner:
        reconstructed += f' {tag_inner}'
    reconstructed += f' {closing}' if not reconstructed.endswith(' ') else closing
    return reconstructed

def main():
    files = glob.glob('learning_platform/client/src/**/*.tsx', recursive=True)
    files = [f for f in files if '__tests__' not in f]

    total_buttons = 0
    updated_files = 0

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        spans = find_button_spans(content)
        if not spans:
            continue

        total_buttons += len(spans)
        # Replace spans from end to beginning so indices remain valid
        new_content = content
        file_changed = False

        for start, end in reversed(spans):
            original_tag = content[start:end]
            transformed = transform_button_tag(original_tag)
            if transformed != original_tag:
                new_content = new_content[:start] + transformed + new_content[end:]
                file_changed = True

        if file_changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files += 1
            print(f"Updated {fpath} ({len(spans)} buttons)")

    print(f"\nDone! Processed {total_buttons} buttons across {len(files)} files. Updated {updated_files} files.")

if __name__ == '__main__':
    main()
