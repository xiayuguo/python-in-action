"""
生产者: 进车, 全部存入redis
"""
import random

from collections import namedtuple
from db import redisdb


def produce(num=10):
    Task = namedtuple("Task", "index nums")
    random.seed(10)
    for index in range(num):
        task = Task(index=index, nums=random.randint(1, 5))
        print(task)
        redisdb.put('%s,%s' % task)
    # redisdb.put("over")


if __name__ == "__main__":
    produce(100)
