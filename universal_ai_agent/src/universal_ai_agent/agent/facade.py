from __future__ import annotations

from typing import Any, Optional

from universal_ai_agent.agent.runtime import AgentRuntime
from universal_ai_agent.core.config import AgentConfig


class UniversalAIAgent:
    """
    Backwards-compatible public facade for the Universal AI Agent.

    The facade preserves the original single-class interface while delegating all
    capability work to the modular runtime and plugin registry.
    """

    def __init__(
        self,
        language: str = "en",
        model_name: str = "google/gemma-2b-it",
        config: Optional[AgentConfig] = None,
        enabled_plugins: Optional[list[str]] = None,
    ) -> None:
        self.config = config or AgentConfig.from_legacy(
            language=language,
            model_name=model_name,
            enabled_plugins=enabled_plugins,
        )
        self.runtime = AgentRuntime(self.config)

    def text_chat(self, prompt: str) -> str:
        return self.runtime.run_text_chat(prompt)

    def voice_chat(self, audio_path: str) -> str:
        return self.runtime.run_voice_chat(audio_path)

    def image_chat(self, image_path: str, prompt: Optional[str] = None) -> str:
        return self.runtime.run_image_chat(image_path=image_path, prompt=prompt)

    def translate(self, text: str, target_language: str) -> str:
        return self.runtime.run_translation(text=text, target_language=target_language)

    def detect_language(self, text: str) -> str:
        return self.runtime.detect_language(text)

    def speak(self, text: str) -> None:
        self.runtime.run_tts(text)

    def register_plugin(self, name: str, func: Any) -> None:
        self.runtime.register_device_action(name, func)

    def list_device_plugins(self) -> list[str]:
        return self.runtime.list_device_actions()

    def call_local_function(self, function_name: str, *args: Any, **kwargs: Any) -> Any:
        return self.runtime.run_device_action(
            function_name=function_name,
            args=args,
            kwargs=kwargs,
        )

    def shutdown(self) -> None:
        self.runtime.shutdown()
