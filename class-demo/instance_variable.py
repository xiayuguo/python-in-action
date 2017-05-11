# coding: utf-8

class A():
    def __init__(self):
        self.params = 0

    def add(self):
        self.params += 1


if __name__ == "__main__":
    a = A()  # 实例化对象1
    b = A()  # 实例化对象2
    print a.params  # 执行结果为: 0
    print b.params  # 执行结果为: 0

    a.add()
    print a.params  # 执行结果为: 1
    print b.params  # 执行结果为: 0

    b.add()
    print a.params # 执行结果为: 1
    print b.params # 执行结果为: 1
