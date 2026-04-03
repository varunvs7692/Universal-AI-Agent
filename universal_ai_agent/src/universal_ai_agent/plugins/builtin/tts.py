from __future__ import annotations

from universal_ai_agent.core.config import AgentConfig
from universal_ai_agent.plugins.base import CapabilityPlugin
from universal_ai_agent.providers.tts import Pyttsx3Provider


class TTSPlugin(CapabilityPlugin):
    name = "tts"
    capability = "tts"

    def __init__(self, config: AgentConfig) -> None:
        super().__init__()
        self.config = config
        self.provider = Pyttsx3Provider()

    def handle(self, **payload) -> None:
        text = payload["text"]
        try:
            self.provider.speak(text)
        except Exception:
            if self.context is not None:
                self.context.logger.warning(self.config.get_fallback_message("tts"))
