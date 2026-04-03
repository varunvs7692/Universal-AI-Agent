import logging

import pytest

from universal_ai_agent.plugins.base import CapabilityPlugin
from universal_ai_agent.plugins.registry import PluginRegistry


class FakePlugin(CapabilityPlugin):
    name = "fake_text"
    capability = "text_chat"

    def handle(self, **payload):
        return payload["prompt"]


def test_registry_registers_and_returns_plugin():
    registry = PluginRegistry(logging.getLogger("test"))
    plugin = FakePlugin()

    registry.register(plugin)

    assert registry.get_plugin("text_chat") is plugin


def test_registry_rejects_duplicate_names():
    registry = PluginRegistry(logging.getLogger("test"))
    registry.register(FakePlugin())

    with pytest.raises(ValueError):
        registry.register(FakePlugin())


def test_registry_activation_requires_matching_capability():
    registry = PluginRegistry(logging.getLogger("test"))
    plugin = FakePlugin()
    registry.register(plugin)

    with pytest.raises(ValueError):
        registry.activate("translation", "fake_text")
