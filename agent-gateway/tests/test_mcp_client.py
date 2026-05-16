from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from app.mcp_client.mcp_client import MCPClient
from app.mcp_client.server_registry import ServerRegistry


def test_server_registry_has_knowledge() -> None:
    registry = ServerRegistry()
    url = registry.get_url("knowledge")
    assert url == "http://localhost:8003/sse"


def test_server_registry_has_business() -> None:
    registry = ServerRegistry()
    url = registry.get_url("business")
    assert url == "http://localhost:8002/sse"


def test_server_registry_unknown() -> None:
    registry = ServerRegistry()
    assert registry.get_url("nonexistent") is None


def test_server_registry_list() -> None:
    registry = ServerRegistry()
    servers = registry.list_servers()
    assert "knowledge" in servers
    assert "business" in servers


def test_mcp_client_init() -> None:
    client = MCPClient("http://localhost:8003")
    assert client.server_url == "http://localhost:8003"


async def test_mcp_client_call_tool_mocked() -> None:
    mock_content = MagicMock()
    mock_content.model_dump.return_value = {
        "type": "text",
        "text": '{"found": true}',
    }

    mock_result = MagicMock()
    mock_result.content = [mock_content]

    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()
    mock_session.call_tool = AsyncMock(return_value=mock_result)

    mock_session_cm = AsyncMock()
    mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_cm.__aexit__ = AsyncMock(return_value=False)

    mock_sse_cm = AsyncMock()
    mock_sse_cm.__aenter__ = AsyncMock(
        return_value=(AsyncMock(), AsyncMock())
    )
    mock_sse_cm.__aexit__ = AsyncMock(return_value=False)

    with patch(
        "app.mcp_client.mcp_client.sse_client",
        return_value=mock_sse_cm,
    ), patch(
        "app.mcp_client.mcp_client.ClientSession",
        return_value=mock_session_cm,
    ):
        client = MCPClient("http://test:8000")
        result = await client.call_tool(
            "order_lookup", {"order_id": "RG1001"}
        )

    assert "content" in result
    assert len(result["content"]) == 1
    mock_session.call_tool.assert_called_once_with(
        "order_lookup", {"order_id": "RG1001"}
    )
