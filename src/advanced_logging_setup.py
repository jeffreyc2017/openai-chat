import logging.config
import os

log_directory = "./logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

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
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './logs/app.log',
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