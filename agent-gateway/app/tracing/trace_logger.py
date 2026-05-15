from __future__ import annotations

import logging

from app.schemas.trace_schema import WorkflowTrace

logger = logging.getLogger(__name__)


def log_workflow_trace(trace: WorkflowTrace) -> None:
    for step in trace.steps:
        logger.info(
            "trace[%s] %s: %s — %s",
            trace.trace_id,
            step.node,
            step.action,
            step.details,
        )
