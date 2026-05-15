# Enterprise Agent Platform

An AI agent orchestration monorepo with RAG capabilities, business domain MCP tools, and a Vue.js frontend.

> **Status**: Early MVP — only `rag-service` is fully implemented. Other services are scaffolded.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       frontend-web (Vue.js)                     │
│                    Chat · Knowledge · Traces · Settings          │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    agent-gateway (LangGraph)                     │
│        intent_router → planner → [rag | tool_executor]          │
│                      → synthesizer                               │
│                    MCP Client · Session Memory                   │
└──────┬─────────────────────────────────────┬────────────────────┘
       │                                     │
┌──────▼──────────┐  ┌──────────────────────▼─────────────────────┐
│   rag-service   │  │           mcp-servers (MCP)                │
│   (FastAPI)     │  │  business · knowledge · ops                │
│                 │  │  Tools · Resources · Prompts                │
│  Upload → Chunk │  └──────────────────────┬─────────────────────┘
│  → Embed → Store│                         │
│  → Search       │  ┌──────────────────────▼─────────────────────┐
└─────────────────┘  │         business-service (Spring Boot)     │
                     │  Customer · Inventory · Order · Ticket     │
                     │  MyBatis-Plus · MySQL · Redis               │
                     └────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| RAG Service | Python 3.12+, FastAPI, Pydantic, pypdf |
| Embeddings | Hash-based (SHA-256, 128-dim) — offline MVP, no external API |
| Vector Store | Local JSON files with Qdrant-compatible interface |
| Retrieval | Hybrid: dense cosine similarity + keyword overlap, weighted reranking |
| Agent Gateway | LangGraph workflow with MCP client (planned) |
| Business Service | Java, Spring Boot, MyBatis-Plus, MySQL, Redis (planned) |
| Frontend | Vue.js, Pinia, Vue Router (planned) |
| MCP Servers | Model Context Protocol — business, knowledge, ops tools (planned) |
| Package Manager | uv (Python) |
| Testing | pytest + httpx |

## Project Structure

```
enterprise-agent-platform/
├── rag-service/            # Document ingestion, embedding, and hybrid search
├── agent-gateway/          # LangGraph-based agent orchestrator (scaffolded)
├── mcp-servers/            # MCP tool servers
│   ├── business-mcp-server/
│   ├── knowledge-mcp-server/
│   └── ops-mcp-server/
├── business-service/       # Spring Boot backend (scaffolded)
├── frontend-web/           # Vue.js SPA (scaffolded)
├── data-infra/             # MySQL, Qdrant, Redis, ES, RabbitMQ configs
└── observability/          # Logs, traces, metrics, dashboards
```

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### Run rag-service

```bash
# Install dependencies
cd rag-service && uv sync

# Start dev server
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Run Tests

```bash
cd rag-service && uv run pytest
```

## rag-service API

The RAG pipeline: **Upload -> Load -> Chunk -> Embed -> Store -> Search**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/rag/documents/upload` | Upload a document (Markdown, TXT, PDF) |
| GET | `/api/rag/documents` | List all indexed documents |
| POST | `/api/rag/documents/reindex` | Re-process a document by ID |
| GET | `/api/rag/chunks/{chunk_id}` | Retrieve a specific chunk |
| POST | `/api/rag/search` | Hybrid search with filters |
| GET | `/api/rag/collections/status` | Storage and index statistics |
| GET | `/api/rag/health` | Health check |

### Search Example

```bash
curl -X POST http://localhost:8000/api/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query": "your search query", "top_k": 5}'
```

## Key Design Decisions

- **Offline-first embeddings** — Hash-based vector generation avoids external API dependencies during development. Swap in a real embedding client by implementing the same interface.
- **Local JSON store** — Mimics Qdrant's API using flat JSON files, so no running Qdrant instance is needed for development.
- **Hybrid retrieval** — Combines dense (vector cosine similarity) and keyword (feature overlap) retrieval with 65/35 weighted reranking.
- **MCP protocol** — The agent gateway discovers and invokes tools via Model Context Protocol, decoupling tool registration from orchestration logic.

## Roadmap

- [ ] Implement `agent-gateway` with LangGraph workflow
- [ ] Implement `knowledge-mcp-server` to bridge rag-service with the agent
- [ ] Implement `business-mcp-server` with order/customer/inventory tools
- [ ] Implement `business-service` Spring Boot backend with MySQL
- [ ] Build `frontend-web` Vue.js chat interface
- [ ] Add real embedding provider support (e.g., OpenAI, Jina)
- [ ] Add Qdrant as production vector store
- [ ] Observability: logging, tracing, metrics
- [ ] Docker Compose for local development stack

## License

MIT
