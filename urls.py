# -*- coding: utf-8 -*-

import tornado.web
from views import *

urls = [
    (r'/websocket', TermSocket, {'term_manager': term_manager}),
    (r'/()', tornado.web.StaticFileHandler, {'path': 'templates/bash'}),
    (r'/(.*)', tornado.web.StaticFileHandler, {'path': '.'}),
]