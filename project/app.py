import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/order_socket", OrderSocketHandler),
        ]
        settings = dict(
            cookie_secret="abcxyz",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class OrderSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        OrderSocketHandler.waiters.add(self)

    def on_close(self):
        OrderSocketHandler.waiters.remove(self)

    def on_message(self, message):

        OrderSocketHandler.send_updates(message)

    @classmethod
    def send_updates(cls, order_data):
        # logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(order_data)
            except:
                logging.error("Error sending message", exc_info=True)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
