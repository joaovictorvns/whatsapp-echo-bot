"""Module for custom logging handlers."""

import logging.handlers
import pathlib
from typing import Any


def namer(filename: str) -> str:
    """Generate a new log file name with a timestamp.

    Args:
        filename (str): The original log file name.

    Returns:
        str: The new log file name with the timestamp in the middle.
    """
    log_file = pathlib.Path(filename)
    name, ext, timestamp = log_file.name.split('.')
    return str(log_file.parent / f'{name}.{timestamp}.{ext}')


def handler_factory(
    *args: Any, **kwargs: Any
) -> logging.handlers.TimedRotatingFileHandler:
    """Create a TimedRotatingFileHandler with a custom namer.

    Args:
        *args (Any): Variable length argument list for
            TimedRotatingFileHandler.
        **kwargs (Any): Arbitrary keyword arguments for
            TimedRotatingFileHandler.

    Returns:
        logging.handlers.TimedRotatingFileHandler: Configured file handler.
    """
    handler = logging.handlers.TimedRotatingFileHandler(*args, **kwargs)
    handler.namer = namer
    return handler
