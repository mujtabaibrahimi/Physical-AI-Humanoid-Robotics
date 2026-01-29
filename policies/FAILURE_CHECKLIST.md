# FAILURE_CHECKLIST.md

## Purpose

This checklist is used to evaluate whether Claude Code outputs,
the book content, or the RAG chatbot implementation **failed spec compliance**.

If any critical item fails, the output is rejected.

---

## A. Spec Compliance Failures (CRITICAL)

Fail immediately if ANY of the following are true:

- Content includes chapters or sections not defined in Spec-Kit Plus
- Required spec fields are missing or partially implemented
- Assumptions were made instead of requesting clarification
- Output contradicts the spec or CLAUDE.md
- Tone or scope deviates from defined constraints

---

## B. Book Content Failures

### Structure
- Missing Docusaurus frontmatter
- Broken Markdown hierarchy
- Inconsistent navigation or ordering
- Sections present without objectives fulfilled

### Content Quality
- Fluff, filler, or motivational language
- Rhetorical questions without purpose
- Undeclared terminology
- Examples added without explicit instruction

---

## C. AI Behavior Failures

- Hallucinated facts, tools, or libraries
- Explanations of internal reasoning without request
- “Helpful” additions outside scope
- Creative improvisation

---

## D. RAG Chatbot Failures (CRITICAL)

- Answers not grounded in retrieved content
- Responses when retrieval returns no relevant context
- Mixing global context with user-selected text queries
- Cross-chapter leakage in scoped queries
- Failure to refuse when data is unavailable

Expected refusal message:
> The answer is not available in the selected content.

---

## E. Data & Retrieval Failures

- Improper chunking of book content
- Missing or incorrect metadata
- Embeddings not aligned to source text
- Vector search not deterministic
- Postgres and vector DB responsibilities mixed

---

## F. Code Quality Failures

- Pseudocode when production code was expected
- Commented-out logic
- Undocumented endpoints
- Silent failure paths
- Non-deterministic behavior

---

## G. Reproducibility Failures

- Outputs change with same inputs
- No versioning strategy
- Unclear build or deployment steps
- Hidden configuration assumptions

---

## H. Translation Failures (CRITICAL)

Fail immediately if ANY of the following are true:

- Translation occurs without retrieved or user-selected content
- Language outside Pashto or Dari is used
- Translation adds explanation, clarification, or summary
- Technical terms are incorrectly translated or localized
- Structure of the original text is altered
- Translation proceeds when retrieval returned no content

Expected refusal message:
"The requested content is not available for translation."

---

## Final Verdict Rules

- Any CRITICAL failure = REJECT
- Two or more non-critical failures = REJECT
- One non-critical failure = FIX REQUIRED

No exceptions.
