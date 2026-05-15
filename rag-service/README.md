# rag-service

Local MVP RAG service for the enterprise-agent-platform project.

## Features

- Upload Markdown, TXT, and PDF documents.
- Extract text and split it by headings and paragraphs.
- Attach document and chunk metadata.
- Generate deterministic hash embeddings for offline development.
- Store documents and chunks in a local JSON-backed Qdrant-style store.
- Search with dense similarity, keyword matching, and simple hybrid reranking.

## Run

```bash
uv run uvicorn app.main:app --reload
```

## API

- `POST /api/rag/documents/upload`
- `GET /api/rag/documents`
- `POST /api/rag/documents/reindex`
- `GET /api/rag/chunks/{chunk_id}`
- `POST /api/rag/search`
- `GET /api/rag/collections/status`
- `GET /api/rag/health`
