"""Custom logging formatter for JSON output.

This module provides a custom logging formatter, `JSONFormatter`, that outputs
log records in JSON format.

Classes:
    JSONFormatter: A custom logging formatter that generates logs in JSON.
"""

import json
import logging
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """A log formatter that produces log records in JSON format.

    This formatter structures log messages in JSON format, making them
    compatible with observability tools. It includes detailed metadata about
    the log, such as timestamp, level, name, message, context, thread and
    process information. Any additional attributes are merged into the
    `LogRecord` object and are captured as `extra`.

    Attributes:
        record_default_attr (tuple): A tuple containing the default attributes
            of a `logging.LogRecord` object, used to filter out extra
            attributes.
    """

    def __init__(self) -> None:
        """Initializes the JSONFormatter with the record's default attributes.

        The default attributes are derived from a dummy `LogRecord` instance
        created during initialization.
        """
        super().__init__()

        # Create a dummy LogRecord to identify default attributes.
        record = logging.LogRecord('', 0, '', 0, None, None, None)
        self.record_default_attr = tuple(vars(record).keys())

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record as a JSON string.

        Constructs a dictionary representation of the log record, including
        timestamp, log level, logger name, message, context details, thread
        and process information, exception details (if any), and any extra
        attributes not part of the default LogRecord attributes.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: A JSON string representing the formatted log record.
        """
        log = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage(),
            'context': {
                'pathname': record.pathname,
                'file': record.filename,
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
            },
            'thread': {'id': record.thread, 'name': record.threadName},
            'process': {'id': record.process, 'name': record.processName},
        }

        if record.exc_info:
            log['exc_info'] = self.formatException(record.exc_info)

        if record.stack_info:
            log['stack_info'] = self.formatStack(record.stack_info)

        if record.taskName:
            log['taskName'] = record.taskName

        extra = self.get_extra(record)
        if extra:
            log['extra'] = extra

        return json.dumps(log, ensure_ascii=False)

    def get_extra(self, record: logging.LogRecord) -> Dict[str, Any]:
        """Gets and returns the extra attributes from the given logging record.

        Extracts additional attributes from a logging record that are not
        part of the default attributes.

        Args:
            record (logging.LogRecord): The logging record containing the
                attributes to process.

        Returns:
            Dict[str, Any]: A dictionary containing all attributes from the
                logging record that are not included in
                `self.record_default_attr`.
        """
        extra = {}
        for attr in vars(record):
            if attr not in self.record_default_attr:
                extra[attr] = getattr(record, attr)
        return extra
