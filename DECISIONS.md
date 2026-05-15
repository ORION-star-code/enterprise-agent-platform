# Design Decisions

## 2026-05-08: Hash-based embeddings for MVP
- **Decision**: Use SHA-256 hash-based deterministic vectors instead of external embedding APIs
- **Why**: Avoids external API dependencies during development; enables fully offline development
- **Tradeoff**: Lower semantic quality than real embeddings, but sufficient for pipeline validation
- **Constraint**: To switch to real embeddings, implement a new client matching `HashEmbeddingClient` interface

## 2026-05-08: Local JSON store instead of Qdrant
- **Decision**: Use `LocalQdrantStore` with flat JSON files (`documents.json`, `chunks.json`)
- **Why**: Enables development without a running Qdrant instance; Qdrant-compatible interface allows easy migration later
- **Constraint**: Storage path managed by `CollectionManager` at `rag-service/storage/`

## 2026-05-08: Hybrid retrieval with weighted reranking
- **Decision**: Combine dense (vector cosine similarity) and keyword (feature overlap) retrieval
- **Why**: Dense retrieval captures semantic similarity; keyword retrieval catches exact term matches
- **Constraint**: Default weighting is 65% dense / 35% keyword via `SimpleReranker`

## 2026-05-08: MCP protocol for tool integration
- **Decision**: Use Model Context Protocol for agent-gateway to communicate with tool servers
- **Why**: Decouples tool discovery and invocation from the orchestrator; standardized protocol
- **Constraint**: Three MCP servers planned — business, knowledge, ops

## 2026-05-08: Monorepo structure
- **Decision**: Single repo with service subdirectories
- **Why**: Simplifies cross-service development and shared configuration
- **Constraint**: Each service has its own dependency management (uv for Python, Maven for Java, npm for JS)
