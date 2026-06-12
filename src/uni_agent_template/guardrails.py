from __future__ import annotations

SENSITIVE_TERMS = {
    "buy", "purchase", "pay", "payment", "medical", "diagnosis", "legal", "lawsuit",
    "investment", "loan", "insurance", "personal data", "upload private",
}


def classify_permission_need(user_message: str, sponsor_payload: dict) -> tuple[bool, str, str]:
    text = f"{user_message} {sponsor_payload}".lower()
    if any(term in text for term in SENSITIVE_TERMS):
        return True, "medium", "The request may involve sensitive or transactional sponsored action."
    permission = sponsor_payload.get("permission") if isinstance(sponsor_payload, dict) else None
    if isinstance(permission, dict) and permission.get("required"):
        return True, str(permission.get("risk_level") or "medium"), str(permission.get("reason") or "Sponsor requires approval.")
    return False, "low", "No sensitive sponsored action detected."


def preserve_primary_answer(answer: str) -> str:
    return answer.strip() or "I can help, but I need a little more detail about your goal and constraints."
