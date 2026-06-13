from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from uni_agent_template.agent import DomainAgent  # noqa: E402
from uni_agent_template.schemas import KnowledgeItem, SkillTrace  # noqa: E402


class CareerAgent(DomainAgent):
    """Example custom agent that reuses the UniAds-safe base template."""

    def fallback_answer(
        self,
        message: str,
        *,
        profile_summary: str,
        knowledge: list[KnowledgeItem],
        skills: list[SkillTrace],
        language: str | None = None,
    ) -> str:
        if language == "zh":
            lines = [
                "这里先给出不依赖广告的职业规划回答：",
                f"画像信号：{profile_summary}",
                "1. 目标岗位：Agent 工程、LLM 应用、AI 产品实习。",
                "2. 作品集：展示工具调用、记忆、评估和安全边界。",
                "3. 搜索顺序：先公司官网，再招聘平台补充。",
                "4. 执行节奏：每周固定投递、复盘和补强项目。",
            ]
            lines.extend([f"- [{item.title}]({item.url})" for item in knowledge])
            return "\n".join(lines)
        lines = [
            "Here is a sponsor-independent career answer first:",
            f"Profile signal: {profile_summary}",
            "1. Target roles: agent engineer, LLM app intern, or AI product intern.",
            "2. Build a portfolio project showing tools, memory, evaluation, and safety boundaries.",
            "3. Search official career pages first, then use job boards as backup.",
            "4. Keep a weekly application and review rhythm.",
        ]
        lines.extend([f"- [{item.title}]({item.url})" for item in knowledge])
        return "\n".join(lines)


if __name__ == "__main__":
    response = CareerAgent().chat("Help me find AI agent internship resources.", language="en")
    print(response.assistant_message)
