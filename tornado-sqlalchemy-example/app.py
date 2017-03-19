import os
import tornado.web
import tornado.options
import tornado.ioloop

from db import db
from model import User


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class IndexHandler(BaseHandler):
    def get(self):
        data = self.db.query(User).all()
        a = User(username="test", password="test")
        self.db.add(a)
        data1 = self.db.query(User).all()
        for d in data:
            self.write("user: %s\n" % d.username)

        self.write("==================")
        for d in data1:
            self.write("second %s" % d.username)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates")
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = db


if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(8000)
    tornado.ioloop.IOLoop.instance().start()
