from __future__ import annotations

from universal_ai_agent.core.config import AgentConfig
from universal_ai_agent.plugins.base import CapabilityPlugin
from universal_ai_agent.providers.huggingface import MultilingualTranslationProvider


class TranslationPlugin(CapabilityPlugin):
    name = "translation"
    capability = "translation"

    def __init__(self, config: AgentConfig) -> None:
        super().__init__()
        self.config = config
        self.provider = MultilingualTranslationProvider(config.translation_model_name)

    def handle(self, **payload) -> str:
        text = payload["text"]
        if payload.get("operation") == "detect_language":
            return self.provider.detect_language(text)
        target_language = payload["target_language"]
        try:
            return self.provider.translate(text=text, target_language=target_language)
        except Exception as exc:
            if self.context is not None:
                self.context.logger.warning("Translation plugin fallback triggered: %s", exc)
            return f"[Gemma4] (translate) {text} -> {target_language} (translation model integration needed)"
