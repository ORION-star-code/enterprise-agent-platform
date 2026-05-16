from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from app.config import get_settings
from app.prompts.faq_answer_prompt import faq_answer_prompt
from app.prompts.policy_answer_prompt import policy_answer_prompt
from app.prompts.summarize_doc_prompt import summarize_doc_prompt
from app.resources.faq_resource import get_faq_resource
from app.resources.policy_resource import get_policy_resource
from app.resources.sop_resource import get_sop_resource
from app.tools.citation_tool import extract_citations
from app.tools.document_tool import (
    get_document_chunk,
    get_document_summary,
    list_available_documents,
)
from app.tools.kb_search_tool import search_knowledge_base

settings = get_settings()

mcp = FastMCP(
    settings.mcp_server_name,
    host=settings.mcp_host,
    port=settings.mcp_port,
)


# --- Tools ---


@mcp.tool()
async def knowledge_search(
    query: str,
    top_k: int = 5,
    doc_type: str | None = None,
    permission: str | None = None,
) -> str:
    """Search the enterprise knowledge base.

    Uses hybrid retrieval (dense + keyword) to find relevant document chunks.
    """
    result = await search_knowledge_base(query, top_k, doc_type, permission)
    return result.model_dump_json(indent=2)


@mcp.tool()
async def get_chunk(chunk_id: str) -> str:
    """Retrieve a specific document chunk by ID."""
    result = await get_document_chunk(chunk_id)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def document_summary(doc_id: str) -> str:
    """Get metadata and summary for a document."""
    result = await get_document_summary(doc_id)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def list_documents(doc_type: str | None = None) -> str:
    """List all indexed documents, optionally filtered by type."""
    result = await list_available_documents(doc_type)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def get_citations(
    query: str,
    top_k: int = 5,
    doc_type: str | None = None,
) -> str:
    """Search and extract formatted citations for a query."""
    result = await extract_citations(query, top_k, doc_type)
    return result.model_dump_json(indent=2)


# --- Resources ---


@mcp.resource("kb://policy/{topic}")
async def policy_resource(topic: str) -> str:
    """Policy documents for a given topic."""
    return await get_policy_resource(topic)


@mcp.resource("kb://faq/{topic}")
async def faq_resource(topic: str) -> str:
    """FAQ entries for a given topic."""
    return await get_faq_resource(topic)


@mcp.resource("kb://sop/{topic}")
async def sop_resource(topic: str) -> str:
    """SOP documents for a given topic."""
    return await get_sop_resource(topic)


# --- Prompts ---


@mcp.prompt()
def policy_answer(question: str, context: str) -> str:
    """Template for answering policy questions with evidence."""
    return policy_answer_prompt(question, context)


@mcp.prompt()
def faq_answer(question: str, context: str) -> str:
    """Template for answering FAQ questions."""
    return faq_answer_prompt(question, context)


@mcp.prompt()
def summarize_document(doc_name: str, content: str) -> str:
    """Template for summarizing a document."""
    return summarize_doc_prompt(doc_name, content)


def main() -> None:
    """Run the MCP server with SSE transport."""
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
