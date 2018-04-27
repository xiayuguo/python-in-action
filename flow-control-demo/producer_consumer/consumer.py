"""
    多进程 + 协程
"""

import time
import asyncio
import logging

from functools import wraps
from db import redisdb, select

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("consumer")

def fn_timer(func):
    @wraps(func)
    def func_time(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        logger.info("Total running time %s:%s" %
                (args[0], str(end - start)))
        return ret

    return func_time

async def execute():
    return select("""select * from user_table""", is_pool=True)

@fn_timer
async def run(nums):
    for _ in range(int(nums)):
        await execute()


async def consumer():
    while 1:
        logger.info("接受任务...")
        item = redisdb.get()
        if isinstance(item, int):
            logger.info(item)
        item = item.decode("utf-8")
        # if item == 'over':
        #     redisdb.put('over')
        #     break
        index, nums = item.split(",")
        await run(nums)



if __name__ == '__main__':
    logger.info("开始处理任务...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consumer())
    loop.close()
