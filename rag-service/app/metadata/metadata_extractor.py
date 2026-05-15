from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def generate_doc_id() -> str:
    return f"doc_{uuid4().hex}"


def build_document_metadata(
    *,
    doc_id: str,
    doc_name: str,
    doc_type: str,
    department: str,
    permission: str,
    source_path: str | Path,
    chunk_count: int,
    created_at: str | None = None,
) -> dict[str, str | int]:
    now = utc_now_iso()
    return {
        "doc_id": doc_id,
        "doc_name": doc_name,
        "doc_type": doc_type,
        "department": department,
        "permission": permission,
        "source_path": str(source_path),
        "chunk_count": chunk_count,
        "status": "indexed",
        "created_at": created_at or now,
        "updated_at": now,
    }


def build_chunk_metadata(
    *,
    doc_id: str,
    doc_name: str,
    doc_type: str,
    department: str,
    permission: str,
    section: str,
    created_at: str,
) -> dict[str, str]:
    return {
        "doc_id": doc_id,
        "doc_name": doc_name,
        "doc_type": doc_type,
        "department": department,
        "permission": permission,
        "section": section,
        "created_at": created_at,
    }
