# Project Memory: AI Career Inbox Intelligence

This file tracks the current state, progress, and architectural decisions of the AI Career Inbox Intelligence platform.

## 🚀 Current Status
- **Phase:** Initial Setup & Infrastructure Testing
- **Completed:**
    - Project structure defined and folders created.
    - Core Cursor rules established (`core-standards`, `ai-workflow`, `backend-infra`, `git-standards`).
    - `.cursorignore` and `.gitignore` configured.
    - `MEMORY.md` initialized.
    - `requirements.txt` added with specific, compatible versions (fixed loguru version and updated others to latest stable 2026 releases).
    - `Makefile` created for easy CLI commands.
    - `docker-compose.yml` created for local Redis and Celery setup.
    - `Dockerfile` added for application services.
    - `app/core/config.py` updated with Celery settings.
    - `app/core/celery_app.py` and `app/workers/tasks.py` created.
    - Infrastructure verified (Redis + Celery + Flower).
    - Initial test scripts cleaned up.
    - `.env.example` created.

## 🏗 Architectural Decisions
- **Orchestration:** LangGraph for workflow state management and routing.
- **Tooling:** MCP (Model Context Protocol) for modular, reusable capabilities.
- **Processing:** Celery + Redis for async Gmail polling and processing.
- **Intelligence:** Hybrid approach (Rule-based prefiltering -> LLM classification).

## 📅 Roadmap
- [ ] Initialize FastAPI application structure.
- [ ] Set up MCP server and basic Gmail tools.
- [ ] Implement LangGraph orchestration flow.
- [ ] Configure Celery workers and Redis.
- [ ] Integrate Google Chat notification webhooks.
- [ ] Set up LangSmith for observability.

## 📝 Notes
- Ensure OAuth2 flow for Gmail is handled securely.
- Focus on high-value categories (INTERVIEW, OFFER) for initial notification logic.
