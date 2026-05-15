# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Enterprise Agent Platform — a monorepo containing an AI agent orchestration system with RAG capabilities, business domain MCP tools, and a Vue.js frontend. The project is in early MVP stage; only the `rag-service` has implemented code. Other services (`agent-gateway`, `business-service`, `frontend-web`, `mcp-servers`) are scaffolded with directory structure but empty source files.

## Tech Stack

- **Python 3.12+** — managed with **uv** (not pip/poetry)
- **rag-service**: FastAPI + Pydantic, local JSON-backed vector store, hash-based embeddings
- **agent-gateway** (planned): LangGraph-based agent orchestrator with MCP client integration
- **business-service** (planned): Java Spring Boot with MyBatis-Plus, MySQL, Redis
- **frontend-web** (planned): Vue.js with Pinia stores, Vue Router
- **mcp-servers** (planned): Model Context Protocol servers for business, knowledge, and ops tools

## Common Commands

### rag-service (the only implemented service)

```bash
# Install dependencies
cd rag-service && uv sync

# Run the dev server
cd rag-service && uv run uvicorn app.main:app --reload

# Run all tests
cd rag-service && uv run pytest

# Run a single test file
cd rag-service && uv run pytest tests/test_api.py

# Run a single test
cd rag-service && uv run pytest tests/test_api.py::test_function_name
```

## Git Operations

### GitHub 信息

- **仓库地址**: https://github.com/ORION-star-code/enterprise-agent-platform
- **用户名**: ORION-star-code
- **远程**: `origin` → `https://github.com/ORION-star-code/enterprise-agent-platform.git`

### gh CLI

Windows 下 gh CLI 安装路径：`C:\Program Files\GitHub CLI\gh.exe`。若终端未刷新 PATH，需使用全路径。

```bash
# 查看登录状态
gh auth status

# 创建仓库
gh repo create <name> --public --source=. --remote=origin --push

# 查看 PR
gh pr list
gh pr view <number>

# 查看 Issue
gh issue list
gh issue view <number>
```

### 常用 Git 命令

```bash
# 提交
git add .
git commit -m "feat: 描述"

# 推送
git push origin main

# 拉取
git pull origin main

# 分支
git checkout -b feature/xxx
git push -u origin feature/xxx
```

### 提交规范

使用 Conventional Commits 前缀：

- `feat:` — 新功能
- `fix:` — 修复 bug
- `refactor:` — 重构
- `docs:` — 文档
- `test:` — 测试
- `chore:` — 构建/工具链

## Architecture

### rag-service (FastAPI, fully implemented)

The RAG pipeline follows this flow: **upload -> load -> chunk -> embed -> store -> search**.

- **Loaders** (`app/loaders/`): Parse documents by format — markdown/text (direct read), PDF (pypdf), DOCX (python-docx). The `SUPPORTED_LOADERS` dict in `app/tasks/document_ingest_task.py` maps file extensions to loader functions.
- **Chunkers** (`app/chunkers/`): `HeadingChunker` splits by markdown headings first, then `RecursiveChunker` further splits large sections into fixed-size chunks.
- **Embeddings** (`app/embeddings/`): `HashEmbeddingClient` produces deterministic vectors via SHA-256 hashing of text features (words + character n-grams). This is an offline MVP — no external embedding API needed. The `cosine_similarity` function is used for vector comparison.
- **Vector Store** (`app/vector_store/`): `LocalQdrantStore` is a JSON-file-backed store (Qdrant-compatible interface) using `documents.json` and `chunks.json` in `rag-service/storage/`. `CollectionManager` handles initialization and paths.
- **Retrievers** (`app/retrievers/`): `HybridRetriever` combines `DenseRetriever` (cosine similarity on embeddings) and `KeywordRetriever` (feature overlap scoring), merged by `SimpleReranker` with 65/35 dense/keyword weighting.
- **API** (`app/api/`): Three routers — document CRUD + upload, search, and collection status. All under `/api/rag/` prefix.
- **Schemas** (`app/schemas/`): Pydantic models for documents, chunks, and search requests/responses.

### agent-gateway (scaffolded, not implemented)

Designed as a LangGraph workflow with these nodes: `intent_router` -> `planner` -> `rag` / `tool_executor` / `human_review` -> `synthesizer`. Uses MCP client to discover and call tools from the MCP servers. State managed via `app/graph/state.py`.

### mcp-servers (scaffolded, not implemented)

