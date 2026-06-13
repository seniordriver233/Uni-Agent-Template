# Internship Agent Demo

This demo shows a realistic outcome built from `Uni-Agent-Template`: an internship-search agent that profiles the user, retrieves trusted career sources, runs planning skills, and remains compatible with UniAds Agent Hub.

## What The Agent Does

- Interviews or infers user direction from the prompt.
- Extracts profile signals such as target track, strengths, and constraints.
- Searches a curated internship knowledge base.
- Produces a concrete weekly search/application plan.
- Keeps UniAds V2 sponsor context separate from the primary answer.
- Returns structured metadata for Agent Hub: `profile`, `knowledge`, `skills`, `workflow`, and `sponsor`.

## Module Configuration

The demo configuration lives in:

```text
demo/internship_agent/agent_config.json
```

Important module settings:

- `memory`: tracks goals, strengths, preferences, and constraints.
- `knowledge`: loads `knowledge_sources.json` and retrieves top career sources.
- `skills`: enables profile interview, source ranking, and weekly planning.
- `llm`: optional OpenAI-compatible model config through environment variables.
- `uniads`: uses `/v2/sponsor-context`, fail-open, proxy-only, and permission breakpoint.

## Step-By-Step Build

1. Copy the template repo.
2. Replace or extend `demo/internship_agent/knowledge_sources.json` with your own trusted sources.
3. Open `internship_agent.py` and customize `infer_track()` for your domain.
4. Customize `InternshipAgent.fallback_answer()` so the agent remains useful without model keys.
5. Optionally configure `.env` with `MODEL_API_KEY`, `MODEL_BASE_URL`, `MODEL_NAME`, and `UNIADS_DEV_API_KEY`.
6. Run the demo locally.
7. Copy `agent_hub_submission` from `agent_config.json` into the UniAds Agent Hub registration form.

Run:

```bash
python demo/internship_agent/internship_agent.py
```

Expected outcome:

- A direct internship plan.
- Trusted links such as LinkedIn, Google Students, Microsoft University Recruiting, OpenAI Careers, Anthropic Careers, and GitHub internship resources.
- Workflow trace showing profile, knowledge, skills, primary answer, and UniAds stages.

## Serve For Agent Hub Trial

For a hosted trial, expose the template FastAPI server:

```bash
uvicorn uni_agent_template.server:create_app --factory --host 0.0.0.0 --port 8080
```

Then submit the hosted URL or repository URL in Agent Hub. The demo manifest already provides a safe description and UniAds compatibility text.

## 中文说明

这个 Demo 展示了一个真实可用的实习智能体：它会提取用户画像、检索可信招聘入口、生成每周投递计划，并把 UniAds 赞助内容作为主回答之后的补充卡片。开发者可以按模块替换知识源、技能、记忆和回答逻辑，然后把 `agent_config.json` 中的 `agent_hub_submission` 信息复制到 Agent Hub 注册表单。
