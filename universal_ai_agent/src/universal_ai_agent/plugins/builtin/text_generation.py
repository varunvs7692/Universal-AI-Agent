from __future__ import annotations

from universal_ai_agent.core.config import AgentConfig
from universal_ai_agent.plugins.base import CapabilityPlugin
from universal_ai_agent.providers.huggingface import HuggingFaceTextProvider


class TextGenerationPlugin(CapabilityPlugin):
    name = "text_generation"
    capability = "text_chat"

    def __init__(self, config: AgentConfig) -> None:
        super().__init__()
        self.config = config
        self.provider = HuggingFaceTextProvider(
            model_name=config.model_name,
            max_length=config.generation_max_length,
        )

    def handle(self, **payload) -> str:
        prompt = payload["prompt"]
        try:
            return self.provider.generate(prompt)
        except Exception as exc:
            if self.context is not None:
                self.context.logger.warning("Text plugin fallback triggered: %s", exc)
            return f"[Gemma4] (text) You said: {prompt}"
