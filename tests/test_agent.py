from uni_agent_template.agent import DomainAgent
from uni_agent_template.memory import SessionMemory


def test_agent_fallback_response_without_keys():
    agent = DomainAgent(memory=SessionMemory())
    response = agent.chat("Help me find internship resources", language="en")
    assert "User goal:" in response.assistant_message
    assert response.session_id == "default"
    assert response.knowledge
    assert response.skills
    assert "knowledge_retrieved" in response.workflow
    assert "skills_executed" in response.workflow
    assert "career/internship" in response.profile.goals


def test_memory_keeps_history():
    memory = SessionMemory()
    agent = DomainAgent(memory=memory)
    agent.chat("hello", session_id="s1")
    assert len(memory.get("s1")) == 2


def test_agent_builder_skill_for_template_question():
    agent = DomainAgent(memory=SessionMemory())
    response = agent.chat("How should I build an agent template with MCP tools?", language="en")
    assert any(skill.name == "agent_builder" for skill in response.skills)
    assert any("Agent" in item.title or "LangChain" in item.title for item in response.knowledge)
