from __future__ import annotations


def infer_request_intent(message: str) -> str:
    text = message.lower()
    if any(term in text for term in ["call api", "execute", "run tool", "book", "buy", "purchase"]):
        return "tool_use"
    if any(term in text for term in ["recommend", "suggest", "which", "choose"]):
        return "recommendation"
    return "direct_answer"


def useful_links_for_domain(message: str) -> list[dict[str, str]]:
    text = message.lower()
    if "intern" in text or "career" in text:
        return [
            {"label": "LinkedIn Jobs", "url": "https://www.linkedin.com/jobs/"},
            {"label": "GitHub student resources", "url": "https://github.com/search?q=awesome+internship"},
        ]
    if "video" in text or "movie" in text:
        return [
            {"label": "IMDb", "url": "https://www.imdb.com/"},
            {"label": "TVMaze", "url": "https://www.tvmaze.com/api"},
        ]
    return []
