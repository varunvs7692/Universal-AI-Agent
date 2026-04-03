from __future__ import annotations

from universal_ai_agent.core.config import AgentConfig
from universal_ai_agent.plugins.base import CapabilityPlugin
from universal_ai_agent.providers.audio import SpeechRecognitionProvider


class VoiceInputPlugin(CapabilityPlugin):
    name = "voice_input"
    capability = "voice_chat"

    def __init__(self, config: AgentConfig) -> None:
        super().__init__()
        self.config = config
        self.provider = SpeechRecognitionProvider(language=config.language)

    def handle(self, **payload) -> str:
        audio_path = payload["audio_path"]
        try:
            transcript = self.provider.transcribe(audio_path)
            if self.context is None:
                return transcript
            return self.context.capability_router("text_chat", prompt=transcript)
        except Exception as exc:
            return f"[Gemma4] (voice) Error: {exc}"
