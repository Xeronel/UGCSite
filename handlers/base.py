import tornado.web
from tornado import gen
from tornado.escape import json_decode


class User:
    def __init__(self, uid, first_name, last_name, email, permissions):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.permissions = permissions


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.json_args = {}

    def get_current_user(self):
        username = self.get_secure_cookie('username')
        uid = self.get_secure_cookie('uid')
        if username is None or uid is None:
            return None
        else:
            return username.decode('utf-8') if type(username) == bytes else username

    @gen.coroutine
    @tornado.web.authenticated
    def get_user(self):
        uid = self.get_secure_cookie('uid')
        uid = uid.decode('utf-8') if type(uid) == bytes else uid
        cursor = yield self.db.execute("SELECT id, username, display_name, email FROM users "
                                       "WHERE (id = %(uid)s);", {'uid': uid})
        uid, first_name, last_name, email = cursor.fetchone()
        permissions = yield self.get_permissions()
        raise gen.Return(User(uid, first_name, last_name, email, permissions))

    @gen.coroutine
    @tornado.web.authenticated
    def get_permissions(self):
        cursor = yield self.db.execute(
            "SELECT * FROM permissions "
            "INNER JOIN users ON permissions.user = user.id "
            "WHERE employee.username = %(username)s;",
            {'username': self.current_user}
        )
        permissions = cursor.fetchone()
        results = {}
        for i in range(len(cursor.description)):
            results[cursor.description[i].name] = permissions[i]
        return results

    @property
    def db(self):
        return self.application.database

    def get_json_arg(self, name, default=None):
        if not self.json_args:
            # Raises TypeError or ValueError if the body is not properly formatted JSON
            self.json_args = json_decode(self.request.body)
        result = self.json_args.get(name, default)
        if result is None:
            raise tornado.web.MissingArgumentError
        return result

    @gen.coroutine
    def render(self, template_name, get_user=True, **kwargs):
        if get_user:
            if 'user' not in kwargs:
                kwargs['user'] = yield self.get_user()
            elif kwargs['user'] is None:
                kwargs['user'] = yield self.get_user()
            super(BaseHandler, self).render(template_name, **kwargs)
        else:
            super(BaseHandler, self).render(template_name, **kwargs)
