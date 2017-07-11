from .base import BaseHandler
from tornado.web import MissingArgumentError
from tornado import gen, web
import psycopg2


class Login(BaseHandler):
    @gen.coroutine
    def get(self):
        if self.get_current_user():
            self.redirect('/')
        else:
            yield self.render('login.html', get_user=False)

    @gen.coroutine
    def post(self):
        try:
            cursor = yield self.db.execute(
                """
                SELECT id, username, display_name, email
                FROM users WHERE pwhash = crypt(%(passwd)s, pwhash) AND username = %(username)s;
                """,
                {'username': self.get_argument('username'),
                 'passwd': self.get_argument('password')})
            rows = cursor.fetchall()
            if len(rows) < 1:
                self.login_failed()
            else:
                uid, username, display_name, email = rows[0]
                next_page = self.get_argument('next', '/')
                self.set_secure_cookie('uid', str(uid))
                self.set_secure_cookie("username", username)
                self.redirect(next_page)
        except (MissingArgumentError, psycopg2.ProgrammingError):
            self.login_failed()

    def login_failed(self):
        self.clear()
        self.set_status(401)
        self.write('Username or password is incorrect.')
        self.flush()


class Logout(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/login')
