# Physical AI & Humanoid Robotics Constitution

<!--
SYNC IMPACT REPORT
==================
Version Change: INITIAL → 1.0.0
Created: 2025-12-13
Ratification: First constitution for Physical AI & Humanoid Robotics textbook project

Modified Principles: N/A (initial creation)
Added Sections:
  - 6 Core Principles (Simplicity, Accuracy, Minimalism, AI-Native Development, Free-Tier First, Accessibility)
  - Development Standards section
  - Quality Gates section
  - Governance rules

Removed Sections: N/A

Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section will reference these 6 principles
  ✅ spec-template.md - Requirements align with accuracy and minimalism principles
  ✅ tasks-template.md - Task structure supports AI-Native Development workflow
  ⚠️  All command files - Should reference claude-code as primary development tool

Follow-up TODOs:
  - None - All placeholders filled with concrete values
  - Review quarterly for alignment with ROS 2, Docusaurus, and free-tier service updates
-->

## Core Principles

### I. Simplicity

**Rule**: Prefer simple solutions over clever ones; implement one feature at a time with full testing before moving to the next.

**Rationale**: Simplicity reduces cognitive load, makes code maintainable, and prevents over-engineering. In an educational project built with AI assistance, clear and straightforward implementations are more valuable than optimized but complex solutions.

**Non-Negotiable Requirements**:
- No premature abstractions - three similar lines of code is better than a forced pattern
- Remove unused code completely (no backwards-compatibility hacks like `_unused_vars` or `// removed` comments)
- One feature per implementation cycle - fully tested and deployed before starting the next
- Clear code prioritized over concise code

### II. Accuracy

**Rule**: All technical content MUST be verified against official sources; all code examples MUST be functional and tested before publication.

**Rationale**: As an educational resource, technical accuracy is paramount. Incorrect information damages learning and erodes trust. Every claim, code snippet, and diagram must reflect current best practices.

**Non-Negotiable Requirements**:
- Cross-check all technical claims with official documentation (ROS 2, NVIDIA Isaac Sim, etc.)
- Test every code example in the target environment before publishing
- RAG system responses MUST be grounded in textbook content only - no hallucinations permitted
- Label opinions vs. facts clearly; use "MUST" for requirements, "SHOULD" for recommendations
- Peer review by subject matter experts for each chapter before release
- 90%+ technical accuracy verified through expert review

### III. Minimalism

**Rule**: Essential features only in MVP; lightweight dependencies with total bundle size <10MB; zero-cost operation on free-tier services only.

**Rationale**: Resource constraints drive focus. Free-tier limitations force thoughtful design decisions. Students worldwide should access this resource regardless of bandwidth or economic constraints.

**Non-Negotiable Requirements**:
- MVP features defined and locked before implementation - no scope creep
- Total frontend bundle size <10MB (Docusaurus build output)
- Images optimized to <100KB each, maximum 5 per chapter
- Dependencies vetted for size and necessity - justify each addition
- Design for graceful degradation when free-tier limits approached
- Excluded features documented explicitly (no user authentication, video content, certificates, payments, mobile apps)

### IV. AI-Native Development

**Rule**: Leverage Claude CLI (claude-code) for implementation tasks; human oversight MUST be maintained for architecture decisions, quality assurance, and educational content review.

**Rationale**: Claude CLI accelerates development for repetitive tasks, code generation, and testing. However, human judgment is essential for architectural choices, pedagogical quality, and strategic direction.

**Non-Negotiable Requirements**:
- Use Claude CLI for: code scaffolding, test generation, content drafting, refactoring, documentation
- Human decision required for: architecture choices, technology selection, content accuracy verification, principle amendments
- Document all AI-generated code decisions in comments or design docs
- Iterative refinement workflow: generate → review → refine → approve
- Update `/sp.context` file after major milestones to preserve project state
- Task prompts MUST be specific with clear acceptance criteria (see Development Standards)

### V. Free-Tier First

**Rule**: Every component MUST operate within free-tier limits; no paid services permitted; monitor usage proactively to prevent tier violations.

**Rationale**: Zero-cost operation ensures project sustainability without funding and maximizes accessibility for learners in all economic contexts.

**Non-Negotiable Requirements**:
- **Qdrant Cloud**: ≤1GB storage (~3,000 vector chunks maximum)
- **Neon PostgreSQL**: ≤0.5GB storage (query logs and metadata only, no content storage)
- **Groq API**: ≤30 requests/minute (implement caching and rate limiting)
- **Railway/Render**: ≤500 hours/month, ≤512MB RAM (single lightweight instance)
- **GitHub Pages**: ≤1GB site size, ≤100GB bandwidth/month
- Weekly monitoring of usage across all services
- Implement caching (Redis for common RAG queries) to reduce API calls
- Rate limit users to 10 queries/minute per IP to prevent tier violations
- Fallback mechanisms when limits approached (e.g., static FAQ when RAG unavailable)

### VI. Accessibility

**Rule**: WCAG 2.1 Level AA compliance minimum; keyboard navigation MUST be fully functional; support viewport widths 320px-1920px; optimize for slow connections (<1 Mbps).

**Rationale**: Educational resources must be accessible to all learners regardless of ability, device, or connection quality. Accessibility is a fundamental right, not a feature.

