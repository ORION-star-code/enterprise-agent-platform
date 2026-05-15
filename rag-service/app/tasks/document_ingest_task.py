from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from app.chunkers.heading_chunker import HeadingChunker
from app.chunkers.recursive_chunker import RecursiveChunker
from app.embeddings.embedding_client import HashEmbeddingClient
from app.loaders.markdown_loader import load_markdown
from app.loaders.pdf_loader import load_pdf
from app.loaders.text_loader import load_text
from app.loaders.word_loader import load_word
from app.metadata.metadata_extractor import (
    build_chunk_metadata,
    build_document_metadata,
    generate_doc_id,
)
from app.schemas.chunk_schema import DocumentChunk
from app.schemas.document_schema import DocumentRecord, DocumentUploadResponse
from app.vector_store.qdrant_store import LocalQdrantStore


SUPPORTED_LOADERS = {
    ".md": load_markdown,
    ".markdown": load_markdown,
    ".txt": load_text,
    ".pdf": load_pdf,
}


@dataclass(frozen=True, slots=True)
class IngestDocumentCommand:
    file_path: Path
    doc_name: str
    doc_type: str = "policy"
    department: str = "general"
    permission: str = "internal"
    doc_id: str | None = None
    created_at: str | None = None


class DocumentIngestTask:
    def __init__(
        self,
        store: LocalQdrantStore | None = None,
        embedding_client: HashEmbeddingClient | None = None,
        chunker: RecursiveChunker | None = None,
    ) -> None:
        self.store = store or LocalQdrantStore()
        self.embedding_client = embedding_client or HashEmbeddingClient()
        self.heading_chunker = HeadingChunker()
        self.chunker = chunker or RecursiveChunker()

    def run(self, command: IngestDocumentCommand) -> DocumentUploadResponse:
        doc_id = command.doc_id or generate_doc_id()
        text = self._load(command.file_path)
        sections = self.heading_chunker.split_sections(text)
        raw_chunks = self.chunker.split_sections(sections)

        if not raw_chunks:
            raise ValueError(f"No text chunks generated for document: {command.doc_name}")

        document_data = build_document_metadata(
            doc_id=doc_id,
            doc_name=command.doc_name,
            doc_type=command.doc_type,
            department=command.department,
            permission=command.permission,
            source_path=command.file_path,
            chunk_count=len(raw_chunks),
            created_at=command.created_at,
        )
        document = DocumentRecord(**document_data)
        chunks: list[DocumentChunk] = []

        for raw_chunk in raw_chunks:
            chunk_id = f"{doc_id}_chunk_{raw_chunk.index + 1:04d}"
            metadata = build_chunk_metadata(
                doc_id=doc_id,
                doc_name=command.doc_name,
                doc_type=command.doc_type,
                department=command.department,
                permission=command.permission,
                section=raw_chunk.section,
                created_at=document.created_at,
            )
            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    doc_name=command.doc_name,
                    section=raw_chunk.section,
                    content=raw_chunk.content,
                    metadata=metadata,
                    embedding=self.embedding_client.embed_text(raw_chunk.content),
                )
            )

        self.store.upsert_document(document, chunks)
        return DocumentUploadResponse(
            doc_id=document.doc_id,
            doc_name=document.doc_name,
            chunk_count=document.chunk_count,
            status=document.status,
        )

    def _load(self, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix == ".docx":
            return load_word(path)

        loader = SUPPORTED_LOADERS.get(suffix)
        if not loader:
            raise ValueError(f"Unsupported document type: {suffix or 'unknown'}")

        text = loader(path)
        text = re.sub(r"\r\n?", "\n", text).strip()
        if not text:
            raise ValueError(f"Document has no extractable text: {path.name}")
        return text
