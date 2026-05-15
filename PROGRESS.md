# Project Progress

## Current Status
- **Latest commit**: 4543986 (feat: configure ruff/mypy toolchain, fix test failures, add harness docs)
- **Test status**: rag-service 7/7, agent-gateway 6/6
- **Lint**: ruff — All checks passed (both services)
- **Type check**: mypy — Success (both services)

## Completed
- [x] Monorepo directory structure scaffolded
- [x] rag-service: FastAPI app with API routers (document, search, collection)
- [x] rag-service: Loaders (markdown, text, PDF)
- [x] rag-service: Chunkers (heading, recursive)
- [x] rag-service: Hash-based embedding client
- [x] rag-service: Local JSON vector store
- [x] rag-service: Hybrid retriever (dense + keyword + reranker)
- [x] rag-service: Pydantic schemas
- [x] Root README.md with architecture overview
- [x] Fix 5 test errors (root cause: stale Windows temp directory permissions)
- [x] Configure ruff linting (E/F/W rules, line-length 88)
- [x] Configure mypy type checking (explicit_package_bases, ignore_missing_imports)
- [x] agent-gateway: LangGraph workflow (intent_router -> planner -> rag/tool_executor -> synthesizer)
- [x] agent-gateway: MockLLMClient (rule-based, no external API)
- [x] agent-gateway: RAG integration via direct rag-service module import
- [x] agent-gateway: FastAPI chat API with session management and traces
- [x] agent-gateway: MCP client stubs (tool_registry, mcp_client)

## In Progress
- (none)

## Blocked
- (none currently)

## Next Steps
1. Implement knowledge-mcp-server to bridge rag-service with agent via MCP
2. Implement business-mcp-server with order/customer/inventory tools
3. Integrate real LLM provider (replace MockLLMClient)
