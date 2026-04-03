from universal_agent import UniversalAIAgent
from universal_ai_agent.core.config import AgentConfig


def test_facade_routes_to_plugins(monkeypatch):
    agent = UniversalAIAgent(config=AgentConfig())

    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("text_chat").provider,
        "generate",
        lambda prompt: f"text:{prompt}",
    )
    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("voice_chat").provider,
        "transcribe",
        lambda audio_path: f"voice:{audio_path}",
    )
    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("image_chat").provider,
        "answer_question",
        lambda image_path, prompt=None: f"image:{image_path}:{prompt}",
    )
    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("translation").provider,
        "translate",
        lambda text, target_language: f"{target_language}:{text}",
    )
    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("translation").provider,
        "detect_language",
        lambda text: "en",
    )
    spoken = []
    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("tts").provider,
        "speak",
        lambda text: spoken.append(text),
    )

    assert agent.text_chat("hello") == "text:hello"
    assert agent.voice_chat("clip.wav") == "text:voice:clip.wav"
    assert agent.image_chat("image.jpg", prompt="What is here?") == "image:image.jpg:What is here?"
    assert agent.translate("hello", "fr") == "fr:hello"
    assert agent.detect_language("hello") == "en"
    agent.speak("hi")
    assert spoken == ["hi"]
    assert "sms" in agent.call_local_function("send_sms", "+1", message="test").lower()


def test_device_plugin_registration():
    agent = UniversalAIAgent(config=AgentConfig())
    agent.register_plugin("echo_device", lambda message: f"echo:{message}")

    assert "echo_device" in agent.list_device_plugins()
    assert agent.call_local_function("echo_device", "hello") == "echo:hello"
    assert "gps" in agent.call_local_function("get_gps_location").lower()
    assert "camera" in agent.call_local_function("capture_image")
    assert "sensor" in agent.call_local_function("read_environment")


def test_text_translation_and_image_fallbacks(monkeypatch):
    agent = UniversalAIAgent(config=AgentConfig())

    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("text_chat").provider,
        "generate",
        lambda prompt: (_ for _ in ()).throw(RuntimeError("text boom")),
    )
    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("translation").provider,
        "translate",
        lambda text, target_language: (_ for _ in ()).throw(RuntimeError("translate boom")),
    )
    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("translation").provider,
        "detect_language",
        lambda text: "en",
    )
    monkeypatch.setattr(
        agent.runtime.registry.get_plugin("image_chat").provider,
        "answer_question",
        lambda image_path, prompt=None: (_ for _ in ()).throw(RuntimeError("image boom")),
    )

    assert agent.text_chat("hello") == "[Gemma4] (text) You said: hello"
    assert (
        agent.translate("hello", "fr")
        == "[Gemma4] (translate) hello -> fr (translation model integration needed)"
    )
    assert agent.image_chat("image.jpg") == "[Gemma4] (image) Error: image boom"
