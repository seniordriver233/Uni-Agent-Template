from __future__ import annotations

from fastapi import FastAPI

from .agent import DomainAgent
from .schemas import ChatRequest, ChatResponse


def create_app() -> FastAPI:
    app = FastAPI(title="Uni Agent Template", version="0.1.0")
    agent = DomainAgent()

    @app.get("/health")
    def health() -> dict[str, bool]:
        return {"ok": True}

    @app.post("/chat", response_model=ChatResponse)
    def chat(request: ChatRequest) -> ChatResponse:
        return agent.chat(
            request.message,
            session_id=request.session_id,
            history=request.history,
            language=request.language,
        )

    return app
