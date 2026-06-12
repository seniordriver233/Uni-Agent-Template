from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class Settings:
    model_api_key: str = ""
    model_base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-4.1-mini"
    uniads_base_url: str = "http://103.242.15.56"
    uniads_dev_api_key: str = ""
    uniads_agent_id: str = "uni-agent-template"
    uniads_agent_name: str = "Uni Agent Template"
    uniads_timeout_seconds: float = 6.0


def load_settings(env_file: str | Path = ".env") -> Settings:
    _load_dotenv(Path(env_file))
    return Settings(
        model_api_key=os.getenv("MODEL_API_KEY", ""),
        model_base_url=os.getenv("MODEL_BASE_URL", "https://api.openai.com/v1"),
        model_name=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
        uniads_base_url=os.getenv("UNIADS_BASE_URL", "http://103.242.15.56"),
        uniads_dev_api_key=os.getenv("UNIADS_DEV_API_KEY", ""),
        uniads_agent_id=os.getenv("UNIADS_AGENT_ID", "uni-agent-template"),
        uniads_agent_name=os.getenv("UNIADS_AGENT_NAME", "Uni Agent Template"),
        uniads_timeout_seconds=float(os.getenv("UNIADS_TIMEOUT_SECONDS", "6")),
    )
