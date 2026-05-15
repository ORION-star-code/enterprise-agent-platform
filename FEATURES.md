# Feature Manifest

Each feature is a three-tuple: (behavior description, verification command, current state).
States: `not_started` | `active` | `blocked` | `passing`
State transitions are controlled by verification results only.

## rag-service

### F01: Document Upload and Ingestion
- **Behavior**: POST /api/rag/documents/upload accepts file, parses (MD/TXT/PDF/DOCX), chunks, embeds, stores
- **Verification**: `cd rag-service && uv run pytest tests/test_api.py tests/test_loaders_and_chunkers.py -x`
- **State**: passing

### F02: Hybrid Search
- **Behavior**: POST /api/rag/search returns ranked results from dense + keyword retrieval
- **Verification**: `cd rag-service && uv run pytest tests/test_store_and_search.py tests/test_embedding.py -x`
- **State**: passing

### F03: Collection Management
- **Behavior**: GET /api/rag/collection/status returns collection info and chunk count
- **Verification**: `cd rag-service && uv run pytest tests/test_api.py -x -k collection`
- **State**: passing

## agent-gateway (not started)

### F04: LangGraph Workflow
- **Behavior**: Intent router -> planner -> rag/tool_executor -> synthesizer pipeline
- **Verification**: `cd agent-gateway && uv run pytest tests/ -x`
- **State**: not_started

### F05: MCP Client Integration
- **Behavior**: Discover and invoke tools from MCP servers via protocol
- **Verification**: `cd agent-gateway && uv run pytest tests/test_mcp_client.py -x`
- **State**: not_started

## mcp-servers (not started)

### F06: Business MCP Server
- **Behavior**: Expose order/customer/inventory/ticket tools via MCP
- **Verification**: `cd mcp-servers/business-mcp-server && uv run pytest tests/ -x`
- **State**: not_started

### F07: Knowledge MCP Server
- **Behavior**: Expose document search/citation tools via MCP, backed by rag-service
- **Verification**: `cd mcp-servers/knowledge-mcp-server && uv run pytest tests/ -x`
- **State**: not_started

## business-service (not started)

### F08: Spring Boot Customer/Order API
- **Behavior**: CRUD endpoints for customers and orders with MySQL persistence
- **Verification**: `cd business-service && mvn test`
- **State**: not_started

## frontend-web (not started)

### F09: Vue.js Chat Interface
- **Behavior**: Chat view with agent message flow, session management
- **Verification**: `cd frontend-web && npm run test:unit`
- **State**: not_started
