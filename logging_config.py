"""Configures the logging system for the WhatsApp Echo Bot project."""

LOGGER_NAME = 'whatsapp_echo_bot'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        LOGGER_NAME: {
            'handlers': ['file',],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': f'./logs/{LOGGER_NAME}.log',
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
    },
    'formatters': {
        'standard': {
            'format': '{asctime} - {levelname} - {name} - {funcName} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M',
        },
    },
}
