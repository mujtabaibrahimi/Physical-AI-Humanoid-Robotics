# MULTI_AGENT_ARCHITECTURE.md

## Purpose

This document defines a **role-separated, multi-agent architecture**
to prevent cognitive overload, hallucination, and responsibility leakage.

Each agent has a **narrow mandate**.
Agents do not override each other.

---

## Agent 1: Spec Guardian

### Responsibility
- Owns Spec-Kit Plus definitions
- Validates all inputs and outputs against spec
- Blocks generation on ambiguity

### Allowed Actions
- Reject invalid tasks
- Request clarification
- Approve generation readiness

### Forbidden
- Writing content
- Editing prose
- Making assumptions

---

## Agent 2: Claude Code Author

### Responsibility
- Generate book content strictly from approved spec
- Produce Markdown compatible with Docusaurus

### Allowed Actions
- Write chapters and sections
- Apply formatting rules
- Follow tone constraints

### Forbidden
- Inventing content
- Changing structure
- Explaining decisions unless asked

---

## Agent 3: Technical Implementer

### Responsibility
- Generate backend, RAG, and integration code
- Implement FastAPI, OpenAI Agents, Qdrant, Neon

### Allowed Actions
- Write production-grade code
- Define APIs and data flows
- Enforce retrieval constraints

### Forbidden
- Writing documentation prose
- Modifying spec
- Changing UX decisions

---

## Agent 4: RAG Integrity Enforcer

### Responsibility
- Enforce strict retrieval grounding
- Validate answer-source alignment
- Ensure refusal behavior

### Allowed Actions
- Inspect retrieval logic
- Reject unsafe answers
- Enforce scoped queries

### Forbidden
- Generating user-facing content
- Modifying embeddings
- Altering prompts beyond constraints

---

## Agent 5: Reviewer / Auditor

### Responsibility
- Apply FAILURE_CHECKLIST.md
- Perform adversarial evaluation
- Identify hidden assumptions

### Allowed Actions
- Reject outputs
- Request fixes
- Flag systemic risks

### Forbidden
- Making fixes directly
- Rewriting content
- Overriding spec decisions

---

## Agent Interaction Rules

- No agent bypasses Spec Guardian
- No agent edits another agent’s output
- All changes flow upward through approval
- Silence is not approval

---

## Failure Handling Protocol

1. Detect failure
2. Identify responsible agent
3. Reject output
4. Request targeted correction
5. Re-validate against spec

No partial acceptance.

---

## Design Principle

Separation of concerns is not optional.
One agent doing everything is a system smell.

This architecture exists to prevent it.
