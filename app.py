# -*- coding: utf-8 -*-

import tornado.web
from tornado.ioloop import IOLoop
from urls import urls

if __name__ == '__main__':
    app = tornado.web.Application(urls)
    app.listen(8080)
    IOLoop.current().start()
