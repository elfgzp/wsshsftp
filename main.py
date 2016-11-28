# -*- coding: utf-8 -*-

import tornado.ioloop
from urls import urls
from settings import settings
from ioloop import IOLoop

if __name__ == '__main__':
    app = tornado.web.Application(urls, **settings)
    app.listen(8080)
    IOLoop.instance().start()
    tornado.ioloop.IOLoop.instance().start()

