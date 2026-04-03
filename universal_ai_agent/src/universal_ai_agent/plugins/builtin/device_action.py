from __future__ import annotations

from universal_ai_agent.core.config import AgentConfig
from universal_ai_agent.plugins.base import CapabilityPlugin
from universal_ai_agent.providers.device import DeviceActionProvider


class DeviceActionPlugin(CapabilityPlugin):
    name = "device_action"
    capability = "device_action"

    def __init__(self, config: AgentConfig) -> None:
        super().__init__()
        self.config = config
        self.provider = DeviceActionProvider(
            default_gps_coordinates=config.default_gps_coordinates,
            default_environment_readings=config.default_environment_readings,
        )

    def handle(self, **payload) -> str:
        function_name = payload["function_name"]
        args = payload.get("args", ())
        kwargs = payload.get("kwargs", {})
        return self.provider.execute(function_name, *args, **kwargs)

    def register_action(self, name: str, func) -> None:
        self.provider.register_action(name, func)

    def list_actions(self) -> list[str]:
        return self.provider.list_actions()
