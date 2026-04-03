from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


DEFAULT_ENABLED_PLUGINS = (
    "text_generation",
    "voice_input",
    "image_qa",
    "translation",
    "tts",
    "device_action",
)


@dataclass(slots=True)
class AgentConfig:
    language: str = "en"
    model_name: str = "google/gemma-2b-it"
    translation_model_name: str = "facebook/m2m100_418M"
    vision_qa_model_name: str = "dandelin/vilt-b32-finetuned-vqa"
    image_caption_model_name: str = "Salesforce/blip-image-captioning-base"
    default_image_prompt: str = "What is in this image?"
    default_gps_coordinates: tuple[float, float] = (28.6139, 77.2090)
    default_environment_readings: dict[str, float] = field(
        default_factory=lambda: {
            "temperature_c": 24.5,
            "humidity_percent": 58.0,
            "air_quality_index": 42.0,
            "light_lux": 315.0,
        }
    )
    generation_max_length: int = 128
    enabled_plugins: tuple[str, ...] = DEFAULT_ENABLED_PLUGINS
    plugin_settings: dict[str, dict[str, Any]] = field(default_factory=dict)
    fallback_messages: dict[str, str] = field(
        default_factory=lambda: {
            "text_chat": "[Gemma4] (text) Model unavailable.",
            "voice_chat": "[Gemma4] (voice) Voice processing unavailable.",
            "image_chat": "[Gemma4] (image) Vision model integration needed.",
            "translation": "[Gemma4] (translate) Translation unavailable.",
            "tts": "[Gemma4] (tts) TTS engine not available.",
            "device_action": "[Gemma4] (function) Device function unavailable.",
        }
    )

    @classmethod
    def from_legacy(
        cls,
        language: str,
        model_name: str,
        enabled_plugins: list[str] | None = None,
    ) -> "AgentConfig":
        return cls(
            language=language,
            model_name=model_name,
            enabled_plugins=tuple(enabled_plugins or DEFAULT_ENABLED_PLUGINS),
        )

    def is_enabled(self, plugin_name: str) -> bool:
        return plugin_name in self.enabled_plugins

    def get_plugin_settings(self, plugin_name: str) -> dict[str, Any]:
        return self.plugin_settings.get(plugin_name, {})

    def get_fallback_message(self, capability: str, error: Exception | None = None) -> str:
        base_message = self.fallback_messages.get(
            capability,
            "[Gemma4] Capability unavailable.",
        )
        if error is None:
            return base_message
        return f"{base_message} Error: {error}"
