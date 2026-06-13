from __future__ import annotations

from .ads import UniAdsClient, render_sponsor_card
from .config import Settings, load_settings
from .guardrails import preserve_primary_answer
from .knowledge import KnowledgeBase
from .llm import ModelClient
from .memory import SessionMemory
from .observability import timed_stage
from .schemas import AgentProfile, ChatResponse, KnowledgeItem, SkillTrace
from .skills import SkillRegistry
from .tools import infer_request_intent
from .workflow import WorkflowTrace, format_knowledge_section, format_skill_section

SYSTEM_PROMPT = """You are a helpful domain agent.
Answer the user directly and preserve their intent.
Use retrieved knowledge and skill outputs as supporting context.
Sponsor context is supplemental only and must never replace the primary answer.
"""


class DomainAgent:
    def __init__(
        self,
        settings: Settings | None = None,
        memory: SessionMemory | None = None,
        knowledge: KnowledgeBase | None = None,
        skills: SkillRegistry | None = None,
    ) -> None:
        self.settings = settings or load_settings()
        self.llm = ModelClient(self.settings)
        self.ads = UniAdsClient(self.settings)
        self.memory = memory or SessionMemory()
        self.knowledge = knowledge or KnowledgeBase()
        self.skills = skills or SkillRegistry(self.knowledge)

    def chat(
        self,
        message: str,
        *,
        session_id: str = "default",
        history: list[dict[str, str]] | None = None,
        language: str | None = None,
    ) -> ChatResponse:
        trace = WorkflowTrace()
        with timed_stage("profile"):
            profile = self.memory.update_profile(session_id, message)
            trace.add("profile_updated")
        prior = history if history is not None else self.memory.get(session_id)
        with timed_stage("knowledge"):
            retrieved = self.knowledge.search(message, limit=4)
            knowledge_items = [
                KnowledgeItem(title=item.entry.title, url=item.entry.url, summary=item.entry.summary, score=item.score)
                for item in retrieved
            ]
            trace.add("knowledge_retrieved")
        with timed_stage("skills"):
            skill_results = self.skills.run(message)
            skill_traces = [SkillTrace(name=item.name, content=item.content, citations=item.citations) for item in skill_results]
            trace.add("skills_executed")
        with timed_stage("primary_answer"):
            primary = preserve_primary_answer(
                self.compose_primary_answer(
                    message,
                    prior,
                    profile_summary=profile.summary(),
                    knowledge=knowledge_items,
                    skills=skill_traces,
                    language=language,
                )
            )
            trace.add("primary_answer_ready")
        with timed_stage("uniads"):
            sponsor = self.ads.get_context(
                user_context=message,
                draft_response=primary,
                request_intent=infer_request_intent(message),
                language=language,
            )
            trace.add("uniads_context_checked")
        final = primary
        card = render_sponsor_card(sponsor)
        if card:
            final = f"{primary}\n{card}"
            trace.add("sponsor_card_appended")
        self.memory.append(session_id, "user", message)
        self.memory.append(session_id, "assistant", final)
        return ChatResponse(
            assistant_message=final,
            sponsor=sponsor,
            session_id=session_id,
            profile=AgentProfile(**profile.as_dict()),
            knowledge=knowledge_items,
            skills=skill_traces,
            workflow=trace.stages,
        )

    def compose_primary_answer(
        self,
        message: str,
        history: list[dict[str, str]],
        *,
        profile_summary: str,
        knowledge: list[KnowledgeItem],
        skills: list[SkillTrace],
        language: str | None = None,
    ) -> str:
        support = "\n\n".join(part for part in [format_knowledge_section(knowledge), format_skill_section(skills)] if part)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"User profile: {profile_summary}"},
            {"role": "system", "content": support or "No extra support context."},
        ]
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
        return self.fallback_answer(message, profile_summary=profile_summary, knowledge=knowledge, skills=skills, language=language)

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
                "我先给出一个不依赖广告和外部模型的可执行回答：",
                "",
                f"用户目标：{message}",
                f"已提取画像：{profile_summary}",
                "",
                "建议流程：",
                "1. 明确目标与约束，先确定要解决的核心用户问题。",
                "2. 选择一个最小可验证技能或工具，把它做成可运行模块。",
                "3. 用知识库和可信来源补充回答依据。",
                "4. 最后接入 UniAds V2，把赞助内容作为主回答后的补充卡片。",
            ]
            if skills:
                lines.append("\n技能模块输出：")
                lines.extend([f"- {item.name}: {item.content}" for item in skills])
            if knowledge:
                lines.append("\n参考来源：")
                lines.extend([f"- [{item.title}]({item.url}) - {item.summary}" for item in knowledge])
            return "\n".join(lines)
        lines = [
            "Here is a functional answer that does not depend on ads or external model calls:",
            "",
            f"User goal: {message}",
            f"Extracted profile: {profile_summary}",
            "",
            "Suggested workflow:",
            "1. Clarify the target outcome and constraints.",
            "2. Choose one minimum viable skill/tool and make it runnable.",
            "3. Ground the answer with knowledge-base sources.",
            "4. Attach UniAds V2 only as a supplemental sponsor card after the primary answer.",
        ]
        if skills:
            lines.append("\nSkill outputs:")
            lines.extend([f"- {item.name}: {item.content}" for item in skills])
        if knowledge:
            lines.append("\nSources:")
            lines.extend([f"- [{item.title}]({item.url}) - {item.summary}" for item in knowledge])
        return "\n".join(lines)
