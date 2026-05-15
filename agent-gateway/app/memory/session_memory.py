from __future__ import annotations

from app.schemas.chat_schema import Message

_sessions: dict[str, list[Message]] = {}


def get_session(session_id: str) -> list[Message]:
    return _sessions.setdefault(session_id, [])


def add_message(session_id: str, message: Message) -> None:
    _sessions.setdefault(session_id, []).append(message)


def clear_session(session_id: str) -> None:
    _sessions.pop(session_id, None)


def list_sessions() -> list[str]:
    return list(_sessions.keys())
