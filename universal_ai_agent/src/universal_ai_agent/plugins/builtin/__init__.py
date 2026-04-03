from __future__ import annotations

from universal_ai_agent.core.config import AgentConfig
from universal_ai_agent.plugins.base import CapabilityPlugin
from universal_ai_agent.plugins.builtin.device_action import DeviceActionPlugin
from universal_ai_agent.plugins.builtin.image_qa import ImageQAPlugin
from universal_ai_agent.plugins.builtin.text_generation import TextGenerationPlugin
from universal_ai_agent.plugins.builtin.translation import TranslationPlugin
from universal_ai_agent.plugins.builtin.tts import TTSPlugin
from universal_ai_agent.plugins.builtin.voice_input import VoiceInputPlugin


def build_builtin_plugins(config: AgentConfig) -> list[CapabilityPlugin]:
    plugins: list[CapabilityPlugin] = []
    for plugin in (
        TextGenerationPlugin(config),
        VoiceInputPlugin(config),
        ImageQAPlugin(config),
        TranslationPlugin(config),
        TTSPlugin(config),
        DeviceActionPlugin(config),
    ):
        if config.is_enabled(plugin.name):
            plugins.append(plugin)
    return plugins
