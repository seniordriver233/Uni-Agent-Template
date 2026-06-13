# Demo: Build Your Agent Module By Module

This directory teaches the intended development path. The examples build a tiny career-planning agent, but the same pattern works for entertainment, education, GEO, video, finance, or internal business agents.

## Step 0: Validate Hub Metadata

```bash
python scripts/validate_agent_hub_compatibility.py
```

## Step 1: Domain Tools

Open `step_01_domain_tools.py`. Define deterministic tools first. Tools should be useful even without an LLM.

```bash
python demo/step_01_domain_tools.py
```

## Step 2: Memory And Profile

Open `step_02_memory_profile.py`. This shows lightweight user profile extraction. In production, replace in-memory storage with your DB.

```bash
python demo/step_02_memory_profile.py
```

## Step 3: Primary Agent Answer

Open `step_03_primary_agent.py`. This connects tools and memory into a primary answer. No sponsor logic yet.

```bash
python demo/step_03_primary_agent.py
```

## Step 4: Attach UniAds V2

Open `step_04_with_uniads.py`. This uses `DomainAgent`, which preserves the primary answer and appends sponsor context if available.

```bash
python demo/step_04_with_uniads.py
```

## Step 5: Serve Through FastAPI

```bash
uvicorn uni_agent_template.server:create_app --factory --host 127.0.0.1 --port 8080
```

## Step 6: Final Example Agent

`final_career_agent.py` is a small complete agent you can copy and rename.

```bash
python demo/final_career_agent.py
```

## 中文提示

开发顺序建议是：先工具，再记忆，再主回答，最后接 UniAds。不要一开始就把广告逻辑写进 prompt。这样 Agent 更稳定，也更容易通过 Agent Hub 审核。
