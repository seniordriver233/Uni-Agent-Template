# Uni-Agent-Template

A clean, modular starter for building agents that can join UniAds without letting sponsor logic damage the primary user experience.

The template is original code, but its structure is informed by modern open-source agent projects:

- [OpenAI Agents SDK for Python](https://github.com/openai/openai-agents-python): lightweight, provider-agnostic agent primitives for multi-agent workflows.
- [OpenAI Agents SDK for TypeScript](https://github.com/openai/openai-agents-js): small set of production-oriented agent abstractions.
- [LangChain](https://github.com/langchain-ai/langchain): interoperable components for tools, models, retrieval, and agent applications.
- [LangChain Open Agent Platform](https://github.com/langchain-ai/open-agent-platform): useful product reference for agent management, tools, MCP, and supervised publication flows.

This repo does not vendor or copy those projects. It provides a practical UniAds-compatible template with a small dependency surface.

## What You Get

- Modular Python package under `src/uni_agent_template/`.
- OpenAI-compatible chat-completions client.
- UniAds V2 sponsor-context client.
- Permission breakpoint support for sensitive sponsored actions.
- Fail-open behavior: sponsor failure never blocks the main answer.
- Compact sponsor card renderer.
- FastAPI server for web deployment.
- CLI smoke test and minimal tests.

## Quick Start

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -e .[server,test]
copy .env.example .env
python scripts/smoke_test.py "Help me plan an internship search for AI agent roles."
uvicorn uni_agent_template.server:create_app --factory --host 127.0.0.1 --port 8080
```

Then call:

```bash
curl -X POST http://127.0.0.1:8080/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Help me choose a tool for internship search\"}"
```

## Configuration

Use environment variables or `.env`:

```text
MODEL_API_KEY=your-model-key
MODEL_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4.1-mini
UNIADS_BASE_URL=http://103.242.15.56
UNIADS_DEV_API_KEY=sk-dev-your-key
UNIADS_AGENT_ID=my-agent
UNIADS_AGENT_NAME=My Agent
```

Never commit real API keys.

## UniAds Contract

The agent always produces the primary answer first. UniAds sponsor context is supplemental.

Flow:

1. Generate or fallback the primary answer.
2. Request `/v2/sponsor-context` through the UniAds proxy.
3. Render compact sponsor card after the answer if a campaign matches.
4. If `permission.required=true`, return a permission prompt instead of executing sponsored actions.
5. If UniAds fails, return the primary answer unchanged.

See [docs/UNIADS_ADS_MODULE.md](docs/UNIADS_ADS_MODULE.md).

## Developer Extension Points

- `src/uni_agent_template/agent.py`: replace `DomainAgent.compose_primary_answer` with your domain logic.
- `src/uni_agent_template/tools.py`: add safe tools and API clients.
- `src/uni_agent_template/memory.py`: replace in-memory storage with database/Redis.
- `src/uni_agent_template/server.py`: expose extra endpoints.

## License

MIT. See [LICENSE](LICENSE).
