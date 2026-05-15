from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def load_pdf(path: str | Path) -> str:
    file_path = Path(path)
    reader = PdfReader(str(file_path))
    pages: list[str] = []

    for page in reader.pages:
        pages.append(page.extract_text() or "")

    text = "\n\n".join(page.strip() for page in pages if page.strip())
    if not text.strip():
        raise ValueError(f"No extractable text found in PDF: {file_path.name}")

    return text
