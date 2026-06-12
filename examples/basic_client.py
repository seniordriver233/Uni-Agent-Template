from uni_agent_template import DomainAgent

agent = DomainAgent()
response = agent.chat("Recommend an internship search plan for AI agent roles.", language="en")
print(response.assistant_message)
