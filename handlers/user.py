from tornado import gen, web
from .base import BaseHandler, permissions
import psycopg2


class CreateUser(BaseHandler):
    @permissions(['create_user'])
    @gen.coroutine
    @web.authenticated
    def get(self, *args, **kwargs):
        groups = yield self.db.group.get()
        yield self.render('createuser.html', groups=groups)

    @permissions(['create_user'])
    @gen.coroutine
    @web.authenticated
    def post(self):
        try:
            username = self.get_argument('username')
            display_name = self.get_argument('display-name')
            email = self.get_argument('email')
            password = self.get_argument('password')
            new_user = yield self.db.user.create(username, display_name, email, password)

            for k in self.request.arguments.keys():
                if k.startswith('permission-') and self.get_argument(k) == 'true':
                    yield self.db.group.add_user(new_user, k.replace('permission-', ''))

            self.finish('Created user %s (%s)' % (username, new_user))
        except web.MissingArgumentError as e:
            self.error(400, '%s is required!' % getattr(e, 'arg_name', 'error').replace('-', ' ').title())
        except psycopg2.IntegrityError as e:
            if e.pgcode == '23505':
                self.error(400, 'User already exists!')
            else:
                self.error(400, 'An unexpected error has occurred.')
