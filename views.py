# -*- coding:utf-8 -*-

import logging.config
import logging
import tornado.web
import tornado.websocket
import hashlib
from ssh import SSH
from data import ClientData
from utils import check_ip, check_port
import models

logging.config.fileConfig('config.ini')
my_log = logging.getLogger('mylog')


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def get_current_user_id(self):
        return self.get_secure_cookie('user_id')


class LoginHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.render('login.html', status=0)

    def post(self, *args, **kwargs):
        email = self.get_argument('email')
        password = self.get_argument('password')
        db_session = models.create_db_session()
        try:
            user = db_session.query(models.User).filter(models.User.email == email).first()
            if user:
                md5 = hashlib.md5()
                md5.update(password)
                password = md5.hexdigest()
                if password == user.password:
                    self.set_secure_cookie('user', email)
                    self.set_secure_cookie('user_id', str(user.id))
                    self.redirect('/')
                else:
                    self.render('login.html', status=1)
            else:
                self.render('login.html', status=2)
        except Exception as e:
            my_log.exception(e)
        finally:
            db_session.close()


class LogoutHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.clear_cookie('user')
        self.redirect('/')


class SignupHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.render('signup.html', status=0)

    def post(self, *args, **kwargs):
        email = self.get_argument('email')
        password = self.get_argument('password')
        db_session = models.create_db_session()
        try:
            user = db_session.query(models.User).filter(models.User.email == email).first()
            if not user:
                md5 = hashlib.md5()
                md5.update(password)
                password = md5.hexdigest()
                user = models.User(email=email, password=password)
                db_session.add(user)
                db_session.commit()
                self.render('signup.html', status=1)
            else:
                self.render('signup.html', status=2)
        except Exception as e:
            my_log.exception(e)
        finally:
            db_session.close()


class IndexHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user_id = int(self.get_current_user_id())
        db_session = models.create_db_session()
        server_list = None
        try:
            server_list = db_session.query(models.Server).filter(models.Server.user_id == user_id)
        except Exception as e:
            my_log.exception(e)
        finally:
            db_session.close()
        self.render('index.html', server_list=server_list)


class ServerHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        delete = self.get_argument('delete', None)
        if delete:
            delete = int(delete)
            db_session = models.create_db_session()
            try:
                server = db_session.query(models.Server).filter(models.Server.id == delete).first()
                if server.user_id == int(self.get_current_user_id()):
                    db_session.delete(server)
                    db_session.commit()
            except Exception as e:
                my_log.exception(e)
            finally:
                db_session.close()
                self.redirect('/')
        else:
            server_id = self.get_argument('server_id', None)
            server_name = self.get_argument('server_name', None)
            host = self.get_argument('host', None)
            port = self.get_argument('port', None)
            parameter = {
                'server_id': server_id,
                'server_name': server_name,
                'host': host,
                'port': port
            }
            self.render('server.html', **parameter)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        db_session = models.create_db_session()
        server_id = self.get_argument('server_id', None)
        server_name = self.get_argument('server_name', 'My Server')
        host = self.get_argument('host')
        port = int(self.get_argument('port', 22))
        username = self.get_argument('username')
        password = self.get_argument('password')
        user_id = int(self.get_current_user_id())
        if server_id:
            if user_id:
                try:
                    server = db_session.query(models.Server).filter(models.Server.id == int(server_id)).first()
                    if server.user_id == int(user_id):
                        server_info = dict(server_name=server_name, host=host, port=port,
                                           username=username, password=password)
                        server.server_name = server_name
                        server.host = host
                        server.port = port
                        server.username = username
                        server.password = password
                        db_session.commit()
                    else:
                        pass
                except Exception as e:
                    my_log.exception(e)
                finally:
                    db_session.close()
                    self.redirect('/')
            else:
                pass
        else:
            try:
                server_info = dict(server_name=server_name, host=host, port=port,
                                   username=username, password=password, user_id=user_id)
                server = models.Server(**server_info)
                db_session.add(server)
                db_session.commit()
            except Exception as e:
                my_log.exception(e)
            finally:
                db_session.close()
                self.redirect('/')


class SSHHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        server_id = self.get_argument('server_id')
        server_info = {}
        if server_id:
            db_session = models.create_db_session()
            try:
                server = db_session.query(models.Server).filter(models.Server.id == int(server_id)).first()
                if server and server.user_id == int(self.get_current_user_id()):
                    server_info = dict(host=server.host,
                                       port=server.port,
                                       username=server.username,
                                       password=server.password)
                    self.render('ssh.html', **server_info)
                else:
                    self.redirect('/')
            except Exception as e:
                my_log.exception(e)
            finally:
                db_session.close()
        else:
            self.redirect('/')


class SFTPHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('sftp.html')


class WSHandler(tornado.websocket.WebSocketHandler):
    clients = dict()

    def get_client(self):
        return self.clients.get(self._id(), None)

    def put_client(self):
        ssh = SSH(self)
        self.clients[self._id()] = ssh

    def remove_client(self):
        bridge = self.get_client()
        if bridge:
            bridge.destroy()
            del self.clients[self._id()]

    @staticmethod
    def _check_init_param(data):
        return check_port(data["port"])

    @staticmethod
    def _is_init_data(data):
        return data.get_type() == 'init'

    def _id(self):
        return id(self)

    def open(self):
        self.put_client()

    def on_message(self, message):
        bridge = self.get_client()
        client_data = ClientData(message)
        if self._is_init_data(client_data):
            if self._check_init_param(client_data.data):
                bridge.open(client_data.data)
                logging.info('connection established from: %s' % self._id())
            else:
                self.remove_client()
                logging.warning('init param invalid: %s' % client_data.data)
        else:
            if bridge:
                bridge.trans_forward(client_data.data)

    def on_close(self):
        self.remove_client()
        logging.info('client close the connection: %s' % self._id())
