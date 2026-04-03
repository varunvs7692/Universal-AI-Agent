from __future__ import annotations

from typing import Any

from universal_ai_agent.core.config import AgentConfig
from universal_ai_agent.core.logging import get_agent_logger
from universal_ai_agent.core.types import AgentContext
from universal_ai_agent.plugins.loader import register_builtin_plugins
from universal_ai_agent.plugins.registry import PluginRegistry


class AgentRuntime:
    """Coordinates configuration, plugin registration, and capability routing."""

    def __init__(self, config: AgentConfig) -> None:
        self.config = config
        self.logger = get_agent_logger()
        self.registry = PluginRegistry(logger=self.logger)
        self.context = AgentContext(
            config=config,
            logger=self.logger,
            capability_router=self.run_capability,
        )
        register_builtin_plugins(self.registry, self.context, config)

    def run_capability(self, capability: str, **payload: Any) -> Any:
        plugin = self.registry.get_plugin(capability)
        if plugin is None:
            return self.config.get_fallback_message(capability)
        try:
            return plugin.handle(**payload)
        except Exception as exc:
            self.logger.warning(
                "Capability '%s' failed in plugin '%s': %s",
                capability,
                plugin.name,
                exc,
            )
            return self.config.get_fallback_message(capability, error=exc)

    def run_text_chat(self, prompt: str) -> str:
        return self.run_capability("text_chat", prompt=prompt)

    def run_voice_chat(self, audio_path: str) -> str:
        return self.run_capability("voice_chat", audio_path=audio_path)

    def run_image_chat(self, image_path: str, prompt: str | None = None) -> str:
        return self.run_capability("image_chat", image_path=image_path, prompt=prompt)

    def run_translation(self, text: str, target_language: str) -> str:
        return self.run_capability(
            "translation",
            text=text,
            target_language=target_language,
        )

    def detect_language(self, text: str) -> str:
        return self.run_capability("translation", operation="detect_language", text=text)

    def run_tts(self, text: str) -> None:
        self.run_capability("tts", text=text)

    def run_device_action(
        self,
        function_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        return self.run_capability(
            "device_action",
            function_name=function_name,
            args=args,
            kwargs=kwargs,
        )

    def register_device_action(self, name: str, func: Any) -> None:
        plugin = self.registry.get_plugin("device_action")
        if plugin is None:
            raise RuntimeError("Device action plugin is not available.")
        plugin.register_action(name, func)

    def list_device_actions(self) -> list[str]:
        plugin = self.registry.get_plugin("device_action")
        if plugin is None:
            return []
        return plugin.list_actions()

    def shutdown(self) -> None:
        self.registry.shutdown_all()
