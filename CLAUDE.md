# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interactive textbook for Physical AI and Humanoid Robotics with a RAG-powered chatbot. Built with Docusaurus (frontend) and FastAPI (backend) for free-tier deployment.

## Commands

### Frontend (Docusaurus)
```bash
cd frontend
npm install          # Install dependencies
npm start            # Dev server at localhost:3000
npm run build        # Production build
npm run lint         # ESLint
npm run format       # Prettier
npm test             # Jest unit tests
npm run test:e2e     # Playwright e2e tests
```

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt    # Install dependencies
python -m uvicorn src.api.main:app --reload  # Dev server at localhost:8000
pytest                             # Run tests
pytest --cov=src                   # Tests with coverage
ruff check .                       # Lint
black .                            # Format
mypy src/ --ignore-missing-imports # Type check
```

## Architecture

```
├── frontend/               # Docusaurus site (deployed to GitHub Pages)
│   ├── docs/              # Markdown chapter content
│   ├── src/
│   │   ├── components/    # React components (chatbot modal, etc.)
│   │   ├── hooks/         # Custom React hooks
│   │   └── services/      # API client for backend
│   └── docusaurus.config.js
│
├── backend/               # FastAPI RAG chatbot service
│   ├── src/
│   │   ├── api/          # FastAPI routers and main.py
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # RAG pipeline, vector search, LLM
│   │   └── utils/        # Helpers
│   └── tests/
│
└── .specify/              # Speckit workflow templates
```

### RAG Pipeline Flow
1. User query → FastAPI `/api/chat` endpoint
2. Query embedding via sentence-transformers
3. Vector search in Qdrant Cloud (≤1GB free tier)
4. Context retrieval + Groq LLM (Llama 3.2) for response
5. Query logs stored in Neon PostgreSQL

## Free-Tier Constraints

All components must operate within these limits:
- **Qdrant Cloud**: ≤1GB storage (~3,000 vector chunks)
- **Neon PostgreSQL**: ≤0.5GB storage
- **Groq API**: ≤30 requests/minute (implement caching)
- **GitHub Pages**: ≤1GB site, ≤100GB bandwidth/month
- **Bundle size**: <10MB total

## Code Standards

### Python (Backend)
- PEP 8 via `ruff`, formatting via `black`
- Type hints required, checked with `mypy` strict mode
- Google-style docstrings for public functions
- Test coverage ≥80%

### JavaScript/React (Frontend)
- Airbnb style guide with ESLint
- Formatting via Prettier

### Git Commits
- Conventional Commits format: `<type>(<scope>): <subject>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Example: `feat(rag): add MMR reranking`

## Quality Gates

Before merge:
- Lighthouse Accessibility ≥95/100
- Bundle size <10MB (CI enforced)
- All code examples in docs must be tested and functional
- RAG responses must include chapter citations

## Key Files

- `backend/.env.example` - Required environment variables (Qdrant, Neon, Groq, Redis)
- `.specify/memory/constitution.md` - Project principles and governance
- `.github/workflows/test.yml` - CI test pipeline
- `.github/workflows/deploy.yml` - GitHub Pages deployment
