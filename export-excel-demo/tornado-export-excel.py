# -*- coding: utf-8 -*-

import xlwt
import functools
import tornado.web
import tornado.ioloop

from tornado import gen
from datetime import datetime
from StringIO import StringIO
from tornado.web import RequestHandler

__author__ = "hugoxia"


def time_cost(method):
    """装饰器: 计算函数执行时间"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        start_time = datetime.now()
        method(self, *args, **kwargs)
        end_time = datetime.now()
        print(u"执行函数%s, 共消耗%s时间" % (method.__name__, str(end_time - start_time)))
    return wrapper


class BaseHandler(RequestHandler):
    def export_excel(self, filename, header, content, *args, **kwargs):
        """
        导出数据到excel中, 实现用户导出报表
        :param filename: 文件名
        :param header: 表头, 格式: [A, B, C, D, E, ...]
        :param content: 表格主体内容, 格式: [(..),(..),(..),...]
        :param args: 其他
        :param kwargs: 其他
        :return:
        """
        wb = xlwt.Workbook()
        ws = wb.add_sheet(u'报表详情')

        # 写表头
        map(lambda h: ws.write(0, h[0], h[1]), enumerate(header))

        # 写主体内容
        map(lambda c: map(lambda sub_c: ws.write(c[0] + 1, sub_c[0], sub_c[1]), enumerate(c[1])),
            enumerate(content))

        # 头文件是为了生成下载
        self.set_header("Content-Type", "application/x-xls")
        self.set_header("Content-Disposition", 'attachment; filename=%s' % filename)

        # 在后台服务中生成一个StringIO的对象返回给前台, 最后把数据流写给前台就实现了下载
        sio = StringIO()
        wb.save(sio)  # save方法, 既可保存到一个文件中, 也可保存到数据流中, 这里保存到数据流中
        self.write(sio.getvalue())
        self.finish()


class TestExportExcelHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        yield gen.Task(self.test_export_excel)

    @time_cost
    def test_export_excel(self, callback=None):
        header = ("A", "B", "C", "D", "E", "F", "G")
        a = xrange(0, 77777 * 1)
        content = [(a[i], a[i + 1], a[i + 2], a[i + 3], a[i + 4], a[i + 5], a[i + 6]) for i in range(len(a))[::7]]
        self.export_excel("test.xls", header=header, content=content)
        print(u"导出成功")


def make_app():
    return tornado.web.Application([
        (r"/test_export", TestExportExcelHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
