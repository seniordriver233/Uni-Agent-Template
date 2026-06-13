from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str = "default"
    history: list[dict[str, str]] = Field(default_factory=list)
    language: Literal["en", "zh"] | None = None


class SponsorCard(BaseModel):
    title: str = ""
    sponsor: str = ""
    body: str = ""
    cta_label: str = ""
    cta_url: str = ""
    disclosure: str = "Sponsored"


class PermissionState(BaseModel):
    required: bool = False
    risk_level: str = "low"
    reason: str = ""
    prompt: str = ""


class SponsorContext(BaseModel):
    raw: dict[str, Any] = Field(default_factory=dict)
    card: SponsorCard | None = None
    permission: PermissionState = Field(default_factory=PermissionState)
    matched: bool = False


class KnowledgeItem(BaseModel):
    title: str
    url: str
    summary: str
    score: float = 0.0


class SkillTrace(BaseModel):
    name: str
    content: str
    citations: list[dict[str, str]] = Field(default_factory=list)


class AgentProfile(BaseModel):
    goals: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class ChatResponse(BaseModel):
    assistant_message: str
    sponsor: SponsorContext = Field(default_factory=SponsorContext)
    session_id: str = "default"
    profile: AgentProfile = Field(default_factory=AgentProfile)
    knowledge: list[KnowledgeItem] = Field(default_factory=list)
    skills: list[SkillTrace] = Field(default_factory=list)
    workflow: list[str] = Field(default_factory=list)