**Non-Negotiable Requirements**:
- Lighthouse Accessibility score ≥95/100
- All images MUST have descriptive alt text (<125 characters)
- Proper heading hierarchy (h1 → h2 → h3, no skipping levels)
- ARIA labels on all interactive elements (buttons, inputs, modals)
- Keyboard navigation support: Tab, Enter, Escape for all interactive features
- Color contrast ratios ≥4.5:1 for normal text, ≥3:1 for large text
- Screen reader compatibility verified with NVDA or JAWS
- Mobile-responsive layouts tested on 320px, 768px, 1024px, 1920px viewports
- Chatbot modal full-screen on mobile devices
- Code blocks with horizontal scrolling on narrow viewports
- No functionality requiring mouse hover (ensure touch alternatives)

## Development Standards

### Code Quality Gates

**Python (Backend)**:
- Style: PEP 8 compliance verified with `ruff`
- Formatting: `black` (line length 88 characters)
- Type checking: `mypy` in strict mode
- Docstrings: Required for all public functions (Google style)
- Test coverage: ≥80% overall, ≥95% for critical paths (RAG, API endpoints)

**JavaScript/React (Frontend)**:
- Style: Airbnb JavaScript guide
- Formatting: Prettier
- Linting: ESLint with recommended rules
- Type checking: TypeScript encouraged for complex components
- Test coverage: ≥70% for UI components (focus on logic, not rendering)

**Git Commits**:
- Format: `<type>(<scope>): <subject>` (Conventional Commits)
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Examples: `feat(rag): add MMR reranking`, `fix(chatbot): resolve mobile overflow`
- Each commit MUST represent atomic, testable change

### Documentation Requirements

Every module MUST include:
1. **Purpose**: Clear one-sentence description
2. **Dependencies**: External libraries/services required
3. **Usage Example**: Minimal working code snippet
4. **Error Handling**: Exceptions that can be raised
5. **Testing**: Command to run unit tests

## Quality Gates

### Pre-Deployment Checklist

All items MUST pass before production deployment:

**Testing**:
- [ ] All unit tests passing (pytest for backend, Jest for frontend)
- [ ] Integration tests passing (API endpoints, database connections)
- [ ] End-to-end tests passing (Playwright for critical user flows)
- [ ] Code coverage ≥80% overall

**Performance**:
- [ ] Lighthouse Performance score ≥90/100
- [ ] RAG query response time <3 seconds (p95)
- [ ] Page load time <2 seconds on 3G connection
- [ ] Build time <5 minutes
- [ ] Bundle size <10MB

**Accessibility**:
- [ ] Lighthouse Accessibility score ≥95/100
- [ ] Keyboard navigation functional on all pages
- [ ] Screen reader tested (NVDA or JAWS)
- [ ] Color contrast verified (≥4.5:1)

**Content Quality**:
- [ ] All code examples tested and functional
- [ ] Technical accuracy verified by subject matter expert
- [ ] No broken internal or external links
- [ ] Images optimized (<100KB each)
- [ ] Grammar and spelling checked

**Infrastructure**:
- [ ] Environment variables documented
- [ ] Health check endpoint returns 200
- [ ] Database migrations tested
- [ ] Rollback plan documented
- [ ] Monitoring configured (UptimeRobot, Google Analytics)

### RAG System Quality Gates

**Accuracy**:
- [ ] 85%+ relevance score on 50-question test set
- [ ] 100% of responses include chapter citations
- [ ] Out-of-scope queries handled gracefully (fallback responses)
- [ ] No hallucinations detected (entailment checking enabled)

**Performance**:
- [ ] Query embedding generation <500ms
- [ ] Qdrant vector search <1 second
- [ ] Groq API response <2 seconds
- [ ] Total end-to-end response time <3 seconds (p95)

**Safety**:
- [ ] Input validation blocks SQL injection, XSS, prompt injection
- [ ] Rate limiting functional (10 queries/minute per user)
- [ ] Error handling returns user-friendly messages
- [ ] Query logs stored with timestamps (Neon PostgreSQL)

## Governance

### Amendment Procedure

1. **Proposal**: Document proposed change with rationale in GitHub Discussion
2. **Review**: Maintainer reviews against project mission and constraints
3. **Impact Analysis**: Assess effect on templates, existing code, deployment
4. **Approval**: Human maintainer approval required (AI cannot amend constitution)
5. **Migration**: Update all dependent files (templates, commands, guidance docs)
6. **Version Bump**: Increment version per semantic versioning rules
7. **Communication**: Update CHANGELOG.md and notify contributors

### Versioning Policy

Constitution follows **Semantic Versioning** (MAJOR.MINOR.PATCH):

- **MAJOR**: Backward-incompatible changes (remove principle, redefine governance)
- **MINOR**: Backward-compatible additions (add principle, expand section)
- **PATCH**: Clarifications, typo fixes, non-semantic refinements

### Compliance Review

- **Frequency**: Review compliance quarterly (every 3 months)
- **Scope**: Verify templates, code, and documentation align with constitution
- **Trigger**: Also review when major dependencies updated (ROS 2 release, Docusaurus major version)
- **Owner**: Human maintainer conducts review; Claude CLI assists with analysis

### Constitution Authority

- This constitution **supersedes** all other practices, guidelines, and preferences
- All pull requests MUST verify compliance before merge
- Complexity MUST be justified against Simplicity and Minimalism principles
- Runtime development guidance: See `/sp.context` for current project state and active tasks

### Enforcement

- **Code Review**: All PRs checked for principle violations
- **CI/CD Gates**: Automated checks for quality gates (test coverage, bundle size, accessibility)
- **Documentation**: Architecture Decision Records (ADRs) MUST justify deviations with migration plan
- **Rollback**: Non-compliant deployments MUST be rolled back immediately

---

**Version**: 1.0.0 | **Ratified**: 2025-12-13 | **Last Amended**: 2025-12-13
