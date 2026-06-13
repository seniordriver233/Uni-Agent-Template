from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CandidateProfile:
    goals: list[str] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)

    def update_from_message(self, message: str) -> None:
        text = message.lower()
        if "intern" in text:
            self.goals.append("internship")
        if "agent" in text or "llm" in text:
            self.preferences.append("AI agent / LLM products")
        if "python" in text:
            self.strengths.append("Python")

    def summary(self) -> str:
        return " | ".join([
            f"goals={sorted(set(self.goals))}",
            f"strengths={sorted(set(self.strengths))}",
            f"preferences={sorted(set(self.preferences))}",
        ])


if __name__ == "__main__":
    profile = CandidateProfile()
    profile.update_from_message("I want an AI agent internship and I know Python.")
    print(profile.summary())
