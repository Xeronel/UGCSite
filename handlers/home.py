from .base import BaseHandler
from tornado import gen


class Home(BaseHandler):
    @gen.coroutine
    def get(self):
        yield self.render('index.html')
