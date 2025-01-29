"""Logging configuration for the application.

This module sets up logging for the application, using a custom `JSONFormatter`
to structure log messages in JSON format. The configuration is compatible with
observability tools and can be customized via environment variables.

Attributes:
    LOG_PATH (str): The directory path where log files will be stored.
        Defaults to './log'.
    LOG_LEVEL (str): The logging level. Defaults to 'DEBUG'.
    PROJECT_NAME (str): The name of the project, used to name the log
        file. Defaults to 'app'.
    APP (str): The package name of the project, used as the
        logger name. Defaults to 'app'.

Functions:
    setup_logging: Configures the logging system.
"""

import logging
import logging.config
import os
import pathlib
import tomllib

from whatsapp_echo_bot.logging.formatter import JSONFormatter
from whatsapp_echo_bot.logging.handler import handler_factory

LOG_PATH = os.getenv('FLASK_LOG_PATH', './log')
LOG_LEVEL = os.getenv('FLASK_LOG_LEVEL', 'DEBUG')
with open('pyproject.toml', 'rb') as file:
    data = tomllib.load(file)
    PROJECT_NAME = data.get('tool', {}).get('poetry', {}).get('name', 'app')
APP = os.getenv('FLASK_APP', 'app')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        APP: {
            'handlers': ['file'],
            'level': LOG_LEVEL,
            'propagate': True,
        }
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            '()': handler_factory,
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'filename': f'{LOG_PATH}/{PROJECT_NAME}.log',
            'encoding': 'utf-8',
            'utc': True,
            'formatter': 'json',
        }
    },
    'formatters': {
        'json': {
            '()': JSONFormatter,
        }
    },
}


def setup_logging():
    """Configures the logging system.

    Creates the log directory (if it doesn't exist) and applies the logging
    configuration defined in `LOGGING_CONFIG`.
    """
    pathlib.Path(LOG_PATH).mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)
