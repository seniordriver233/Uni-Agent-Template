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


class ChatResponse(BaseModel):
    assistant_message: str
    sponsor: SponsorContext = Field(default_factory=SponsorContext)
    session_id: str = "default"
