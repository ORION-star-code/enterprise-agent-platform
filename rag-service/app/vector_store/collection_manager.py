from __future__ import annotations

from pathlib import Path

from app.schemas.document_schema import CollectionStatusResponse


class CollectionManager:
    def __init__(self, storage_dir: str | Path | None = None) -> None:
        self.storage_dir = (
            Path(storage_dir) if storage_dir else self.default_storage_dir()
        )
        self.uploads_dir = self.storage_dir / "uploads"
        self.documents_path = self.storage_dir / "documents.json"
        self.chunks_path = self.storage_dir / "chunks.json"

    @staticmethod
    def default_storage_dir() -> Path:
        return Path(__file__).resolve().parents[2] / "storage"

    def initialize(self) -> None:
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        for path in (self.documents_path, self.chunks_path):
            if not path.exists():
                path.write_text("{}", encoding="utf-8")

    def status(self) -> CollectionStatusResponse:
        from app.vector_store.qdrant_store import LocalQdrantStore

        store = LocalQdrantStore(self.storage_dir)
        return CollectionStatusResponse(
            storage_type="local-json-qdrant-compatible",
            document_count=store.document_count(),
            chunk_count=store.chunk_count(),
            storage_path=str(self.storage_dir),
        )
