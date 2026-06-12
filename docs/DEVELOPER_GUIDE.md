# Developer Guide

## Recommended Structure

This template separates agent code into replaceable modules:

- `agent.py`: orchestration and primary answer generation.
- `llm.py`: OpenAI-compatible model client.
- `ads.py`: UniAds V2 sponsor-context integration.
- `guardrails.py`: permission and sensitive-action boundary.
- `memory.py`: session history.
- `tools.py`: domain utilities and safe external tools.
- `server.py`: FastAPI HTTP surface.

## How To Build Your Agent

1. Rename `DomainAgent` to your product agent name.
2. Replace `compose_primary_answer` with your core logic.
3. Add domain APIs in `tools.py`.
4. Keep UniAds sponsor requests in `ads.py` so every sponsored API stays proxy-only.
5. Keep sponsor content after the primary answer.
6. Return permission prompts for sensitive sponsored actions instead of executing silently.

## UniAds Compatibility Checklist

- Primary answer works without sponsor context.
- Sponsor failure never blocks response.
- `/v2/sponsor-context` is the active endpoint.
- No direct vendor sponsor calls from the agent.
- Developer API key is configured outside source code.
- Sensitive actions require user permission.
