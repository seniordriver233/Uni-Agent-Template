# Agent Hub Compatibility

UniAds Agent Hub can list a developer agent when the agent clearly describes what it does and how it handles sponsored content safely.

## Manifest

This template includes:

```text
uniads.agent.json
```

The manifest is intentionally close to the Agent Hub submission form.

```json
{
  "name": "Uni Agent Template",
  "description": "A modular starter agent...",
  "main_functions": ["chat", "domain tools", "UniAds sponsor context"],
  "ad_compatibility": "Primary answer works without ads...",
  "supported_protocols": ["REST", "SDK", "MCP"],
  "agent_site_url": "",
  "repository_url": "https://github.com/seniordriver233/Uni-Agent-Template"
}
```

Validate before publishing:

```bash
python scripts/validate_agent_hub_compatibility.py
```

## Submission Mapping

| Agent Hub field | Manifest key | Notes |
| --- | --- | --- |
| Agent name | `name` | Clear product name |
| Main functions | `main_functions` | 3-8 concise capabilities |
| Description | `description` | At least 20 characters |
| Compatibility | `ad_compatibility` | Explain proxy-only and fail-open behavior |
| Protocols | `supported_protocols` | REST, SDK, MCP |
| Hosted URL | `agent_site_url` | Optional |
| Repository | `repository_url` | Recommended |

## Compatibility Rules

- The agent must answer even when UniAds is unavailable.
- Sponsored API calls must go through UniAds proxy.
- Sponsor content must be supplemental and visually separable.
- Sensitive sponsored actions require a permission prompt.
- Developer API keys and model API keys must not be committed.
- The `/chat` endpoint should return structured response data that Agent Hub can render.

## ????

Agent Hub ?????????????????????????????????????????? UniAds ?????? API??????????????`uniads.agent.json` ??????????????
