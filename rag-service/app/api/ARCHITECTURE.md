# API Layer Architecture

## Responsibility
HTTP interface for the RAG service. Three routers under `/api/rag/` prefix.

## Routers
- **document_api.py**: Document CRUD + file upload. Upload triggers async ingest pipeline (load -> chunk -> embed -> store).
- **search_api.py**: Hybrid search endpoint. Accepts query text and optional metadata filters, returns ranked results.
- **collection_api.py**: Collection status and management. Returns collection info, chunk counts, storage stats.

## Request/Response Flow
1. Client sends request to FastAPI endpoint
2. Pydantic schema validates input
3. Business logic delegates to retrievers/vector_store/loaders
4. Pydantic schema serializes response

## Constraints
- All endpoints under `/api/rag/` prefix
- Input/output validated via Pydantic schemas in `app/schemas/`
- No direct database access from API layer — go through vector_store abstraction
