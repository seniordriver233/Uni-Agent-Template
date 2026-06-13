from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from .sources import SourceCatalog, SourceEntry

TOKEN_RE = re.compile(r"[a-zA-Z0-9_\-]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


@dataclass(frozen=True)
class RetrievedKnowledge:
    entry: SourceEntry
    score: float
    reason: str


class KnowledgeBase:
    """Small lexical retriever that developers can replace with vector DB/RAG."""

    def __init__(self, catalog: SourceCatalog | None = None) -> None:
        self.catalog = catalog or SourceCatalog()

    def search(self, query: str, *, limit: int = 5) -> list[RetrievedKnowledge]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        q = Counter(query_tokens)
        results: list[RetrievedKnowledge] = []
        for entry in self.catalog.all():
            text = " ".join([entry.title, entry.summary, " ".join(entry.tags)])
            d = Counter(tokenize(text))
            overlap = sum(min(q[token], d[token]) for token in q)
            tag_bonus = sum(1 for token in set(q) if token in {tag.lower() for tag in entry.tags})
            if overlap == 0 and tag_bonus == 0:
                continue
            q_norm = math.sqrt(sum(value * value for value in q.values())) or 1.0
            d_norm = math.sqrt(sum(value * value for value in d.values())) or 1.0
            score = overlap / (q_norm * d_norm) + 0.15 * tag_bonus
            results.append(RetrievedKnowledge(entry=entry, score=round(score, 4), reason="lexical/tag match"))
        results.sort(key=lambda item: item.score, reverse=True)
        return results[:limit]

    def context_block(self, query: str, *, limit: int = 4) -> str:
        items = self.search(query, limit=limit)
        if not items:
            return "No knowledge matches found."
        lines = ["Relevant knowledge sources:"]
        for item in items:
            lines.append(f"- {item.entry.title}: {item.entry.summary} ({item.entry.url})")
        return "\n".join(lines)
