from __future__ import annotations

from .ads import UniAdsClient, render_sponsor_card
from .config import Settings, load_settings
from .guardrails import preserve_primary_answer
from .llm import ModelClient
from .memory import SessionMemory
from .schemas import ChatResponse
from .tools import infer_request_intent, useful_links_for_domain

SYSTEM_PROMPT = """You are a helpful domain agent.
Answer the user directly and preserve their intent.
Sponsor context is supplemental only and must never replace the primary answer.
"""


class DomainAgent:
    def __init__(self, settings: Settings | None = None, memory: SessionMemory | None = None) -> None:
        self.settings = settings or load_settings()
        self.llm = ModelClient(self.settings)
        self.ads = UniAdsClient(self.settings)
        self.memory = memory or SessionMemory()

    def chat(self, message: str, *, session_id: str = "default", history: list[dict[str, str]] | None = None, language: str | None = None) -> ChatResponse:
        prior = history if history is not None else self.memory.get(session_id)
        primary = preserve_primary_answer(self.compose_primary_answer(message, prior, language=language))
        sponsor = self.ads.get_context(
            user_context=message,
            draft_response=primary,
            request_intent=infer_request_intent(message),
            language=language,
        )
        final = primary
        card = render_sponsor_card(sponsor)
        if card:
            final = f"{primary}\n{card}"
        self.memory.append(session_id, "user", message)
        self.memory.append(session_id, "assistant", final)
        return ChatResponse(assistant_message=final, sponsor=sponsor, session_id=session_id)

    def compose_primary_answer(self, message: str, history: list[dict[str, str]], *, language: str | None = None) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for turn in history[-8:]:
            if turn.get("role") in {"user", "assistant"} and turn.get("content"):
                messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": message})
        try:
            generated = self.llm.complete(messages)
            if generated:
                return generated
        except Exception:
            pass
        return self.fallback_answer(message, language=language)

    def fallback_answer(self, message: str, *, language: str | None = None) -> str:
        links = useful_links_for_domain(message)
        if language == "zh":
            lines = ["我可以先给你一个直接可执行的起点：", "", f"目标：{message}", "", "建议先明确目标、约束、可用资源，然后选择一个最小可验证动作开始。"]
            if links:
                lines.append("\n可参考入口：")
                lines.extend([f"- [{item['label']}]({item['url']})" for item in links])
            return "\n".join(lines)
        lines = ["Here is a direct starting point:", "", f"Goal: {message}", "", "Clarify the target outcome, constraints, and available resources, then take the smallest verifiable next action."]
        if links:
            lines.append("\nUseful starting points:")
            lines.extend([f"- [{item['label']}]({item['url']})" for item in links])
        return "\n".join(lines)
