from __future__ import annotations

from pathlib import Path


ENCODINGS = ("utf-8", "utf-8-sig", "gb18030")


def load_text(path: str | Path) -> str:
    file_path = Path(path)
    last_error: UnicodeDecodeError | None = None

    for encoding in ENCODINGS:
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc

    raise ValueError(f"Unable to decode text file: {file_path.name}") from last_error
