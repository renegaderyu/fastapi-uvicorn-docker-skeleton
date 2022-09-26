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


def timestamper(_, __, event_dict):
    """Structlog processors to create timestamps as we wish"""
    event_dict["@timestamp"] = datetime.now().isoformat()
    return event_dict


structlog.configure(
    processors=[
        timestamper,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        # structlog.processors.JSONRenderer(),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)

# Load config from file
with open(os.path.join(Path(__file__).parent, LOG_FILENAME)) as f:
    loaded_config = json.loads(f.read())
logging.config.dictConfig(loaded_config)


def _log(msg, level="INFO", **kwargs):
    temp_logger = structlog.get_logger().bind(**kwargs)
    log_meth = getattr(temp_logger, level.lower(), "info")
    log_meth(msg)
