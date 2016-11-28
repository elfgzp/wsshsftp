# -*- coding: utf-8 -*-

import paramiko
import re


class SFTP(object):
    def __init__(self, hostname, port, username, password):
        transport = paramiko.Transport((hostname, port))
        transport.connect(username, password)
        self._sftp = paramiko.SFTPClient.from_transport(transport)
        self._sftp.chdir('/')

    def getcwd(self):
        return self._sftp.getcwd()

    def chdir(self, dir):
        self._sftp.chdir(dir)

    def list_dir(self):
        dir_list = self._sftp.listdir_attr()
        formatted_dir_list = []
        for each_dir in dir_list:
            each_dir = re.split(r'\s+', each_dir.longname)
            each_dir_dict = \
                {
                    'remote_name': each_dir[8],
                    'size': each_dir[4],
                    'modified': '{0} {1} {2}'.format(each_dir[5], each_dir[6], each_dir[7]),
                    'attributes': each_dir[0]
                }
            formatted_dir_list.append(each_dir_dict)
        return formatted_dir_list
