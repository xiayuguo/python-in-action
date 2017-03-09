# -*- coding: utf-8 -*-

import logging

import tornado.web
import tornado.ioloop
import tornado.websocket


log = logging.getLogger(__name__)


def main():
    try:
        # 启动websocket-server
        application = tornado.web.Application([
            (r"/websocket", tornado.websocket.WebSocketHandler),
        ])
        web_socket_port = 12345
        log.info("websocket server is running on port %d" % web_socket_port)
        application.listen(web_socket_port)
        tornado.ioloop.IOLoop.instance().start()
    except Exception, err:
        log.exception(str(err))


if __name__ == "__main__":
    main()
