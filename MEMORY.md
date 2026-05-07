# Project Memory: AI Career Inbox Intelligence

This file tracks the current state, progress, and architectural decisions of the AI Career Inbox Intelligence platform.

## 🚀 Current Status
- **Phase:** Initial Setup & Architecture Definition
- **Completed:**
    - Project structure defined and folders created.
    - Core Cursor rules established (`core-standards`, `ai-workflow`, `backend-infra`).
    - `.cursorignore` and `.gitignore` configured.
    - `MEMORY.md` initialized.
    - `requirements.txt` added with specific, compatible versions (2026 stable releases).
    - `git-standards.mdc` rule added for Git/GitHub best practices.
    - `Makefile` created for easy CLI commands.

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
