from tornado import gen, web
from .base import BaseHandler, permissions
import psycopg2


class CreateUser(BaseHandler):
    @permissions(['create_user'])
    @gen.coroutine
    @web.authenticated
    def get(self, *args, **kwargs):
        yield self.render('createuser.html')

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
            self.finish('Created user %s (%s)' % (username, new_user))
        except web.MissingArgumentError as e:
            self.error(400, '%s is required!' % getattr(e, 'arg_name', 'error').replace('-', ' ').title())
        except psycopg2.IntegrityError as e:
            if e.pgcode == '23505':
                self.error(400, 'User already exists!')
            else:
                self.error(400, 'An unexpected error has occurred.')
