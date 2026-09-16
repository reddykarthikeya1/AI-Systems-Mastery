# Beginner Playground: NVIDIA NeMo Colang & Llama Guard

Welcome to Dialog Guardrails! When building conversational bots, you need strict conversational boundaries and standard safety category checks.

---

## 1. The Core Mental Model: Colang Flows & Llama Guard

- **Colang (NeMo)**: A domain-specific language for modeling dialogue flows as finite state machines. When a user strays into forbidden territory (e.g. politics), Colang halts the LLM and triggers a deterministic diversion flow.
- **Llama Guard (Meta)**: A specialized classifier model fine-tuned on the MLCommons AI Safety Taxonomy (S1-S6 hazard categories: Violence, Hate, Sexual Crimes, Cyberattacks, etc.).

```
 User Input ---> [ Llama Guard Classifier ]  --(Unsafe: S6 Cyberattack)--> [ Block ]
                          |
                       (Safe)
                          v
                 [ Colang Dialog Rails ]   --(Political Intent)--> [ Divert Flow ]
                          |
                       (On-Topic)
                          v
                 [ Main LLM Generator ]
```

---

## 2. Interactive Pure-Python Experiment: Colang Intent Router

```python
def classify_user_intent(text: str) -> str:
    text_lower = text.lower()
    if any(w in text_lower for w in ["election", "president", "vote", "politics"]):
        return "ask_politics"
    elif any(w in text_lower for w in ["hello", "hi", "hey"]):
        return "express_greeting"
    return "general_query"

def colang_flow_step(intent: str) -> str:
    if intent == "ask_politics":
        # Deterministic diversion rail
        return "bot refuse_political_discussion: I am an enterprise support assistant and cannot comment on political topics."
    elif intent == "express_greeting":
        return "bot express_greeting: Hello! How can I assist you with your cloud infrastructure today?"
    return "bot pass_to_llm"

print("User: Hello ->", colang_flow_step(classify_user_intent("Hello there")))
print("User: Who should I vote for? ->", colang_flow_step(classify_user_intent("Who should I vote for in the election?")))
```
