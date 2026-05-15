from __future__ import annotations

import re

from app.chunkers.base_chunker import BaseChunker, RawChunk, SectionBlock
from app.chunkers.heading_chunker import HeadingChunker


PARAGRAPH_SPLIT_PATTERN = re.compile(r"\n\s*\n+")


class RecursiveChunker(BaseChunker):
    def __init__(self, max_chars: int = 900, overlap_chars: int = 120) -> None:
        self.max_chars = max_chars
        self.overlap_chars = min(overlap_chars, max_chars // 3)
        self.heading_chunker = HeadingChunker()

    def split(self, text: str) -> list[RawChunk]:
        return self.split_sections(self.heading_chunker.split_sections(text))

    def split_sections(self, sections: list[SectionBlock]) -> list[RawChunk]:
        chunks: list[RawChunk] = []

        for section in sections:
            chunks.extend(self._split_section(section, start_index=len(chunks)))

        return chunks

    def _split_section(self, section: SectionBlock, start_index: int) -> list[RawChunk]:
        paragraphs = [
            paragraph.strip()
            for paragraph in PARAGRAPH_SPLIT_PATTERN.split(section.text)
            if paragraph.strip()
        ]
        chunks: list[RawChunk] = []
        buffer: list[str] = []
        buffer_len = 0

        def emit_buffer() -> None:
            nonlocal buffer, buffer_len
            content = "\n\n".join(buffer).strip()
            if content:
                chunks.append(
                    RawChunk(
                        index=start_index + len(chunks),
                        section=section.section,
                        content=content,
                    )
                )
            buffer = []
            buffer_len = 0

        for paragraph in paragraphs:
            if len(paragraph) > self.max_chars:
                emit_buffer()
                chunks.extend(
                    self._split_long_text(
                        paragraph,
                        section=section.section,
                        start_index=start_index + len(chunks),
                    )
                )
                continue

            projected_len = buffer_len + len(paragraph) + (2 if buffer else 0)
            if projected_len > self.max_chars:
                emit_buffer()

            buffer.append(paragraph)
            buffer_len = buffer_len + len(paragraph) + (2 if buffer_len else 0)

        emit_buffer()
        return chunks

    def _split_long_text(self, text: str, section: str, start_index: int) -> list[RawChunk]:
        chunks: list[RawChunk] = []
        step = max(1, self.max_chars - self.overlap_chars)
        start = 0

        while start < len(text):
            content = text[start : start + self.max_chars].strip()
            if content:
                chunks.append(
                    RawChunk(
                        index=start_index + len(chunks),
                        section=section,
                        content=content,
                    )
                )
            start += step

        return chunks
