# Troubleshooting & Production Edge Cases

### 1. Handoff Oscillation (Ping-Pong Loop)
- **Symptom**: Triage agent transfers to Support agent, which immediately transfers back to Triage agent.
- **Root Cause**: Both agents' classification prompts lack unambiguous domain boundary definitions.
- **Fix**: Add mutual exclusion rules and maintain an active session history of visited agents, forbidding re-routing to the caller without new user input.

### 2. Context Amnesia After Agent Handoff
- **Symptom**: After transferring to Billing Agent, the agent asks: "What is your name and what can I help you with?"
- **Root Cause**: Execution engine wiped conversation history upon switching agent pointers.
- **Fix**: Persist the conversation message list across agent handoffs while dynamically switching only the active system prompt and tool definitions.
