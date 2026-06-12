from __future__ import annotations

from collections import defaultdict


class SessionMemory:
    """Replace this with Redis/Postgres in production."""

    def __init__(self) -> None:
        self._history: dict[str, list[dict[str, str]]] = defaultdict(list)

    def get(self, session_id: str) -> list[dict[str, str]]:
        return list(self._history[session_id])

    def append(self, session_id: str, role: str, content: str) -> None:
        self._history[session_id].append({"role": role, "content": content})
        self._history[session_id] = self._history[session_id][-12:]
