from demo.internship_agent.internship_agent import InternshipAgent


def test_internship_demo_returns_realistic_agent_metadata():
    response = InternshipAgent().chat(
        "I want an AI agent internship and I know Python.",
        session_id="test-internship-demo",
        language="en",
    )
    assert "AI agent / LLM application internship" in response.assistant_message
    assert response.knowledge
    assert response.skills
    assert "Python" in response.profile.strengths
    assert response.workflow == [
        "profile_updated",
        "knowledge_retrieved",
        "skills_executed",
        "primary_answer_ready",
        "uniads_context_checked",
    ]
