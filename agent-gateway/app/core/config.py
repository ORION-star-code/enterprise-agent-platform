from __future__ import annotations


class Settings:
    app_name: str = "agent-gateway"
    debug: bool = False
    llm_provider: str = "mock"
    mcp_business_url: str = "http://localhost:8002/sse"
    mcp_knowledge_url: str = "http://localhost:8003/sse"


def get_settings() -> Settings:
    return Settings()
