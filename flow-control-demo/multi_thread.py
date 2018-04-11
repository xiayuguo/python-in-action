import time
import random
import string

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


def cost(seconds=0):
    time.sleep(seconds)


class LiftConfig:
    """每个电梯的配置"""

    INOUT_TIME = 2  # 进出电梯时间(电梯打开时的停留时间), 单位: seconds
    SPEED = 1  # 电梯运行时经历每层的时间, 单位: seconds
    VOLUME = 20  # 电梯所能容纳的人数
    DEFAULT_FLOOR = 1  # 电梯所处的默认楼层, 默认为一楼
    FLOOR_RANGE = range(0, 30)  # 默认为0-29, 0为负一层


class Consumer(Thread):
    def __init__(self, name='', speed=LiftConfig.SPEED, volume=LiftConfig.VOLUME,
                 default_floor=LiftConfig.DEFAULT_FLOOR, floor_range=LiftConfig.FLOOR_RANGE,
                 inout_time=LiftConfig.INOUT_TIME, *args, **kwargs):
        Thread.__init__(self, name=name, *args, **kwargs)
        self.name = name
        self.speed = speed
        self.volume = volume
        self.inout_time = inout_time
        self.current_floor = default_floor
        self.floor_range = floor_range
        self.event = []
        self.status = STOP

    def up(self):
        if self.is_top():
            self.status = STOP
            raise RuntimeError("电梯%s已经到达顶层" % self.name)
        self.status = UP
        cost(self.speed)
        self.current_floor += 1

    def up_nums(self, nums):
        for _ in range(nums):
            self.up()

    def down(self):
        if self.is_bottom():
            self.status = STOP
            raise RuntimeError("电梯%s已经到达底层" % self.name)
        self.status = DOWN
        cost(self.speed)
        self.current_floor -= 1

    def down_nums(self, nums):
        for _ in range(nums):
            self.down()

    def is_top(self):
        return self.current_floor == self.floor_range[-1]

    def is_bottom(self):
        return self.current_floor == self.floor_range[0]

    def in_lift(self, who='未知'):
        print("电梯(%s): %s楼到了; %s上电梯" % (self.name, self.current_floor, who))
        cost(self.inout_time)

    def out_lift(self, who='未知'):
        print("电梯(%s): %s楼到了; %s下电梯" % (self.name, self.current_floor, who))
        cost(self.inout_time)

    def add_event(self, event):
        if len(self.event) == self.volume:
            raise RuntimeError("电梯%s已经满员" % self.name)
        self.event.append(event)

    def remove_event(self, event):
        if len(self.event) == 0:
            self.status = STOP
            raise RuntimeError("电梯%s已经清空" % self.name)
        self.event.remove(event)

    def run_event(self):
        lst = ((k, list(v)) for k, v in groupby(sorted(self.event, key=itemgetter(2)), itemgetter(2)))
        for floor, peoples in lst:
            self.up_nums(floor - self.current_floor)  # 电梯上行
            self.out_lift(",".join(map(itemgetter(0), peoples)))  # 电梯停止, 人下电梯
            for people in peoples:
                self.event.remove(people)

        # 一轮结束后, 下行到一楼
        # self.down_nums(self.current_floor - 1)
        # print("电梯%s: 结束一波任务，在一楼继续等待任务" % self.name)
        self.status = STOP  # 等待新的人乘坐电梯

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
                queue.put(None)  # 通知其他线程任务结束
                self.run_event()
                break
            else:
                self.run_event()


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


def generate_people(n=1, nums=20, interval=10):
    """生产乘坐电梯的人

    :param n: 生成几轮
    :param nums: 每轮多少人
    :param interval: 每轮间隔时间，单位秒
    :return:
    """
    random.seed(10)  # 设定伪随机种子
    while n:
        events = map(lambda x: LiftEvent(str(x + 1), 1, random.randint(2, 29)), range(0, nums))
        for event in events:
            queue.put(event)
        n -= 1
        time.sleep(interval)


if __name__ == "__main__":
    random.seed(10)
    count = 4
    consumers = [Consumer(i) for i in string.ascii_uppercase[:count]]
    producers = [Producer(i, 2) for i in string.ascii_lowercase[:count]]
    for w in producers:
        w.daemon = True
        w.start()

    for c in consumers:
        c.daemon = True
        c.start()

    all_thread = consumers + producers
    flag = 0
    while 1:
        for w in all_thread:
            if not w.is_alive():
                print("%s is dead" % w.name)
                all_thread.remove(w)
        if not any((flag, list(filter(lambda x: x.is_alive(), producers)))):  # 生产者都over了, 发送结束任务
            queue.put(None)

        if not list(filter(lambda x: x.is_alive(), all_thread)):
            break

        time.sleep(1)
