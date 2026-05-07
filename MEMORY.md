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
    - `.env.example` updated with Google and Notifier settings.
    - `app/services/gmail_service.py` implemented (OAuth2 + Fetch).
    - `app/services/prefilter_service.py` implemented (Keyword-based).
    - `app/services/notifier_service.py` implemented (Telegram Bot API).
    - `app/workers/tasks.py` updated with `poll_gmail` logic and Redis checkpointing.
    - Celery Beat configured for 5-minute polling.
    - `docker-compose.yml` updated with `beat` service.
    - LangGraph workflow implemented for AI-driven classification, extraction, and summarization.
    - AI inference switched from OpenAI to Groq for high-speed processing.
    - `requirements.txt` corrected with compatible `0.x` series for LangChain and LangGraph to fix build errors.
    - `app/workflows/` structure created with state, nodes, and graph definition.
    - `poll_gmail` task updated to use LangGraph orchestration.
    - Fault tolerance implemented with `RetryPolicy` and `MemorySaver` checkpointing in LangGraph.

## 🏗 Architectural Decisions
- **Orchestration:** LangGraph for workflow state management and routing.
- **Tooling:** MCP (Model Context Protocol) for modular, reusable capabilities.
- **Processing:** Celery + Redis for async Gmail polling and processing.
- **Intelligence:** Hybrid approach (Rule-based prefiltering -> LLM classification).

## 📅 Roadmap
- [ ] Initialize FastAPI application structure.
- [ ] Set up MCP server and basic Gmail tools.
- [x] Implement LangGraph orchestration flow.
- [x] Configure Celery workers and Redis.
- [x] Integrate Telegram notification bot.
- [ ] Set up LangSmith for observability.

## 📝 Notes
- Ensure OAuth2 flow for Gmail is handled securely.
- Focus on high-value categories (INTERVIEW, OFFER) for initial notification logic.
