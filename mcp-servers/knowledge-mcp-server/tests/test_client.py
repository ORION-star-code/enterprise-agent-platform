from __future__ import annotations

import httpx
import pytest
import respx

from app.clients.rag_service_client import RagServiceClient
from tests.conftest import (
    MOCK_CHUNK_RESPONSE,
    MOCK_DOCUMENTS_RESPONSE,
    MOCK_SEARCH_RESPONSE,
)


@pytest.fixture
def client() -> RagServiceClient:
    return RagServiceClient(base_url="http://test-rag:8000")


@respx.mock
async def test_search_calls_correct_endpoint(client: RagServiceClient) -> None:
    route = respx.post("http://test-rag:8000/api/rag/search").mock(
        return_value=httpx.Response(200, json=MOCK_SEARCH_RESPONSE)
    )
    result = await client.search("refund", top_k=5)
    assert route.called
    assert result["query"] == "refund"
    assert len(result["results"]) == 1


@respx.mock
async def test_search_with_filters(client: RagServiceClient) -> None:
    route = respx.post("http://test-rag:8000/api/rag/search").mock(
        return_value=httpx.Response(200, json=MOCK_SEARCH_RESPONSE)
    )
    await client.search("refund", doc_type="policy", permission="internal")
    request = route.calls.last.request
    import json

    body = json.loads(request.content)
    assert body["doc_type"] == "policy"
    assert body["permission"] == "internal"


@respx.mock
async def test_list_documents(client: RagServiceClient) -> None:
    respx.get("http://test-rag:8000/api/rag/documents").mock(
        return_value=httpx.Response(200, json=MOCK_DOCUMENTS_RESPONSE)
    )
    result = await client.list_documents()
    assert result["total"] == 2
    assert len(result["documents"]) == 2


@respx.mock
async def test_get_chunk(client: RagServiceClient) -> None:
    respx.get("http://test-rag:8000/api/rag/chunks/chunk_001").mock(
        return_value=httpx.Response(200, json=MOCK_CHUNK_RESPONSE)
    )
    result = await client.get_chunk("chunk_001")
    assert result["chunk_id"] == "chunk_001"
    assert result["doc_name"] == "refund_policy.md"


@respx.mock
async def test_collection_status(client: RagServiceClient) -> None:
    status_response = {
        "storage_type": "local-json-qdrant-compatible",
        "document_count": 2,
        "chunk_count": 8,
        "storage_path": "/storage",
    }
    respx.get("http://test-rag:8000/api/rag/collections/status").mock(
        return_value=httpx.Response(200, json=status_response)
    )
    result = await client.collection_status()
    assert result["document_count"] == 2


@respx.mock
async def test_http_error_raises(client: RagServiceClient) -> None:
    respx.post("http://test-rag:8000/api/rag/search").mock(
        return_value=httpx.Response(400, json={"detail": "Bad request"})
    )
    with pytest.raises(httpx.HTTPStatusError):
        await client.search("")
