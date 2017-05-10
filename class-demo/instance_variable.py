# coding: utf-8

class A():
    params = 0 # 类变量，也称为“静态变量”

    def add(self):
        self.params += 1


if __name__ == "__main__":
    a = A()  # 实例化对象1
    b = A()  # 实例化对象2
    print a.params  # 执行结果为: 0
    print b.params  # 执行结果为: 0
    print A.params # 执行结果为: 0

    a.add()
    print a.params  # 执行结果为: 1
    print b.params  # 执行结果为: 0
    print A.params # 执行结果为: 0

    b.add()
    print a.params # 执行结果为: 1
    print b.params # 执行结果为: 1
    print A.params # 执行结果为: 0
