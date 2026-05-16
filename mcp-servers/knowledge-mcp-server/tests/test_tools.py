from __future__ import annotations

from unittest.mock import AsyncMock, patch

from app.tools.citation_tool import extract_citations
from app.tools.document_tool import (
    get_document_chunk,
    get_document_summary,
    list_available_documents,
)
from app.tools.kb_search_tool import search_knowledge_base
from tests.conftest import (
    MOCK_CHUNK_RESPONSE,
    MOCK_DOCUMENTS_RESPONSE,
    MOCK_SEARCH_RESPONSE,
)


def _mock_client() -> AsyncMock:
    client = AsyncMock()
    client.search = AsyncMock(return_value=MOCK_SEARCH_RESPONSE)
    client.list_documents = AsyncMock(return_value=MOCK_DOCUMENTS_RESPONSE)
    client.get_chunk = AsyncMock(return_value=MOCK_CHUNK_RESPONSE)
    return client


async def test_search_knowledge_base() -> None:
    with patch(
        "app.tools.kb_search_tool.RagServiceClient",
        return_value=_mock_client(),
    ):
        result = await search_knowledge_base("refund")
        assert result.query == "refund"
        assert result.total == 1
        assert result.results[0].chunk_id == "chunk_001"


async def test_search_knowledge_base_with_filters() -> None:
    mock = _mock_client()
    with patch(
        "app.tools.kb_search_tool.RagServiceClient",
        return_value=mock,
    ):
        await search_knowledge_base("refund", doc_type="policy")
        mock.search.assert_called_once_with("refund", 5, "policy", None)


async def test_get_document_chunk() -> None:
    with patch(
        "app.tools.document_tool.RagServiceClient",
        return_value=_mock_client(),
    ):
        result = await get_document_chunk("chunk_001")
        assert result["chunk_id"] == "chunk_001"


async def test_list_available_documents() -> None:
    with patch(
        "app.tools.document_tool.RagServiceClient",
        return_value=_mock_client(),
    ):
        result = await list_available_documents()
        assert result["total"] == 2


async def test_list_available_documents_filtered() -> None:
    with patch(
        "app.tools.document_tool.RagServiceClient",
        return_value=_mock_client(),
    ):
        result = await list_available_documents(doc_type="policy")
        assert result["total"] == 1
        assert result["documents"][0]["doc_type"] == "policy"


async def test_get_document_summary() -> None:
    with patch(
        "app.tools.document_tool.RagServiceClient",
        return_value=_mock_client(),
    ):
        result = await get_document_summary("doc_001")
        assert result["doc_id"] == "doc_001"
        assert result["doc_name"] == "refund_policy.md"
        assert result["chunk_count"] == 3


async def test_get_document_summary_not_found() -> None:
    with patch(
        "app.tools.document_tool.RagServiceClient",
        return_value=_mock_client(),
    ):
        result = await get_document_summary("nonexistent")
        assert "error" in result


async def test_extract_citations() -> None:
    with patch(
        "app.tools.citation_tool.RagServiceClient",
        return_value=_mock_client(),
    ):
        result = await extract_citations("refund")
        assert result.query == "refund"
        assert result.total == 1
        assert result.citations[0].chunk_id == "chunk_001"


async def test_extract_citations_truncates_snippets() -> None:
    mock = _mock_client()
    long_content = "x" * 500
    mock.search.return_value = {
        "query": "test",
        "total": 1,
        "results": [
            {
                "chunk_id": "c1",
                "doc_id": "d1",
                "doc_name": "doc.md",
                "section": "s",
                "content": long_content,
                "score": 0.9,
                "metadata": {},
            }
        ],
    }
    with patch(
        "app.tools.citation_tool.RagServiceClient",
        return_value=mock,
    ):
        result = await extract_citations("test")
        assert len(result.citations[0].content_snippet) == 200
