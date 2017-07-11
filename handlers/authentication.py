from .base import BaseHandler
from tornado.web import MissingArgumentError
from tornado import gen


class Login(BaseHandler):
    @gen.coroutine
    def get(self):
        if self.get_current_user():
            self.redirect('/')
        else:
            yield self.render('login.html')

    @gen.coroutine
    def post(self):
        try:
            user = yield self.db.user.login(self.get_argument('username'),
                                            self.get_argument('password'))
            if user:
                next_page = self.get_argument('next', '/')
                self.set_secure_cookie('uid', user.uid)
                self.set_secure_cookie("username", user.username)
                self.redirect(next_page)
            else:
                self.login_failed()
        except MissingArgumentError:
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
