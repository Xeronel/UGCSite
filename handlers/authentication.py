from .base import BaseHandler
from tornado.web import MissingArgumentError
from tornado import gen


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
                "select id, username, display_name, email "
                "from users where pwhash = crypt(%(passwd)s, pwhash) and username = %(username)s;",
                {'username': self.get_argument('username'),
                 'passwd': self.get_argument('password')})
        except MissingArgumentError:
            self.send_error(401)
            return

        rows = cursor.fetchall()
        if len(rows) < 1:
            self.send_error(401)
        else:
            uid, username, first_name, last_name, email = rows[0]
            next_page = self.get_argument('next', '/dashboard')
            self.set_secure_cookie('uid', str(uid))
            self.set_secure_cookie("username", username)
            self.redirect(next_page)


class Logout(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/login')
