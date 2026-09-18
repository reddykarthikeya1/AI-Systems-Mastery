# Debug Lab: Speculative Decoding Accepts Draft Tokens Past a Rejection
# Course 09 - Module 07 Speculative Decoding Architectures

def draft_model_propose(context, num_speculative_tokens=5):
    """Cheap draft model proposes several tokens ahead greedily. It's usually
    right but occasionally diverges from what the (expensive) target model
    would have generated."""
    # Pretend the draft model gets the first 2 tokens right, then guesses
    # wrong for the rest because it lost track of subject-verb agreement.
    return ["is", "a", "helpful", "assistant", "today"]


def target_model_verify(context, draft_tokens):
    """The target model recomputes logits over the full context + draft
    tokens in one forward pass and returns what IT would have generated at
    each position, for comparison against the draft."""
    # Ground truth the target model would have produced token-by-token.
    return ["is", "a", "great", "helper", "."]


def accept_draft_tokens(draft_tokens, target_tokens):
    """Walk the draft tokens and keep every one that matches the target
    model's own prediction at that position. Speculative decoding must stop
    accepting at the FIRST mismatch: everything the draft model generated
    after a divergence was conditioned on a token the target model never
    actually produced, so it can't be trusted either."""
    accepted = []
    for draft_tok, target_tok in zip(draft_tokens, target_tokens):
        if draft_tok == target_tok:
            accepted.append(draft_tok)
        else:
            accepted.append(target_tok)  # correct the mismatch and keep scanning
    return accepted


if __name__ == "__main__":
    context = ["You"]
    draft = draft_model_propose(context)
    target = target_model_verify(context, draft)

    accepted = accept_draft_tokens(draft, target)

    print(f"Draft model proposed:  {draft}")
    print(f"Target model verified: {target}")
    print("Expected: accept the verified prefix up to and including the first "
          "mismatch position, then discard everything after it (draft tokens "
          "past a rejection were never actually checked against the true "
          "continuation).")
    print(f"Actual accepted sequence: {accepted}")
    print(f"Final sentence: 'You ' + '{' '.join(accepted)}'")
