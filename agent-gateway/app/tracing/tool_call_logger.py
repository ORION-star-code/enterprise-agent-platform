from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def log_tool_call(
    tool_name: str, server: str, arguments: dict[str, Any], result: Any
) -> None:
    logger.info("tool_call: %s/%s args=%s", server, tool_name, arguments)
