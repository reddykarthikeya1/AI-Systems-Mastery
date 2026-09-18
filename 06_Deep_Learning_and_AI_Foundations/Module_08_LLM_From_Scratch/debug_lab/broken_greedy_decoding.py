# Debug Lab: Greedy Decoder Repeats the Same Token Forever
# Course 06 - Module 08 LLM From Scratch

def build_bigram_table():
    return {
        "the": "cat",
        "cat": "sat",
        "sat": "on",
        "on": "the",
        "mat": ".",
    }


def greedy_generate(start_token, table, max_tokens=8):
    current = start_token
    generated = [current]
    for _ in range(max_tokens - 1):
        next_token = table.get(current, "<end>")
        generated.append(next_token)
    return generated


if __name__ == "__main__":
    table = build_bigram_table()
    sequence = greedy_generate("the", table)

    print("Generated sequence:")
    print(" ".join(sequence))
    print(f"Unique tokens produced: {len(set(sequence))} out of {len(sequence)} generated")
