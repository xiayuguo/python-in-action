
from . import celeryconfig
from celery import Celery


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
