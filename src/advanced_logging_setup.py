import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'loggers': {
        'openai-chat': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'detailed',
        },
    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
}


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('openai-chat')