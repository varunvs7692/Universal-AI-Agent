from universal_ai_agent import AgentConfig, UniversalAIAgent


def test_agent_constructs_with_default_plugins():
    agent = UniversalAIAgent(config=AgentConfig())

    plugins = agent.runtime.registry.list_plugins()

    assert "text_generation" in plugins
    assert "voice_input" in plugins
    assert "translation" in plugins
    assert "device_action" in plugins
    assert "send_sms" in agent.list_device_plugins()
