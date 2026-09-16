# Module 02: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Cost-Optimized Batch Contextualization at Scale
**Question**: You need to ingest 500,000 document chunks. Generating contextual headers using Claude 3.5 Sonnet would cost $15,000 in API tokens. How do you design an ingestion architecture that achieves $> 95\%$ of Sonnet's contextual quality at $< 5\%$ of the cost?

**Solution**:
1. **Model Selection**: Switch auxiliary context generation to an ultra-low-cost small model (e.g. Gemini 1.5 Flash, Claude 3 Haiku, or fine-tuned Llama-3-8B). Small models excel at localized summarization.
2. **Prompt Caching**: Structure the context prompt so that the full parent document is cached in the API provider's prompt cache:
   ```
   [CACHED DOCUMENT TEXT]
   Here is chunk 14: ... Provide 2 sentences of context.
   ```
   Prompt caching cuts input token costs by $75\% - 90\%$.
3. **Total Cost**: Drops from $15,000 to $< $450$.

---

### Scenario 2: Context Bleed & Hallucination Prevention
**Question**: What safeguards prevent the auxiliary model from hallucinating false context that poisons the retrieval index?

**Solution**:
1. Constrain generation with strict temperature $T = 0.0$.
2. Limit output length to $\le 60$ tokens with a rigid system prompt: *"Give only succinct factual context regarding document title, section, and entities. Never invent details."*
3. Keyword verification: Ensure all named entities in $p_i$ exist verbatim in document $\mathcal{D}$.
