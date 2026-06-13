from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from uni_agent_template.agent import DomainAgent  # noqa: E402
from uni_agent_template.tools import useful_links_for_domain  # noqa: E402


class CareerAgent(DomainAgent):
    """Example custom agent that reuses the UniAds-safe base template."""

    def fallback_answer(self, message: str, *, language: str | None = None) -> str:
        links = useful_links_for_domain(message)
        if language == "zh":
            lines = [
                "????????????????????",
                "1. ???????Agent ???LLM ???AI ?????",
                "2. ????????????????????????",
                "3. ??????????????????",
                "4. ??????????",
            ]
            lines.extend([f"- [{item['label']}]({item['url']})" for item in links])
            return "\n".join(lines)
        lines = [
            "Here is a sponsor-independent career answer first:",
            "1. Target roles: agent engineer, LLM app intern, or AI product intern.",
            "2. Build a portfolio project showing tools, memory, evaluation, and safety boundaries.",
            "3. Search official career pages first, then use job boards as backup.",
            "4. Keep a weekly application and review rhythm.",
        ]
        lines.extend([f"- [{item['label']}]({item['url']})" for item in links])
        return "\n".join(lines)


if __name__ == "__main__":
    response = CareerAgent().chat("Help me find AI agent internship resources.", language="en")
    print(response.assistant_message)
