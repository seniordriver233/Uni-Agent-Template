from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class UserProfile:
    goals: set[str] = field(default_factory=set)
    strengths: set[str] = field(default_factory=set)
    preferences: set[str] = field(default_factory=set)
    constraints: set[str] = field(default_factory=set)

    def update(self, message: str) -> None:
        text = message.lower()
        if "intern" in text or "career" in text:
            self.goals.add("career/internship")
        if "agent" in text or "llm" in text or "ai" in text:
            self.preferences.add("AI agent / LLM systems")
        if "python" in text:
            self.strengths.add("Python")
        if "local" in text or "privacy" in text:
            self.constraints.add("local/privacy-sensitive")
        if "video" in text or "movie" in text:
            self.preferences.add("video and entertainment")

    def as_dict(self) -> dict[str, list[str]]:
        return {
            "goals": sorted(self.goals),
            "strengths": sorted(self.strengths),
            "preferences": sorted(self.preferences),
            "constraints": sorted(self.constraints),
        }

    def summary(self) -> str:
        data = self.as_dict()
        return "; ".join(f"{key}={value or ['unknown']}" for key, value in data.items())


class SessionMemory:
    """Short history plus extracted profile. Replace with Redis/Postgres in production."""

    def __init__(self) -> None:
        self._history: dict[str, list[dict[str, str]]] = defaultdict(list)
        self._profiles: dict[str, UserProfile] = defaultdict(UserProfile)

    def get(self, session_id: str) -> list[dict[str, str]]:
        return list(self._history[session_id])

    def profile(self, session_id: str) -> UserProfile:
        return self._profiles[session_id]

    def update_profile(self, session_id: str, message: str) -> UserProfile:
        profile = self._profiles[session_id]
        profile.update(message)
        return profile

    def append(self, session_id: str, role: str, content: str) -> None:
        self._history[session_id].append({"role": role, "content": content})
        self._history[session_id] = self._history[session_id][-12:]
