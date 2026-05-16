# Knowledge MCP Server

MCP server that exposes RAG knowledge base capabilities to the agent-gateway via the Model Context Protocol.

## Architecture

```
agent-gateway (MCP client) --> knowledge-mcp-server (SSE, port 8003) --> rag-service (HTTP, port 8000)
```

## Quick Start

```bash
# Install dependencies
cd mcp-servers/knowledge-mcp-server && uv sync

# Run tests
uv run pytest tests/ -x

# Start the server (requires rag-service on port 8000)
uv run python -m app.server
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `knowledge_search` | Hybrid search (dense + keyword) across the knowledge base |
| `get_chunk` | Retrieve a specific document chunk by ID |
| `document_summary` | Get metadata and summary for a document |
| `list_documents` | List all indexed documents, optionally filtered by type |
| `get_citations` | Search and extract formatted citations with snippets |

## MCP Resources

| URI Pattern | Description |
|-------------|-------------|
| `kb://policy/{topic}` | Policy documents for a topic |
| `kb://faq/{topic}` | FAQ entries for a topic |
| `kb://sop/{topic}` | SOP documents for a topic |

## MCP Prompts

| Prompt | Parameters | Description |
|--------|-----------|-------------|
| `policy_answer` | question, context | Template for answering policy questions with citations |
| `faq_answer` | question, context | Template for answering FAQ questions |
| `summarize_document` | doc_name, content | Template for summarizing a document |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RAG_SERVICE_URL` | `http://localhost:8000` | rag-service base URL |
| `MCP_HOST` | `0.0.0.0` | MCP server bind host |
| `MCP_PORT` | `8003` | MCP server bind port |
