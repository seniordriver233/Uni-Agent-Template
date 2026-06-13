# Agent Hub Compatibility

UniAds Agent Hub can list a developer agent when the agent clearly describes what it does, exposes a predictable API, and handles sponsored content safely.

## Manifest

This template includes `uniads.agent.json`. Validate before publishing:

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
- The response should include useful metadata: profile, knowledge, skill traces, and workflow stages.

## 中文说明

Agent Hub 审核重点不是“广告越强越好”，而是：主功能是否可靠、赞助内容是否边界清晰、是否只通过 UniAds 代理访问赞助 API、敏感动作是否需要用户许可。`uniads.agent.json` 是给开发者准备的发布清单，`/chat` 返回的结构化字段则帮助 Agent Hub 更好地展示智能体能力。
