from uni_agent_template.agent import DomainAgent
from uni_agent_template.memory import SessionMemory


def test_agent_fallback_response_without_keys():
    agent = DomainAgent(memory=SessionMemory())
    response = agent.chat("Help me find internship resources", language="en")
    assert "Goal:" in response.assistant_message
    assert response.session_id == "default"


def test_memory_keeps_history():
    memory = SessionMemory()
    agent = DomainAgent(memory=memory)
    agent.chat("hello", session_id="s1")
    assert len(memory.get("s1")) == 2
