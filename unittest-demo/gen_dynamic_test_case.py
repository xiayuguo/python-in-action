import unittest


class MyTestMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # 从excel中读出的数据, 遍历后设置测试用例
        for x in range(5):
            attrs['test_%s' % x] = cls.gen(x)
        return super(MyTestMetaclass, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def gen(cls, x):
        def fn(self):
            # 此处安放具体测试断言
            self.assertEqual(self.val + x, 3)
        return fn


class MyTestCase(unittest.TestCase, metaclass=MyTestMetaclass):

    def setUp(self):
        self.val = 1

    def test_haha(self):
        assert "0" == "0"


if __name__ == "__main__":
    unittest.main()
