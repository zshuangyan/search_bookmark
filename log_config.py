import os

DIR_PATH = os.path.dirname(__file__)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'debug': {
            'format': '%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': [],
            'class': 'logging.StreamHandler',
            'formatter': 'debug',
        },
        'info_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': 7,
            'filename': os.path.join(DIR_PATH, 'info.log'),
            'formatter': 'debug',
        },
        'exception_handler': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': 7,
            'filename': os.path.join(DIR_PATH, 'error.log'),
            'formatter': 'debug',
        },

    },
    'loggers': {
        '': {
            'handlers': ['console', 'info_handler', 'exception_handler'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}
