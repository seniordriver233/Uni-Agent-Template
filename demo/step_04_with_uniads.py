from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from uni_agent_template import DomainAgent  # noqa: E402


if __name__ == "__main__":
    agent = DomainAgent()
    response = agent.chat(
        "I want an AI agent internship plan and useful search sources.",
        session_id="demo-career-user",
        language="en",
    )
    print(response.assistant_message)
    print("\nSponsor matched:", response.sponsor.matched)
