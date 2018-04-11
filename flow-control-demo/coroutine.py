import time
import random
import string
import asyncio

from queue import Queue
from itertools import groupby
from operator import itemgetter
from collections import namedtuple
from threading import Thread


"""
    生产者: 乘坐电梯的人
    消费者: 电梯
"""

STOP, UP, DOWN = 0, 1, 2  # 电梯运行时的三种状态
LiftEvent = namedtuple('LiftEvent', 'user start end')

queue = Queue()


@asyncio.coroutine
def cost(seconds=0):
    yield from asyncio.sleep(seconds)


class LiftConfig:
    """每个电梯的配置"""

    INOUT_TIME = 2  # 进出电梯时间(电梯打开时的停留时间), 单位: seconds
    SPEED = 1  # 电梯运行时经历每层的时间, 单位: seconds
    VOLUME = 20  # 电梯所能容纳的人数
    DEFAULT_FLOOR = 1  # 电梯所处的默认楼层, 默认为一楼
    FLOOR_RANGE = range(0, 30)  # 默认为0-29, 0为负一层


class Consumer(object):
    def __init__(self, name='', speed=LiftConfig.SPEED, volume=LiftConfig.VOLUME,
                 default_floor=LiftConfig.DEFAULT_FLOOR, floor_range=LiftConfig.FLOOR_RANGE,
                 inout_time=LiftConfig.INOUT_TIME, *args, **kwargs):
        self.name = name
        self.speed = speed
        self.volume = volume
        self.inout_time = inout_time
        self.current_floor = default_floor
        self.floor_range = floor_range
        self.event = []
        self.status = STOP

    @asyncio.coroutine
    def up(self):
        if self.is_top():
            self.status = STOP
            raise RuntimeError("电梯%s已经到达顶层" % self.name)
        self.status = UP
        yield from cost(self.speed)
        self.current_floor += 1

    @asyncio.coroutine
    def up_nums(self, nums):
        for _ in range(nums):
            yield from self.up()

    @asyncio.coroutine
    def down(self):
        if self.is_bottom():
            self.status = STOP
            raise RuntimeError("电梯%s已经到达底层" % self.name)
        self.status = DOWN
        yield from cost(self.speed)
        self.current_floor -= 1

    @asyncio.coroutine
    def down_nums(self, nums):
        for _ in range(nums):
            yield from self.down()

    def is_top(self):
        return self.current_floor == self.floor_range[-1]

    def is_bottom(self):
        return self.current_floor == self.floor_range[0]

    @asyncio.coroutine
    def in_lift(self, who='未知'):
        print("电梯(%s): %s楼到了; %s上电梯" % (self.name, self.current_floor, who))
        yield from cost(self.inout_time)

    @asyncio.coroutine
    def out_lift(self, who='未知'):
        print("电梯(%s): %s楼到了; %s下电梯" % (self.name, self.current_floor, who))
        yield from cost(self.inout_time)

    def add_event(self, event):
        if len(self.event) == self.volume:
            raise RuntimeError("电梯%s已经满员" % self.name)
        self.event.append(event)

    def remove_event(self, event):
        if len(self.event) == 0:
            self.status = STOP
            raise RuntimeError("电梯%s已经清空" % self.name)
        self.event.remove(event)

    @asyncio.coroutine
    def run_event(self):
        lst = ((k, list(v)) for k, v in groupby(sorted(self.event, key=itemgetter(2)), itemgetter(2)))
        for floor, peoples in lst:
            yield from self.up_nums(floor - self.current_floor)  # 电梯上行
            yield from self.out_lift(",".join(map(itemgetter(0), peoples)))  # 电梯停止, 人下电梯
            for people in peoples:
                self.event.remove(people)

        # 一轮结束后, 下行到一楼
        # yield from self.down_nums(self.current_floor - 1)
        # print("电梯%s: 结束一波任务，在一楼继续等待任务" % self.name)
        self.status = STOP  # 等待新的人乘坐电梯

    @asyncio.coroutine
    def run(self):
        print("电梯%s开始处理事件" % self.name)
        global queue
        while 1:
            # 获取乘坐电梯的人
            for _ in range(self.volume):
                if queue.empty():
                    break
                else:
                    event = queue.get()
                    print("电梯%s, 接受任务: %s" % (self.name, str(event)))
                    self.event.append(event)
                    if event is None:
                        break
            if None in self.event:
                self.event.remove(None)
                queue.put(None)  # 通知其他协程任务结束
                yield from self.run_event()
                break
            else:
                yield from self.run_event()


class Producer(Thread):
    def __init__(self, name, nums=10, *args, **kwargs):
        Thread.__init__(self, name=name)
        self.nums = nums

    def run(self):
        global queue
        events = map(lambda x: LiftEvent(self.name + str(x + 1), 1, random.randint(2, 29)), range(0, self.nums))
        for event in events:
            queue.put(event)
            print('生产者(%s)发布任务: %s' % (self.name, str(event)))


async def generate_people(n=1, nums=20, interval=10):
    """生产乘坐电梯的人

    :param n: 生成几轮
    :param nums: 每轮多少人
    :param interval: 每轮间隔时间，单位秒
    :return:
    """
    random.seed(10)  # 设定伪随机种子
    tmp = n
    while tmp:
        order = n - tmp + 1
        events = map(lambda x: LiftEvent(str(order - 1) + str(x + 1), 1, random.randint(2, 29)), range(0, nums))
        print("=====================第%s轮=====================" % str(order))
        for event in events:
            print('发布任务: %s' % str(event))
            queue.put(event)
        tmp -= 1
        await asyncio.sleep(interval)
    queue.put(None)  # 设置结束标志


if __name__ == "__main__":
    start = time.time()
    random.seed(10)
    loop_producer = asyncio.get_event_loop()
    loop_consumer = asyncio.get_event_loop()
    loop_producer.run_until_complete(generate_people(1, 3, 0))
    tasks = [Consumer(x).run() for x in string.ascii_uppercase[:4]]
    result = loop_consumer.run_until_complete(asyncio.wait(tasks))
    loop_producer.close()
    loop_consumer.close()
    print("time cost %s" % str(time.time() - start))
