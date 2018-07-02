import time
import json
import asyncio
import tornado.web
import tornado.ioloop
import tornado.websocket


class SocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")

    async def sleep_send(self, message, second=0.5):
        await asyncio.sleep(second)
        msg_dict = json.loads(message)
        msg_dict["res_time"] = int(time.time() * 1000)
        self.write_message(json.dumps(msg_dict))

    async def on_message(self, message):
        print(f"client: {message}")
        await self.sleep_send(message, second=1)

    def on_close(self):
        print("WebSocket closed")


def main(port):
    application = tornado.web.Application([
        (r"/websocket", SocketHandler),
    ])
    application.listen(port)
    print("ws_server is running.")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main(18889)
