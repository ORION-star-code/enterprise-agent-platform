# Project Progress

## Current Status
- **Latest commit**: f875d40 (feat: implement agent-gateway with LangGraph workflow)
- **Test status**: rag-service 7/7, agent-gateway 12/12, knowledge-mcp-server 28/28, business-mcp-server 24/24
- **Lint**: ruff — All checks passed (all four services)
- **Type check**: mypy — Success (all four services)

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
- [x] knowledge-mcp-server: MCP tools (knowledge_search, get_chunk, document_summary, list_documents, get_citations)
- [x] knowledge-mcp-server: MCP resources (kb://policy, kb://faq, kb://sop)
- [x] knowledge-mcp-server: MCP prompts (policy_answer, faq_answer, summarize_document)
- [x] knowledge-mcp-server: RagServiceClient HTTP bridge to rag-service
- [x] knowledge-mcp-server: 28 tests passing (client, tools, resources, prompts)
- [x] business-mcp-server: 5 MCP tools (order, customer, inventory, ticket lookup)
- [x] business-mcp-server: 5 MCP resources (order status, refund rules, invoice rules, table schemas)
- [x] business-mcp-server: 2 MCP prompts (order summary, customer reply)
- [x] business-mcp-server: Mock data client (MVP, ready for Spring Boot replacement)
- [x] business-mcp-server: 24 tests passing
- [x] agent-gateway: MCPClient rewritten with real SSE transport (mcp SDK)
- [x] agent-gateway: ServerRegistry mapping knowledge/business server URLs
- [x] agent-gateway: tool_executor_node calls MCP servers via asyncio.run()
- [x] agent-gateway: 12 tests passing (6 original + 6 new MCP tests)

## In Progress
- (none)

## Blocked
- (none currently)

## Next Steps
1. Integrate real LLM provider (replace MockLLMClient)
2. Implement frontend-web Vue.js chat interface
