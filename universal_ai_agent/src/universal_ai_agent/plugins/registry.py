from __future__ import annotations

from logging import Logger

from universal_ai_agent.plugins.base import CapabilityPlugin


class PluginRegistry:
    """Stores plugins by name and active capability mapping."""

    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self._plugins_by_name: dict[str, CapabilityPlugin] = {}
        self._active_capabilities: dict[str, str] = {}

    def register(self, plugin: CapabilityPlugin) -> None:
        if plugin.name in self._plugins_by_name:
            raise ValueError(f"Plugin '{plugin.name}' is already registered.")
        self._plugins_by_name[plugin.name] = plugin
        self._active_capabilities.setdefault(plugin.capability, plugin.name)

    def activate(self, capability: str, plugin_name: str) -> None:
        if plugin_name not in self._plugins_by_name:
            raise KeyError(f"Plugin '{plugin_name}' is not registered.")
        plugin = self._plugins_by_name[plugin_name]
        if plugin.capability != capability:
            raise ValueError(
                f"Plugin '{plugin_name}' does not implement capability '{capability}'."
            )
        self._active_capabilities[capability] = plugin_name

    def get_plugin(self, capability: str) -> CapabilityPlugin | None:
        plugin_name = self._active_capabilities.get(capability)
        if plugin_name is None:
            return None
        return self._plugins_by_name.get(plugin_name)

    def list_plugins(self) -> dict[str, CapabilityPlugin]:
        return dict(self._plugins_by_name)

    def shutdown_all(self) -> None:
        for plugin in self._plugins_by_name.values():
            try:
                plugin.shutdown()
            except Exception as exc:
                self.logger.warning("Failed to shutdown plugin '%s': %s", plugin.name, exc)
