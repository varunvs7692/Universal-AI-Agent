from __future__ import annotations

from dataclasses import dataclass
from logging import Logger
from typing import Any, Callable

from universal_ai_agent.core.config import AgentConfig


CapabilityRouter = Callable[..., Any]


@dataclass(slots=True)
class AgentContext:
    config: AgentConfig
    logger: Logger
    capability_router: CapabilityRouter
