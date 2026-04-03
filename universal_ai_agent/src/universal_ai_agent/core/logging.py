from __future__ import annotations

import logging


def get_agent_logger() -> logging.Logger:
    logger = logging.getLogger("universal_ai_agent")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(name)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger
