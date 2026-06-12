from __future__ import annotations

import requests

from .config import Settings


class ModelClient:
    """Tiny OpenAI-compatible chat-completions client."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def complete(self, messages: list[dict[str, str]], *, temperature: float = 0.3) -> str:
        if not self.settings.model_api_key:
            return ""
        endpoint = f"{self.settings.model_base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self.settings.model_name,
            "messages": messages,
            "temperature": temperature,
        }
        headers = {
            "Authorization": f"Bearer {self.settings.model_api_key}",
            "Content-Type": "application/json",
        }
        with requests.Session() as session:
            session.trust_env = False
            response = session.post(endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return content.strip() if isinstance(content, str) else ""
