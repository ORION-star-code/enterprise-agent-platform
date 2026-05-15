from __future__ import annotations


class AgentError(Exception):
    """Base exception for agent-gateway."""


class WorkflowError(AgentError):
    """Error during workflow execution."""


class IntentClassificationError(AgentError):
    """Failed to classify user intent."""


class ToolExecutionError(AgentError):
    """Error invoking an MCP tool."""
