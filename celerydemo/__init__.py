import logging.config

from . import celeryconfig
from celery import Celery


LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s [%(name)s: %(lineno)s] -- %(message)s',
            'datefmt': '%m-%d-%Y %H:%M:%S'
        }
    },
    'handlers': {
        'celerydemo.tasks': {
            'level': 'INFO',
            'filters': None,
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'tasks.log'
        },
        'celerydemo.other': {
            'level': 'INFO',
            'filters': None,
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'other.log'
        },
    },
    'loggers': {
        'celerydemo.tasks': {
            'handlers': ['celerydemo.tasks'],
            'level': 'INFO',
            'propagate': True,
        },
        'celerydemo.other': {
            'handlers': ['celerydemo.other'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)


def create_app():
    app = Celery(
        main="celerydemo",
        include=[
            "celerydemo.tasks",
            "celerydemo.other"
        ]
    )
    app.config_from_object(celeryconfig)
    print(app.conf)
    return app


app = create_app()

