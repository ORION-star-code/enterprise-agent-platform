from __future__ import annotations

import re

from app.chunkers.base_chunker import SectionBlock


HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


class HeadingChunker:
    def split_sections(
        self, text: str, default_section: str = "General"
    ) -> list[SectionBlock]:
        current_section = default_section
        current_lines: list[str] = []
        sections: list[SectionBlock] = []

        def flush() -> None:
            content = "\n".join(current_lines).strip()
            if content:
                sections.append(SectionBlock(section=current_section, text=content))

        for line in text.splitlines():
            match = HEADING_PATTERN.match(line)
            if match:
                flush()
                current_section = match.group(2).strip()
                current_lines = []
                continue
            current_lines.append(line)

        flush()

        if not sections and text.strip():
            return [SectionBlock(section=default_section, text=text.strip())]

        return sections
