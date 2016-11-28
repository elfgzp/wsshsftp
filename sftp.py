# -*- coding: utf-8 -*-

import paramiko


class SFTP(object):
    def __init__(self, hostname, port, username, password):
        self._hostname = hostname
        self._