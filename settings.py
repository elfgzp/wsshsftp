# -*- coding: utf-8 -*-

import os

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret': "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    'xsrf_cookies': True,
    'login_url': '/login',
    'debug': True
}
