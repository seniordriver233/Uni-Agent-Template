from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class SourceEntry:
    id: str
    title: str
    url: str
    summary: str
    tags: tuple[str, ...] = field(default_factory=tuple)
    source_type: str = "reference"
    language: str = "en"


DEFAULT_SOURCES: tuple[SourceEntry, ...] = (
    SourceEntry(
        id="openai-agents-python",
        title="OpenAI Agents SDK for Python",
        url="https://github.com/openai/openai-agents-python",
        summary="Lightweight primitives for agents, tools, handoffs, tracing, and model-agnostic workflows.",
        tags=("agent", "sdk", "tools", "workflow", "openai"),
    ),
    SourceEntry(
        id="openai-agents-js",
        title="OpenAI Agents SDK for TypeScript",
        url="https://github.com/openai/openai-agents-js",
        summary="TypeScript agent runtime with tools, handoffs, guardrails, and structured outputs.",
        tags=("agent", "typescript", "sdk", "tools"),
    ),
    SourceEntry(
        id="langchain",
        title="LangChain",
        url="https://github.com/langchain-ai/langchain",
        summary="Composable model, retrieval, tool, and chain abstractions for production LLM applications.",
        tags=("agent", "retrieval", "tools", "rag", "workflow"),
    ),
    SourceEntry(
        id="open-agent-platform",
        title="LangChain Open Agent Platform",
        url="https://github.com/langchain-ai/open-agent-platform",
        summary="Reference platform for managing agents, MCP tools, and supervised publication flows.",
        tags=("agent hub", "platform", "mcp", "admin", "template"),
    ),
    SourceEntry(
        id="linkedin-jobs",
        title="LinkedIn Jobs",
        url="https://www.linkedin.com/jobs/",
        summary="Mainstream job search entry for current role discovery and company filtering.",
        tags=("career", "internship", "jobs", "search"),
    ),
    SourceEntry(
        id="github-internships",
        title="GitHub Internship Resources",
        url="https://github.com/search?q=awesome+internship",
        summary="Community-maintained internship lists, preparation guides, and role discovery resources.",
        tags=("career", "internship", "github", "student"),
    ),
    SourceEntry(
        id="imdb",
        title="IMDb",
        url="https://www.imdb.com/",
        summary="Movie and TV metadata reference useful for entertainment recommendation agents.",
        tags=("entertainment", "movie", "video", "recommendation"),
    ),
    SourceEntry(
        id="tvmaze-api",
        title="TVMaze API",
        url="https://www.tvmaze.com/api",
        summary="Open API for TV metadata, show search, episode data, and recommendation prototypes.",
        tags=("entertainment", "video", "api", "open data"),
    ),
)


class SourceCatalog:
    def __init__(self, entries: Iterable[SourceEntry] = DEFAULT_SOURCES) -> None:
        self.entries = list(entries)

    def all(self) -> list[SourceEntry]:
        return list(self.entries)

    def by_tag(self, tag: str, *, limit: int = 5) -> list[SourceEntry]:
        normalized = tag.lower().strip()
        return [
            entry
            for entry in self.entries
            if normalized in {item.lower() for item in entry.tags}
        ][:limit]
