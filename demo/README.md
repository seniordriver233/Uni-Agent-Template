# Demo: Build A Real Internship Agent Module By Module

This demo is not a toy chat wrapper. It shows how to build a realistic **Internship Agent** on top of the template modules.

Final outcome:

```bash
python demo/internship_agent/internship_agent.py
```

The final agent can:

- infer the user’s target internship track
- extract profile signals
- retrieve trusted internship sources
- run selected planning skills
- generate a weekly application plan
- append UniAds sponsor context safely as a sidecar
- return metadata compatible with Agent Hub

## Module-by-module path

1. `agent_config.json`: declare module config and Agent Hub submission fields.
2. `knowledge_sources.json`: configure trusted internship sources.
3. `internship_agent.py`: customize domain inference and fallback answer.
4. `src/uni_agent_template/memory.py`: reuse or replace profile memory.
5. `src/uni_agent_template/knowledge.py`: reuse lexical retrieval or replace with vector search.
6. `src/uni_agent_template/skills.py`: add skill adapters or MCP/API tools.
7. `src/uni_agent_template/ads.py`: keep UniAds V2 sponsor context proxy-only and fail-open.
8. `src/uni_agent_template/server.py`: expose `/chat` for Agent Hub trials.

## Run the build steps

These older step files remain as learning fragments:

```bash
python demo/step_01_domain_tools.py
python demo/step_02_memory_profile.py
python demo/step_03_primary_agent.py
python demo/step_04_with_uniads.py
```

Then run the realistic final demo:

```bash
python demo/internship_agent/internship_agent.py
```

## Link The Outcome To Agent Hub

After testing, use:

```text
demo/internship_agent/agent_config.json -> agent_hub_submission
```

Copy those fields into UniAds Agent Hub registration:

- agent name
- main functions
- description
- UniAds compatibility
- supported protocols
- repository URL

## 中文说明

这个 Demo 的目标是让开发者看到一个真实的实习智能体如何从模板搭出来：先配置知识源，再配置记忆和技能，再生成主回答，最后接入 UniAds V2。最终结果可以作为 Agent Hub 注册时的 outcome illustration。
