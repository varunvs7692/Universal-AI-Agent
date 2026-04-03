from __future__ import annotations

from universal_ai_agent.core.config import AgentConfig
from universal_ai_agent.plugins.base import CapabilityPlugin
from universal_ai_agent.providers.image import ImageProvider


class ImageQAPlugin(CapabilityPlugin):
    name = "image_qa"
    capability = "image_chat"

    def __init__(self, config: AgentConfig) -> None:
        super().__init__()
        self.config = config
        self.provider = ImageProvider(
            vision_qa_model_name=config.vision_qa_model_name,
            image_caption_model_name=config.image_caption_model_name,
            default_prompt=config.default_image_prompt,
        )

    def handle(self, **payload) -> str:
        image_path = payload["image_path"]
        prompt = payload.get("prompt")
        try:
            return self.provider.answer_question(image_path=image_path, prompt=prompt)
        except Exception as exc:
            return f"[Gemma4] (image) Error: {exc}"
