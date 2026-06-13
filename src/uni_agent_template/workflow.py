from __future__ import annotations

from dataclasses import dataclass, field

from .schemas import KnowledgeItem, SkillTrace


@dataclass
class WorkflowTrace:
    stages: list[str] = field(default_factory=list)

    def add(self, stage: str) -> None:
        self.stages.append(stage)


def format_skill_section(skills: list[SkillTrace]) -> str:
    if not skills:
        return ""
    lines = ["Skill outputs:"]
    for skill in skills:
        lines.append(f"- {skill.name}: {skill.content}")
    return "\n".join(lines)


def format_knowledge_section(items: list[KnowledgeItem]) -> str:
    if not items:
        return ""
    lines = ["Useful sources:"]
    for item in items:
        lines.append(f"- [{item.title}]({item.url}) - {item.summary}")
    return "\n".join(lines)
