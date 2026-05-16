from __future__ import annotations

import os


class Settings:
    business_service_url: str = os.environ.get(
        "BUSINESS_SERVICE_URL", "http://localhost:8080"
    )
    mcp_server_name: str = "business-mcp-server"
    mcp_host: str = os.environ.get("MCP_HOST", "0.0.0.0")
    mcp_port: int = int(os.environ.get("MCP_PORT", "8002"))


def get_settings() -> Settings:
    return Settings()
