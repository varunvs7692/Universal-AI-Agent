from __future__ import annotations

from universal_ai_agent.core.config import AgentConfig
from universal_ai_agent.core.types import AgentContext
from universal_ai_agent.plugins.builtin import build_builtin_plugins
from universal_ai_agent.plugins.registry import PluginRegistry


def register_builtin_plugins(
    registry: PluginRegistry,
    context: AgentContext,
    config: AgentConfig,
) -> None:
    for plugin in build_builtin_plugins(config):
        plugin.initialize(context)
        registry.register(plugin)
