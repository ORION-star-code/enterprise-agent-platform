from __future__ import annotations

import os


class Settings:
    rag_service_url: str = os.environ.get(
        "RAG_SERVICE_URL", "http://localhost:8000"
    )
    mcp_server_name: str = "knowledge-mcp-server"
    mcp_host: str = os.environ.get("MCP_HOST", "0.0.0.0")
    mcp_port: int = int(os.environ.get("MCP_PORT", "8003"))


def get_settings() -> Settings:
    return Settings()
