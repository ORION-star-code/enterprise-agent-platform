from __future__ import annotations

from pathlib import Path


SUPPORTED = False


def load_word(path: str | Path) -> str:
    file_path = Path(path)
    raise ValueError(
        f"Word documents are not supported in the rag-service MVP: {file_path.name}"
    )
