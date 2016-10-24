# -*- coding: utf-8 -*-

import tornado.web
from tornado.ioloop import IOLoop
from terminado import TermSocket, UniqueTermManager

if __name__ == '__main__':
    term_manager = UniqueTermManager(shell_command=['bash'])
    handlers = [
        (r'/websocket', TermSocket, {'term_manager': term_manager}),
        (r'/()', tornado.web.StaticFileHandler, {'path': 'templates/index.html'}),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': '.'}),
    ]
    app = tornado.web.Application(handlers)
    app.listen(8080)
    IOLoop.current().start()
