# AGENT_HANDOFF_CONTRACTS.md

## Purpose

This document defines **explicit handoff contracts** between agents in the
Unified AI-Driven Book & RAG System.

A handoff is a formal boundary.
If a contract is violated, downstream work is invalid.

No agent is allowed to “fix it later”.

---

## Global Handoff Rules

These rules apply to all agent transitions:

- All handoffs must be explicit, no implicit context sharing
- Inputs and outputs must be structured and verifiable
- An agent may only act after its input contract is satisfied
- Silence is NOT acceptance
- Any ambiguity triggers rejection, not interpretation

---

## Contract 1: Spec Guardian → Claude Code Author

### Input Requirements

The Spec Guardian must provide:

- Finalized Spec-Kit Plus files
- Approved chapter and section structure
- Declared tone and audience
- Explicit constraints and prohibitions

Input must be:
- Complete
- Unambiguous
- Versioned

### Output Expectations (from Claude Code Author)

Claude Code Author must return:

- Markdown files only
- Content strictly matching the provided structure
- No additional sections, concepts, or examples

### Rejection Conditions

Claude Code Author must reject input if:

- Any spec field is missing
- Chapter or section definitions are vague
- Tone or scope is undefined

---

## Contract 2: Claude Code Author → Reviewer / Auditor

### Input Requirements

Claude Code Author must submit:

- Generated Markdown content
- Reference to the spec version used
- Zero explanatory commentary unless requested

### Output Expectations (from Reviewer)

Reviewer must produce:

- Pass or Reject decision
- Checklist-based failure report if rejected
- No content edits

### Rejection Conditions

Reviewer must reject if:

- Any FAILURE_CHECKLIST critical item fails
- Content exceeds or deviates from spec
- Formatting or structure is inconsistent

---

## Contract 3: Spec Guardian → Technical Implementer

### Input Requirements

Spec Guardian must provide:

- Approved RAG architecture constraints
- Allowed tech stack list
- Data flow definitions
- Retrieval and refusal rules

No prose descriptions without formal constraints.

### Output Expectations (from Technical Implementer)

Technical Implementer must return:

- Production-ready code
- Deterministic retrieval logic
- Explicit refusal handling
- No alternative tooling

### Rejection Conditions

Technical Implementer must reject if:

- Retrieval rules are underspecified
- Context boundaries are unclear
- Tooling choices are ambiguous

---

## Contract 4: Technical Implementer → RAG Integrity Enforcer

### Input Requirements

Technical Implementer must submit:

- Retrieval logic
- Prompt constraints
- Vector query configuration
- Refusal behavior implementation

### Output Expectations (from RAG Integrity Enforcer)

RAG Integrity Enforcer must return:

- Pass or Reject verdict
- Specific grounding violations if rejected
- Confirmation of scoped query isolation

### Rejection Conditions

RAG Integrity Enforcer must reject if:

- Answers can be generated without retrieved context
- User-selected text scope can be bypassed
- Cross-chapter leakage is possible

---

## Contract 5: RAG Integrity Enforcer → Reviewer / Auditor

### Input Requirements

RAG Integrity Enforcer must provide:

- Verified grounding guarantees
- Known failure modes
- Tested refusal scenarios

### Output Expectations (from Reviewer)

Reviewer must:

- Apply FAILURE_CHECKLIST RAG section
- Approve or reject system readiness
- Log risks, not fixes

---

## Conflict Resolution Protocol

If two agents disagree:

1. Work stops
2. Conflict is documented
3. Spec Guardian resolves
4. Pipeline restarts from last valid state

No agent may override another agent’s rejection.

---

## Anti-Patterns (Explicitly Forbidden)

- “I assumed…” handoffs
- Fixing upstream mistakes downstream
- Combining roles to save time
- Informal approvals
- Partial acceptance

---

## Enforcement Principle

A handoff contract is a gate, not a suggestion.

If the gate fails:
- Nothing proceeds
- No exceptions
- No shortcuts

This is intentional.
