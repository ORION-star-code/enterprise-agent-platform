from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SectionBlock:
    section: str
    text: str


@dataclass(frozen=True, slots=True)
class RawChunk:
    index: int
    section: str
    content: str


class BaseChunker(ABC):
    @abstractmethod
    def split(self, text: str) -> list[RawChunk]:
        raise NotImplementedError
