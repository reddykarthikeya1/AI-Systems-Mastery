"""
Module 25: AI Prompt Template & Streaming Simulator
Run: python try_it_yourself.py
"""

import time


def render_prompt(template, **kwargs):
    return template.format(**kwargs)


def stream_tokens(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.06)


def main():
    print("=" * 60)
    print("  MODULE 25: AI ENGINEERING PLAYGROUND [*]")
    print("=" * 60)

    template = "System: You are an expert {role}.\nUser: Explain {topic} in one sentence."
    prompt = render_prompt(template, role="Database Architect", topic="Database Indexing")
    print(f"Rendered Prompt:\n{prompt}\n")

    print("Streaming AI Response:")
    mock_reply = "An index is like a book catalog that lets the database find data without reading every page."
    for token in stream_tokens(mock_reply):
        print(token, end="", flush=True)
    print("\n\n[OK] Prompt templating and token streaming simulated!")


if __name__ == "__main__":
    main()