Three MCP servers following the Model Context Protocol:
- **business-mcp-server**: Tools for orders, customers, inventory, tickets; resources for MySQL schema and business rules; prompts for order summaries and customer replies. Clients for business-service API and MySQL.
- **knowledge-mcp-server**: Tools for document search, citations; resources for policies, FAQs, SOPs. Client calls rag-service.
- **ops-mcp-server**: Operational tooling (structure only).

### business-service (scaffolded, not implemented)

Spring Boot Java service with modules for customer, inventory, order, and ticket management. Uses MyBatis-Plus for MySQL, Redis for caching. Config in `src/main/resources/application.yml`.

### frontend-web (scaffolded, not implemented)

Vue.js SPA with views for chat, knowledge base, tool traces, and settings. API clients for agent, documents, and sessions.

### data-infra & observability (placeholder directories)

`data-infra/` has `.gitkeep` placeholders for MySQL, Qdrant, Redis, Elasticsearch, RabbitMQ. `observability/` has placeholders for logs, traces, metrics, dashboards, SQL.

## Key Design Decisions

- **Offline-first embeddings**: The hash-based embedding client avoids external API dependencies during development. To switch to real embeddings, implement a new client matching the `HashEmbeddingClient` interface and update `embedding_config.py`.
- **Local JSON store instead of Qdrant**: The `LocalQdrantStore` mimics Qdrant's interface using flat JSON files, enabling development without a running Qdrant instance. The `CollectionManager` manages storage paths at `rag-service/storage/`.
- **Hybrid retrieval**: Search uses both dense (vector) and keyword retrieval with weighted reranking (65% dense, 35% keyword by default).
- **MCP protocol**: The agent-gateway communicates with tool servers via MCP (Model Context Protocol), allowing tool discovery and invocation to be decoupled from the orchestrator.

---

## Harness Five Subsystems

This project follows the Harness Engineering methodology. Five subsystems ensure agent effectiveness.

### 1. Instruction Subsystem
- Entry file: `CLAUDE.md` (this file) — project overview, run commands, hard constraints
- Feature manifest: `FEATURES.md` — behavior + verification + state for each feature
- Decision log: `DECISIONS.md` — what, why, when for each design decision

### 2. Tools Subsystem
- Minimum privilege: agent gets only the access needed for current task
- Standardized commands below — always use these, not ad-hoc commands

### 3. Environment Subsystem
- Python 3.12+ managed by **uv** (not pip/poetry)
- Dependencies locked in `pyproject.toml` + `uv.lock`
- Self-describing: `pyproject.toml` specifies all deps and versions

### 4. State Subsystem
- `PROGRESS.md` — current commit, test status, completed/in-progress/blocked items, next steps
- `DECISIONS.md` — design decision log
- `FEATURES.md` — feature manifest with verification-based state machine
- Git commits serve as checkpoints — one atomic commit per logical unit

### 5. Feedback Subsystem
- Verification commands (see below) — run after every change
- Three-layer verification: syntax -> runtime behavior -> system-level
- Completion = verification passing, not "code looks done"

---

## Verification Commands

```bash
# Tests (rag-service)
cd rag-service && uv run pytest

# Single test file
cd rag-service && uv run pytest tests/test_api.py

# Single test
cd rag-service && uv run pytest tests/test_api.py::test_function_name

# App starts
cd rag-service && uv run python -c "from app.main import app; print('OK')"
```

---

## Work Rules

- **WIP=1**: Only one feature active at a time. Complete and verify before starting next.
- **Completion evidence**: A feature is "done" when its verification command passes, not when code "looks right."
- **No premature optimization**: Core functionality must pass verification before any refactoring.
- **No scope creep**: Don't "顺便" refactor unrelated code while implementing a feature.

---

## Session Lifecycle

### Session Start (Clock In)
1. Read `PROGRESS.md` — understand current state
2. Read `DECISIONS.md` — recall important decisions
3. Run verification commands — confirm clean state
4. Continue from `PROGRESS.md` "Next Steps"

### Session End (Clock Out)
1. Update `PROGRESS.md` with current status
2. Run full verification — ensure clean state
3. Commit all completed work
4. Verify: build passes, tests pass, no debug artifacts

---

## Session Exit Checklist

- [ ] App starts: `cd rag-service && uv run python -c "from app.main import app; print('OK')"`
- [ ] Tests pass: `cd rag-service && uv run pytest`
- [ ] `PROGRESS.md` updated
- [ ] No debug artifacts (print statements, debugger, TODO hacks)
- [ ] All changes committed
