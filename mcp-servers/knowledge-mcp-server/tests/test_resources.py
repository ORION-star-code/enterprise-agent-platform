from __future__ import annotations

from unittest.mock import AsyncMock, patch

from app.resources.faq_resource import get_faq_resource
from app.resources.policy_resource import get_policy_resource
from app.resources.sop_resource import get_sop_resource
from tests.conftest import MOCK_SEARCH_RESPONSE


def _mock_client_with_results() -> AsyncMock:
    client = AsyncMock()
    client.search = AsyncMock(return_value=MOCK_SEARCH_RESPONSE)
    return client


def _mock_client_empty() -> AsyncMock:
    client = AsyncMock()
    client.search = AsyncMock(
        return_value={"query": "test", "total": 0, "results": []}
    )
    return client


async def test_policy_resource_with_results() -> None:
    with patch(
        "app.resources.policy_resource.RagServiceClient",
        return_value=_mock_client_with_results(),
    ):
        result = await get_policy_resource("refund")
        assert "Policy search results for: refund" in result
        assert "refund_policy.md" in result


async def test_policy_resource_no_results() -> None:
    with patch(
        "app.resources.policy_resource.RagServiceClient",
        return_value=_mock_client_empty(),
    ):
        result = await get_policy_resource("nonexistent")
        assert "No policy documents found" in result


async def test_faq_resource_with_results() -> None:
    with patch(
        "app.resources.faq_resource.RagServiceClient",
        return_value=_mock_client_with_results(),
    ):
        result = await get_faq_resource("refund")
        assert "FAQ search results for: refund" in result


async def test_faq_resource_no_results() -> None:
    with patch(
        "app.resources.faq_resource.RagServiceClient",
        return_value=_mock_client_empty(),
    ):
        result = await get_faq_resource("nonexistent")
        assert "No FAQ entries found" in result


async def test_sop_resource_with_results() -> None:
    with patch(
        "app.resources.sop_resource.RagServiceClient",
        return_value=_mock_client_with_results(),
    ):
        result = await get_sop_resource("refund")
        assert "SOP search results for: refund" in result


async def test_sop_resource_no_results() -> None:
    with patch(
        "app.resources.sop_resource.RagServiceClient",
        return_value=_mock_client_empty(),
    ):
        result = await get_sop_resource("nonexistent")
        assert "No SOP documents found" in result
