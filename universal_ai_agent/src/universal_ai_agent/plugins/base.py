from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from universal_ai_agent.core.types import AgentContext


class CapabilityPlugin(ABC):
    """Base class for capability-oriented plugins."""

    name = "base_plugin"
    capability = "base_capability"
    version = "0.1.0"

    def __init__(self) -> None:
        self.context: AgentContext | None = None

    def initialize(self, context: AgentContext) -> None:
        self.context = context

    @abstractmethod
    def handle(self, **payload: Any) -> Any:
        raise NotImplementedError

    def shutdown(self) -> None:
        return None
