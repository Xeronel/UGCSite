from tornado import gen, web
from tornado.escape import json_decode


def permissions(perms):
    def decorator(func):
        @gen.coroutine
        def wrapper(self, *args, **kwargs):
            user = yield self.get_user()

            # Check permissions
            for p in perms:
                # If any of the required permissions is false deny access
                if getattr(user.permissions, p, False) is False:
                    self.send_error(401)
                    return

            # Call original function
            yield func(self, *args, **kwargs)

        return wrapper

    return decorator


class BaseHandler(web.RequestHandler):
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

    def get_current_user_id(self):
        uid = self.get_secure_cookie('uid')
        uid = uid.decode('utf-8') if type(uid) == bytes else uid
        return uid

    @gen.coroutine
    def get_user(self):
        """
        Get information about the current user
        :return: User object
        """
        uid = self.get_secure_cookie('uid')
        uid = uid.decode('utf-8') if type(uid) == bytes else uid
        user = yield self.db.user.get(uid)
        return user

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

    def error(self, status_code, message):
        self.clear()
        self.set_status(status_code)
        self.write(message)
        self.flush()

    @gen.coroutine
    def render(self, template_name, **kwargs):
        ext = template_name.rfind('.')
        kwargs['template'] = template_name[:ext] if ext > 0 else template_name

        if 'user' not in kwargs:
            kwargs['user'] = yield self.get_user()
        elif kwargs['user'] is None:
            kwargs['user'] = yield self.get_user()

        super(BaseHandler, self).render(template_name, **kwargs)
