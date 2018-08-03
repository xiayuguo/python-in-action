from celery import Task
from celery.utils.log import get_task_logger

from celerydemo import app

logger = get_task_logger(__name__)


@app.task
def multi(x, y):
    logger.info('x * y')
    return x * y
