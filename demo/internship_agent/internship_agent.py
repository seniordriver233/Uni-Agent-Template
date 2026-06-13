from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from uni_agent_template.agent import DomainAgent  # noqa: E402
from uni_agent_template.knowledge import KnowledgeBase  # noqa: E402
from uni_agent_template.schemas import KnowledgeItem, SkillTrace  # noqa: E402
from uni_agent_template.sources import SourceCatalog, SourceEntry  # noqa: E402


def load_demo_sources() -> list[SourceEntry]:
    raw = json.loads((DEMO_ROOT / "knowledge_sources.json").read_text(encoding="utf-8"))
    return [
        SourceEntry(
            id=item["id"],
            title=item["title"],
            url=item["url"],
            summary=item["summary"],
            tags=tuple(item.get("tags", [])),
        )
        for item in raw
    ]


def infer_track(message: str) -> str:
    text = message.lower()
    if any(term in text for term in ["agent", "llm", "openai", "anthropic"]):
        return "AI agent / LLM application internship"
    if any(term in text for term in ["data", "ml", "machine learning"]):
        return "data and machine learning internship"
    if "product" in text:
        return "AI product internship"
    return "software engineering internship"


class InternshipAgent(DomainAgent):
    """Concrete demo agent for realistic internship search guidance."""

    def __init__(self) -> None:
        knowledge = KnowledgeBase(SourceCatalog(load_demo_sources()))
        super().__init__(knowledge=knowledge)

    def fallback_answer(
        self,
        message: str,
        *,
        profile_summary: str,
        knowledge: list[KnowledgeItem],
        skills: list[SkillTrace],
        language: str | None = None,
    ) -> str:
        track = infer_track(message)
        if language == "zh":
            lines = [
                "下面是 Internship Agent Demo 给出的主回答，广告或赞助内容只会在后面作为补充卡片出现：",
                "",
                f"定位方向：{track}",
                f"用户画像信号：{profile_summary}",
                "",
                "建议执行路径：",
                "1. 明确岗位关键词：agent intern、LLM application intern、AI product intern、software engineering intern。",
                "2. 优先查官方入口：大厂学生招聘页、AI 公司官网、创业公司岗位页。",
                "3. 准备作品集：一个能展示工具调用、记忆、评估和安全边界的 Agent 项目。",
                "4. 每周节奏：固定搜索 2 次，投递 5-10 个岗位，记录反馈并迭代简历。",
                "5. 简历重点：把项目写成业务问题、你的动作、技术栈、可衡量结果。",
            ]
            if knowledge:
                lines.append("\n推荐入口：")
                lines.extend([f"- [{item.title}]({item.url})：{item.summary}" for item in knowledge])
            return "\n".join(lines)
        lines = [
            "Internship Agent Demo primary answer. Sponsored content, if any, is appended later as a separate UniAds card.",
            "",
            f"Target track: {track}",
            f"Profile signal: {profile_summary}",
            "",
            "Action path:",
            "1. Use focused keywords: agent intern, LLM application intern, AI product intern, software engineering intern.",
            "2. Search official sources first: university recruiting pages, AI company career pages, and startup job boards.",
            "3. Build a portfolio signal: one agent project showing tools, memory, evaluation, and safety boundaries.",
            "4. Weekly rhythm: search twice, apply to 5-10 roles, track feedback, and improve the resume.",
            "5. Resume framing: business problem, your action, tech stack, and measurable result.",
        ]
        if knowledge:
            lines.append("\nRecommended entry points:")
            lines.extend([f"- [{item.title}]({item.url}) - {item.summary}" for item in knowledge])
        return "\n".join(lines)


if __name__ == "__main__":
    prompt = "I want an AI agent internship and I know Python. Help me find sources and a weekly plan."
    result = InternshipAgent().chat(prompt, session_id="internship-demo-user", language="en")
    print(result.assistant_message)
    print("\nWorkflow:", " -> ".join(result.workflow))
    print("Profile:", result.profile.model_dump())
