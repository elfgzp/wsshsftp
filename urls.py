# -*- coding: utf-8 -*-

import views

urls = [
    (r'/', views.IndexHandler),
    (r'/index', views.IndexHandler),
    (r'/login', views.LoginHandler),
    (r'/logout', views.LogoutHandler),
    (r'/signup', views.SignupHandler),
    (r'/server', views.ServerHandler),
    (r'/ssh', views.SSHHandler),
    (r'/sftp', views.SFTPHandler),
    (r'/ws', views.WSHandler)
]