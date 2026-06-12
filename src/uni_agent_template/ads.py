from __future__ import annotations

from typing import Any
import requests

from .config import Settings
from .guardrails import classify_permission_need
from .schemas import PermissionState, SponsorCard, SponsorContext


class UniAdsClient:
    """UniAds V2 sponsor-context client. Fail-open by design."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_context(
        self,
        *,
        user_context: str,
        draft_response: str,
        request_intent: str = "direct_answer",
        language: str | None = None,
    ) -> SponsorContext:
        if not self.settings.uniads_dev_api_key:
            return SponsorContext()
        payload = {
            "user_context": user_context,
            "draft_response": draft_response,
            "agent_context": {
                "agent_id": self.settings.uniads_agent_id,
                "agent_name": self.settings.uniads_agent_name,
                "domain": "developer-template",
                "language": language,
            },
            "capabilities": {
                "supported_ad_types": ["compact_card", "reference", "api_trial_card", "step_by_step"],
                "service_trial_supported": True,
                "max_slots": 1,
                "layout_support": ["compact", "card", "inline-safe"],
            },
            "layout_preferences": {"preferred": "compact", "inline_safe": True},
            "sensitivity_context": {"text": user_context},
            "request_intent": request_intent,
        }
        headers = {
            "Authorization": f"Bearer {self.settings.uniads_dev_api_key}",
            "Content-Type": "application/json",
        }
        endpoint = f"{self.settings.uniads_base_url.rstrip('/')}/v2/sponsor-context"
        try:
            with requests.Session() as session:
                session.trust_env = False
                response = session.post(
                    endpoint,
                    json=payload,
                    headers=headers,
                    timeout=self.settings.uniads_timeout_seconds,
                )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        except Exception:
            return SponsorContext()

        card = self._card_from_payload(data)
        required, risk, reason = classify_permission_need(user_context, data)
        permission_data = data.get("permission") if isinstance(data.get("permission"), dict) else {}
        permission = PermissionState(
            required=required,
            risk_level=risk,
            reason=reason,
            prompt=str(permission_data.get("user_facing_permission_prompt") or "Approve sponsored action before continuing?"),
        )
        return SponsorContext(raw=data, card=card, permission=permission, matched=card is not None)

    def _card_from_payload(self, data: dict[str, Any]) -> SponsorCard | None:
        presentation = data.get("presentation") if isinstance(data.get("presentation"), dict) else {}
        sponsor = data.get("sponsor") if isinstance(data.get("sponsor"), dict) else {}
        card = presentation.get("card") if isinstance(presentation.get("card"), dict) else {}
        title = str(card.get("title") or sponsor.get("title") or "").strip()
        body = str(card.get("body") or sponsor.get("description") or sponsor.get("details") or "").strip()
        if not title and not body:
            return None
        return SponsorCard(
            title=title,
            sponsor=str(card.get("sponsor") or sponsor.get("brand") or sponsor.get("sponsor_name") or "Sponsor"),
            body=body,
            cta_label=str(card.get("cta_label") or card.get("cta") or "Learn more"),
            cta_url=str(card.get("cta_url") or sponsor.get("url") or ""),
            disclosure=str(presentation.get("disclosure_label") or "Sponsored"),
        )


def render_sponsor_card(context: SponsorContext) -> str:
    if not context.card:
        return ""
    card = context.card
    lines = [
        "",
        "---",
        f"**{card.disclosure}: {card.title}**",
    ]
    if card.sponsor:
        lines.append(f"By: {card.sponsor}")
    if card.body:
        lines.append(card.body)
    if card.cta_url:
        lines.append(f"[{card.cta_label}]({card.cta_url})")
    if context.permission.required:
        lines.append(f"Permission needed: {context.permission.prompt}")
    return "\n".join(lines)
