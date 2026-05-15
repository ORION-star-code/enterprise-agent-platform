from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.schemas.chunk_schema import DocumentChunk
from app.schemas.document_schema import DocumentRecord
from app.vector_store.collection_manager import CollectionManager


def _model_dump(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        result: dict[str, Any] = model.model_dump()
        return result
    result = model.dict()
    return result


class LocalQdrantStore:
    def __init__(self, storage_dir: str | Path | None = None) -> None:
        self.collection_manager = CollectionManager(storage_dir)
        self.collection_manager.initialize()
        self.documents_path = self.collection_manager.documents_path
        self.chunks_path = self.collection_manager.chunks_path

    def upsert_document(
        self, document: DocumentRecord, chunks: list[DocumentChunk]
    ) -> None:
        documents = self._read_json(self.documents_path)
        existing_chunks = self._read_json(self.chunks_path)

        documents[document.doc_id] = _model_dump(document)
        existing_chunks = {
            chunk_id: chunk
            for chunk_id, chunk in existing_chunks.items()
            if chunk.get("doc_id") != document.doc_id
        }

        for chunk in chunks:
            existing_chunks[chunk.chunk_id] = _model_dump(chunk)

        self._write_json(self.documents_path, documents)
        self._write_json(self.chunks_path, existing_chunks)

    def list_documents(self) -> list[DocumentRecord]:
        return [
            DocumentRecord(**document)
            for document in self._read_json(self.documents_path).values()
        ]

    def get_document(self, doc_id: str) -> DocumentRecord | None:
        document = self._read_json(self.documents_path).get(doc_id)
        return DocumentRecord(**document) if document else None

    def list_chunks(self, filters: dict[str, str] | None = None) -> list[DocumentChunk]:
        chunks = [
            DocumentChunk(**chunk)
            for chunk in self._read_json(self.chunks_path).values()
        ]
        if not filters:
            return chunks

        return [
            chunk
            for chunk in chunks
            if all(
                chunk.metadata.get(key) == value
                for key, value in filters.items()
                if value
            )
        ]

    def get_chunk(self, chunk_id: str) -> DocumentChunk | None:
        chunk = self._read_json(self.chunks_path).get(chunk_id)
        return DocumentChunk(**chunk) if chunk else None

    def document_count(self) -> int:
        return len(self._read_json(self.documents_path))

    def chunk_count(self) -> int:
        return len(self._read_json(self.chunks_path))

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            return {}
        result: dict[str, Any] = json.loads(content)
        return result

    def _write_json(self, path: Path, payload: dict[str, Any]) -> None:
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
