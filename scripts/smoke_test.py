from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from uni_agent_template import DomainAgent  # noqa: E402


def main() -> int:
    prompt = " ".join(sys.argv[1:]) or "Help me plan a useful agent."
    response = DomainAgent().chat(prompt, language="en")
    assert response.assistant_message.strip()
    print(response.assistant_message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
