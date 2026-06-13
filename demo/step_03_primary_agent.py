from __future__ import annotations

try:
    from demo.step_01_domain_tools import career_sources
    from demo.step_02_memory_profile import CandidateProfile
except ModuleNotFoundError:
    from step_01_domain_tools import career_sources
    from step_02_memory_profile import CandidateProfile


def compose_primary_answer(message: str, profile: CandidateProfile) -> str:
    profile.update_from_message(message)
    sources = career_sources(message)
    lines = [
        "Primary answer first:",
        f"Profile signal: {profile.summary()}",
        "Recommended first actions:",
        "1. Define target roles: AI agent engineer, LLM product intern, or AI tooling intern.",
        "2. Prepare one portfolio project that demonstrates agent workflow design.",
        "3. Search official career pages first, then use job boards as backup.",
        "Useful sources:",
    ]
    lines.extend([f"- {item['label']}: {item['url']}" for item in sources])
    return "\n".join(lines)


if __name__ == "__main__":
    profile = CandidateProfile()
    print(compose_primary_answer("I want an AI agent internship and I know Python.", profile))
