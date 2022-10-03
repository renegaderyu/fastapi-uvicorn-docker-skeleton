#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Application logging configuration."""
import json
import logging.config
import os
from datetime import datetime
from pathlib import Path

import structlog

LOG_FILENAME = "logging_config.json"

timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%dT%H:%M:%S")

structlog.configure(
    processors=[
        timestamper,
        # structlog.stdlib.filter_by_level,
        # structlog.stdlib.add_logger_name,
        structlog.processors.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
        # structlog.dev.ConsoleRenderer(colors=False),
    ],
    wrapper_class=structlog.stdlib.AsyncBoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)

# Load config from file
with open(os.path.join(Path(__file__).parent, LOG_FILENAME)) as f:
    loaded_config = json.loads(f.read())
logging.config.dictConfig(loaded_config)


async def _log(msg, level="INFO", **kwargs):
    temp_logger = structlog.get_logger().bind(**kwargs)
    log_meth = getattr(temp_logger, level.lower(), "info")
    await log_meth(msg)
