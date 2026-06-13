from __future__ import annotations


def career_sources(goal: str) -> list[dict[str, str]]:
    text = goal.lower()
    sources = [
        {"label": "LinkedIn Jobs", "url": "https://www.linkedin.com/jobs/", "why": "Mainstream job search entry."},
        {"label": "GitHub Internship Resources", "url": "https://github.com/search?q=awesome+internship", "why": "Community-maintained internship resources."},
    ]
    if "agent" in text or "llm" in text or "ai" in text:
        sources.append({"label": "OpenAI Careers", "url": "https://openai.com/careers/", "why": "AI-first company career page."})
    return sources


if __name__ == "__main__":
    for item in career_sources("AI agent internship"):
        print(f"- {item['label']}: {item['why']} ({item['url']})")
