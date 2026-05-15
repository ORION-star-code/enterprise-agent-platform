from __future__ import annotations

from pathlib import Path

from app.loaders.text_loader import load_text


def load_markdown(path: str | Path) -> str:
    return load_text(path)
