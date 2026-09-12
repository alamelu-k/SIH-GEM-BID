"""
common/logging_config.py

One shared logger setup so log lines from every Pod 4 module look
consistent and are easy to trace during integration/demo debugging.

Usage in any module:
    from common.logging_config import get_logger
    logger = get_logger(__name__)
    logger.info("Extracted %d fields from document %s", len(fields), doc_id)
"""

import logging
import sys

_CONFIGURED = False

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger once. Safe to call multiple times —
    subsequent calls are no-ops."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger, ensuring root config has run first."""
    configure_logging()
    return logging.getLogger(name)
