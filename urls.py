# -*- coding: utf-8 -*-

from views import SSHHandler, WSHandler

urls = [
    (r'/ssh', SSHHandler),
    (r'/ws', WSHandler)
]