from celery import Task
from celery.utils.log import get_task_logger

from celerydemo import app

logger = get_task_logger(__name__)

print("tasks's logger is %s" % logger)



class AddTask(Task):

    def run(self, x, y):
        logger.info("Calling task add(%d, %d)" % (x, y))
        return x + y


AddTask = app.register_task(AddTask())


class SubstractTask(Task):

    def run(self, x, y):
        logger.info("Calling task subtract(%d, %d)" % (x, y))
        return x - y


SubstractTask = app.register_task(SubstractTask())
