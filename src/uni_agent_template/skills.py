from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .knowledge import KnowledgeBase


@dataclass(frozen=True)
class SkillResult:
    name: str
    content: str
    citations: list[dict[str, str]]


class Skill:
    def __init__(
        self,
        name: str,
        description: str,
        triggers: tuple[str, ...],
        handler: Callable[[str], SkillResult],
    ) -> None:
        self.name = name
        self.description = description
        self.triggers = triggers
        self.handler = handler

    def matches(self, message: str) -> bool:
        text = message.lower()
        return any(trigger in text for trigger in self.triggers)

    def run(self, message: str) -> SkillResult:
        return self.handler(message)


class SkillRegistry:
    """Simple skill adapter. Replace handlers with API tools, MCP tools, or SDK tools."""

    def __init__(self, knowledge: KnowledgeBase | None = None) -> None:
        self.knowledge = knowledge or KnowledgeBase()
        self.skills = [
            Skill("career_planner", "Career and internship planning", ("intern", "career", "job"), self._career),
            Skill("agent_builder", "Agent architecture and template guidance", ("agent", "template", "tool", "mcp"), self._agent_builder),
            Skill("entertainment_recommender", "Entertainment references", ("movie", "video", "game", "book"), self._entertainment),
        ]

    def select(self, message: str) -> list[Skill]:
        matches = [skill for skill in self.skills if skill.matches(message)]
        return matches or [self.skills[1]]

    def run(self, message: str, *, max_skills: int = 2) -> list[SkillResult]:
        return [skill.run(message) for skill in self.select(message)[:max_skills]]

    def _result_from_knowledge(self, name: str, message: str, lead: str) -> SkillResult:
        retrieved = self.knowledge.search(message, limit=4)
        citations = [{"title": item.entry.title, "url": item.entry.url} for item in retrieved]
        lines = [lead]
        for item in retrieved:
            lines.append(f"- {item.entry.title}: {item.entry.summary}")
        return SkillResult(name=name, content="\n".join(lines), citations=citations)

    def _career(self, message: str) -> SkillResult:
        return self._result_from_knowledge(
            "career_planner",
            message,
            "Career skill plan: clarify target roles, prepare a portfolio signal, search official sources, then track weekly applications.",
        )

    def _agent_builder(self, message: str) -> SkillResult:
        return self._result_from_knowledge(
            "agent_builder",
            message,
            "Agent builder skill plan: separate orchestration, tools, memory, retrieval, guardrails, and deployment endpoints.",
        )

    def _entertainment(self, message: str) -> SkillResult:
        return self._result_from_knowledge(
            "entertainment_recommender",
            message,
            "Entertainment skill plan: infer mood, format, constraints, novelty level, and provide legal discovery links.",
        )
