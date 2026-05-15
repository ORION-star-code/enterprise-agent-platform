from __future__ import annotations

from pathlib import Path

import pytest

from app.chunkers.heading_chunker import HeadingChunker
from app.chunkers.recursive_chunker import RecursiveChunker
from app.loaders.markdown_loader import load_markdown
from app.loaders.pdf_loader import load_pdf
from app.loaders.text_loader import load_text
from app.loaders.word_loader import load_word


def test_markdown_and_text_loaders_read_content(tmp_path: Path) -> None:
    markdown = tmp_path / "policy.md"
    text = tmp_path / "faq.txt"
    markdown.write_text("# Refund\n\nRefund within 7 days.", encoding="utf-8")
    text.write_text("FAQ content", encoding="utf-8")

    assert "Refund" in load_markdown(markdown)
    assert load_text(text) == "FAQ content"


def test_pdf_loader_uses_extractable_page_text(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    class FakePage:
        def extract_text(self) -> str:
            return "Refund Policy PDF"

    class FakeReader:
        pages = [FakePage()]

    monkeypatch.setattr("app.loaders.pdf_loader.PdfReader", lambda _: FakeReader())

    pdf = tmp_path / "policy.pdf"
    pdf.write_bytes(b"%PDF-1.4")

    assert load_pdf(pdf) == "Refund Policy PDF"


def test_word_loader_is_explicitly_unsupported(tmp_path: Path) -> None:
    docx = tmp_path / "policy.docx"
    docx.write_bytes(b"placeholder")

    with pytest.raises(ValueError, match="not supported"):
        load_word(docx)


def test_heading_and_recursive_chunkers_keep_sections() -> None:
    text = "# Refund Policy\n\nRefund within 7 days.\n\n" + ("Details. " * 300)
    sections = HeadingChunker().split_sections(text)
    chunks = RecursiveChunker(max_chars=200, overlap_chars=30).split_sections(sections)

    assert sections[0].section == "Refund Policy"
    assert len(chunks) > 1
    assert all(chunk.section == "Refund Policy" for chunk in chunks)
